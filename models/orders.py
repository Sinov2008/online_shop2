from db import Base
from sqlalchemy import Column, String, Integer, Float, DateTime, func, Boolean, ForeignKey


class Orders(Base):
    __tablename__ = "Orders"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    date = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    user_id = Column(Integer, ForeignKey('Users.id'), nullable=False)
    status = Column(Boolean, default=True)