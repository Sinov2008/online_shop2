from pydantic import BaseModel
import datetime
from typing import Optional, List






class Types_Base(BaseModel):
    name: str
    date: datetime




class Types_Create(Types_Base):
    pass


class Types_Update(Types_Base):
    id: int
    date:datetime
    status: bool = True
