from pydantic import BaseModel
from typing import Optional, List



class CustomersBase(BaseModel):
    name: str
    status: bool


class CustomersCreate(CustomersBase):
    number: str



class CustomersUpdate(CustomersBase):
    id: int
    number: str



class UpdateCustomersBalance(BaseModel):
    id: int
    balance: float
    user_id: int


class UpdateCustomersSalary(BaseModel):
    id: int
    salary: float
    user_id: int


class UpdateCustomersSalaryBalance(BaseModel):
    id: int
    balance: int
    salary: int
    user_id: int



class CustomersCurrent(BaseModel):
    id:int
    name: str
    username: str
    password:str
    status: bool
