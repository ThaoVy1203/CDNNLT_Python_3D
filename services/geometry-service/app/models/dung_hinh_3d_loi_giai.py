from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class DungHinh3DLoiGiaiCreate(BaseModel):
    maLoiGiai: int
    cacBuocVe: str
    hamThreeJS: str
    thamSo: str
    codeThreeJS: str
    huongDanVe: str


class DungHinh3DLoiGiai(BaseModel):
    maDungHinhLoiGiai: int
    maLoiGiai: int
    cacBuocVe: str
    hamThreeJS: str
    thamSo: str
    codeThreeJS: str
    huongDanVe: str
    ngayTao: Optional[datetime] = None
