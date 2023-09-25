from typing import Optional

from pydantic import BaseModel


class QuestionOptionsAnswerCreate(BaseModel):
    question_option_id: int
    question_state_id: int
    answer: str
    comment: Optional[str] = ''


class QuestionOptionsAnswerUpdate(BaseModel):
    id: int
    question_option_id: int
    question_state_id: int
    answer: str
    comment: Optional[str] = ''

