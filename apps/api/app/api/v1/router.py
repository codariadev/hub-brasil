from fastapi import APIRouter

from app.api.v1.endpoints import articles, categories, editorial

api_router = APIRouter()
api_router.include_router(articles.router, prefix="/articles", tags=["articles"])
api_router.include_router(categories.router, prefix="/categories", tags=["categories"])
api_router.include_router(editorial.router, prefix="/editorial", tags=["editorial"])
