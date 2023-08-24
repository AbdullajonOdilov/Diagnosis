from pydantic import BaseModel


class QuestionTypeCreate(BaseModel):
    name: str
    comment: str


class QuestionTypeUpdate(BaseModel):
    id: int
    name: str
    comment: str


