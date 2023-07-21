from sqlalchemy import Column, Integer, String, Boolean,Float,Text , DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from db import Base




class Products(Base):
    __tablename__ = "Products"
    id = Column(Integer,primary_key=True,nullable=False,autoincrement=True)
    name = Column(String(20),nullable=False)
    type = Column(Integer,ForeignKey('Orders.id'),nullable=False)
    birlik = Column(String(20),nullable=False)
    old_price = Column(Integer, nullable=False)
    new_price = Column(Integer, nullable=False)
    date = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    user_id = Column(Integer,ForeignKey('Users.id'),nullable=False)
    status = Column(Boolean, default=True)





    # id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    # name = Column(String(20), nullable=False)
    # # type = Column(Integer, ForeignKey('Product_types.id'), nullable=False)
    # birlik = Column(String(20), nullable=False)
    # old_price = Column(Integer, nullable=False)
    # new_price = Column(Integer, nullable=False)
    # date = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    # # user_id = Column(Integer, ForeignKey('Users.id'), nullable=False)
    # status = Column(Boolean, default=True)



