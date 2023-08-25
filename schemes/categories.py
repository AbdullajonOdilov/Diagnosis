from pydantic import BaseModel


class CategoryCreate(BaseModel):
    name: str
    comment: str
    source_id: int


class CategoryUpdate(BaseModel):
    id: int
    name: str
    comment: str
    source_id: int
    status: bool


