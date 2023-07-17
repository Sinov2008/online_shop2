from pydantic import BaseModel

from db import Base


class OrderBase(BaseModel):
    status: bool =True
    customer_id: int

class OrderCreate(OrderBase):
    pass


class OrderUpdate(OrderBase):
    id: int
    user_id: int

