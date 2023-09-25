from typing import Optional

from pydantic import BaseModel


class QuestionOptionCreate(BaseModel):
    question_id: int
    comment: Optional[str] = ''


class Answer(BaseModel):
    answer: str


class QuestionOptionUpdate(BaseModel):
    id: int
    question_id: int
    answer: str
    comment: Optional[str] = ''



