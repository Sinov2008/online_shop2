from sqlalchemy.orm import relationship

from db import Base
from sqlalchemy import *

class Expenses(Base):
    __tablename__="Expenses"
    id = Column(Integer,primary_key=True,nullable=False,autoincrement=True)
    price = Column(Integer,nullable=False)
    worker_id = Column(Integer, ForeignKey("Users.id"), nullable=False)
    sourke = Column(String(50),nullable=True)
    date = Column(DateTime(timezone=True),default=func.now(),nullable=False)
    user_id = Column(Integer,nullable=False)
    comment = Column(String(999),nullable=True)
    status = Column(Boolean,default=True)

    owner = relationship('Users',back_populates='salary')