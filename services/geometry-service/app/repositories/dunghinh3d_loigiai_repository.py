from app.core.database import DatabaseConnection
from typing import Optional


class DungHinh3DLoiGiaiRepository:
    """
    Repository cho bảng DUNGHINH3D_LOIGIAI.
    Lưu dữ liệu dựng hình bổ sung theo lời giải.

    Quy tắc nghiệp vụ:
        Mỗi maLoiGiai chỉ được phép có duy nhất 1 bản ghi.
        → create_from_dict thực hiện UPSERT: xóa bản ghi cũ rồi insert mới.
    """

    def __init__(self):
        self.db = DatabaseConnection()

    def create_from_dict(self, data: dict) -> int:
        """Upsert dữ liệu dựng hình bổ sung theo maLoiGiai."""
        ma_loi_giai = data.get("maLoiGiai")

        # Xóa bản ghi cũ (nếu có) cho cùng maLoiGiai
        if ma_loi_giai is not None:
            self.delete_by_loi_giai(ma_loi_giai)

        # Insert bản ghi mới
        query = """
        INSERT INTO DUNGHINH3D_LOIGIAI (maLoiGiai, cacBuocVe, hamThreeJS, thamSo, codeThreeJS, huongDanVe)
        OUTPUT INSERTED.maDungHinhLoiGiai
        VALUES (%s, %s, %s, %s, %s, %s);
        """
        result = self.db.execute_query(query, (
            ma_loi_giai,
            data.get("cacBuocVe"),
            data.get("hamThreeJS"),
            data.get("thamSo"),
            data.get("codeThreeJS"),
            data.get("huongDanVe")
        ))
        return result[0]['maDungHinhLoiGiai']

    def get_by_loi_giai(self, ma_loi_giai: int) -> Optional[dict]:
        """Lấy dữ liệu dựng hình bổ sung theo mã lời giải."""
        query = (
            "SELECT TOP 1 * FROM DUNGHINH3D_LOIGIAI "
            "WHERE maLoiGiai = %s ORDER BY maDungHinhLoiGiai DESC"
        )
        results = self.db.execute_query(query, (ma_loi_giai,))
        return results[0] if results else None

    def get_by_id(self, ma_dung_hinh_loi_giai: int) -> Optional[dict]:
        """Lấy dữ liệu dựng hình bổ sung theo ID."""
        query = "SELECT * FROM DUNGHINH3D_LOIGIAI WHERE maDungHinhLoiGiai = %s"
        results = self.db.execute_query(query, (ma_dung_hinh_loi_giai,))
        return results[0] if results else None

    def delete_by_loi_giai(self, ma_loi_giai: int) -> int:
        """Xóa toàn bộ bản ghi theo maLoiGiai."""
        query = "DELETE FROM DUNGHINH3D_LOIGIAI WHERE maLoiGiai = %s"
        return self.db.execute_non_query(query, (ma_loi_giai,))
