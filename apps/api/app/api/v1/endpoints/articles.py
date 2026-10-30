import os

from fastapi import APIRouter

from app.integrations.firebase.admin import get_firestore_client
from app.repositories.article_repository import ArticleRepository
from app.schemas.article import Article
from app.services.content_catalog import list_articles

router = APIRouter()


@router.get("", response_model=list[Article])
def get_articles() -> list[Article]:
	if os.getenv("APP_ENV", "development").lower() == "development":
		if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
			return list_articles()
		published = ArticleRepository(get_firestore_client()).list_published()
		return published or list_articles()
	return ArticleRepository(get_firestore_client()).list_published()
