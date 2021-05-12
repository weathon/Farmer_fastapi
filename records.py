from pydantic import BaseModel

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



