from pydantic import BaseModel

from db import Base


class ExpensesBase(BaseModel):
    sourke:str
    comment: str
    worker_id: int
    status: bool = True
    price: int

class ExpensesCreate(ExpensesBase):
    pass


class ExpensesUpdate(ExpensesBase):
    user_id: int
    id:int


