"""
Model cho bảng BAI_TOAN_TUONG_TU_CACHE
Lưu cache kết quả tìm kiếm bài toán tương tự
"""
from datetime import datetime
from typing import Optional


class BaiToanTuongTuCache:
    """Model cho cache bài toán tương tự"""
    
    def __init__(
        self,
        ma_cache: Optional[int] = None,
        tu_khoa: str = "",
        ket_qua: str = "",
        ngay_tao: Optional[datetime] = None,
        lan_cap_nhat: Optional[datetime] = None
    ):
        self.ma_cache = ma_cache
        self.tu_khoa = tu_khoa
        self.ket_qua = ket_qua
        self.ngay_tao = ngay_tao or datetime.now()
        self.lan_cap_nhat = lan_cap_nhat or datetime.now()
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            "maCache": self.ma_cache,
            "tuKhoa": self.tu_khoa,
            "ketQua": self.ket_qua,
            "ngayTao": self.ngay_tao.isoformat() if self.ngay_tao else None,
            "lanCapNhat": self.lan_cap_nhat.isoformat() if self.lan_cap_nhat else None
        }
    
    @staticmethod
    def from_db_row(row):
        """Create model from database row (dict format from pymssql with as_dict=True)"""
        if not row:
            return None
        
        return BaiToanTuongTuCache(
            ma_cache=row.get('maCache'),
            tu_khoa=row.get('tuKhoa', ''),
            ket_qua=row.get('ketQua', ''),
            ngay_tao=row.get('ngayTao'),
            lan_cap_nhat=row.get('lanCapNhat')
        )
