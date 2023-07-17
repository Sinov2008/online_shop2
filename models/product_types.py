from sqlalchemy.orm import relationship

from db import Base
from sqlalchemy import *


class Product_types(Base):
    __tablename__ = "Product_types"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(20), nullable=False)
    date = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    status = Column(Boolean, default=True)

    savdolar = relationship("Products", back_populates='owner')
