from pydantic import BaseModel
from typing import List

from schemes.phones import CreatePhone, UpdatePhone


class CustomerCreate(BaseModel):
    name: str
    address: str
    comment: str
    phones: List[CreatePhone]


class CustomerUpdate(BaseModel):
    id: int
    name: str
    address: str
    comment: str
    phones: List[UpdatePhone]

