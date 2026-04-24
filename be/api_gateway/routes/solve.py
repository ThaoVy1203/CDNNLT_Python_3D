from fastapi import APIRouter
from api_gateway.schemas.geometry import GeometryResponse

router = APIRouter(prefix="/solve", tags=["solve"])

@router.get("", response_model=GeometryResponse)
def solve():
    return {
        "points": {
            "A": [-2, 0, -2],
            "B": [2, 0, -2],
            "C": [0, 0, 2],
            "S": [0, 3, 0],
        }
    }
