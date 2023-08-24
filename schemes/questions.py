from pydantic import BaseModel


class QuestionCreate(BaseModel):
    name: str
    comment: str
    category_id: int
    step: int
    question_type_id: int


class QuestionUpdate(BaseModel):
    id: int
    name: str
    comment: str
    category_id: int
    step: int
    question_type_id: int


