from app.core.database import DatabaseConnection
from app.models.nguoi_dung import NguoiDungCreate
from typing import List, Optional

class NguoiDungRepository:
    def __init__(self):
        self.db = DatabaseConnection()
    
    def create(self, nguoi_dung: NguoiDungCreate) -> int:
        query = """
        INSERT INTO NGUOIDUNG (tenDangNhap, email, matKhau, vaiTro)
        OUTPUT INSERTED.maNguoiDung
        VALUES (%s, %s, %s, %s);
        """
        result = self.db.execute_query(query, (
            nguoi_dung.tenDangNhap,
            nguoi_dung.email,
            nguoi_dung.matKhau,
            nguoi_dung.vaiTro
        ))
        return result[0]['maNguoiDung']
    
    def create_from_dict(self, data: dict) -> str:
        """Tạo user từ dict (dùng cho Google OAuth)"""
        query = """
        INSERT INTO NGUOIDUNG (maNguoiDung, tenDangNhap, email, matKhau, vaiTro)
        VALUES (%s, %s, %s, %s, %s);
        """
        self.db.execute_non_query(query, (
            data.get('maNguoiDung'),
            data.get('tenDangNhap', 'Google User'),
            data.get('email', ''),
            data.get('matKhau', ''),  # Google OAuth không cần password
            data.get('vaiTro', 'Thành viên')  # Sửa từ 'user' thành 'Thành viên'
        ))
        return data.get('maNguoiDung')
    
    def get_or_create_google_user(self, google_id: str, email: str = '', name: str = '') -> str:
        """Lấy hoặc tạo user Google OAuth"""
        # Kiểm tra user đã tồn tại chưa
        existing = self.get_by_id_string(google_id)
        if existing:
            return google_id
        
        # Tạo user mới
        try:
            self.create_from_dict({
                'maNguoiDung': google_id,
                'tenDangNhap': name or f'User_{google_id[:8]}',
                'email': email,
                'matKhau': '',  # Google OAuth không cần password
                'vaiTro': 'Thành viên'  # Sửa từ 'user' thành 'Thành viên'
            })
            print(f"Created new Google user: {google_id}")
            return google_id
        except Exception as e:
            print(f"Error creating Google user: {e}")
            raise
    
    def get_all(self) -> List[dict]:
        query = "SELECT * FROM NGUOIDUNG"
        return self.db.execute_query(query)
    
    def get_by_id(self, ma_nguoi_dung: int) -> Optional[dict]:
        query = "SELECT * FROM NGUOIDUNG WHERE maNguoiDung = %s"
        results = self.db.execute_query(query, (ma_nguoi_dung,))
        return results[0] if results else None
    
    def get_by_id_string(self, ma_nguoi_dung: str) -> Optional[dict]:
        """Lấy user theo ID dạng string (cho Google OAuth)"""
        query = "SELECT * FROM NGUOIDUNG WHERE maNguoiDung = %s"
        results = self.db.execute_query(query, (ma_nguoi_dung,))
        return results[0] if results else None
    
    def delete(self, ma_nguoi_dung: int) -> int:
        query = "DELETE FROM NGUOIDUNG WHERE maNguoiDung = %s"
        return self.db.execute_non_query(query, (ma_nguoi_dung,))

