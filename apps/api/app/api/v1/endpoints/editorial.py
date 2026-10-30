from fastapi import APIRouter, Depends, HTTPException, status

from app.api.v1.dependencies import get_editorial_repository
from app.core.security import require_editorial_admin
from app.repositories.editorial_repository import (
    EditorialRepository,
    SourceItemAlreadyReviewedError,
    SourceItemNotFoundError,
)
from app.schemas.editorial import EditorialActionResponse, PublishSourceItemRequest
from app.services.content_catalog import list_categories

router = APIRouter()


@router.get("/source-items")
def list_pending_source_items(
    _: dict = Depends(require_editorial_admin),
    repository: EditorialRepository = Depends(get_editorial_repository),
) -> list[dict]:
    return repository.list_pending_items()


@router.post(
    "/source-items/{item_id}/publish",
    response_model=EditorialActionResponse,
    status_code=status.HTTP_201_CREATED,
)
def publish_source_item(
    item_id: str,
    publication: PublishSourceItemRequest,
    claims: dict = Depends(require_editorial_admin),
    repository: EditorialRepository = Depends(get_editorial_repository),
) -> EditorialActionResponse:
    categories = {category.id: category for category in list_categories()}
    category = categories.get(publication.category_id)
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Categoria desconhecida.",
        )

    try:
        article = repository.publish_source_item(
            item_id,
            title=publication.title,
            summary=publication.summary,
            content=publication.content,
            category_id=category.id,
            category_name=category.name,
            actor_email=claims["email"].strip().casefold(),
        )
    except SourceItemNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item de fonte não encontrado.",
        ) from error
    except SourceItemAlreadyReviewedError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="O item não está pendente de revisão.",
        ) from error

    return EditorialActionResponse(article_id=article["id"], status="published")