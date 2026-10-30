from app.integrations.firebase.admin import get_firestore_client
from app.repositories.editorial_repository import EditorialRepository


def get_editorial_repository() -> EditorialRepository:
    return EditorialRepository(get_firestore_client())