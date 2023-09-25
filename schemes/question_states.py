from typing import Optional

from pydantic import BaseModel


class QuestionStateCreate(BaseModel):
    name: str
    comment: Optional[str] = ''


class QuestionStateUpdate(BaseModel):
    id: int
    name: str
    comment: Optional[str] = ''


