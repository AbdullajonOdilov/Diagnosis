from pydantic import BaseModel


class QuestionStateCreate(BaseModel):
    name: str
    comment: str


class QuestionStateUpdate(BaseModel):
    id: int
    name: str
    comment: str


