from pydantic import BaseModel
from typing import Optional

class DuLieuHinhHocBase(BaseModel):
    toaDoDiem: Optional[str] = None
    cacCanh: Optional[str] = None
    cacQuanHe: Optional[str] = None

class DuLieuHinhHocCreate(DuLieuHinhHocBase):
    maBaiToan: int

class DuLieuHinhHocResponse(DuLieuHinhHocBase):
    id: int
    maBaiToan: int
    
    class Config:
        from_attributes = True
