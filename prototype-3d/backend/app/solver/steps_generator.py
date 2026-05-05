"""
Steps Generator - Tạo thứ tự dựng hình logic
"""
from typing import Dict, List, Any

class StepsGenerator:
    """Generator tạo các bước dựng hình"""
    
    def generate(self, shape_type: str, geometry_data: Dict) -> List[Dict]:
        """
        Tạo steps dựa trên loại hình
        
        Args:
            shape_type: Loại hình
            geometry_data: Dữ liệu geometry (points, edges, faces, annotations)
            
        Returns:
            List các steps với annotations phân bổ theo từng bước
        """
        if "pyramid" in shape_type.lower():
            return self.generate_pyramid_steps(geometry_data)
        elif "prism" in shape_type.lower():
            return self.generate_prism_steps(geometry_data)
        elif "cube" in shape_type.lower():
            return self.generate_cube_steps(geometry_data)
        else:
            return self.generate_generic_steps(geometry_data)
    
    def distribute_annotations(self, steps: List[Dict], all_annotations: Dict) -> List[Dict]:
        """
        Phân bổ annotations vào từng step dựa trên objects của step đó
        
        Args:
            steps: Danh sách steps
            all_annotations: Tất cả annotations từ solver
            
        Returns:
            Steps với annotations được phân bổ
        """
        if not all_annotations:
            return steps
        
        for step in steps:
            step_annotations = {
                "edges": [],
                "points": [],
                "perpendicular": [],
                "angles": []
            }
            
            step_objects = set(step.get("objects", []))
            
            # Phân bổ edge annotations
            for edge_ann in all_annotations.get("edges", []):
                edge_name = edge_ann.get("edge")
                # Kiểm tra cả 2 chiều của edge
                edge_reverse = "-".join(reversed(edge_name.split("-")))
                if edge_name in step_objects or edge_reverse in step_objects:
                    step_annotations["edges"].append(edge_ann)
            
            # Phân bổ point annotations
            for point_ann in all_annotations.get("points", []):
                point_name = point_ann.get("point")
                if point_name in step_objects:
                    step_annotations["points"].append(point_ann)
            
            # Phân bổ perpendicular annotations
            for perp_ann in all_annotations.get("perpendicular", []):
                line_name = perp_ann.get("line")
                line_reverse = "-".join(reversed(line_name.split("-")))
                if line_name in step_objects or line_reverse in step_objects:
                    step_annotations["perpendicular"].append(perp_ann)
            
            # Phân bổ angle annotations
            for angle_ann in all_annotations.get("angles", []):
                vertex_name = angle_ann.get("vertex")
                if vertex_name in step_objects:
                    step_annotations["angles"].append(angle_ann)
            
            # Chỉ thêm annotations nếu có ít nhất 1 loại
            if any(step_annotations.values()):
                step["annotations"] = step_annotations
        
        return steps
    
    def generate_pyramid_steps(self, data: Dict) -> List[Dict]:
        """Steps cho hình chóp"""
        points = data["points"]
        edges = data["edges"]
        annotations = data.get("annotations", {})
        
        # Tìm đỉnh (điểm cao nhất)
        apex = max(points.items(), key=lambda p: p[1][1])[0]
        
        # Tìm đáy
        base_points = sorted([p for p in points.keys() if p != apex and p != "M"])
        
        # Kiểm tra có điểm đặc biệt M không
        has_special_point = "M" in points
        
        # Tạo tên cạnh đáy
        base_edges = []
        for i in range(len(base_points)):
            p1 = base_points[i]
            p2 = base_points[(i+1) % len(base_points)]
            base_edges.append(f"{p1}-{p2}")
        
        # Tạo tên cạnh bên
        side_edges = [f"{apex}-{p}" for p in base_points]
        
        steps = [
            {
                "order": 1,
                "description": f"Vẽ đáy {''.join(base_points)}",
                "objects": base_points + base_edges,
                "highlight": base_points
            },
            {
                "order": 2,
                "description": f"Dựng đỉnh {apex}",
                "objects": [apex] + [f"{apex}-{base_points[0]}"],  # Thêm cạnh SA
                "highlight": [apex, f"{apex}-{base_points[0]}"]
            }
        ]
        
        # Nếu có điểm M, thêm bước vẽ M
        if has_special_point:
            steps.append({
                "order": 3,
                "description": "Nối các cạnh bên còn lại",
                "objects": [e for e in side_edges if e != f"{apex}-{base_points[0]}"],
                "highlight": [e for e in side_edges if e != f"{apex}-{base_points[0]}"]
            })
            steps.append({
                "order": 4,
                "description": "Xác định điểm M (trung điểm)",
                "objects": ["M"],
                "highlight": ["M"]
            })
            steps.append({
                "order": 5,
                "description": "Nối SM",
                "objects": [f"{apex}-M"],
                "highlight": [f"{apex}-M"]
            })
            steps.append({
                "order": 6,
                "description": "Hoàn thiện hình chóp",
                "objects": base_points + [apex, "M"] + base_edges + side_edges + [f"{apex}-M"],
                "highlight": []
            })
        else:
            steps.append({
                "order": 3,
                "description": "Nối các cạnh bên còn lại",
                "objects": [e for e in side_edges if e != f"{apex}-{base_points[0]}"],
                "highlight": [e for e in side_edges if e != f"{apex}-{base_points[0]}"]
            })
            steps.append({
                "order": 4,
                "description": "Hoàn thiện hình chóp",
                "objects": base_points + [apex] + base_edges + side_edges,
                "highlight": []
            })
        
        # Phân bổ annotations vào từng step
        steps = self.distribute_annotations(steps, annotations)
        
        return steps
    
    def generate_prism_steps(self, data: Dict) -> List[Dict]:
        """Steps cho lăng trụ"""
        points = data["points"]
        annotations = data.get("annotations", {})
        
        # Tách đáy và đỉnh
        base = sorted([p for p in points.keys() if "'" not in p])
        top = sorted([p for p in points.keys() if "'" in p])
        
        # Cạnh đáy
        base_edges = []
        for i in range(len(base)):
            p1 = base[i]
            p2 = base[(i+1) % len(base)]
            base_edges.append(f"{p1}-{p2}")
        
        # Cạnh đỉnh
        top_edges = []
        for i in range(len(top)):
            p1 = top[i]
            p2 = top[(i+1) % len(top)]
            top_edges.append(f"{p1}-{p2}")
        
        # Cạnh bên
        side_edges = [f"{b}-{b}'" for b in base]
        
        steps = [
            {
                "order": 1,
                "description": f"Vẽ đáy {''.join(base)}",
                "objects": base + base_edges,
                "highlight": base
            },
            {
                "order": 2,
                "description": f"Vẽ đỉnh {''.join(top)}",
                "objects": top + top_edges,
                "highlight": top
            },
            {
                "order": 3,
                "description": "Nối các cạnh bên",
                "objects": side_edges,
                "highlight": side_edges
            },
            {
                "order": 4,
                "description": "Hoàn thiện lăng trụ",
                "objects": base + top + base_edges + top_edges + side_edges,
                "highlight": []
            }
        ]
        
        # Phân bổ annotations
        steps = self.distribute_annotations(steps, annotations)
        
        return steps
    
    def generate_cube_steps(self, data: Dict) -> List[Dict]:
        """Steps cho hình lập phương"""
        return self.generate_prism_steps(data)
    
    def generate_generic_steps(self, data: Dict) -> List[Dict]:
        """Steps tổng quát"""
        points = data["points"]
        
        return [
            {
                "order": 1,
                "description": "Vẽ các điểm",
                "objects": list(points.keys()),
                "highlight": list(points.keys())
            },
            {
                "order": 2,
                "description": "Nối các cạnh",
                "objects": [],
                "highlight": []
            }
        ]
