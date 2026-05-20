from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.similar_problems_service import SimilarProblemsService


router = APIRouter(prefix="/search", tags=["Search"])
similar_service = SimilarProblemsService()


class SimilarProblemsRequest(BaseModel):
    de_bai: str
    use_cache: bool = True


@router.post("/similar")
async def find_similar_problems(request: SimilarProblemsRequest):
    if not request.de_bai.strip():
        raise HTTPException(status_code=400, detail="de_bai is required")

    results = await similar_service.find_similar(
        request.de_bai,
        use_cache=request.use_cache,
    )

    return {
        "success": True,
        "data": results,
        "count": len(results),
    }
