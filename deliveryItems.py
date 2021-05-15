from pydantic import BaseModel
from sqlalchemy.sql.sqltypes import DateTime
from mydatabase import Base
from sqlalchemy import Column, Integer, String, Float


class Day(BaseModel):
    farmerEmail: str
    buyer: str
    amount: int
    moisture: float
    crop: str
    date: str
    periodNumber: int


class DayBase(Base):
    __tablename__ = 'deliveries'
    id = Column(Integer, primary_key=True, autoincrement=True)
    farmerEmail = Column(String)
    buyer = Column(String)
    amount = Column(Integer)
    moisture = Column(Float)
    crop = Column(String)
    date = Column(String)
    periodNumber = Column(Integer)
