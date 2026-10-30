from datetime import datetime

from pydantic import BaseModel, Field


class Article(BaseModel):
	id: str
	title: str
	summary: str
	category_id: str
	category_name: str
	scope: str
	published_at: datetime | None = None
	is_example: bool = False
	content: str | None = None
	source_ids: list[str] = Field(default_factory=list)
