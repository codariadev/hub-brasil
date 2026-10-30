from datetime import datetime, timezone
from typing import Any

from firebase_admin import firestore


class SourceItemNotFoundError(Exception):
    pass


class SourceItemAlreadyReviewedError(Exception):
    pass


class EditorialRepository:
    def __init__(self, client: Any) -> None:
        self.client = client
        self.source_items = client.collection("source_items")
        self.articles = client.collection("articles")
        self.audit_logs = client.collection("audit_logs")

    def list_pending_items(self, limit: int = 50) -> list[dict[str, Any]]:
        documents = (
            self.source_items.where("status", "==", "pending_review")
            .limit(limit)
            .stream()
        )
        return [{"id": document.id, **document.to_dict()} for document in documents]

    def publish_source_item(
        self,
        item_id: str,
        *,
        title: str,
        summary: str,
        content: str,
        category_id: str,
        category_name: str,
        actor_email: str,
    ) -> dict[str, Any]:
        source_ref = self.source_items.document(item_id)
        article_ref = self.articles.document(item_id)
        audit_ref = self.audit_logs.document()
        published_at = datetime.now(timezone.utc)
        transaction = self.client.transaction()

        @firestore.transactional
        def publish_in_transaction(current_transaction: Any) -> dict[str, Any]:
            source_snapshot = source_ref.get(transaction=current_transaction)
            if not source_snapshot.exists:
                raise SourceItemNotFoundError(item_id)

            source_item = source_snapshot.to_dict()
            if (
                source_item.get("status") != "pending_review"
                or source_item.get("is_example") is not False
            ):
                raise SourceItemAlreadyReviewedError(item_id)

            article = {
                "id": item_id,
                "title": title,
                "summary": summary,
                "content": content,
                "category_id": category_id,
                "category_name": category_name,
                "scope": source_item["scope"],
                "state_ids": source_item.get("state_ids", []),
                "source_ids": [source_item["source_id"]],
                "sources": [
                    {
                        "id": source_item["source_id"],
                        "name": source_item["source_name"],
                        "url": source_item["url"],
                        "published_at": source_item.get("published_at"),
                    }
                ],
                "status": "published",
                "is_example": False,
                "published_at": published_at,
                "created_by": actor_email,
            }

            current_transaction.create(article_ref, article)
            current_transaction.update(
                source_ref,
                {
                    "status": "published",
                    "article_id": item_id,
                    "reviewed_by": actor_email,
                    "reviewed_at": published_at,
                    "published_at": published_at,
                },
            )
            current_transaction.create(
                audit_ref,
                {
                    "action": "article.published",
                    "target_id": item_id,
                    "actor_email": actor_email,
                    "created_at": published_at,
                },
            )
            return article

        return publish_in_transaction(transaction)