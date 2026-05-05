from app.core.database import DatabaseConnection
from app.models.bai_toan import BaiToanCreate
from typing import List, Optional

class BaiToanRepository:
    def __init__(self):
        self.db = DatabaseConnection()
    
    def create(self, bai_toan: BaiToanCreate) -> int:
        query = """
        INSERT INTO BAITOAN (maNguoiDung, duongDan, deBaiTho, loaiHinh, tomTatDe)
        OUTPUT INSERTED.maBaiToan
        VALUES (%s, %s, %s, %s, %s);
        """
        result = self.db.execute_query(query, (
            bai_toan.maNguoiDung,
            bai_toan.duongDan,
            bai_toan.deBaiTho,
            bai_toan.loaiHinh,
            bai_toan.tomTatDe
        ))
        return result[0]['maBaiToan']
    
    def create_from_dict(self, data: dict) -> int:
        """Tạo bài toán từ dict (dùng cho AI upload)"""
        query = """
        INSERT INTO BAITOAN (maNguoiDung, duongDan, deBaiTho, loaiHinh, tomTatDe)
        OUTPUT INSERTED.maBaiToan
        VALUES (%s, %s, %s, %s, %s);
        """
        print(f"Executing query with params: maNguoiDung={data.get('maNguoiDung')}, duongDan={data.get('duongDan')}")
        result = self.db.execute_query(query, (
            data.get("maNguoiDung"),
            data.get("duongDan"),
            data.get("deBaiTho"),
            data.get("loaiHinh"),
            data.get("tomTatDe")
        ))
        print(f"Query result: {result}")
        return result[0]['maBaiToan']
    
    def get_all(self) -> List[dict]:
        query = "SELECT * FROM BAITOAN"
        return self.db.execute_query(query)
    
    def get_by_id(self, ma_bai_toan: int) -> Optional[dict]:
        query = "SELECT * FROM BAITOAN WHERE maBaiToan = %s"
        results = self.db.execute_query(query, (ma_bai_toan,))
        return results[0] if results else None
    
    def get_by_user(self, ma_nguoi_dung: int) -> List[dict]:
        query = "SELECT * FROM BAITOAN WHERE maNguoiDung = %s"
        return self.db.execute_query(query, (ma_nguoi_dung,))
