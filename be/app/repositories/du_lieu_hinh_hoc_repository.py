from app.core.database import DatabaseConnection
from typing import Optional

class DuLieuHinhHocRepository:
    def __init__(self):
        self.db = DatabaseConnection()
    
    def create_from_dict(self, data: dict) -> int:
        """Tạo dữ liệu hình học từ dict"""
        query = """
        INSERT INTO DULIEUHINHHOC (maBaiToan, toaDoDiem, cacCanh, cacQuanHe)
        VALUES (%s, %s, %s, %s);
        SELECT SCOPE_IDENTITY() as id;
        """
        result = self.db.execute_query(query, (
            data.get("maBaiToan"),
            data.get("toaDoDiem"),
            data.get("cacCanh"),
            data.get("cacQuanHe")
        ))
        return int(result[0]['id'])
    
    def get_by_bai_toan(self, ma_bai_toan: int) -> Optional[dict]:
        """Lấy dữ liệu hình học theo mã bài toán"""
        query = "SELECT * FROM DULIEUHINHHOC WHERE maBaiToan = %s"
        results = self.db.execute_query(query, (ma_bai_toan,))
        return results[0] if results else None
