from pydantic import BaseModel


class QuestionData(BaseModel):
    name: str
    comment: str
    step: int
    question_type_id: int
    id: int
    category_id: int
    user_id: int
    


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


