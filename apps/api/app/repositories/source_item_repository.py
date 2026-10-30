from typing import Any


class SourceItemRepository:
    def __init__(self, collection: Any) -> None:
        self.collection = collection

    def save_new(self, items: list[dict[str, Any]]) -> int:
        from google.api_core.exceptions import AlreadyExists

        created = 0
        for item in items:
            try:
                self.collection.document(item["id"]).create(item)
            except AlreadyExists:
                continue
            created += 1
        return created