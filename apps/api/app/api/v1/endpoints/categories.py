from fastapi import APIRouter

from app.schemas.category import Category
from app.services.content_catalog import list_categories

router = APIRouter()


@router.get("", response_model=list[Category])
def get_categories() -> list[Category]:
	return list_categories()
