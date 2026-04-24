from fastapi import APIRouter, HTTPException
from models.nguoi_dung import NguoiDungCreate, NguoiDungResponse
from repositories.nguoi_dung_repository import NguoiDungRepository
from typing import List

router = APIRouter(prefix="/nguoi-dung", tags=["Người dùng"])
repo = NguoiDungRepository()

@router.post("/", response_model=dict)
def create_nguoi_dung(nguoi_dung: NguoiDungCreate):
    try:
        ma_nguoi_dung = repo.create(nguoi_dung)
        return {"message": "Tạo người dùng thành công", "maNguoiDung": ma_nguoi_dung}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[dict])
def get_all_nguoi_dung():
    try:
        return repo.get_all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{ma_nguoi_dung}", response_model=dict)
def get_nguoi_dung(ma_nguoi_dung: int):
    try:
        nguoi_dung = repo.get_by_id(ma_nguoi_dung)
        if not nguoi_dung:
            raise HTTPException(status_code=404, detail="Không tìm thấy người dùng")
        return nguoi_dung
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{ma_nguoi_dung}")
def delete_nguoi_dung(ma_nguoi_dung: int):
    try:
        rows = repo.delete(ma_nguoi_dung)
        if rows == 0:
            raise HTTPException(status_code=404, detail="Không tìm thấy người dùng")
        return {"message": "Xóa người dùng thành công"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
