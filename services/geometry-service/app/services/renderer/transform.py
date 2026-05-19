"""
3D Renderer - Chuyển đổi dữ liệu hình học sang định dạng 3D JSON
"""
from typing import Dict, List, Any

class GeometryRenderer:
    """Renderer để chuyển đổi dữ liệu hình học sang 3D visualization"""
    
    def __init__(self):
        self.default_camera = [5, 5, 5]
    
    def transform_to_3d(self, geometry_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Chuyển đổi dữ liệu hình học sang định dạng 3D JSON
        
        Args:
            geometry_data: Dict chứa points, edges, relations
            
        Returns:
            Dict với format cho Three.js/React Three Fiber
        """
        points = geometry_data.get("points", [])
        edges = geometry_data.get("edges", [])
        relations = geometry_data.get("relations", [])
        
        # Transform points
        points_3d = self._transform_points(points)
        
        # Transform edges
        edges_3d = self._transform_edges(edges, points_3d)
        
        # Generate faces (nếu có)
        faces_3d = self._generate_faces(points_3d, edges_3d, relations)
        
        # Calculate camera position
        camera_pos = self._calculate_camera_position(points_3d)
        
        return {
            "points": points_3d,
            "edges": edges_3d,
            "faces": faces_3d,
            "camera_position": camera_pos,
            "metadata": {
                "point_count": len(points_3d),
                "edge_count": len(edges_3d),
                "face_count": len(faces_3d)
            }
        }
    
    def _transform_points(self, points: List[Dict]) -> Dict[str, List[float]]:
        """Chuyển đổi danh sách điểm sang dict với tên điểm làm key"""
        result = {}
        
        for point in points:
            name = point.get("name", "")
            coords = point.get("coordinates")
            
            if name and coords and len(coords) == 3:
                result[name] = coords
            elif name and not coords:
                # Tạo tọa độ mặc định nếu chưa có
                result[name] = [0, 0, 0]
        
        return result
    
    def _transform_edges(self, edges: List[List[str]], 
                        points: Dict[str, List[float]]) -> List[Dict[str, Any]]:
        """Chuyển đổi danh sách cạnh"""
        result = []
        
        for edge in edges:
            if len(edge) >= 2:
                p1, p2 = edge[0], edge[1]
                if p1 in points and p2 in points:
                    result.append({
                        "start": p1,
                        "end": p2,
                        "start_coords": points[p1],
                        "end_coords": points[p2]
                    })
        
        return result
    
    def _generate_faces(self, points: Dict[str, List[float]], 
                       edges: List[Dict], 
                       relations: List[Dict]) -> List[Dict[str, Any]]:
        """Tạo các mặt phẳng từ quan hệ hình học"""
        faces = []
        
        # Tìm các mặt phẳng từ relations
        for relation in relations:
            rel_type = relation.get("type", "").lower()
            entities = relation.get("entities", [])
            
            # Nếu là mặt phẳng hoặc đa giác
            if "plane" in rel_type or "polygon" in rel_type:
                if len(entities) >= 3:
                    # Lấy tọa độ các điểm
                    face_points = []
                    for entity in entities:
                        if entity in points:
                            face_points.append(points[entity])
                    
                    if len(face_points) >= 3:
                        faces.append({
                            "vertices": entities,
                            "coordinates": face_points,
                            "type": rel_type
                        })
        
        return faces
    
    def _calculate_camera_position(self, points: Dict[str, List[float]]) -> List[float]:
        """Tính vị trí camera tối ưu dựa trên bounding box"""
        if not points:
            return self.default_camera
        
        # Tìm bounding box
        coords = list(points.values())
        
        min_x = min(p[0] for p in coords)
        max_x = max(p[0] for p in coords)
        min_y = min(p[1] for p in coords)
        max_y = max(p[1] for p in coords)
        min_z = min(p[2] for p in coords)
        max_z = max(p[2] for p in coords)
        
        # Center
        center_x = (min_x + max_x) / 2
        center_y = (min_y + max_y) / 2
        center_z = (min_z + max_z) / 2
        
        # Distance
        size = max(max_x - min_x, max_y - min_y, max_z - min_z)
        distance = size * 2
        
        return [
            center_x + distance,
            center_y + distance,
            center_z + distance
        ]


def convert_to_3d_json(geometry_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Helper function - backward compatibility
    """
    renderer = GeometryRenderer()
    return renderer.transform_to_3d(geometry_data)
