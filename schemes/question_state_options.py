from pydantic import BaseModel


class QuestionStateOptionCreate(BaseModel):
    question_state_id: int
    question_id: int
    answer: text
    comment: str


class QuestionStateOptionUpdate(BaseModel):
    id: int
    question_state_id: int
    question_id: int
    answer: str
    comment: str


