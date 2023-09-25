from typing import Optional

from pydantic import BaseModel, Field


class CreatePhone(BaseModel):
    number: str
    comment: Optional[str] = ''


class UpdatePhone(BaseModel):
    id: int
    number: str
    comment: Optional[str] = ''
