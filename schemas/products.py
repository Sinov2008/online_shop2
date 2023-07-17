from pydantic import BaseModel

from db import Base

class ProductBase(BaseModel):
    name: str
    type: str
    old_price: int
    new_price: int
    birlik:str


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    id: int
    status: bool = True
    user_id: int