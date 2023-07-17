from pydantic import BaseModel

from db import Base


class CustomersBase(BaseModel):
    name:str
    phone: str
    address: str

class CustomersCreate(CustomersBase):
    pass


class CustmoerUpdate(CustomersBase):
    id: int
    status: bool =True