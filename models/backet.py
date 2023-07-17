from sqlalchemy.orm import relationship

from db import Base
from sqlalchemy import *

class Backet(Base):
    __tablename__="Backet"
    id = Column(Integer,primary_key=True,nullable=False,autoincrement=True)
    name = Column(String(20),nullable=False)
    quantity = Column(Integer,nullable=False)
    order_id = Column(Integer,ForeignKey("Orders.id"),nullable=False)
    date = Column(DateTime(timezone=True),default=func.now(),nullable=False)
    customer_id = Column(Integer,ForeignKey("Customers.id"),nullable=False)
    status = Column(Boolean,default=True)
    owner = relationship('Customers',back_populates='savdo')