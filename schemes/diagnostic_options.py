from pydantic import BaseModel


class DiagnosticOptionCreate(BaseModel):
    diagnostic_id: int


class QuestionOption(BaseModel):
    question_option_id: int


class DiagnosticOptionUpdate(BaseModel):
    id: int
    diagnostic_id: int
    question_options_id: int


