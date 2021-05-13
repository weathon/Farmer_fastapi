from pydantic import BaseModel
from mydatabase import Base
#这里的和main里面的不一样
from sqlalchemy import Column, Integer, String, Float
class Record(BaseModel):
    email: str
    crop: str
    contractDate: str
    deliverieMonth: str
    buyer: str
    contractAmount: str
    deliverieAmount: str
    unitPrice: float
    totalValue: float
    status: int
    class Config():
        orm_mode = True


class RecordBase(Base):
    __tablename__ = 'records'
    email = Column(String, primary_key=True, index=True)
    crop: Column(String, index=True)
    contractDate: Column(String)
    deliverieMonth: Column(String)
    buyer: Column(String)
    contractAmount: Column(String)
    deliverieAmount: Column(String)
    unitPrice: Column(Float)
    totalValue: Column(Float)
    status: Column(Integer())
