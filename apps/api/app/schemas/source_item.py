from datetime import datetime
from typing import Literal

from pydantic import BaseModel, HttpUrl


class SourceItem(BaseModel):
    id: str
    source_id: str
    source_name: str
    title: str
    summary: str
    url: HttpUrl
    suggested_category_ids: list[str]
    scope: Literal["national", "state"]
    state_ids: list[str]
    item_type: Literal["news", "alert"]
    published_at: datetime | None
    status: Literal["pending_review"]
    is_example: Literal[False]
    imported_at: datetime