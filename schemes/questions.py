from typing import Optional

from pydantic import BaseModel
    

class QuestionCreate(BaseModel):
    name: str
    comment: Optional[str] = ''
    category_id: int
    step: int
    question_type_id: int


class QuestionUpdate(BaseModel):
    id: int
    name: str
    comment: Optional[str] = ''
    category_id: int
    step: int
    question_type_id: int


