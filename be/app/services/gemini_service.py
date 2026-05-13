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
            import json
            import re
            import asyncio

            prompt = build_solve_prompt(problem_text)

            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.gemini_client.client.models.generate_content(
                    model=self.gemini_client.model_name,
                    contents=prompt,
                    config=self.gemini_client.generation_config
                )
            )
            
            # Parse response
            response_text = response.text
            if "```json" in response_text:
                json_str = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                json_str = response_text.split("```")[1].split("```")[0].strip()
            else:
                json_str = response_text.strip()
            
            # Fix: Replace single backslashes with double backslashes for LaTeX
            # But be careful not to break already escaped sequences
            # This regex finds backslashes that are not already escaped
            json_str = re.sub(r'(?<!\\)\\(?!["\\/bfnrtu])', r'\\\\', json_str)
            
            try:
                solution = json.loads(json_str)
                
                # Validate: Ensure steps is not too long
                if "steps" in solution and len(solution["steps"]) > 10:
                    print(f"⚠️  Too many steps ({len(solution['steps'])}), truncating to first 5")
                    solution["steps"] = solution["steps"][:5]
                    
            except json.JSONDecodeError as e:
                print(f"❌ JSON parse error: {e}")
                print(f"Problematic JSON (first 1000 chars): {json_str[:1000]}")
                print(f"Problematic JSON (last 500 chars): {json_str[-500:]}")
                
                # Try to extract steps manually from text
                lines = response_text.split('\n')
                steps = []
                for line in lines:
                    line = line.strip()
                    if line and (line.startswith('-') or line.startswith('Bước') or line.startswith('•')):
                        steps.append(line.lstrip('-•').strip())
                        if len(steps) >= 5:
                            break
                
                if not steps:
                    steps = ["Không thể phân tích lời giải. Vui lòng thử lại."]
                
                solution = {
                    "steps": steps,
                    "result": "Xem chi tiết trong các bước giải",
                    "formulas_used": []
                }
            
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
            import asyncio

            prompt = build_drawing_guide_prompt(problem_text, shape_type)

            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.gemini_client.client.models.generate_content(
                    model=self.gemini_client.model_name,
                    contents=prompt,
                    config=self.gemini_client.generation_config
                )
            )

            return response.text.strip()
        except Exception as e:
            # Fallback nếu AI lỗi
            return f"HƯỚNG DẪN DỰNG HÌNH {shape_type.upper()}\n\nBước 1: Vẽ các điểm cơ bản\nBước 2: Nối các cạnh theo đề bài\nBước 3: Hoàn thiện hình vẽ"

    async def solve_problem_with_context(self, problem_text: str) -> dict:
        """
        Giải bài toán với context từ tài liệu (File Search)
        
        CHIẾN LƯỢC MỚI:
        1. Gọi solve_problem() để có kết quả chính xác
        2. Dùng File Search + kết quả đó để viết lại lời giải chuẩn SGK
        
        Args:
            problem_text: Đề bài toán
            
        Returns:
            {
                "steps": [...],
                "result": "...",
                "formulas_used": [...],
                "references": [...]
            }
        """
        try:
            from app.services.file_search_service import file_search_service
            from app.services.ai.prompt import build_solve_prompt
            import json
            import asyncio
            
            # BƯỚC 1: Giải bài toán để có kết quả chính xác
            print(f"\n🧮 Step 1: Solving problem for accurate result...")
            initial_solution = await self.solve_problem(problem_text)
            initial_result = initial_solution.get("result", "")
            initial_steps = initial_solution.get("steps", [])
            
            print(f"✅ Initial result: {initial_result}")
            
            # BƯỚC 2: Search tài liệu liên quan
            print(f"\n📚 Step 2: Searching documents for context...")
            search_results = await file_search_service.search(problem_text)
            
            # BƯỚC 3: Viết lại lời giải chuẩn SGK
            if search_results:
                print(f"✅ Found {len(search_results)} relevant documents")
                
                # Extract context from search results
                context_parts = []
                for result in search_results:
                    context_parts.append(f"""
📄 TÀI LIỆU: {result['file']}

CÔNG THỨC:
{chr(10).join('- ' + f for f in result.get('formulas', []))}

ĐỊNH LÝ:
{chr(10).join('- ' + t for t in result.get('theorems', []))}

PHƯƠNG PHÁP:
{chr(10).join('- ' + m for m in result.get('methods', []))}
""")
                
                context = "\n\n".join(context_parts)
                
                # Enhanced prompt: Refine solution with context
                refine_prompt = f"""
Bạn là giáo viên toán chuyên về hình học không gian.

ĐỀ BÀI:
{problem_text}

KẾT QUẢ ĐÚNG (đã tính toán):
{initial_result}

CÁC BƯỚC ĐÃ GIẢI (tham khảo):
{chr(10).join(f"{i+1}. {step}" for i, step in enumerate(initial_steps))}

THÔNG TIN TỪ TÀI LIỆU THAM KHẢO:
{context}

YÊU CẦU:
Hãy viết lại lời giải theo PHONG CÁCH SÁCH GIÁO KHOA:
- Sử dụng phương pháp và công thức từ tài liệu tham khảo
- Giữ nguyên KẾT QUẢ ĐÚNG: {initial_result}
- Tối đa 5 bước, mỗi bước 1 câu ngắn gọn
- Mỗi bước phải logic, dễ hiểu như trong SGK
- KHÔNG dùng LaTeX, dùng Unicode: √, ², ³, ⊥, ∥, ⇒

VÍ DỤ FORMAT:
{{
  "steps": [
    "Gọi G là trọng tâm △ABC, M là trung điểm BC",
    "Ta có A'G ⊥ (ABC) ⇒ A'G ⊥ BC; BC ⊥ AM ⇒ BC ⊥ (MAA')",
    "Kẻ MI ⊥ AA', BC ⊥ IM ⇒ d(AA', BC) = IM = a√3/4",
    "Kẻ GH ⊥ AA', áp dụng định lý Thales: GH = (2/3) × IM = a√3/6",
    "Vậy V = A'G × S_ABC = (a/3) × (a²√3/4) = a³√3/12"
  ],
  "result": "{initial_result}",
  "formulas_used": ["Định lý 3 đường vuông góc", "Khoảng cách hai đường thẳng chéo nhau", "Thể tích khối lăng trụ"]
}}

Trả về JSON:
"""
                
                print(f"\n✍️  Step 3: Refining solution with textbook style...")
                
            else:
                print(f"⚠️  No relevant documents found, using initial solution")
                return initial_solution
            
            # Call Gemini to refine
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.gemini_client.client.models.generate_content(
                    model=self.gemini_client.model_name,
                    contents=refine_prompt,
                    config=self.gemini_client.generation_config
                )
            )
            
            response_text = response.text.strip()
            
            # Extract JSON from response
            if "```json" in response_text:
                json_str = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                json_str = response_text.split("```")[1].split("```")[0].strip()
            else:
                json_str = response_text
            
            # Clean up JSON string
            import re
            json_str = re.sub(r'(?<!\\)\\(?!["\\/bfnrtu])', r'\\\\', json_str)
            
            try:
                refined_solution = json.loads(json_str)
                
                # Validate: Ensure steps is not too long
                if "steps" in refined_solution and len(refined_solution["steps"]) > 10:
                    print(f"⚠️  Too many steps ({len(refined_solution['steps'])}), truncating to first 5")
                    refined_solution["steps"] = refined_solution["steps"][:5]
                
                # Ensure result matches initial result
                if "result" not in refined_solution or not refined_solution["result"]:
                    refined_solution["result"] = initial_result
                    
            except json.JSONDecodeError as e:
                print(f"❌ JSON parse error in refine: {e}")
                print(f"Falling back to initial solution")
                refined_solution = initial_solution
            
            # Add references to solution
            refined_solution["references"] = [
                {
                    "file": r["file"],
                    "excerpt": r["excerpt"],
                    "formulas": r.get("formulas", []),
                    "theorems": r.get("theorems", [])
                }
                for r in search_results
            ]
            
            print(f"✅ Refined solution ready!")
            return refined_solution
            
        except Exception as e:
            print(f"❌ Error in solve_with_context: {e}")
            # Fallback to normal solve
            return await self.solve_problem(problem_text)
