from database.connection import DatabaseConnection
from models.nguoi_dung import NguoiDungCreate, NguoiDungResponse
from typing import List, Optional

class NguoiDungRepository:
    def __init__(self):
        self.db = DatabaseConnection()
    
    def create(self, nguoi_dung: NguoiDungCreate) -> int:
        query = """
        INSERT INTO NGUOIDUNG (tenDangNhap, email, matKhau, vaiTro)
        VALUES (%s, %s, %s, %s);
        SELECT SCOPE_IDENTITY() as id;
        """
        result = self.db.execute_query(query, (
            nguoi_dung.tenDangNhap,
            nguoi_dung.email,
            nguoi_dung.matKhau,
            nguoi_dung.vaiTro
        ))
        return int(result[0]['id'])
    
    def get_all(self) -> List[dict]:
        query = "SELECT * FROM NGUOIDUNG"
        return self.db.execute_query(query)
    
    def get_by_id(self, ma_nguoi_dung: int) -> Optional[dict]:
        query = "SELECT * FROM NGUOIDUNG WHERE maNguoiDung = %s"
        results = self.db.execute_query(query, (ma_nguoi_dung,))
        return results[0] if results else None
    
    def delete(self, ma_nguoi_dung: int) -> int:
        query = "DELETE FROM NGUOIDUNG WHERE maNguoiDung = %s"
        return self.db.execute_non_query(query, (ma_nguoi_dung,))
