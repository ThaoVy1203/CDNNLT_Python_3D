"""
Repository cho bảng BAI_TOAN_TUONG_TU_CACHE
Xử lý các thao tác database với cache bài toán tương tự
"""
from datetime import datetime, timedelta
from typing import Optional
from app.core.database import DatabaseConnection
from app.models.bai_toan_tuong_tu_cache import BaiToanTuongTuCache


class BaiToanTuongTuCacheRepository:
    """Repository cho cache bài toán tương tự"""
    
    def __init__(self):
        self.db = DatabaseConnection()
    
    def get_by_keywords(self, tu_khoa: str, max_age_days: int = 7) -> Optional[BaiToanTuongTuCache]:
        """
        Lấy cache theo keywords, chỉ lấy nếu còn mới (< max_age_days)
        
        Args:
            tu_khoa: Keywords để tìm
            max_age_days: Số ngày tối đa cache còn hiệu lực (default: 7)
        
        Returns:
            BaiToanTuongTuCache nếu tìm thấy và còn mới, None nếu không
        """
        query = """
            SELECT maCache, tuKhoa, ketQua, ngayTao, lanCapNhat
            FROM BAI_TOAN_TUONG_TU_CACHE
            WHERE tuKhoa = %s
            AND ngayTao >= %s
        """
        cutoff_date = datetime.now() - timedelta(days=max_age_days)
        
        try:
            results = self.db.execute_query(query, (tu_khoa, cutoff_date))
            if results and len(results) > 0:
                return BaiToanTuongTuCache.from_db_row(results[0])
            return None
        except Exception as e:
            print(f"Error getting cache by keywords: {e}")
            return None
    
    def create(self, tu_khoa: str, ket_qua: str) -> bool:
        """
        Tạo cache mới
        
        Args:
            tu_khoa: Keywords
            ket_qua: JSON string kết quả
        
        Returns:
            True nếu thành công, False nếu thất bại
        """
        query = """
            INSERT INTO BAI_TOAN_TUONG_TU_CACHE (tuKhoa, ketQua)
            VALUES (%s, %s)
        """
        
        try:
            self.db.execute_non_query(query, (tu_khoa, ket_qua))
            print(f"✅ Created cache for keywords: {tu_khoa}")
            return True
        except Exception as e:
            print(f"❌ Error creating cache: {e}")
            # Nếu lỗi duplicate key, thử update
            if "duplicate" in str(e).lower() or "unique" in str(e).lower():
                return self.update_by_keywords(tu_khoa, ket_qua)
            return False
    
    def update_by_keywords(self, tu_khoa: str, ket_qua: str) -> bool:
        """
        Cập nhật cache theo keywords
        
        Args:
            tu_khoa: Keywords
            ket_qua: JSON string kết quả mới
        
        Returns:
            True nếu thành công, False nếu thất bại
        """
        query = """
            UPDATE BAI_TOAN_TUONG_TU_CACHE
            SET ketQua = %s, lanCapNhat = GETDATE()
            WHERE tuKhoa = %s
        """
        
        try:
            self.db.execute_non_query(query, (ket_qua, tu_khoa))
            print(f"✅ Updated cache for keywords: {tu_khoa}")
            return True
        except Exception as e:
            print(f"❌ Error updating cache: {e}")
            return False
    
    def delete_old_cache(self, days: int = 30) -> int:
        """
        Xóa cache cũ hơn X ngày (maintenance task)
        
        Args:
            days: Số ngày (default: 30)
        
        Returns:
            Số bản ghi đã xóa
        """
        query = """
            DELETE FROM BAI_TOAN_TUONG_TU_CACHE
            WHERE ngayTao < %s
        """
        cutoff_date = datetime.now() - timedelta(days=days)
        
        try:
            rows_affected = self.db.execute_non_query(query, (cutoff_date,))
            print(f"🗑️ Deleted {rows_affected} old cache entries")
            return rows_affected
        except Exception as e:
            print(f"❌ Error deleting old cache: {e}")
            return 0
    
    def get_all(self) -> list:
        """Lấy tất cả cache (for debugging)"""
        query = """
            SELECT maCache, tuKhoa, ketQua, ngayTao, lanCapNhat
            FROM BAI_TOAN_TUONG_TU_CACHE
            ORDER BY ngayTao DESC
        """
        
        try:
            results = self.db.execute_query(query, ())
            return [BaiToanTuongTuCache.from_db_row(row) for row in results]
        except Exception as e:
            print(f"Error getting all cache: {e}")
            return []
