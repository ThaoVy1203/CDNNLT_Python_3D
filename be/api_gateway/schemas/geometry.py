from pydantic import BaseModel
from typing import List

Point3D = List[float]

class Points(BaseModel):
    A: Point3D
    B: Point3D
    C: Point3D
    S: Point3D

class GeometryResponse(BaseModel):
    points: Points
