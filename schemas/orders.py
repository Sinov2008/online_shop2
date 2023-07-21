from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List



# class UserBase(BaseModel):
#     name: str
#     username: str
#     roll: str
#     status: bool
#
#
# class UserCreate(UserBase):
#     password: str
#     number: str
#
#
#
# class UserUpdate(UserBase):
#     id: int
#     password: str
#     number: str

class OrderBase(BaseModel):
    user_id: int



class Order_Create(OrderBase):
    date: datetime


class Order_Update(OrderBase):
    id: int
    date: datetime
    status: bool = True


class UpdateUserBalance(BaseModel):
    id: int
    balance: float
    user_id: int

class UpdateUserSalary(BaseModel):
    id: int
    salary: float
    user_id: int
class UpdateUserSalaryBalance(BaseModel):
    id: int
    balance: int
    salary: int
    user_id: int





class UserCurrent(BaseModel):
    id:int
    name: str
    username: str
    password:str
    roll: str
    status: bool
