"""
Gemini AI Service - Xử lý phân tích ảnh và giải toán hình học
Tích hợp: AI extraction, Geometry solver, 3D renderer
"""
from typing import Optional, Union
from PIL import Image
from app.services.ai.gemini_client import GeminiClient, solve_with_ai
from app.services.renderer.transform import GeometryRenderer
from app.core.config import settings

class GeminiService:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.GEMINI_API_KEY
        self.gemini_client = GeminiClient(api_key=self.api_key)
        self.renderer = GeometryRenderer()
    
    async def analyze_image(self, image: Union[str, bytes]) -> dict:
        """
        Phân tích ảnh bài toán hình học
        Trả về: dữ liệu hình học đã trích xuất
        """
        try:
            extraction = await self.gemini_client.extract_geometry_from_image(image)
            return {
                "problem_text": extraction.problem_text,
                "problem_type": extraction.problem_type,
                "shape_type": extraction.problem_type,
                "points": [{"name": p.name, "coordinates": p.coordinates} for p in extraction.points],
                "relationships": [{"type": r.relation_type, "entities": r.entities} for r in extraction.relations],
                "confidence_score": extraction.confidence_score,
                "given_conditions": extraction.given_conditions,
                "questions": extraction.questions
            }
        except Exception as e:
            raise Exception(f"Image analysis failed: {str(e)}")
    
    async def solve_problem(self, problem_text: str) -> dict:
        """
        Giải bài toán hình học bằng Gemini AI
        Trả về: các bước giải và kết quả từ AI
        """
        try:
            from app.services.ai.prompt import build_solve_prompt
            
            # Gọi Gemini AI để giải toán
            prompt = build_solve_prompt(problem_text)
            
            response = self.gemini_client.client.models.generate_content(
                model=self.gemini_client.model_name,
                contents=prompt,
                config=self.gemini_client.generation_config
            )
            
            # Parse response
            response_text = response.text
            if "```json" in response_text:
                json_str = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                json_str = response_text.split("```")[1].split("```")[0].strip()
            else:
                json_str = response_text.strip()
            
            # KHÔNG xử lý escape characters - để JSON parser tự xử lý
            # Đây là fix cho lỗi LaTeX escape sequences
            
            import json
            solution = json.loads(json_str)
            
            return {
                "steps": solution.get("steps", []),
                "result": solution.get("result", ""),
                "formulas_used": solution.get("formulas_used", [])
            }
        except Exception as e:
            raise Exception(f"Problem solving failed: {str(e)}")
    
    async def generate_3d_coordinates(self, geometry_data: dict) -> dict:
        """
        Tạo tọa độ 3D cho visualization
        Trả về: dữ liệu 3D JSON cho frontend
        """
        try:
            # Transform to 3D coordinates
            result_3d = self.renderer.transform_to_3d(geometry_data)
            
            return {
                "points": result_3d.get("points", {}),
                "edges": result_3d.get("edges", []),
                "faces": result_3d.get("faces", []),
                "camera_position": result_3d.get("camera_position", [5, 5, 5])
            }
        except Exception as e:
            raise Exception(f"3D generation failed: {str(e)}")
    
    async def generate_drawing_guide(self, problem_text: str, shape_type: str) -> str:
        """
        Tạo hướng dẫn dựng hình cho học sinh bằng Gemini AI
        Trả về: hướng dẫn từng bước theo thứ tự logic
        """
        try:
            from app.services.ai.prompt import build_drawing_guide_prompt
            
            prompt = build_drawing_guide_prompt(problem_text, shape_type)
            
            response = self.gemini_client.client.models.generate_content(
                model=self.gemini_client.model_name,
                contents=prompt,
                config=self.gemini_client.generation_config
            )
            
            return response.text.strip()
        except Exception as e:
            # Fallback nếu AI lỗi
            return f"HƯỚNG DẪN DỰNG HÌNH {shape_type.upper()}\n\nBước 1: Vẽ các điểm cơ bản\nBước 2: Nối các cạnh theo đề bài\nBước 3: Hoàn thiện hình vẽ"
