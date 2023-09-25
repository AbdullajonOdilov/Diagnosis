from typing import Optional

from pydantic import BaseModel


class QuestionTypeCreate(BaseModel):
    name: str
    comment: Optional[str] = ''


class QuestionTypeUpdate(BaseModel):
    id: int
    name: str
    comment: Optional[str] = ''


