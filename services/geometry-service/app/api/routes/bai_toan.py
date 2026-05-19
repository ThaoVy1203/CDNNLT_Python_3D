import asyncio
from typing import List

import requests
from fastapi import APIRouter, HTTPException

from app.core.config import settings
from app.repositories.bai_toan_repository import BaiToanRepository


router = APIRouter(prefix="/bai-toan", tags=["Bai toan"])
repo = BaiToanRepository()


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
            raise HTTPException(status_code=404, detail="Khong tim thay bai toan")
        return bai_toan
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/user/{ma_nguoi_dung}", response_model=List[dict])
def get_bai_toan_by_user(ma_nguoi_dung: str):
    """Lay lich su bai toan cua nguoi dung"""
    try:
        return repo.get_by_user(ma_nguoi_dung)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{ma_bai_toan}")
def delete_bai_toan(ma_bai_toan: int):
    """Xoa bai toan"""
    try:
        success = repo.delete(ma_bai_toan)
        if not success:
            raise HTTPException(status_code=404, detail="Khong tim thay bai toan")
        return {"success": True, "message": "Da xoa bai toan"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{ma_bai_toan}/similar")
async def get_similar_problems(ma_bai_toan: int):
    """
    Lay danh sach bai toan tuong tu qua search-service.
    Geometry/backend service chi lay de bai tu DB va uy quyen tim kiem cho search-service.
    """
    try:
        bai_toan = repo.get_by_id(ma_bai_toan)

        if not bai_toan:
            raise HTTPException(status_code=404, detail="Khong tim thay bai toan")

        de_bai = bai_toan.get("deBaiTho", "") or bai_toan.get("tomTatDe", "")

        if not de_bai:
            return {
                "success": False,
                "message": "Bai toan chua co de bai de tim kiem",
            }

        def call_search_service():
            response = requests.post(
                f"{settings.SEARCH_SERVICE_URL.rstrip('/')}/search/similar",
                json={"de_bai": de_bai, "use_cache": True},
                timeout=45,
            )
            response.raise_for_status()
            return response.json()

        search_response = await asyncio.to_thread(call_search_service)
        similar = search_response.get("data", [])

        return {
            "success": True,
            "data": similar,
            "count": len(similar),
        }

    except HTTPException:
        raise
    except requests.RequestException as e:
        print(f"Error calling search-service: {e}")
        raise HTTPException(status_code=503, detail="Search service unavailable")
    except Exception as e:
        print(f"Error getting similar problems: {e}")
        raise HTTPException(status_code=500, detail=str(e))
