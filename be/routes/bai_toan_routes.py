from fastapi import APIRouter, HTTPException
from models.bai_toan import BaiToanCreate
from repositories.bai_toan_repository import BaiToanRepository
from typing import List

router = APIRouter(prefix="/bai-toan", tags=["Bài toán"])
repo = BaiToanRepository()

@router.post("/", response_model=dict)
def create_bai_toan(bai_toan: BaiToanCreate):
    try:
        ma_bai_toan = repo.create(bai_toan)
        return {"message": "Tạo bài toán thành công", "maBaiToan": ma_bai_toan}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[dict])
def get_all_bai_toan():
    try:
        return repo.get_all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{ma_bai_toan}", response_model=dict)
def get_bai_toan(ma_bai_toan: int):
    try:
        bai_toan = repo.get_by_id(ma_bai_toan)
        if not bai_toan:
            raise HTTPException(status_code=404, detail="Không tìm thấy bài toán")
        return bai_toan
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/user/{ma_nguoi_dung}", response_model=List[dict])
def get_bai_toan_by_user(ma_nguoi_dung: int):
    try:
        return repo.get_by_user(ma_nguoi_dung)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
