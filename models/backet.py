from sqlalchemy import Column, Integer, String, Boolean,Float,Text ,DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from db import Base




class Backet(Base):
    __tablename__ = "Backet"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(20), nullable=False)
    quantity = Column(Integer, default=func.now(), nullable=False)
    order_id = Column(Integer, ForeignKey("Orders.id"), nullable=False)
    date = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    user_id = Column(Integer, ForeignKey('Users.id'), nullable=False)
    status = Column(Boolean, default=True)



    # id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    # name = Column(String(20), nullable=False)
    # quantity = Column(Integer, default=func.now(), nullable=False)
    # # order_id = Column(Integer, ForeignKey("worker.id"), nullable=False)
    # date = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    # # user_id = Column(Integer, ForeignKey(''), nullable=False)
    # status = Column(Boolean, default=True)



