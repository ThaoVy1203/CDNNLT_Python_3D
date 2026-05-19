from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class LoiGiaiBase(BaseModel):
    cacBuocGiai: Optional[str] = None
    ketQuaCuoi: Optional[str] = None
    congThucSuDung: Optional[str] = None

class LoiGiaiCreate(LoiGiaiBase):
    maBaiToan: int

class LoiGiaiResponse(LoiGiaiBase):
    maLoiGiai: int
    maBaiToan: int
    ngayTao: datetime
    
    class Config:
        from_attributes = True
