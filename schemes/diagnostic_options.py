from pydantic import BaseModel


class DiagnosticOptionCreate(BaseModel):
    diagnostic_id: int
    question_state_option_id: int


class DiagnosticOptionUpdate(BaseModel):
    id: int
    diagnostic_id: int
    question_state_option_id: int


