from fastapi import APIRouter, HTTPException
from app.models.bai_toan import BaiToanCreate
from app.repositories.bai_toan_repository import BaiToanRepository
from app.services.similar_problems_service import SimilarProblemsService
from typing import List

router = APIRouter(prefix="/bai-toan", tags=["Bài toán"])
repo = BaiToanRepository()
similar_service = SimilarProblemsService()
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
def get_bai_toan_by_user(ma_nguoi_dung: str):
    """Lấy lịch sử bài toán của người dùng"""
    try:
        return repo.get_by_user(ma_nguoi_dung)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{ma_bai_toan}")
def delete_bai_toan(ma_bai_toan: int):
    """Xóa bài toán"""
    try:
        success = repo.delete(ma_bai_toan)
        if not success:
            raise HTTPException(status_code=404, detail="Không tìm thấy bài toán")
        return {"success": True, "message": "Đã xóa bài toán"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{ma_bai_toan}/similar")
async def get_similar_problems(ma_bai_toan: int):
    """
    Lấy danh sách bài toán tương tự
    
    Args:
        ma_bai_toan: Mã bài toán cần tìm bài tương tự
    
    Returns:
        {
            "success": true,
            "data": [
                {
                    "title": "Tên bài toán",
                    "source": "toanmath.com",
                    "url": "https://...",
                    "summary": "Tóm tắt",
                    "difficulty": "Trung bình"
                }
            ]
        }
    """
    try:
        # 1. Lấy đề bài từ database
        bai_toan = repo.get_by_id(ma_bai_toan)
        
        if not bai_toan:
            raise HTTPException(status_code=404, detail="Không tìm thấy bài toán")
        
        # 2. Lấy đề bài text
        de_bai = bai_toan.get("deBaiTho", "") or bai_toan.get("tomTatDe", "")
        
        if not de_bai:
            return {
                "success": False,
                "message": "Bài toán chưa có đề bài để tìm kiếm"
            }
        
        # 3. Tìm bài tương tự (có cache)
        similar = await similar_service.find_similar(de_bai, use_cache=True)
        
        return {
            "success": True,
            "data": similar,
            "count": len(similar)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error getting similar problems: {e}")
        raise HTTPException(status_code=500, detail=str(e))

