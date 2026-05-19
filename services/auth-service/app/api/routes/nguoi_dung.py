from typing import List

from fastapi import APIRouter, HTTPException

from app.models.nguoi_dung import NguoiDungCreate
from app.repositories.nguoi_dung_repository import NguoiDungRepository


router = APIRouter(prefix="/nguoi-dung", tags=["Nguoi dung"])
repo = NguoiDungRepository()


@router.post("/", response_model=dict)
def create_nguoi_dung(nguoi_dung: NguoiDungCreate):
    try:
        ma_nguoi_dung = repo.create(nguoi_dung)
        return {"message": "Tao nguoi dung thanh cong", "maNguoiDung": ma_nguoi_dung}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[dict])
def get_all_nguoi_dung():
    try:
        return repo.get_all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{ma_nguoi_dung}", response_model=dict)
def get_nguoi_dung(ma_nguoi_dung: str):
    try:
        nguoi_dung = repo.get_by_id_string(ma_nguoi_dung)
        if not nguoi_dung:
            raise HTTPException(status_code=404, detail="Khong tim thay nguoi dung")
        return nguoi_dung
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{ma_nguoi_dung}")
def delete_nguoi_dung(ma_nguoi_dung: str):
    try:
        rows = repo.delete(ma_nguoi_dung)
        if rows == 0:
            raise HTTPException(status_code=404, detail="Khong tim thay nguoi dung")
        return {"message": "Xoa nguoi dung thanh cong"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
