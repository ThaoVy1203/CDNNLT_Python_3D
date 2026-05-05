"""
SymPy Solver - Tính toán tọa độ 3D từ ràng buộc hình học
"""
from typing import Dict, List
import math

class SymPySolver:
    """Solver tính toán tọa độ 3D"""
    
    def solve(self, shape_type: str, constraints: Dict) -> Dict:
        """
        Giải bài toán hình học
        
        Args:
            shape_type: Loại hình (pyramid, prism, cube)
            constraints: Ràng buộc hình học
            
        Returns:
            Dict chứa points, edges, faces
        """
        if "pyramid" in shape_type.lower():
            return self.solve_pyramid(constraints)
        elif "prism" in shape_type.lower():
            return self.solve_prism(constraints)
        elif "cube" in shape_type.lower():
            return self.solve_cube(constraints)
        else:
            return self.solve_generic(constraints)
    
    def solve_pyramid(self, constraints: Dict) -> Dict:
        """
        Giải hình chóp
        
        Giả sử: Hình chóp S.ABCD
        - Đáy ABCD là hình vuông cạnh a
        - S là đỉnh, SA vuông góc đáy
        """
        base = constraints.get("base", {})
        apex = constraints.get("apex", {})
        special_points = constraints.get("special_points", [])
        
        a = base.get("side", 1.0)
        h = apex.get("height", 1.414)
        
        # Đặt hệ tọa độ: A tại gốc, đáy trên mặt phẳng z=0
        points = {
            "A": [0, 0, 0],
            "B": [a, 0, 0],
            "C": [a, 0, a],
            "D": [0, 0, a],
            "S": [0, h, 0]  # S vuông góc đáy tại A
        }
        
        # Danh sách điểm đặc biệt
        special_point_names = []
        
        # Thêm các điểm đặc biệt
        if special_points and isinstance(special_points, list):
            for sp in special_points:
                if sp.get("type") == "midpoint":
                    segment = sp.get("segment", [])
                    if len(segment) == 2 and segment[0] in points and segment[1] in points:
                        p1 = points[segment[0]]
                        p2 = points[segment[1]]
                        points[sp["name"]] = [
                            (p1[0] + p2[0]) / 2,
                            (p1[1] + p2[1]) / 2,
                            (p1[2] + p2[2]) / 2
                        ]
                        special_point_names.append(sp["name"])
        
        # Cạnh chính (solid)
        edges = [
            {"start": "A", "end": "B", "style": "solid", "type": "main"},
            {"start": "B", "end": "C", "style": "solid", "type": "main"},
            {"start": "C", "end": "D", "style": "solid", "type": "main"},
            {"start": "D", "end": "A", "style": "solid", "type": "main"},
            {"start": "S", "end": "A", "style": "solid", "type": "main"},
            {"start": "S", "end": "B", "style": "solid", "type": "main"},
            {"start": "S", "end": "C", "style": "solid", "type": "main"},
            {"start": "S", "end": "D", "style": "solid", "type": "main"}
        ]
        
        # Thêm cạnh đến điểm đặc biệt - VẼ DẠNG NÉT ĐỨT
        if special_points and isinstance(special_points, list):
            for sp_name in special_point_names:
                # Cạnh từ đỉnh S đến điểm đặc biệt
                edges.append({
                    "start": "S",
                    "end": sp_name,
                    "style": "dashed",
                    "type": "auxiliary"
                })
        
        faces = [
            {"vertices": ["A", "B", "C", "D"]},  # Đáy
            {"vertices": ["S", "A", "B"]},       # Mặt bên
            {"vertices": ["S", "B", "C"]},
            {"vertices": ["S", "C", "D"]},
            {"vertices": ["S", "D", "A"]}
        ]
        
        # Tạo annotations mặc định
        annotations = {
            "edges": [],
            "points": [],
            "perpendicular": [],
            "angles": []
        }
        
        return {
            "points": points,
            "edges": edges,
            "faces": faces,
            "annotations": annotations
        }
    
    def solve_prism(self, constraints: Dict) -> Dict:
        """Giải lăng trụ"""
        base = constraints.get("base", {})
        a = base.get("side", 1.0)
        h = constraints.get("height", 1.0)
        
        # Lăng trụ tam giác ABC.A'B'C'
        points = {
            "A": [0, 0, 0],
            "B": [a, 0, 0],
            "C": [a/2, 0, a * math.sqrt(3)/2],
            "A'": [0, h, 0],
            "B'": [a, h, 0],
            "C'": [a/2, h, a * math.sqrt(3)/2]
        }
        
        edges = [
            {"start": "A", "end": "B"},
            {"start": "B", "end": "C"},
            {"start": "C", "end": "A"},
            {"start": "A'", "end": "B'"},
            {"start": "B'", "end": "C'"},
            {"start": "C'", "end": "A'"},
            {"start": "A", "end": "A'"},
            {"start": "B", "end": "B'"},
            {"start": "C", "end": "C'"}
        ]
        
        faces = [
            {"vertices": ["A", "B", "C"]},
            {"vertices": ["A'", "B'", "C'"]},
            {"vertices": ["A", "B", "B'", "A'"]},
            {"vertices": ["B", "C", "C'", "B'"]},
            {"vertices": ["C", "A", "A'", "C'"]}
        ]
        
        return {
            "points": points,
            "edges": edges,
            "faces": faces
        }
    
    def solve_cube(self, constraints: Dict) -> Dict:
        """Giải hình lập phương"""
        a = constraints.get("side", 1.0)
        
        points = {
            "A": [0, 0, 0],
            "B": [a, 0, 0],
            "C": [a, 0, a],
            "D": [0, 0, a],
            "A'": [0, a, 0],
            "B'": [a, a, 0],
            "C'": [a, a, a],
            "D'": [0, a, a]
        }
        
        edges = [
            # Đáy
            {"start": "A", "end": "B"},
            {"start": "B", "end": "C"},
            {"start": "C", "end": "D"},
            {"start": "D", "end": "A"},
            # Đỉnh
            {"start": "A'", "end": "B'"},
            {"start": "B'", "end": "C'"},
            {"start": "C'", "end": "D'"},
            {"start": "D'", "end": "A'"},
            # Cạnh bên
            {"start": "A", "end": "A'"},
            {"start": "B", "end": "B'"},
            {"start": "C", "end": "C'"},
            {"start": "D", "end": "D'"}
        ]
        
        faces = [
            {"vertices": ["A", "B", "C", "D"]},
            {"vertices": ["A'", "B'", "C'", "D'"]},
            {"vertices": ["A", "B", "B'", "A'"]},
            {"vertices": ["B", "C", "C'", "B'"]},
            {"vertices": ["C", "D", "D'", "C'"]},
            {"vertices": ["D", "A", "A'", "D'"]}
        ]
        
        return {
            "points": points,
            "edges": edges,
            "faces": faces
        }
    
    def solve_generic(self, constraints: Dict) -> Dict:
        """Giải hình tổng quát - fallback"""
        return self.solve_pyramid(constraints)
