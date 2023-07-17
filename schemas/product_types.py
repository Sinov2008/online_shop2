from pydantic import BaseModel

from db import Base


class product_typeBase(BaseModel):
    name: str
    status: bool = True

class Product_typeCreate(product_typeBase):
    pass


class Product_typeUpdate(product_typeBase):
    id: int
