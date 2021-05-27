from pydantic import BaseModel
from sqlalchemy.sql.sqltypes import DateTime
from mydatabase import Base
from sqlalchemy import Column, Integer, String, Float, Boolean


class price(Base):
    __tablename__ = 'price'
    id = Column(Integer, primary_key=True, autoincrement=True)
    crop = Column(String)
    buyer = Column(String)
    rprice = Column(Integer) #easiler
    aprice = Column(Integer)
    percentage = Column(Integer)
    closed = Column(Boolean)
    month = Column(String)
