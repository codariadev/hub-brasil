from pydantic import BaseModel, Field


class PublishSourceItemRequest(BaseModel):
    title: str = Field(min_length=8, max_length=180)
    summary: str = Field(min_length=20, max_length=500)
    content: str = Field(min_length=80, max_length=30000)
    category_id: str


class EditorialActionResponse(BaseModel):
    article_id: str
    status: str