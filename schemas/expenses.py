from pydantic import BaseModel
from typing import Optional, List



class ExpensesBase(BaseModel):
    name: str

    status: bool


class ExpensesCreate(ExpensesBase):

    number: str



class ExpensesUpdate(ExpensesBase):
    id: int

    number: str



class UpdateExpensesBalance(BaseModel):
    id: int
    balance: float


class UpdateExpensesSalary(BaseModel):
    id: int
    salary: float
    user_id: int


class UpdateExpensesSalaryBalance(BaseModel):
    id: int
    balance: int
    salary: int


class ExpensesCurrent(BaseModel):
    id:int
    name: str
    username: str
    password:str
    roll: str
    status: bool
