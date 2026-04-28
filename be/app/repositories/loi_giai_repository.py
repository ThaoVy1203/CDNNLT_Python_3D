from app.core.database import DatabaseConnection
from typing import Optional

class LoiGiaiRepository:
    def __init__(self):
        self.db = DatabaseConnection()
    
    def create_from_dict(self, data: dict) -> int:
        """Tạo lời giải từ dict"""
        query = """
        INSERT INTO LOIGIAI (maBaiToan, cacBuocGiai, ketQuaCuoi, congThucSuDung)
        VALUES (%s, %s, %s, %s);
        SELECT SCOPE_IDENTITY() as id;
        """
        result = self.db.execute_query(query, (
            data.get("maBaiToan"),
            data.get("cacBuocGiai"),
            data.get("ketQuaCuoi"),
            data.get("congThucSuDung")
        ))
        return int(result[0]['id'])
    
    def get_by_bai_toan(self, ma_bai_toan: int) -> Optional[dict]:
        """Lấy lời giải theo mã bài toán"""
        query = "SELECT * FROM LOIGIAI WHERE maBaiToan = %s"
        results = self.db.execute_query(query, (ma_bai_toan,))
        return results[0] if results else None
