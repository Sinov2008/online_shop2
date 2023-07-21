from pydantic import BaseModel
from typing import Optional, List
import datetime








class IncomesBase(BaseModel):
    price: int
    order_id: int
    user_id:int
    comment:str



class IncomesCreate(IncomesBase):
    pass


class IncomesUpdate(IncomesBase):
    id: int
    date:datetime
    status: bool = True