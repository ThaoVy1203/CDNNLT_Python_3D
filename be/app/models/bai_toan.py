from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BaiToanBase(BaseModel):
    duongDan: Optional[str] = None
    deBaiTho: Optional[str] = None
    loaiHinh: Optional[str] = None
    tomTatDe: Optional[str] = None

class BaiToanCreate(BaiToanBase):
    maNguoiDung: int

class BaiToanResponse(BaiToanBase):
    maBaiToan: int
    maNguoiDung: int
    ngayTao: datetime
    
    class Config:
        from_attributes = True
