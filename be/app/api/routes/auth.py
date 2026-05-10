"""
Authentication API Routes
Xử lý đăng nhập, đăng ký, Google OAuth
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.repositories.nguoi_dung_repository import NguoiDungRepository
from typing import Optional

router = APIRouter(prefix="/auth", tags=["Authentication"])
repo = NguoiDungRepository()


class GoogleLoginRequest(BaseModel):
    googleId: str
    email: Optional[str] = ""
    name: Optional[str] = ""
    picture: Optional[str] = ""


class LoginRequest(BaseModel):
    username: str
    password: str


@router.post("/google-login")
async def google_login(request: GoogleLoginRequest):
    """
    Đăng nhập bằng Google OAuth
    - Tự động tạo user nếu chưa tồn tại
    - Trả về thông tin user
    """
    try:
        # Tạo hoặc lấy user
        ma_nguoi_dung = repo.get_or_create_google_user(
            google_id=request.googleId,
            email=request.email or "",
            name=request.name or f"User_{request.googleId[:8]}"
        )
        
        # Lấy thông tin user
        user = repo.get_by_id_string(ma_nguoi_dung)
        
        if not user:
            raise HTTPException(status_code=500, detail="Không thể tạo hoặc lấy thông tin user")
        
        return {
            "success": True,
            "message": "Đăng nhập thành công",
            "user": {
                "maNguoiDung": user.get('maNguoiDung'),
                "tenDangNhap": user.get('tenDangNhap'),
                "email": user.get('email'),
                "vaiTro": user.get('vaiTro')
            }
        }
        
    except Exception as e:
        print(f"Google login error: {e}")
        raise HTTPException(status_code=500, detail=f"Lỗi đăng nhập Google: {str(e)}")


@router.post("/login")
async def login(request: LoginRequest):
    """
    Đăng nhập thông thường (username/password)
    """
    try:
        # TODO: Implement username/password authentication
        # For now, just return error
        raise HTTPException(status_code=501, detail="Chức năng đăng nhập thông thường chưa được triển khai")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/register")
async def register(request: LoginRequest):
    """
    Đăng ký tài khoản mới
    """
    try:
        # TODO: Implement user registration
        raise HTTPException(status_code=501, detail="Chức năng đăng ký chưa được triển khai")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/check/{ma_nguoi_dung}")
async def check_user_exists(ma_nguoi_dung: str):
    """
    Kiểm tra user có tồn tại không
    """
    try:
        user = repo.get_by_id_string(ma_nguoi_dung)
        return {
            "exists": user is not None,
            "user": user if user else None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
