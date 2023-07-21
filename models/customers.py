from sqlalchemy import Column, Integer, String, Boolean,Float,Text,DateTime,func
from sqlalchemy.orm import relationship

from db import Base




class Customers(Base):
    __tablename__ = "Customers"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(20), nullable=False)
    phone = Column(String(20), nullable=False)
    address = Column(String(50), nullable=False)
    date = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    status = Column(Boolean, default=True)




