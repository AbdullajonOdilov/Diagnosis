from pydantic import BaseModel


class CategoryCreate(BaseModel):
    name: str
    comment: str
    source_id: int


class CustomerUpdate(BaseModel):
    id: int
    name: str
    comment: str
    source_id: int

