from typing import Optional

from pydantic import BaseModel


class CategoryCreate(BaseModel):
    name: str
    comment: Optional[str] = ''
    status: bool
    source_id: int


class CategoryUpdate(BaseModel):
    id: int
    name: str
    status: bool
    comment: Optional[str] = ''
    source_id: int
    status: bool


