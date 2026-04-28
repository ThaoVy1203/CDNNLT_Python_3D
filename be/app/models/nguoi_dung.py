from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class NguoiDungBase(BaseModel):
    tenDangNhap: str
    email: EmailStr
    vaiTro: str = "Thành viên"

class NguoiDungCreate(NguoiDungBase):
    matKhau: str

class NguoiDungResponse(NguoiDungBase):
    maNguoiDung: int
    ngayTao: datetime
    
    class Config:
        from_attributes = True
