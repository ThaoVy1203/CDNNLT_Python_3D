from app.core.database import DatabaseConnection
from typing import Optional, List


class DungHinh3DRepository:
    """
    Repository cho bảng DUNGHINH3D.

    Quy tắc nghiệp vụ:
        Mỗi maBaiToan chỉ được phép có duy nhất 1 bản ghi DUNGHINH3D.
        → create_from_dict thực hiện UPSERT: xóa hết bản ghi cũ (nếu có)
          rồi mới insert bản ghi mới.
    """

    def __init__(self):
        self.db = DatabaseConnection()

    def create_from_dict(self, data: dict) -> int:
        """Upsert dữ liệu dựng hình 3D theo maBaiToan.

        Đảm bảo 1 bài toán chỉ có duy nhất 1 bản ghi DUNGHINH3D bằng cách
        xóa hết bản ghi cũ trước khi insert mới. Nhờ đó dù route gọi với
        force_refresh hay không, dữ liệu vẫn không bị trùng.
        """
        ma_bai_toan = data.get("maBaiToan")

        # Bước 1: Xóa toàn bộ bản ghi cũ (nếu có) cho cùng maBaiToan
        if ma_bai_toan is not None:
            self.delete_by_bai_toan(ma_bai_toan)

        # Bước 2: Insert bản ghi mới
        query = """
        INSERT INTO DUNGHINH3D (maBaiToan, cacBuocVe, hamThreeJS, thamSo, codeThreeJS, huongDanVe)
        OUTPUT INSERTED.maDungHinh
        VALUES (%s, %s, %s, %s, %s, %s);
        """
        result = self.db.execute_query(query, (
            ma_bai_toan,
            data.get("cacBuocVe"),
            data.get("hamThreeJS"),
            data.get("thamSo"),
            data.get("codeThreeJS"),
            data.get("huongDanVe")
        ))
        return result[0]['maDungHinh']

    def get_by_bai_toan(self, ma_bai_toan: int) -> Optional[dict]:
        """Lấy dữ liệu dựng hình theo mã bài toán.

        Lý thuyết chỉ có 1 bản ghi/maBaiToan, nhưng vẫn ORDER BY DESC + TOP 1
        để phòng dữ liệu legacy còn trùng (đã sinh trước khi áp dụng upsert).
        """
        query = (
            "SELECT TOP 1 * FROM DUNGHINH3D "
            "WHERE maBaiToan = %s ORDER BY maDungHinh DESC"
        )
        results = self.db.execute_query(query, (ma_bai_toan,))
        return results[0] if results else None

    def get_by_id(self, ma_dung_hinh: int) -> Optional[dict]:
        """Lấy dữ liệu dựng hình theo ID"""
        query = "SELECT * FROM DUNGHINH3D WHERE maDungHinh = %s"
        results = self.db.execute_query(query, (ma_dung_hinh,))
        return results[0] if results else None

    def delete_by_bai_toan(self, ma_bai_toan: int) -> int:
        """Xóa toàn bộ bản ghi DUNGHINH3D theo maBaiToan.

        Phải dùng execute_non_query: DELETE không có resultset nên nếu dùng
        execute_query thì cursor.fetchall() sẽ raise và DELETE bị rollback,
        khiến bản ghi cũ vẫn còn → mỗi lần force_refresh lại sinh thêm 1 bản
        ghi trùng.
        """
        query = "DELETE FROM DUNGHINH3D WHERE maBaiToan = %s"
        return self.db.execute_non_query(query, (ma_bai_toan,))
