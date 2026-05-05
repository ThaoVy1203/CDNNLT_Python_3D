"""
API Routes
"""
from fastapi import APIRouter, HTTPException
from app.models.schemas import SolveRequest, SolveResponse
from app.solver.sympy_solver import SymPySolver
from app.solver.steps_generator import StepsGenerator

router = APIRouter()

solver = SymPySolver()
steps_gen = StepsGenerator()

@router.post("/solve", response_model=SolveResponse)
async def solve_geometry(request: SolveRequest):
    """
    Giải bài toán hình học và trả về tọa độ 3D
    
    Args:
        request: SolveRequest với shape_type và constraints
        
    Returns:
        SolveResponse với points, edges, faces, steps
    """
    try:
        # Giải bằng SymPy solver
        geometry_data = solver.solve(request.shape_type, request.constraints)
        
        # Generate steps
        steps = steps_gen.generate(request.shape_type, geometry_data)
        
        # Tính camera position
        points = geometry_data["points"]
        if points:
            # Tính center và size
            coords = list(points.values())
            min_x = min(p[0] for p in coords)
            max_x = max(p[0] for p in coords)
            min_y = min(p[1] for p in coords)
            max_y = max(p[1] for p in coords)
            min_z = min(p[2] for p in coords)
            max_z = max(p[2] for p in coords)
            
            center_x = (min_x + max_x) / 2
            center_y = (min_y + max_y) / 2
            center_z = (min_z + max_z) / 2
            
            size = max(max_x - min_x, max_y - min_y, max_z - min_z)
            distance = size * 2
            
            camera = {
                "position": [center_x + distance, center_y + distance, center_z + distance],
                "lookAt": [center_x, center_y, center_z]
            }
        else:
            camera = {
                "position": [3, 3, 3],
                "lookAt": [0, 0, 0]
            }
        
        return SolveResponse(
            points=geometry_data["points"],
            edges=geometry_data["edges"],
            faces=geometry_data["faces"],
            steps=steps,
            camera=camera
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/mock/{shape_type}")
async def get_mock_data(shape_type: str):
    """
    Lấy mock data cho testing
    
    Args:
        shape_type: pyramid, pyramid-special, prism, hoặc cube
        
    Returns:
        Mock geometry data
    """
    # Xử lý pyramid đặc biệt (có điểm M)
    if shape_type == "pyramid-special":
        mock_constraints = {
            "base": {"type": "square", "side": 1.0},
            "apex": {"height": 1.414, "perpendicular_to_base": True},
            "special_points": [
                {
                    "name": "M",
                    "type": "midpoint",
                    "segment": ["A", "B"]
                }
            ]
        }
        request = SolveRequest(
            shape_type="pyramid",
            constraints=mock_constraints
        )
        return await solve_geometry(request)
    
    # Các hình thông thường
    mock_constraints = {
        "pyramid": {
            "base": {"type": "square", "side": 1.0},
            "apex": {"height": 1.414, "perpendicular_to_base": True}
        },
        "prism": {
            "base": {"type": "triangle", "side": 1.0},
            "height": 1.0
        },
        "cube": {
            "side": 1.0
        }
    }
    
    if shape_type not in mock_constraints:
        raise HTTPException(status_code=404, detail="Shape type not found")
    
    request = SolveRequest(
        shape_type=shape_type,
        constraints=mock_constraints[shape_type]
    )
    
    return await solve_geometry(request)
