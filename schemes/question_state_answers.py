from pydantic import BaseModel


class QuestionStateAnswerCreate(BaseModel):
    question_state_option_id: int
    answer: str
    comment: str


class QuestionStateAnswerUpdate(BaseModel):
    id: int
    question_state_option_id: int
    answer: str
    comment: str

