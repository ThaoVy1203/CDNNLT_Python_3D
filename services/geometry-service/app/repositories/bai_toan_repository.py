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
    
    def get_by_user(self, ma_nguoi_dung: str) -> List[dict]:
        """Lấy tất cả bài toán của người dùng, sắp xếp theo ngày tạo mới nhất"""
        query = """
        SELECT 
            bt.*,
            CASE WHEN lg.maLoiGiai IS NOT NULL THEN 1 ELSE 0 END AS hasSolution
        FROM BAITOAN bt
        LEFT JOIN LOIGIAI lg ON bt.maBaiToan = lg.maBaiToan
        WHERE bt.maNguoiDung = %s 
        ORDER BY bt.ngayTao DESC
        """
        return self.db.execute_query(query, (ma_nguoi_dung,))
    
    def delete(self, ma_bai_toan: int) -> bool:
        """Xóa bài toán và các dữ liệu liên quan (cascading delete)"""
        try:
            # Xóa theo thứ tự: LOIGIAI -> DUNGHINH3D -> DULIEUHINHHOC -> BAITOAN
            self.db.execute_query("DELETE FROM LOIGIAI WHERE maBaiToan = %s", (ma_bai_toan,))
            self.db.execute_query("DELETE FROM DUNGHINH3D WHERE maBaiToan = %s", (ma_bai_toan,))
            self.db.execute_query("DELETE FROM DULIEUHINHHOC WHERE maBaiToan = %s", (ma_bai_toan,))
            self.db.execute_query("DELETE FROM BAITOAN WHERE maBaiToan = %s", (ma_bai_toan,))
            return True
        except Exception as e:
            print(f"Error deleting problem: {e}")
            return False
