from pydantic import BaseModel
from typing import Optional

class DungHinh3DCreate(BaseModel):
    maBaiToan: int
    cacBuocVe: str
    hamThreeJS: str
    thamSo: str
    codeThreeJS: str
    huongDanVe: str

class DungHinh3D(BaseModel):
    maDungHinh: int
    maBaiToan: int
    cacBuocVe: str
    hamThreeJS: str
    thamSo: str
    codeThreeJS: str
    huongDanVe: str
    ngayTao: Optional[str] = None
