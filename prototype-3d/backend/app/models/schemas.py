"""
Pydantic models cho API
"""
from pydantic import BaseModel
from typing import Dict, List, Optional

class BaseConstraints(BaseModel):
    type: str
    side: Optional[float] = 1.0

class ApexConstraints(BaseModel):
    height: float
    perpendicular_to_base: bool = True

class SolveRequest(BaseModel):
    shape_type: str
    constraints: Dict

class Point3D(BaseModel):
    x: float
    y: float
    z: float

class Edge(BaseModel):
    start: str
    end: str
    style: Optional[str] = "solid"  # solid, dashed, dotted
    type: Optional[str] = "main"    # main, auxiliary

class Face(BaseModel):
    vertices: List[str]

class Step(BaseModel):
    order: int
    description: str
    objects: List[str]
    highlight: Optional[List[str]] = []
    annotations: Optional[Dict] = None  # Annotations cho step này

class SolveResponse(BaseModel):
    points: Dict[str, List[float]]
    edges: List[Edge]
    faces: List[Face]
    steps: List[Step]
    camera: Optional[Dict] = None
