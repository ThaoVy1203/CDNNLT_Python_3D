"""
Geometry Solver - Tính toán tọa độ 3D từ đề bài hình học
Sử dụng SymPy và các thuật toán hình học không gian
"""
import math
import re
from typing import Dict, List, Any, Optional


class GeometrySolver:
    """Solver tính toán tọa độ 3D cho hình học không gian"""
    
    def solve_from_extraction(self, extraction_data: Dict, problem_type: str) -> Dict[str, Any]:
        """
        Giải bài toán hình học từ dữ liệu Gemini AI extraction
        
        Args:
            extraction_data: Dữ liệu đã được Gemini AI trích xuất
                {
                    "problem_text": str,
                    "problem_type": str,
                    "given_conditions": List[str],
                    "questions": List[str],
                    "points": List[str],
                    "relationships": List[str]
                }
            problem_type: Loại hình (pyramid, prism, cube, tetrahedron)
            
        Returns:
            Dict chứa points, edges, faces, steps, annotations
        """
        try:
            print(f"📊 [GeometrySolver] Solving from extraction data")
            print(f"   Problem type: {problem_type}")
            print(f"   Extraction data type: {type(extraction_data)}")
            print(f"   Given conditions: {extraction_data.get('given_conditions', [])}")
            print(f"   Points: {extraction_data.get('points', [])}")
            
            # Validate extraction_data
            if not isinstance(extraction_data, dict):
                print(f"⚠️ [GeometrySolver] extraction_data is not dict, converting...")
                extraction_data = {}
            
            # Detect shape type
            shape_type = self._detect_shape_type_from_extraction(extraction_data, problem_type)
            print(f"   Detected shape: {shape_type}")
            
            # Extract constraints from Gemini data
            constraints = self._extract_constraints_from_gemini(extraction_data, shape_type)
            print(f"   Extracted constraints: {constraints}")
            
            # Solve geometry
            result = self.solve(shape_type, constraints)
            print(f"✅ [GeometrySolver] Geometry solved successfully")
            
            return result
        except Exception as e:
            print(f"❌ [GeometrySolver] Error in solve_from_extraction: {e}")
            import traceback
            traceback.print_exc()
            # Return default pyramid as fallback
            return self._solve_pyramid({
                "base": {"type": "square", "side": 1.0},
                "apex": {"height": 1.414, "perpendicular_to_base": True}
            })
    
    def solve_from_problem(self, problem_text: str, problem_type: str) -> Dict[str, Any]:
        """
        Giải bài toán hình học từ text (fallback method)
        
        Args:
            problem_text: Đề bài (text)
            problem_type: Loại hình (pyramid, prism, cube, tetrahedron)
            
        Returns:
            Dict chứa points, edges, faces, steps, annotations
        """
        print(f"⚠️ [GeometrySolver] Using fallback text parsing (not recommended)")
        print(f"   Problem text: {problem_text[:100]}...")
        
        # Parse problem type
        shape_type = self._detect_shape_type(problem_text, problem_type)
        
        # Extract constraints from problem text
        constraints = self._extract_constraints(problem_text, shape_type)
        
        # Solve geometry
        return self.solve(shape_type, constraints)
    
    def solve(self, shape_type: str, constraints: Dict) -> Dict[str, Any]:
        """Giải bài toán hình học"""
        # Ensure shape_type is string
        if not isinstance(shape_type, str):
            shape_type = str(shape_type) if shape_type else "pyramid"
        
        shape_type_lower = shape_type.lower()
        
        if "pyramid" in shape_type_lower or "chóp" in shape_type_lower:
            return self._solve_pyramid(constraints)
        elif "prism" in shape_type_lower or "lăng trụ" in shape_type_lower:
            return self._solve_prism(constraints)
        elif "cube" in shape_type_lower or "lập phương" in shape_type_lower:
            return self._solve_cube(constraints)
        elif "tetrahedron" in shape_type_lower or "tứ diện" in shape_type_lower:
            return self._solve_tetrahedron(constraints)
        else:
            return self._solve_pyramid(constraints)  # Default
    
    def _detect_shape_type_from_extraction(self, extraction_data: Dict, problem_type: str) -> str:
        """Phát hiện loại hình từ dữ liệu Gemini extraction"""
        # Priority 1: Use problem_type from extraction
        extracted_type = extraction_data.get("problem_type", "")
        if isinstance(extracted_type, str):
            extracted_type = extracted_type.lower()
        else:
            extracted_type = ""
        
        if "tứ diện" in extracted_type or "tetrahedron" in extracted_type:
            return "tetrahedron"
        elif "lăng trụ" in extracted_type or "prism" in extracted_type:
            return "prism"
        elif "lập phương" in extracted_type or "cube" in extracted_type:
            return "cube"
        elif "chóp" in extracted_type or "pyramid" in extracted_type:
            return "pyramid"
        
        # Priority 2: Check problem_text
        problem_text = extraction_data.get("problem_text", "")
        if isinstance(problem_text, str):
            problem_text = problem_text.lower()
            if "tứ diện" in problem_text or "tetrahedron" in problem_text:
                return "tetrahedron"
            elif "lăng trụ" in problem_text or "prism" in problem_text:
                return "prism"
            elif "lập phương" in problem_text or "cube" in problem_text:
                return "cube"
            elif "chóp" in problem_text or "pyramid" in problem_text:
                return "pyramid"
        
        # Priority 3: Use provided problem_type
        if isinstance(problem_type, str) and problem_type:
            return problem_type.lower()
        
        return "pyramid"
    
    def _detect_shape_type(self, problem_text: str, problem_type: str) -> str:
        """Phát hiện loại hình từ đề bài (fallback)"""
        text_lower = problem_text.lower()
        
        if "tứ diện" in text_lower or "tetrahedron" in text_lower:
            return "tetrahedron"
        elif "lăng trụ" in text_lower or "prism" in text_lower:
            return "prism"
        elif "lập phương" in text_lower or "cube" in text_lower:
            return "cube"
        elif "chóp" in text_lower or "pyramid" in text_lower:
            return "pyramid"
        
        return problem_type or "pyramid"
    
    def _extract_constraints_from_gemini(self, extraction_data: Dict, shape_type: str) -> Dict:
        """
        Trích xuất ràng buộc từ dữ liệu Gemini AI extraction
        
        Args:
            extraction_data: Dữ liệu từ Gemini AI
            shape_type: Loại hình đã detect
            
        Returns:
            Dict chứa constraints để dựng hình
        """
        constraints = {}
        
        given_conditions = extraction_data.get("given_conditions", [])
        points = extraction_data.get("points", [])
        relationships = extraction_data.get("relationships", [])
        problem_text = extraction_data.get("problem_text", "")
        
        # Parse base type and dimensions
        base_info = self._parse_base_from_conditions(given_conditions, problem_text)
        if base_info:
            constraints["base"] = base_info
        
        # Parse height/apex information
        apex_info = self._parse_apex_from_conditions(given_conditions, problem_text)
        if apex_info:
            constraints["apex"] = apex_info
        
        # Parse special points (trung điểm, tâm, etc.)
        special_points = self._parse_special_points(given_conditions, problem_text)
        if special_points:
            constraints["special_points"] = special_points
        
        # Parse perpendicular relationships
        perpendicular = self._parse_perpendicular(relationships, given_conditions)
        if perpendicular:
            constraints["perpendicular"] = perpendicular
        
        # Store points list
        if points:
            constraints["points_list"] = points
        
        # Store raw conditions & problem_text để các hàm solve có thể đọc thêm
        # (VD: _solve_prism cần biết "lăng trụ đứng" hay không)
        constraints["given_conditions"] = given_conditions
        constraints["problem_text"] = problem_text
        
        return constraints
    
    def _parse_base_from_conditions(self, conditions: List[str], problem_text: str) -> Optional[Dict]:
        """Parse thông tin đáy từ given_conditions"""
        # Helper: kiểm tra chuỗi có "hình vuông" thực sự không (không phải "vuông góc"/"tam giác vuông")
        def is_real_square(text: str) -> bool:
            t = text.lower()
            if "hình vuông" in t:
                return True
            # "vuông cạnh a" cũng coi là hình vuông (VD: "đáy ABCD là vuông cạnh a")
            if "vuông cạnh" in t or "vuông tâm" in t:
                return True
            return False
        
        for condition in conditions:
            # Ensure condition is string
            if not isinstance(condition, str):
                continue
            
            condition_lower = condition.lower()
            
            # ƯU TIÊN: Tam giác vuông (check TRƯỚC hình vuông để tránh nhầm "vuông tại B")
            if "tam giác vuông" in condition_lower or "vuông tại" in condition_lower:
                side = self._extract_number(condition, default=1.0)
                return {"type": "right_triangle", "side": side}
            
            # Tam giác đều
            elif "tam giác đều" in condition_lower:
                side = self._extract_number(condition, default=1.0)
                return {"type": "equilateral_triangle", "side": side}
            
            # Tam giác thường
            elif "tam giác" in condition_lower:
                side = self._extract_number(condition, default=1.0)
                return {"type": "triangle", "side": side}
            
            # Hình vuông (chỉ match "hình vuông" thực sự, không match "vuông góc")
            elif is_real_square(condition):
                side = self._extract_number(condition, default=1.0)
                return {"type": "square", "side": side}
            
            # Hình chữ nhật
            elif "hình chữ nhật" in condition_lower or "chữ nhật" in condition_lower:
                # Try to extract width and height
                numbers = self._extract_all_numbers(condition)
                if len(numbers) >= 2:
                    return {"type": "rectangle", "width": numbers[0], "height": numbers[1]}
                else:
                    return {"type": "rectangle", "width": 1.0, "height": 1.5}
        
        # Fallback: check problem_text (CŨNG ƯU TIÊN TAM GIÁC TRƯỚC)
        if isinstance(problem_text, str):
            text_lower = problem_text.lower()
            if "tam giác vuông" in text_lower or "vuông tại" in text_lower:
                return {"type": "right_triangle", "side": 1.0}
            elif "tam giác đều" in text_lower:
                return {"type": "equilateral_triangle", "side": 1.0}
            elif "tam giác" in text_lower:
                return {"type": "triangle", "side": 1.0}
            elif "hình vuông" in text_lower:
                return {"type": "square", "side": 1.0}
            elif "hình chữ nhật" in text_lower or "chữ nhật" in text_lower:
                return {"type": "rectangle", "width": 1.0, "height": 1.5}
        
        return None
    
    def _parse_apex_from_conditions(self, conditions: List[str], problem_text: str) -> Optional[Dict]:
        """Parse thông tin đỉnh/chiều cao từ given_conditions"""
        for condition in conditions:
            # Ensure condition is string
            if not isinstance(condition, str):
                continue
            
            condition_lower = condition.lower()
            
            # SA = ... (cạnh bên)
            if re.search(r'sa\s*=', condition_lower):
                height = self._extract_number(condition, default=1.414)
                # Check if perpendicular
                perpendicular = "⊥" in condition or "vuông góc" in condition_lower
                return {
                    "height": height,
                    "perpendicular_to_base": perpendicular,
                    "edge_name": "SA"
                }
            
            # Chiều cao
            elif "chiều cao" in condition_lower or "cao" in condition_lower:
                height = self._extract_number(condition, default=1.0)
                return {
                    "height": height,
                    "perpendicular_to_base": True
                }
            
            # Check for perpendicular notation: "SA vuông góc với mặt phẳng đáy"
            elif "vuông góc" in condition_lower or "⊥" in condition:
                # Extract edge name (e.g., "SA ⊥ (ABCD)" or "cạnh bên SA vuông góc")
                match = re.search(r'(?:cạnh bên\s+)?([A-Z]{2})\s+(?:vuông góc|⊥)', condition)
                if match:
                    edge_name = match.group(1)
                    # Try to find length of this edge
                    height = self._extract_number(condition, default=1.414)
                    print(f"   [_parse_apex] Found perpendicular edge: {edge_name}, height={height}")
                    return {
                        "height": height,
                        "perpendicular_to_base": True,
                        "edge_name": edge_name
                    }
        
        # Fallback: Check problem_text for SA perpendicular
        if isinstance(problem_text, str):
            if "sa vuông góc" in problem_text.lower() or "sa ⊥" in problem_text.lower():
                print(f"   [_parse_apex] Found SA perpendicular in problem_text (fallback)")
                return {
                    "height": 1.414,  # Default
                    "perpendicular_to_base": True,
                    "edge_name": "SA"
                }
        
        return None
    
    def _parse_special_points(self, conditions: List[str], problem_text: str) -> Optional[Dict]:
        """Parse các điểm đặc biệt (trung điểm, tâm, etc.)"""
        special = {}
        
        for condition in conditions:
            # Ensure condition is string
            if not isinstance(condition, str):
                continue
            
            condition_lower = condition.lower()
            
            # Trung điểm - hỗ trợ nhiều format:
            # "M là trung điểm AB"
            # "M là trung điểm của AB"
            # "Gọi M là trung điểm của CD"
            if "trung điểm" in condition_lower:
                # Try multiple patterns
                patterns = [
                    r'([A-Z])\s+(?:là\s+)?trung điểm\s+của\s+([A-Z]{2})',  # "M là trung điểm của CD"
                    r'([A-Z])\s+(?:là\s+)?trung điểm\s+([A-Z]{2})',        # "M là trung điểm CD"
                    r'gọi\s+([A-Z])\s+là\s+trung điểm\s+của\s+([A-Z]{2})', # "Gọi M là trung điểm của CD"
                    r'gọi\s+([A-Z])\s+là\s+trung điểm\s+([A-Z]{2})'        # "Gọi M là trung điểm CD"
                ]
                
                for pattern in patterns:
                    match = re.search(pattern, condition, re.IGNORECASE)
                    if match:
                        point_name = match.group(1)
                        edge = match.group(2)
                        special[point_name] = {
                            "type": "midpoint",
                            "of": edge
                        }
                        print(f"   [_parse_special_points] Found midpoint: {point_name} of {edge}")
                        break
            
            # Tâm đáy - hỗ trợ nhiều format:
            # "O là tâm đáy"
            # "O là tâm của đáy"
            # "Gọi O là tâm đáy ABCD"
            # "tâm đáy là O"
            elif "tâm" in condition_lower and ("đáy" in condition_lower or "day" in condition_lower):
                patterns = [
                    r'([A-Z])\s+(?:là\s+)?tâm\s+(?:của\s+)?đáy',           # "O là tâm đáy"
                    r'gọi\s+([A-Z])\s+là\s+tâm\s+(?:của\s+)?đáy',         # "Gọi O là tâm đáy"
                    r'tâm\s+(?:của\s+)?đáy\s+(?:là\s+)?([A-Z])',          # "tâm đáy là O"
                    r'([A-Z])\s+là\s+tâm\s+(?:của\s+)?hình\s+vuông',      # "O là tâm hình vuông"
                    r'([A-Z])\s+là\s+tâm\s+(?:của\s+)?tam\s+giác'         # "O là tâm tam giác"
                ]
                
                for pattern in patterns:
                    match = re.search(pattern, condition, re.IGNORECASE)
                    if match:
                        point_name = match.group(1)
                        special[point_name] = {
                            "type": "base_center",
                            "description": "Tâm đáy"
                        }
                        print(f"   [_parse_special_points] Found base center: {point_name}")
                        break
            
            # Tâm (không phải tâm đáy)
            elif "tâm" in condition_lower and "đáy" not in condition_lower:
                match = re.search(r'([A-Z])\s+(?:là\s+)?tâm', condition)
                if match:
                    point_name = match.group(1)
                    special[point_name] = {
                        "type": "center",
                        "description": "Tâm"
                    }
                    print(f"   [_parse_special_points] Found center: {point_name}")
        
        return special if special else None
    
    def _parse_perpendicular(self, relationships: List[str], conditions: List[str]) -> Optional[List[Dict]]:
        """Parse các quan hệ vuông góc"""
        perpendicular = []
        
        # Check relationships
        for rel in relationships:
            if not isinstance(rel, str):
                continue
            if "⊥" in rel or "vuông góc" in rel.lower():
                perpendicular.append({"description": rel})
        
        # Check conditions
        for condition in conditions:
            if not isinstance(condition, str):
                continue
            if "⊥" in condition or "vuông góc" in condition.lower():
                perpendicular.append({"description": condition})
        
        return perpendicular if perpendicular else None
    
    def _extract_number(self, text: str, default: float = 1.0) -> float:
        """
        Trích xuất số từ text
        Hỗ trợ: "a", "2a", "a√2", "√2", "1.5", etc.
        """
        if not isinstance(text, str):
            return default
        
        # Remove spaces
        text = text.replace(" ", "")
        
        # Pattern: số * a * √số
        # Examples: "2a√3", "a√2", "√2", "2a", "a", "1.5"
        
        # Check for √ pattern first
        if "√" in text:
            # Try to find: coefficient * a * √number
            # Pattern: (number)a√(number) or a√(number) or √(number)
            match = re.search(r'(\d*\.?\d*)\s*a?\s*√(\d+\.?\d*)', text)
            if match:
                coef_str = match.group(1)
                sqrt_str = match.group(2)
                
                coef = float(coef_str) if coef_str else 1.0
                sqrt_val = float(sqrt_str) if sqrt_str else 2.0
                
                result = coef * math.sqrt(sqrt_val)
                print(f"   [_extract_number] '{text}' → {coef} * √{sqrt_val} = {result}")
                return result
        
        # Try to find coefficient with 'a': "2a", "3a"
        match = re.search(r'(\d+\.?\d*)\s*a\b', text)
        if match:
            coef = float(match.group(1))
            print(f"   [_extract_number] '{text}' → {coef}a = {coef}")
            return coef
        
        # Try simple number: "3", "1.5", "2.5"
        match = re.search(r'\b(\d+\.?\d*)\b', text)
        if match:
            num = float(match.group(1))
            print(f"   [_extract_number] '{text}' → {num}")
            return num
        
        # If just 'a', return default
        if 'a' in text.lower():
            print(f"   [_extract_number] '{text}' → default (a) = {default}")
            return default
        
        print(f"   [_extract_number] '{text}' → default = {default}")
        return default
    
    def _extract_all_numbers(self, text: str) -> List[float]:
        """Trích xuất tất cả các số từ text"""
        numbers = []
        matches = re.findall(r'(\d+\.?\d*)', text)
        for match in matches:
            numbers.append(float(match))
        return numbers
    
    def _extract_actual_lengths(self, constraints: Dict) -> Dict[str, float]:
        """
        Trích xuất độ dài thực tế từ constraints
        
        Returns:
            Dict với key là tên cạnh/đoạn, value là độ dài thực tế
            Ví dụ: {"AB": 4.0, "SA": 6.0, "base_side": 4.0, "height": 6.0}
        """
        lengths = {}
        # Lưu cả biểu thức gốc để dùng làm label đẹp ("a√3" thay vì 1.732...)
        raw_labels = {}
        
        # Lấy độ dài cạnh đáy
        base = constraints.get("base", {})
        if "side" in base:
            side_value = base["side"]
            lengths["base_side"] = side_value
            lengths["AB"] = side_value
            lengths["BC"] = side_value
            lengths["CD"] = side_value
            lengths["DA"] = side_value
        
        # Lấy chiều cao
        apex = constraints.get("apex", {})
        if "height" in apex:
            height_value = apex["height"]
            lengths["height"] = height_value
            lengths["SA"] = height_value
            edge_name = apex.get("edge_name", "SA")
            lengths[edge_name] = height_value
        
        # Pattern parse "AB = a√3", "SA = 6", "BC = a√2"... 
        # Dùng findall để bắt TẤT CẢ matches trong 1 chuỗi (không chỉ match đầu)
        # Group 1: tên cạnh (2 chữ in hoa, có thể có dấu '), Group 2: biểu thức bên phải dấu =
        edge_pattern = r"([A-Z][A-Z'’]?)\s*=\s*([0-9a-zA-Z√√.]+(?:\s*[/√][0-9a-zA-Z]+)*)"
        
        def parse_text(text: str, source: str = ""):
            """Tìm tất cả 'XX = value' trong text và lưu vào lengths/raw_labels"""
            if not isinstance(text, str):
                return
            for m in re.finditer(edge_pattern, text):
                edge_name = m.group(1)
                value_str = m.group(2).strip()
                # Loại bỏ dấu câu thừa ở cuối (., ,, ;, :, !, ?)
                value_str = re.sub(r"[.,;:!?]+$", "", value_str).strip()
                # Loại bỏ dấu chấm thập phân thừa nếu nó nằm cuối số nguyên (VD: "2." → "2")
                if value_str.endswith("."):
                    value_str = value_str.rstrip(".")
                # Bỏ qua nếu value rỗng sau khi strip
                if not value_str:
                    continue
                value = self._extract_number(value_str, default=1.0)
                lengths[edge_name] = value
                raw_labels[edge_name] = re.sub(r"\s+", "", value_str)
                print(f"   [_extract_actual_lengths] [{source}] {edge_name} = '{value_str}' → {value}")
        
        # Parse từ given_conditions (có thể từng item gộp nhiều thông tin)
        for condition in constraints.get("given_conditions", []) or []:
            parse_text(condition, source="conditions")
        
        # Parse luôn problem_text để bắt thông tin bị Gemini bỏ sót khi tách conditions
        parse_text(constraints.get("problem_text", ""), source="problem_text")
        
        # Gắn raw_labels vào lengths qua key đặc biệt để _solve_pyramid đọc được
        lengths["__raw__"] = raw_labels
        return lengths
    
    def _extract_constraints(self, problem_text: str, shape_type: str) -> Dict:
        """Trích xuất ràng buộc từ đề bài (fallback method)"""
        constraints = {}
        text_lower = problem_text.lower()
        
        # Detect base type
        if "hình vuông" in text_lower or "vuông" in text_lower:
            side = self._extract_number(problem_text, default=1.0)
            constraints["base"] = {"type": "square", "side": side}
        elif "tam giác đều" in text_lower:
            side = self._extract_number(problem_text, default=1.0)
            constraints["base"] = {"type": "equilateral_triangle", "side": side}
        elif "tam giác" in text_lower:
            side = self._extract_number(problem_text, default=1.0)
            constraints["base"] = {"type": "triangle", "side": side}
        
        # Detect height/apex
        if "sa =" in text_lower or "chiều cao" in text_lower:
            height = self._extract_number(problem_text, default=1.414)
            constraints["apex"] = {"height": height, "perpendicular_to_base": True}
        
        # Detect special points
        if "trung điểm" in text_lower:
            constraints["special_points"] = True
        
        return constraints
    
    def _solve_pyramid(self, constraints: Dict) -> Dict[str, Any]:
        """Giải hình chóp với constraints động từ Gemini extraction"""
        base = constraints.get("base", {"type": "square", "side": 1.0})
        apex = constraints.get("apex", {"height": 1.414, "perpendicular_to_base": True})
        special_points = constraints.get("special_points", {})
        
        # Nếu base chưa xác định, suy ra từ danh sách điểm Gemini trả về
        if base is None or base.get("type") is None:
            points_list = constraints.get("points_list", [])
            # Loại bỏ đỉnh S (apex), đếm số điểm đáy
            base_points = [p for p in points_list if p != "S"]
            if len(base_points) == 3:
                base = {"type": "equilateral_triangle", "side": 1.0}
                print(f"   [Pyramid] Inferred triangle base from points: {base_points}")
            else:
                base = {"type": "square", "side": 1.0}
                print(f"   [Pyramid] Defaulting to square base")
        
        # Get dimensions
        a = base.get("side", 1.0)
        h = apex.get("height", 1.414)
        
        print(f"🔧 [Pyramid Solver] Building pyramid with:")
        print(f"   - Base: {base['type']}, side = {a}")
        print(f"   - Apex: height = {h}, perpendicular = {apex.get('perpendicular_to_base', True)}")
        print(f"   - Special points: {special_points}")
        
        # Tọa độ các điểm - ABCD là hình vuông trên mặt phẳng XZ (y=0)
        # S là đỉnh ở trên (y=h)
        points = {}
        
        if base.get("type") == "square":
            # Hình vuông ABCD
            points = {
                "A": [0, 0, 0],
                "B": [a, 0, 0],
                "C": [a, 0, a],
                "D": [0, 0, a],
                "S": [0, h, 0]  # S ở phía trên A (nếu SA ⊥ đáy)
            }
        elif base.get("type") == "equilateral_triangle":
            # Tam giác đều ABC
            h_triangle = a * math.sqrt(3) / 2
            points = {
                "A": [0, 0, 0],
                "B": [a, 0, 0],
                "C": [a/2, 0, h_triangle],
                "S": [a/2, h, h_triangle/3]  # S ở trên tâm tam giác
            }
        elif base.get("type") == "right_triangle":
            # Tam giác vuông tại B (mặc định) - hai cạnh AB, BC vuông góc tại B
            # Cố gắng đọc độ dài thực tế từ given_conditions (AB, BC)
            actual = self._extract_actual_lengths(constraints)
            ab_len = actual.get("AB", a)
            bc_len = actual.get("BC", a)
            
            # Nếu vẫn lấy default 1 cho BC, thử đọc từ raw_labels
            raw = actual.get("__raw__", {})
            print(f"   [Pyramid right_triangle] actual={actual}, raw={raw}")
            
            # Đặt B ở gốc để dễ thấy góc vuông tại B
            # B = (0,0,0); A nằm trên trục X (+AB); C nằm trên trục Z (+BC)
            points = {
                "B": [0, 0, 0],
                "A": [ab_len, 0, 0],
                "C": [0, 0, bc_len],
                "S": [ab_len, h, 0]  # S thẳng đứng phía trên A (vì SA ⊥ đáy)
            }
            print(f"   [Pyramid] Right triangle base at B: AB={ab_len}, BC={bc_len}, SA={h}")
        elif base.get("type") == "triangle":
            # Tam giác thường ABC (dùng tọa độ tam giác đều làm mặc định)
            h_triangle = a * math.sqrt(3) / 2
            points = {
                "A": [0, 0, 0],
                "B": [a, 0, 0],
                "C": [a/2, 0, h_triangle],
                "S": [a/2, h, h_triangle/3]
            }
        else:
            # Default: square
            points = {
                "A": [0, 0, 0],
                "B": [a, 0, 0],
                "C": [a, 0, a],
                "D": [0, 0, a],
                "S": [0, h, 0]
            }
        
        # Thêm các điểm đặc biệt
        if special_points:
            for point_name, point_info in special_points.items():
                point_type = point_info.get("type")
                
                # Trung điểm
                if point_type == "midpoint":
                    edge = point_info.get("of", "")
                    if len(edge) == 2 and edge[0] in points and edge[1] in points:
                        p1 = points[edge[0]]
                        p2 = points[edge[1]]
                        points[point_name] = [
                            (p1[0] + p2[0]) / 2,
                            (p1[1] + p2[1]) / 2,
                            (p1[2] + p2[2]) / 2
                        ]
                        print(f"   ✓ Added midpoint {point_name} of {edge}")
                
                # Tâm đáy
                elif point_type == "base_center":
                    # Tính tâm đáy dựa vào loại đáy
                    if base.get("type") == "square" and "D" in points:
                        # Tâm hình vuông ABCD
                        points[point_name] = [
                            (points["A"][0] + points["C"][0]) / 2,
                            0,  # y = 0 (trên mặt đáy)
                            (points["A"][2] + points["C"][2]) / 2
                        ]
                        print(f"   ✓ Added base center {point_name} (square)")
                    elif base.get("type") == "equilateral_triangle":
                        # Tâm tam giác đều ABC
                        points[point_name] = [
                            (points["A"][0] + points["B"][0] + points["C"][0]) / 3,
                            0,
                            (points["A"][2] + points["B"][2] + points["C"][2]) / 3
                        ]
                        print(f"   ✓ Added base center {point_name} (triangle)")
                    else:
                        # Default: trung điểm AC
                        if "A" in points and "C" in points:
                            points[point_name] = [
                                (points["A"][0] + points["C"][0]) / 2,
                                0,
                                (points["A"][2] + points["C"][2]) / 2
                            ]
                            print(f"   ✓ Added base center {point_name} (default)")
                
                # Tâm (center) - tương tự tâm đáy
                elif point_type == "center":
                    if "A" in points and "C" in points:
                        points[point_name] = [
                            (points["A"][0] + points["C"][0]) / 2,
                            0,
                            (points["A"][2] + points["C"][2]) / 2
                        ]
                        print(f"   ✓ Added center {point_name}")
        
        # Fallback: Thêm điểm M nếu có mention "trung điểm" nhưng không parse được
        if constraints.get("special_points") == True and "M" not in points:
            if "A" in points and "B" in points:
                points["M"] = [
                    (points["A"][0] + points["B"][0]) / 2,
                    (points["A"][1] + points["B"][1]) / 2,
                    (points["A"][2] + points["B"][2]) / 2
                ]
                print(f"   ✓ Added fallback midpoint M of AB")
        
        # Cạnh - PHÂN LOẠI ĐÚNG: Cạnh hình = nét liền, Đường phụ = nét đứt
        edges = []
        
        # Kiểm tra xem có điểm đặc biệt nằm trên cạnh không
        edge_with_midpoint = None
        if "M" in points:
            # Tìm cạnh chứa M
            for edge_name in ["AB", "BC", "CD", "DA", "AC", "BD"]:
                if len(edge_name) == 2 and edge_name[0] in points and edge_name[1] in points:
                    p1 = points[edge_name[0]]
                    p2 = points[edge_name[1]]
                    pm = points["M"]
                    # Check if M is on this edge
                    expected_m = [(p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2, (p1[2] + p2[2]) / 2]
                    if abs(pm[0] - expected_m[0]) < 0.01 and abs(pm[1] - expected_m[1]) < 0.01 and abs(pm[2] - expected_m[2]) < 0.01:
                        edge_with_midpoint = edge_name
                        print(f"   [Edges] M is midpoint of {edge_name}")
                        break
        
        # Base edges - TẤT CẢ NÉT LIỀN (cạnh của hình)
        # Dù có điểm M trên cạnh, cạnh vẫn là nét liền (vì là cạnh thật của hình)
        if "D" in points:
            # Square base - tất cả cạnh đều nét liền
            base_edges_list = [
                ("A", "B", "a"),  # (start, end, label)
                ("B", "C", None),
                ("C", "D", None),
                ("D", "A", None)
            ]
            
            for start, end, label in base_edges_list:
                # Cạnh bình thường → NÉT LIỀN (dù có điểm M trên cạnh)
                edge_data = {"start": start, "end": end, "style": "solid"}
                if label:
                    edge_data["label"] = label
                edges.append(edge_data)
            
            # Apex edges - TẤT CẢ NÉT LIỀN (cạnh bên của hình chóp)
            edges.extend([
                {"start": "S", "end": "A", "style": "solid", "color": "teal"},  # SA - đường cao (highlight)
                {"start": "S", "end": "B", "style": "solid"},                   # SB
                {"start": "S", "end": "C", "style": "solid"},                   # SC
                {"start": "S", "end": "D", "style": "solid"}                    # SD
            ])
        else:
            # Triangle base - tất cả nét liền
            base_edges_list = [
                ("A", "B", "a"),
                ("B", "C", None),
                ("C", "A", None)
            ]
            
            for start, end, label in base_edges_list:
                # Cạnh bình thường → NÉT LIỀN
                edge_data = {"start": start, "end": end, "style": "solid"}
                if label:
                    edge_data["label"] = label
                edges.append(edge_data)
            
            # Apex edges - tất cả nét liền
            edges.extend([
                {"start": "S", "end": "A", "style": "solid", "color": "teal"},
                {"start": "S", "end": "B", "style": "solid"},
                {"start": "S", "end": "C", "style": "solid"}
            ])
        
        # Đường phụ trợ - NÉT ĐỨT (không phải cạnh của hình)
        
        # Xử lý điểm O (tâm đáy)
        if "O" in points:
            # Vẽ đường chéo AC và BD (nét đứt) để thể hiện tâm
            if "D" in points:  # Hình vuông
                edges.extend([
                    {"start": "A", "end": "C", "style": "dashed", "color": "gray", "linewidth": 1},
                    {"start": "B", "end": "D", "style": "dashed", "color": "gray", "linewidth": 1}
                ])
                print(f"   [Edges] Added diagonals AC, BD (dashed) for center O")
        
        # Xử lý điểm M (trung điểm)
        if "M" in points:
            # SM - đường cần xét (NÉT ĐỨT màu vàng)
            edges.append({
                "start": "S", 
                "end": "M", 
                "style": "dashed",
                "color": "gold", 
                "label": "SM",
                "linewidth": 2
            })
            print(f"   [Edges] Added SM (dashed, gold)")
        
        # Mặt
        faces = []
        if "D" in points:
            # Square pyramid
            faces = [
                {"vertices": ["A", "B", "C", "D"], "opacity": 0.15, "color": "lightblue"},  # Đáy
                {"vertices": ["S", "A", "B"], "opacity": 0.08, "color": "lightgray"},
                {"vertices": ["S", "B", "C"], "opacity": 0.08, "color": "lightgray"},
                {"vertices": ["S", "C", "D"], "opacity": 0.05, "color": "lightgray"},  # Mặt sau (mờ hơn)
                {"vertices": ["S", "D", "A"], "opacity": 0.08, "color": "lightgray"}
            ]
        else:
            # Triangle pyramid
            faces = [
                {"vertices": ["A", "B", "C"], "opacity": 0.15, "color": "lightblue"},
                {"vertices": ["S", "A", "B"], "opacity": 0.08, "color": "lightgray"},
                {"vertices": ["S", "B", "C"], "opacity": 0.08, "color": "lightgray"},
                {"vertices": ["S", "C", "A"], "opacity": 0.08, "color": "lightgray"}
            ]
        
        # Steps
        steps = self._generate_pyramid_steps(points, edges, base.get("type", "square"))
        
        # Annotations - KÝ HIỆU TOÁN HỌC VÀ HÌNH HỌC
        annotations = {
            "edges": [],
            "points": [],
            "perpendicular": [],
            "angles": [],
            "distances": [],
            "equal_segments": []  # Các đoạn bằng nhau
        }
        
        # Parse độ dài thực tế từ constraints
        actual_lengths = self._extract_actual_lengths(constraints)
        raw_labels = actual_lengths.pop("__raw__", {})
        print(f"   [Annotations] Actual lengths: {actual_lengths}")
        print(f"   [Annotations] Raw labels: {raw_labels}")
        
        def fmt_label(edge_name: str, fallback: str = "a") -> str:
            """
            Lấy label đẹp cho cạnh: 
            - Ưu tiên tuyệt đối biểu thức gốc từ đề bài (VD: 'a√3', 'a√2', 'a')
            - KHÔNG BAO GIỜ trả về số thập phân kiểu '1.7' hoặc '1.414'
            """
            # Ưu tiên 1: Biểu thức gốc lấy thẳng từ given_conditions
            if edge_name in raw_labels and raw_labels[edge_name]:
                return raw_labels[edge_name]
            # Ưu tiên 2: Thử tên cạnh đảo ngược (BA thay vì AB)
            reversed_name = edge_name[::-1] if len(edge_name) == 2 else None
            if reversed_name and reversed_name in raw_labels and raw_labels[reversed_name]:
                return raw_labels[reversed_name]
            # Không có raw label → dùng fallback theo giá trị số
            val = actual_lengths.get(edge_name)
            if val is None:
                return fallback
            # Số nguyên đẹp (1, 2, 3...) → trả thẳng
            if abs(val - round(val)) < 0.01:
                return str(int(round(val)))
            # Gần với 1.0 (default 'a') → dùng fallback
            if abs(val - 1.0) < 0.01:
                return fallback
            # Còn lại không có biểu thức → dùng fallback (KHÔNG hiển thị số thập phân)
            return fallback
        
        # Ghi chú độ dài cạnh đáy
        if "D" in points:
            # Hình vuông - tất cả cạnh bằng nhau
            label_text = fmt_label("AB", fallback="a")
            
            # Ghi độ dài lên 1 cạnh (ví dụ AB)
            annotations["edges"].append({
                "edge": "A-B",
                "label": label_text,
                "position": "bottom",
                "color": "black"
            })
            
            # Ký hiệu các cạnh bằng nhau (dấu gạch)
            annotations["equal_segments"].append({
                "segments": ["A-B", "B-C", "C-D", "D-A"],
                "mark": "single",  # single, double, triple
                "description": "Các cạnh đáy bằng nhau"
            })
        else:
            # Tam giác - ghi label cho TỪNG cạnh (vì có thể độ dài khác nhau như AB=a, BC=a√2)
            for edge_pair in [("A", "B"), ("B", "C"), ("C", "A")]:
                edge_key = edge_pair[0] + edge_pair[1]
                edge_key_rev = edge_pair[1] + edge_pair[0]
                # Ưu tiên đọc theo đúng tên trong đề (AB, BC, CA)
                if edge_key in raw_labels:
                    label_text = raw_labels[edge_key]
                elif edge_key_rev in raw_labels:
                    label_text = raw_labels[edge_key_rev]
                elif edge_key in actual_lengths:
                    label_text = fmt_label(edge_key, fallback="a")
                elif edge_pair == ("A", "B"):
                    label_text = "a"  # Mặc định cạnh AB là "a"
                else:
                    continue  # Không có dữ liệu cho cạnh này → bỏ qua
                
                annotations["edges"].append({
                    "edge": f"{edge_pair[0]}-{edge_pair[1]}",
                    "label": label_text,
                    "position": "bottom",
                    "color": "black"
                })
        
        # Ghi chú chiều cao SA
        if apex.get("perpendicular_to_base", True):
            edge_name = apex.get("edge_name", "SA")
            sa_label = fmt_label(edge_name, fallback="h")
            
            # Ghi độ dài SA
            annotations["edges"].append({
                "edge": "S-A",
                "label": sa_label,
                "position": "left",
                "color": "teal"
            })
            
            # Ký hiệu vuông góc tại A
            annotations["perpendicular"].append({
                "vertex": "A",
                "line1": "S-A",
                "line2": "A-B",
                "symbol": "⊥",
                "description": "SA ⊥ (ABCD)"
            })
            
            # Nếu là hình vuông, thêm ký hiệu vuông góc tại các đỉnh khác
            if "D" in points:
                annotations["perpendicular"].append({
                    "vertex": "A",
                    "line1": "S-A",
                    "line2": "A-D",
                    "symbol": "⊥",
                    "description": "SA ⊥ AD"
                })
        
        # Ký hiệu góc vuông tại các đỉnh đáy (nếu là hình vuông)
        if "D" in points and base.get("type") == "square":
            for vertex in ["A", "B", "C", "D"]:
                if vertex == "A":
                    annotations["angles"].append({
                        "vertex": "A",
                        "line1": "A-B",
                        "line2": "A-D",
                        "angle": 90,
                        "symbol": "∟",
                        "description": "Góc vuông tại A"
                    })
                elif vertex == "B":
                    annotations["angles"].append({
                        "vertex": "B",
                        "line1": "B-A",
                        "line2": "B-C",
                        "angle": 90,
                        "symbol": "∟"
                    })
                elif vertex == "C":
                    annotations["angles"].append({
                        "vertex": "C",
                        "line1": "C-B",
                        "line2": "C-D",
                        "angle": 90,
                        "symbol": "∟"
                    })
                elif vertex == "D":
                    annotations["angles"].append({
                        "vertex": "D",
                        "line1": "D-C",
                        "line2": "D-A",
                        "angle": 90,
                        "symbol": "∟"
                    })
        
        # Ghi chú điểm đặc biệt
        
        # Điểm O (tâm đáy)
        if "O" in points:
            annotations["points"].append({
                "point": "O",
                "label": "O",
                "description": "Tâm đáy",
                "color": "purple"
            })
            
            # Ghi chú: O là giao điểm AC và BD
            annotations["distances"].append({
                "description": "O là giao điểm của AC và BD",
                "related_points": ["O", "A", "C", "B", "D"]
            })
        
        # Điểm M (trung điểm)
        if "M" in points:
            annotations["points"].append({
                "point": "M",
                "label": "M",
                "description": "Trung điểm",
                "color": "gold"
            })
            
            # Ghi chú đường SM
            sm_label = fmt_label("SM", fallback="SM")
            annotations["edges"].append({
                "edge": "S-M",
                "label": sm_label,
                "position": "right",
                "color": "gold"
            })
            
            # Ghi chú: M là trung điểm của cạnh nào
            if edge_with_midpoint:
                annotations["distances"].append({
                    "description": f"M là trung điểm của {edge_with_midpoint}",
                    "related_points": ["M", edge_with_midpoint[0], edge_with_midpoint[1]]
                })
                
                # Ký hiệu 2 đoạn bằng nhau (CM = MD)
                annotations["equal_segments"].append({
                    "segments": [f"{edge_with_midpoint[0]}-M", f"M-{edge_with_midpoint[1]}"],
                    "mark": "double",
                    "description": f"{edge_with_midpoint[0]}M = M{edge_with_midpoint[1]}"
                })
        
        # Ghi chú các đỉnh
        for point_name in ["A", "B", "C", "D", "S"]:
            if point_name in points:
                annotations["points"].append({
                    "point": point_name,
                    "label": point_name,
                    "color": "black" if point_name != "S" else "indigo"
                })
        
        # Camera
        max_coord = max(a, h)
        camera = {
            "position": [max_coord*2, h*1.5, max_coord*2],
            "lookAt": [a/2, h/2, a/2]
        }
        
        return {
            "points": points,
            "edges": edges,
            "faces": faces,
            "steps": steps,
            "annotations": annotations,
            "camera": camera
        }
    
    def _solve_prism(self, constraints: Dict) -> Dict[str, Any]:
        """
        Giải lăng trụ.
        - Mặc định: vẽ lăng trụ XIÊN (tránh trùng hình đặc biệt)
        - Chỉ vẽ ĐỨNG khi đề bài nói rõ "lăng trụ đứng"
        """
        base = constraints.get("base", {})
        a = base.get("side", 1.0)
        h = constraints.get("height", 1.0)
        
        # Kiểm tra xem có phải lăng trụ ĐỨNG không (đọc từ given_conditions hoặc problem_text)
        is_upright = False
        given_conditions = constraints.get("given_conditions", []) or []
        problem_text = constraints.get("problem_text", "") or ""
        
        # Check trong given_conditions
        for cond in given_conditions:
            if isinstance(cond, str) and "lăng trụ đứng" in cond.lower():
                is_upright = True
                break
        
        # Check trong problem_text (fallback)
        if not is_upright and isinstance(problem_text, str):
            if "lăng trụ đứng" in problem_text.lower():
                is_upright = True
        
        if is_upright:
            # Lăng trụ ĐỨNG: đáy trên thẳng phía trên đáy dưới
            offset_x, offset_z = 0, 0
            print(f"   [Prism] Drawing UPRIGHT prism (đề bài yêu cầu lăng trụ đứng)")
        else:
            # Lăng trụ XIÊN (mặc định)
            offset_x = a * 0.35  # Dịch sang phải 35% cạnh
            offset_z = a * 0.20  # Dịch ra trước 20% cạnh
            print(f"   [Prism] Drawing OBLIQUE prism (mặc định, offset x={offset_x}, z={offset_z})")
        
        points = {
            # Đáy dưới ABC (tam giác đều, y = 0)
            "A": [0, 0, 0],
            "B": [a, 0, 0],
            "C": [a/2, 0, a * math.sqrt(3)/2],
            # Đáy trên A'B'C' (y = h, có offset nếu xiên)
            "A'": [0 + offset_x, h, 0 + offset_z],
            "B'": [a + offset_x, h, 0 + offset_z],
            "C'": [a/2 + offset_x, h, a * math.sqrt(3)/2 + offset_z]
        }
        
        edges = [
            {"start": "A", "end": "B", "style": "solid"},
            {"start": "B", "end": "C", "style": "solid"},
            {"start": "C", "end": "A", "style": "solid"},
            {"start": "A'", "end": "B'", "style": "solid"},
            {"start": "B'", "end": "C'", "style": "solid"},
            {"start": "C'", "end": "A'", "style": "solid"},
            {"start": "A", "end": "A'", "style": "solid"},
            {"start": "B", "end": "B'", "style": "solid"},
            {"start": "C", "end": "C'", "style": "solid"}
        ]
        
        faces = [
            {"vertices": ["A", "B", "C"]},
            {"vertices": ["A'", "B'", "C'"]},
            {"vertices": ["A", "B", "B'", "A'"]},
            {"vertices": ["B", "C", "C'", "B'"]},
            {"vertices": ["C", "A", "A'", "C'"]}
        ]
        
        steps = self._generate_prism_steps(points, edges)
        
        return {
            "points": points,
            "edges": edges,
            "faces": faces,
            "steps": steps,
            "annotations": {},
            "camera": {"position": [a*2, h*1.5, a*2], "lookAt": [a/2, h/2, 0]}
        }
    
    def _solve_cube(self, constraints: Dict) -> Dict[str, Any]:
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
            {"start": "A", "end": "B", "style": "solid"},
            {"start": "B", "end": "C", "style": "solid"},
            {"start": "C", "end": "D", "style": "solid"},
            {"start": "D", "end": "A", "style": "solid"},
            {"start": "A'", "end": "B'", "style": "solid"},
            {"start": "B'", "end": "C'", "style": "solid"},
            {"start": "C'", "end": "D'", "style": "solid"},
            {"start": "D'", "end": "A'", "style": "solid"},
            {"start": "A", "end": "A'", "style": "solid"},
            {"start": "B", "end": "B'", "style": "solid"},
            {"start": "C", "end": "C'", "style": "solid"},
            {"start": "D", "end": "D'", "style": "solid"}
        ]
        
        faces = [
            {"vertices": ["A", "B", "C", "D"]},
            {"vertices": ["A'", "B'", "C'", "D'"]},
            {"vertices": ["A", "B", "B'", "A'"]},
            {"vertices": ["B", "C", "C'", "B'"]},
            {"vertices": ["C", "D", "D'", "C'"]},
            {"vertices": ["D", "A", "A'", "D'"]}
        ]
        
        steps = self._generate_cube_steps(points, edges)
        
        return {
            "points": points,
            "edges": edges,
            "faces": faces,
            "steps": steps,
            "annotations": {},
            "camera": {"position": [a*2, a*2, a*2], "lookAt": [a/2, a/2, a/2]}
        }
    
    def _solve_tetrahedron(self, constraints: Dict) -> Dict[str, Any]:
        """Giải tứ diện"""
        a = 1.0
        h_A = a * math.sqrt(1.25)
        h_D = a * math.sqrt(1.25)
        
        points = {
            "B": [-a, 0, 0],
            "C": [a, 0, 0],
            "I": [0, 0, 0],
            "A": [0, h_A, 0],
            "D": [0, 0, h_D],
            "H": [0, 0, 0]
        }
        
        edges = [
            {"start": "A", "end": "B", "style": "solid"},
            {"start": "A", "end": "C", "style": "solid"},
            {"start": "B", "end": "C", "style": "solid"},
            {"start": "D", "end": "B", "style": "solid"},
            {"start": "D", "end": "C", "style": "solid"},
            {"start": "A", "end": "D", "style": "solid"},
            {"start": "A", "end": "I", "style": "dashed"},
            {"start": "D", "end": "I", "style": "dashed"},
            {"start": "A", "end": "H", "style": "dashed"}
        ]
        
        faces = [
            {"vertices": ["A", "B", "C"]},
            {"vertices": ["D", "B", "C"]},
            {"vertices": ["A", "B", "D"]},
            {"vertices": ["A", "C", "D"]}
        ]
        
        steps = self._generate_tetrahedron_steps(points, edges)
        
        return {
            "points": points,
            "edges": edges,
            "faces": faces,
            "steps": steps,
            "annotations": {},
            "camera": {"position": [a*3, h_A*1.5, h_D*1.5], "lookAt": [0, h_A/2, h_D/2]}
        }
    
    def _generate_pyramid_steps(self, points: Dict, edges: List, base_type: str = "square") -> List[Dict]:
        """Tạo steps cho hình chóp"""
        steps = []
        
        # Determine base points
        if base_type == "square" and "D" in points:
            base_points = ["A", "B", "C", "D"]
            base_edges = ["A-B", "B-C", "C-D", "D-A"]
            base_desc = "Vẽ đáy ABCD (hình vuông)"
        elif "C" in points and "D" not in points:
            base_points = ["A", "B", "C"]
            base_edges = ["A-B", "B-C", "C-A"]
            base_desc = "Vẽ đáy ABC (tam giác)"
        else:
            base_points = ["A", "B", "C", "D"]
            base_edges = ["A-B", "B-C", "C-D", "D-A"]
            base_desc = "Vẽ đáy"
        
        has_m = "M" in points
        has_o = "O" in points
        
        steps.append({
            "order": 1,
            "description": base_desc,
            "objects": base_points + base_edges,
            "highlight": base_points
        })
        
        # Thêm bước vẽ tâm đáy O nếu có
        current_order = 2
        if has_o:
            steps.append({
                "order": current_order,
                "description": "Xác định O - tâm đáy",
                "objects": ["O"],
                "highlight": ["O"]
            })
            current_order += 1
        
        steps.append({
            "order": current_order,
            "description": "Dựng SA ⊥ đáy",
            "objects": ["S", "S-A"],
            "highlight": ["S", "S-A"]
        })
        current_order += 1
        
        # Apex edges
        apex_edges = [f"S-{p}" for p in base_points if p != "A"]
        steps.append({
            "order": current_order,
            "description": "Nối các cạnh bên",
            "objects": apex_edges,
            "highlight": apex_edges
        })
        current_order += 1
        
        if has_m:
            steps.append({
                "order": current_order,
                "description": "Xác định M - trung điểm",
                "objects": ["M"],
                "highlight": ["M"]
            })
            current_order += 1
            steps.append({
                "order": current_order,
                "description": "Nối SM",
                "objects": ["S-M"],
                "highlight": ["S-M"]
            })
        
        return steps
    
    def _generate_prism_steps(self, points: Dict, edges: List) -> List[Dict]:
        """Tạo steps cho lăng trụ"""
        return [
            {
                "order": 1,
                "description": "Vẽ đáy ABC",
                "objects": ["A", "B", "C", "A-B", "B-C", "C-A"],
                "highlight": ["A", "B", "C"]
            },
            {
                "order": 2,
                "description": "Vẽ đỉnh A'B'C'",
                "objects": ["A'", "B'", "C'", "A'-B'", "B'-C'", "C'-A'"],
                "highlight": ["A'", "B'", "C'"]
            },
            {
                "order": 3,
                "description": "Nối các cạnh bên",
                "objects": ["A-A'", "B-B'", "C-C'"],
                "highlight": ["A-A'", "B-B'", "C-C'"]
            }
        ]
    
    def _generate_cube_steps(self, points: Dict, edges: List) -> List[Dict]:
        """Tạo steps cho hình lập phương"""
        return self._generate_prism_steps(points, edges)
    
    def _generate_tetrahedron_steps(self, points: Dict, edges: List) -> List[Dict]:
        """Tạo steps cho tứ diện"""
        return [
            {
                "order": 1,
                "description": "Vẽ tam giác ABC",
                "objects": ["A", "B", "C", "A-B", "B-C", "A-C"],
                "highlight": ["A", "B", "C"]
            },
            {
                "order": 2,
                "description": "Xác định điểm I",
                "objects": ["I"],
                "highlight": ["I"]
            },
            {
                "order": 3,
                "description": "Vẽ điểm D",
                "objects": ["D", "D-B", "D-C"],
                "highlight": ["D"]
            },
            {
                "order": 4,
                "description": "Hoàn thiện tứ diện",
                "objects": ["A-D", "A-I", "D-I"],
                "highlight": ["A-D"]
            }
        ]
