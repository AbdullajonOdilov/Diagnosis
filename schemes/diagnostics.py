from pydantic import BaseModel


class DiagnosticCreate(BaseModel):
    customer_id: int
    category_id: int
    status: bool


class DiagnosticUpdate(BaseModel):
    id: int
    customer_id: int
    category_id: int
    status: bool


