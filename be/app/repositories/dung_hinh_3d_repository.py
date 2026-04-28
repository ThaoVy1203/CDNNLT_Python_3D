from app.core.database import DatabaseConnection
from typing import Optional, List

class DungHinh3DRepository:
    def __init__(self):
        self.db = DatabaseConnection()
    
    def create_from_dict(self, data: dict) -> int:
        """Tạo dữ liệu dựng hình 3D từ dict"""
        query = """
        INSERT INTO DUNGHINH3D (maBaiToan, cacBuocVe, hamThreeJS, thamSo, codeThreeJS, huongDanVe)
        VALUES (%s, %s, %s, %s, %s, %s);
        SELECT SCOPE_IDENTITY() as id;
        """
        result = self.db.execute_query(query, (
            data.get("maBaiToan"),
            data.get("cacBuocVe"),
            data.get("hamThreeJS"),
            data.get("thamSo"),
            data.get("codeThreeJS"),
            data.get("huongDanVe")
        ))
        return int(result[0]['id'])
    
    def get_by_bai_toan(self, ma_bai_toan: int) -> Optional[dict]:
        """Lấy dữ liệu dựng hình theo mã bài toán"""
        query = "SELECT * FROM DUNGHINH3D WHERE maBaiToan = %s"
        results = self.db.execute_query(query, (ma_bai_toan,))
        return results[0] if results else None
    
    def get_by_id(self, ma_dung_hinh: int) -> Optional[dict]:
        """Lấy dữ liệu dựng hình theo ID"""
        query = "SELECT * FROM DUNGHINH3D WHERE maDungHinh = %s"
        results = self.db.execute_query(query, (ma_dung_hinh,))
        return results[0] if results else None
