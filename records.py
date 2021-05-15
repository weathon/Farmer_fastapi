from pydantic import BaseModel
from mydatabase import Base
#这里的和main里面的不一样
from sqlalchemy import Column, Integer, String, Float
# from fastapi_utils.guid_type import GUID

class Record(BaseModel):
    # email: str
    crop: str
    contractDate: str
    deliverieMonth: str
    buyer: str
    contractAmount: float
    deliverieAmount: float
    unitPrice: float
    # totalValue: float
    # status: int
    # class Config():
    #     orm_mode = True


class RecordBase(Base):
    __tablename__ = 'records'
    id = Column(Integer, primary_key=True,autoincrement=True)
    email = Column(String)
    # crop: Column(String)
    # contractDate: Column(String)
    # deliverieMonth: Column(String)
    # buyer: Column(String)
    # contractAmount: Column(String)
    # deliverieAmount: Column(String)
    # unitPrice: Column(Float)
    # totalValue: Column(Float)
    # status: Column(Integer)
    crop= Column(String)
    contractDate= Column(String)
    deliverieMonth= Column(String)
    buyer= Column(String)
    contractAmount= Column(String)
    deliverieAmount= Column(String)
    unitPrice= Column(Float)
    totalValue= Column(Float)
    status= Column(Integer)