from sqlalchemy import Column, Integer, String, Boolean,Float,Text,ForeignKey,DateTime,func
from sqlalchemy.orm import relationship

from db import Base




class Incomes(Base):
    __tablename__ = "Incomes"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    price = Column(Integer,nullable=False)
    order_id = Column(Integer,ForeignKey("Orders.id"),nullable=False)
    date = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    user_id = Column(Integer, ForeignKey('Users.id'), nullable=False)
    comment = Column(String(100),nullable=True)
    status = Column(Boolean, default=True)

