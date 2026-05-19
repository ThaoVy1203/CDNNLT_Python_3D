"""
Gemini AI Service - Xử lý phân tích ảnh và giải toán hình học
Tích hợp: AI extraction, Geometry solver, 3D renderer
"""
from typing import Optional, Union
from app.services.ai.gemini_client import GeminiClient
from app.services.renderer.transform import GeometryRenderer
from app.core.config import settings

class GeminiService:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.GEMINI_API_KEY
        self.gemini_client = GeminiClient(api_key=self.api_key)
        self.renderer = GeometryRenderer()
    
    async def analyze_image(self, image: Union[str, bytes]) -> dict:
        """Phân tích ảnh bài toán hình học"""
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
        """Giải bài toán hình học bằng Gemini AI (không dùng PDF)"""
        try:
            from app.services.ai.prompt import build_solve_prompt
            import json
            import re
            import asyncio

            prompt = build_solve_prompt(problem_text)

            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.gemini_client._generate_with_retry(
                    model=self.gemini_client.model_name,
                    contents=prompt,
                    config=self.gemini_client.generation_config
                )
            )
            
            response_text = response.text
            if "```json" in response_text:
                json_str = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                json_str = response_text.split("```")[1].split("```")[0].strip()
            else:
                json_str = response_text.strip()
            
            json_str = re.sub(r'(?<!\\)\\(?!["\\/bfnrtu])', r'\\\\', json_str)
            
            try:
                solution = json.loads(json_str)
                if "steps" in solution and len(solution["steps"]) > 10:
                    solution["steps"] = solution["steps"][:5]
            except json.JSONDecodeError as e:
                print(f"❌ JSON parse error: {e}")
                print(f"Problematic JSON (first 1000 chars): {json_str[:1000]}")
                solution = {
                    "steps": ["Không thể phân tích lời giải. Vui lòng thử lại."],
                    "result": "Lỗi phân tích",
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
        """Tạo tọa độ 3D cho visualization"""
        try:
            result_3d = self.renderer.transform_to_3d(geometry_data)
            return {
                "points": result_3d.get("points", {}),
                "edges": result_3d.get("edges", []),
                "faces": result_3d.get("faces", []),
                "camera_position": result_3d.get("camera_position", [5, 5, 5])
            }
        except Exception as e:
            raise Exception(f"3D generation failed: {str(e)}")

    async def generate_render_commands(self, problem_text: str) -> dict:
        """Sinh mảng lệnh vẽ Three.js cho 1 bài toán hình học."""
        from app.services.ai.prompt import build_render_3d_prompt
        import asyncio
        import json
        import re

        prompt = build_render_3d_prompt(problem_text)

        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: self.gemini_client._generate_with_retry(
                model=self.gemini_client.model_name,
                contents=prompt,
                config=self.gemini_client.generation_config,
            ),
        )

        text = (response.text or "").strip()
        cleaned = text
        if "```" in cleaned:
            m = re.search(r"```(?:json)?\s*([\s\S]+?)\s*```", cleaned)
            if m:
                cleaned = m.group(1).strip()

        try:
            commands = json.loads(cleaned)
        except json.JSONDecodeError as e:
            m = re.search(r"\[[\s\S]+\]", cleaned)
            if not m:
                raise Exception(f"Gemini không trả về JSON hợp lệ: {e}")
            commands = json.loads(m.group(0))

        if isinstance(commands, dict):
            commands = commands.get("commands") or commands.get("steps") or []

        if not isinstance(commands, list):
            raise Exception("Output Gemini không phải mảng lệnh vẽ")

        ALLOWED_FN = {
            "drawPoint", "drawEdge", "drawFace", "drawLabel",
            "drawRightAngle", "drawEqualMark", "drawAngle",
            "setCamera",
        }
        valid_commands = []
        for cmd in commands:
            if not isinstance(cmd, dict):
                continue
            fn = cmd.get("fn")
            args = cmd.get("args") or {}
            if fn not in ALLOWED_FN:
                continue
            valid_commands.append({"fn": fn, "args": args})

        return {
            "commands": valid_commands,
            "raw_response": text,
        }

    async def generate_drawing_guide(self, problem_text: str, shape_type: str) -> str:
        """Tạo hướng dẫn dựng hình cho học sinh"""
        try:
            from app.services.ai.prompt import build_drawing_guide_prompt
            import asyncio

            prompt = build_drawing_guide_prompt(problem_text, shape_type)
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.gemini_client._generate_with_retry(
                    model=self.gemini_client.model_name,
                    contents=prompt,
                    config=self.gemini_client.generation_config
                )
            )
            return response.text.strip()
        except Exception as e:
            return f"HƯỚNG DẪN DỰNG HÌNH\n\nBước 1: Vẽ các điểm cơ bản\nBước 2: Nối các cạnh\nBước 3: Hoàn thiện"

    async def solve_problem_with_context(self, problem_text: str) -> dict:
        """
        Giải bài toán — GỘP 1 LẦN GỌI DUY NHẤT.
        Gửi: đề bài + 2 file PDF + prompt từ prompt.py → Gemini trả về lời giải hoàn chỉnh.
        """
        try:
            import google.generativeai as genai
            import json
            import re
            import asyncio
            from app.services.file_search_service import file_search_service
            from app.services.ai.prompt import build_solve_with_context_prompt

            # Lấy file refs từ PDF đã upload
            file_refs = []
            if file_search_service.uploaded_files:
                for file_id in file_search_service.uploaded_files.values():
                    try:
                        file_refs.append(genai.get_file(file_id))
                    except Exception as e:
                        print(f"⚠️ Could not get file {file_id}: {e}")

            print(f"\n🧮 Solving with {len(file_refs)} PDF files in ONE call...")

            # Lấy prompt từ prompt.py
            solve_prompt = build_solve_with_context_prompt(problem_text)

            # Gọi Gemini 1 lần duy nhất: prompt + PDF files
            model = genai.GenerativeModel(model_name=self.gemini_client.model_name)
            contents = [solve_prompt] + file_refs

            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: model.generate_content(
                    contents=contents,
                    generation_config=genai.GenerationConfig(
                        temperature=0.3,
                        top_p=0.9,
                        max_output_tokens=4096,
                    )
                )
            )

            response_text = response.text.strip()
            print(f"✅ Got response ({len(response_text)} chars)")

            # Parse JSON
            if "```json" in response_text:
                json_str = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                json_str = response_text.split("```")[1].split("```")[0].strip()
            else:
                json_str = response_text

            json_str = re.sub(r'(?<!\\)\\(?!["\\/bfnrtu])', r'\\\\', json_str)

            try:
                solution = json.loads(json_str)
                if "steps" in solution and len(solution["steps"]) > 10:
                    solution["steps"] = solution["steps"][:5]
            except json.JSONDecodeError as e:
                print(f"❌ JSON parse error: {e}")
                print(f"Response (first 500): {json_str[:500]}")
                print("⚠️ Falling back to solve_problem() without PDF")
                solution = await self.solve_problem(problem_text)

            # Thêm references (tên file PDF đã dùng)
            solution["references"] = [
                {"file": fname, "excerpt": "", "formulas": [], "theorems": []}
                for fname in file_search_service.uploaded_files.keys()
            ]

            print(f"✅ Solution ready: {solution.get('result', 'N/A')}")
            return solution

        except Exception as e:
            print(f"❌ Error in solve_with_context: {e}")
            return await self.solve_problem(problem_text)
