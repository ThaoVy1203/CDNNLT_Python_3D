from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.repositories.nguoi_dung_repository import NguoiDungRepository


router = APIRouter(prefix="/auth", tags=["Authentication"])
repo = NguoiDungRepository()


class GoogleLoginRequest(BaseModel):
    googleId: str
    email: Optional[str] = ""
    name: Optional[str] = ""
    picture: Optional[str] = ""


class EnsureGoogleUserRequest(BaseModel):
    googleId: str
    email: Optional[str] = ""
    name: Optional[str] = ""


class LoginRequest(BaseModel):
    username: str
    password: str


def _user_response(user: dict) -> dict:
    return {
        "maNguoiDung": user.get("maNguoiDung"),
        "tenDangNhap": user.get("tenDangNhap"),
        "email": user.get("email"),
        "vaiTro": user.get("vaiTro"),
    }


@router.post("/google-login")
async def google_login(request: GoogleLoginRequest):
    try:
        ma_nguoi_dung = repo.get_or_create_google_user(
            google_id=request.googleId,
            email=request.email or f"{request.googleId}@google.local",
            name=request.name or f"User_{request.googleId[:8]}",
        )
        user = repo.get_by_id_string(ma_nguoi_dung)

        if not user:
            raise HTTPException(status_code=500, detail="Could not create or fetch user")

        return {
            "success": True,
            "message": "Dang nhap thanh cong",
            "user": _user_response(user),
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"Google login error: {e}")
        raise HTTPException(status_code=500, detail=f"Google login error: {str(e)}")


@router.post("/ensure-google-user")
async def ensure_google_user(request: EnsureGoogleUserRequest):
    """
    Internal endpoint for geometry-service.
    Ensures the Google user exists before geometry-service writes BAITOAN.maNguoiDung.
    """
    try:
        ma_nguoi_dung = repo.get_or_create_google_user(
            google_id=request.googleId,
            email=request.email or f"{request.googleId}@google.local",
            name=request.name or f"User_{request.googleId[:8]}",
        )
        user = repo.get_by_id_string(ma_nguoi_dung)
        return {
            "success": True,
            "exists": user is not None,
            "maNguoiDung": ma_nguoi_dung,
            "user": _user_response(user) if user else None,
        }
    except Exception as e:
        print(f"Ensure Google user error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/login")
async def login(request: LoginRequest):
    raise HTTPException(status_code=501, detail="Username/password login is not implemented")


@router.post("/register")
async def register(request: LoginRequest):
    raise HTTPException(status_code=501, detail="Registration is not implemented")


@router.get("/check/{ma_nguoi_dung}")
async def check_user_exists(ma_nguoi_dung: str):
    try:
        user = repo.get_by_id_string(ma_nguoi_dung)
        return {
            "exists": user is not None,
            "user": _user_response(user) if user else None,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
