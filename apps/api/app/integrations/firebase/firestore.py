from typing import Any

from app.integrations.firebase.admin import get_firestore_client

SOURCE_ITEMS_COLLECTION = "source_items"


def get_source_items_collection() -> Any:
	return get_firestore_client().collection(SOURCE_ITEMS_COLLECTION)
