from pydantic import BaseModel
from sqlalchemy.sql.sqltypes import Boolean
from mydatabase import Base
#这里的和main里面的不一样
from sqlalchemy import Column, Integer, String, Float
# from fastapi_utils.guid_type import GUID

class Day(BaseModel):
    date: str
    full: bool



class DayBase(Base):
    __tablename__ = 'days'
    id = Column(Integer, primary_key=True,autoincrement=True)
    full = Column(Boolean)
    # kun nans hou shouzhang
    # 性能差后来优化
    periods = Column(String,default=","*47)
    # 逗号隔开，如果是-1代表没有占用，数字的话对应DeliveryItem 一共48个 kunyun
    day = Column(Integer)
    month = Column(String) #toutongkun example=012020 122021  完全是空的话就代表没有
