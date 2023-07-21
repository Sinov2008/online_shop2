from sqlalchemy import Column, Integer, String, Boolean,Float,Text,DateTime,ForeignKey,func
from sqlalchemy.orm import relationship

from db import Base




class Expenses(Base):
    __tablename__ = "Expenses"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    price = Column(Integer, nullable=False)
    worker_id = Column(Integer, ForeignKey("Users.id"), nullable=True)
    source = Column(String(50), nullable=True)
    date = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    user_id = Column(Integer, ForeignKey('Users.id'), nullable=False)
    comment = Column(String(100), nullable=True)
    status = Column(Boolean, default=True)





    # id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    # price = Column(Integer, nullable=False)
    # worker_id = Column(Integer, ForeignKey("Users.id"), nullable=True)
    # source = Column(String(50), nullable=True)
    # date = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    # user_id = Column(Integer, ForeignKey('Users.id'), nullable=False)
    # comment = Column(String(100), nullable=True)
    # status = Column(Boolean, default=True)




