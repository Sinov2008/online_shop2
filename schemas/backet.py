from pydantic import BaseModel

from db import Base


class BacketBase(BaseModel):
    name:str
    status: bool = True
    order_id: int
    customer_id:int
    quantity: int


class BacketCreate(BacketBase):
    pass


class BacketUpdate(BacketBase):
    id: int
    quantity: int

