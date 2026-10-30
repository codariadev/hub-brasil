from typing import Any

from app.schemas.article import Article


class ArticleRepository:
	def __init__(self, client: Any) -> None:
		self.collection = client.collection("articles")

	def list_published(self, limit: int = 20) -> list[Article]:
		documents = (
			self.collection.where("status", "==", "published")
			.order_by("published_at", direction="DESCENDING")
			.limit(limit)
			.stream()
		)
		return [Article(**document.to_dict()) for document in documents]
