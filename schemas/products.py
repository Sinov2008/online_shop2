
from pydantic import BaseModel
from typing import Optional, List



class ProductBase(BaseModel):
    name: str
    status: bool


class ProductCreate(ProductBase):
    id: int
    status: bool




class ProductUpdate(ProductBase):
    id: int
    status: bool




class UpdateProductBalance(BaseModel):
    id: int
    balance: float


class UpdateProductSalary(BaseModel):
    id: int
    salary: float


class UpdateProductSalaryBalance(BaseModel):
    id: int
    balance: int
    salary: int
    user_id: int



class ProductCurrent(BaseModel):
    id:int
    name: str
    username: str
    password:str
    roll: str
    status: bool
