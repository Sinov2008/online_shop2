from pydantic import BaseModel
from typing import Optional, List



class BacketBase(BaseModel):
    name: str
    status: bool
    quantity: int
    order_id: str



class BacketCreate(BacketBase):
    dare: int
    quantity: int





class BacketUpdate(BacketBase):
    id: int
    number: str
    quantity: int



class UpdateBacketBalance(BaseModel):
    id: int
    balance: float

class UpdateBacketSalary(BaseModel):
    id: int
    salary: float
class UpdateBacketSalaryBalance(BaseModel):
    id: int
    balance: int
    salary: int




class BacketCurrent(BaseModel):
    id:int
    name: str
    status: bool