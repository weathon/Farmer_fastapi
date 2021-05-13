from pydantic import BaseModel
from mydatabase import Base
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
class Message(BaseModel):
    title: str
    sender: str
    archived: bool
    content: str
    reciver: str #reciver email
    read: bool
    dt: str
    class Config():
        orm_mode = True


class MessageBase(Base):
    __tablename__ = 'messages'
    reciver = Column(String, primary_key=True)
    content= Column(String)
    title= Column(String)
    sender= Column(String)
    archived= Column(Boolean)
    read= Column(Boolean)
    dt = Column(String)
# 两边分开？ 这个read什么的要分开检索
# 群组消息怎么办？ 所有消息怎么办 忘记了世家