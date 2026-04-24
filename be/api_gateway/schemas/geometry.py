from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from enum import Enum

# ============= Định nghĩa các kiểu dữ liệu cơ bản =============

Point3D = List[float]

class RelationType(str, Enum):
    """Các loại quan hệ hình học"""
    PERPENDICULAR = "perpendicular"  # Vuông góc
    PARALLEL = "parallel"  # Song song
    INTERSECT = "intersect"  # Giao nhau
    CONTAINS = "contains"  # Chứa
    COPLANAR = "coplanar"  # Đồng phẳng

class EntityType(str, Enum):
    """Các loại thực thể hình học"""
    POINT = "point"
    LINE = "line"
    PLANE = "plane"
    SEGMENT = "segment"
    VECTOR = "vector"

# ============= Schemas cho các thực thể hình học =============

class Point(BaseModel):
    """Điểm trong không gian 3D"""
    name: str = Field(..., description="Tên điểm (vd: A, B, C, S)")
    coordinates: Optional[Point3D] = Field(None, description="Tọa độ [x, y, z]")
    description: Optional[str] = Field(None, description="Mô tả vị trí điểm")

class Line(BaseModel):
    """Đường thẳng trong không gian 3D"""
    name: str = Field(..., description="Tên đường thẳng (vd: AB, d)")
    points: List[str] = Field(..., description="Các điểm thuộc đường thẳng")
    direction_vector: Optional[Point3D] = Field(None, description="Vector chỉ phương")
    description: Optional[str] = Field(None, description="Mô tả đường thẳng")

class Plane(BaseModel):
    """Mặt phẳng trong không gian 3D"""
    name: str = Field(..., description="Tên mặt phẳng (vd: ABC, (P))")
    points: List[str] = Field(..., description="Các điểm thuộc mặt phẳng")
    normal_vector: Optional[Point3D] = Field(None, description="Vector pháp tuyến")
    description: Optional[str] = Field(None, description="Mô tả mặt phẳng")

class GeometricRelation(BaseModel):
    """Quan hệ giữa các thực thể hình học"""
    entity1: str = Field(..., description="Tên thực thể thứ nhất")
    entity1_type: EntityType = Field(..., description="Loại thực thể thứ nhất")
    relation: RelationType = Field(..., description="Loại quan hệ")
    entity2: str = Field(..., description="Tên thực thể thứ hai")
    entity2_type: EntityType = Field(..., description="Loại thực thể thứ hai")
    confidence: float = Field(default=1.0, ge=0.0, le=1.0, description="Độ tin cậy (0-1)")

# ============= Schema chính cho dữ liệu trích xuất =============

class GeometryExtraction(BaseModel):
    """Dữ liệu hình học được trích xuất từ ảnh/text"""
    
    # Thông tin bài toán
    problem_text: str = Field(..., description="Nội dung bài toán được OCR")
    problem_type: str = Field(..., description="Loại bài toán (vd: tính khoảng cách, góc, thể tích)")
    
    # Các thực thể hình học
    points: List[Point] = Field(default_factory=list, description="Danh sách các điểm")
    lines: List[Line] = Field(default_factory=list, description="Danh sách các đường thẳng")
    planes: List[Plane] = Field(default_factory=list, description="Danh sách các mặt phẳng")
    
    # Quan hệ hình học
    relations: List[GeometricRelation] = Field(default_factory=list, description="Các quan hệ hình học")
    
    # Điều kiện và yêu cầu
    given_conditions: List[str] = Field(default_factory=list, description="Các điều kiện cho trước")
    questions: List[str] = Field(default_factory=list, description="Các câu hỏi cần giải")
    
    # Metadata
    confidence_score: float = Field(default=1.0, ge=0.0, le=1.0, description="Độ tin cậy tổng thể")
    extraction_notes: Optional[str] = Field(None, description="Ghi chú về quá trình trích xuất")

# ============= Response schemas cho API =============

class Points(BaseModel):
    """Legacy schema - giữ để tương thích"""
    A: Point3D
    B: Point3D
    C: Point3D
    S: Point3D

class GeometryResponse(BaseModel):
    """Response trả về từ API"""
    points: Points
    extraction: Optional[GeometryExtraction] = None

class ImageAnalysisRequest(BaseModel):
    """Request để phân tích ảnh"""
    image_base64: Optional[str] = Field(None, description="Ảnh dạng base64")
    additional_context: Optional[str] = Field(None, description="Thông tin bổ sung")
