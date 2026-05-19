from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.file_search_service import file_search_service
from app.services.similar_problems_service import SimilarProblemsService


router = APIRouter(prefix="/search", tags=["Search"])
similar_service = SimilarProblemsService()


class SimilarProblemsRequest(BaseModel):
    de_bai: str
    use_cache: bool = True


class FileSearchRequest(BaseModel):
    query: str
    max_results: Optional[int] = None


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


@router.get("/file/status")
async def get_file_search_status():
    return {
        "success": True,
        "data": file_search_service.get_status(),
    }


@router.post("/file/initialize")
async def initialize_file_search():
    success = await file_search_service.initialize()
    return {
        "success": success,
        "message": "File Search initialized successfully" if success else "Failed to initialize File Search",
    }


@router.post("/file")
async def search_files(request: FileSearchRequest):
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="query is required")

    results = await file_search_service.search(request.query)
    if request.max_results:
        results = results[:request.max_results]

    return {
        "success": True,
        "data": results,
        "count": len(results),
    }

