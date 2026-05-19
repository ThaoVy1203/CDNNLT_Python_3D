"""
Gemini Client - Tích hợp Google Gemini API cho phân tích hình học
"""
import os
import json
import base64
from typing import Optional, Union, List, Dict, Any
from io import BytesIO
from PIL import Image

try:
    from google import genai
    from google.genai import types
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False
    print("Warning: google-genai not installed. Install with: pip install google-genai")

from .prompt import build_extraction_prompt, VALIDATION_PROMPT, COORDINATE_ESTIMATION_PROMPT


class Point:
    """Điểm trong không gian 3D"""
    def __init__(self, name: str, coordinates: Optional[List[float]] = None):
        self.name = name
        self.coordinates = coordinates or []


class Line:
    """Đường thẳng nối 2 điểm"""
    def __init__(self, point1: str, point2: str):
        self.point1 = point1
        self.point2 = point2


class Relation:
    """Quan hệ hình học"""
    def __init__(self, relation_type: str, entities: List[str]):
        self.relation_type = relation_type
        self.entities = entities


class GeometryExtraction:
    """Kết quả trích xuất dữ liệu hình học"""
    def __init__(self, **kwargs):
        self.problem_text = kwargs.get('problem_text', '')
        self.problem_type = kwargs.get('problem_type', '')
        self.confidence_score = kwargs.get('confidence_score', 0.0)
        self.given_conditions = kwargs.get('given_conditions', [])
        self.questions = kwargs.get('questions', [])
        self.extraction_notes = kwargs.get('extraction_notes', '')
        
        # Parse points
        points_data = kwargs.get('points', [])
        self.points = [
            Point(p['name'], p.get('coordinates')) 
            if isinstance(p, dict) else p 
            for p in points_data
        ]
        
        # Parse lines
        lines_data = kwargs.get('lines', [])
        self.lines = [
            Line(l['point1'], l['point2']) 
            if isinstance(l, dict) else l 
            for l in lines_data
        ]
        
        # Parse relations
        relations_data = kwargs.get('relations', [])
        self.relations = [
            Relation(r['type'], r['entities']) 
            if isinstance(r, dict) else r 
            for r in relations_data
        ]


class GeminiClient:
    """Client để tương tác với Gemini API"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Khởi tạo Gemini client"""
        if not GENAI_AVAILABLE:
            raise ImportError("google-genai package is required. Install: pip install google-genai")
        
        # Load tất cả API keys từ environment
        self.api_keys = self._load_api_keys(api_key)
        self.current_key_index = 0
        
        # Khởi tạo client với key đầu tiên
        self.api_key = self.api_keys[0]
        self.client = genai.Client(api_key=self.api_key)
        
        # Đọc model từ environment variable
        self.model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        print(f"🤖 Using Gemini model: {self.model_name}")
        print(f"🔑 Loaded {len(self.api_keys)} API key(s)")
        
        self.generation_config = types.GenerateContentConfig(
            temperature=1.0,
            top_p=0.95,
            top_k=40,
            max_output_tokens=8192,
        )
    
    def _load_api_keys(self, primary_key: Optional[str] = None) -> list:
        """Load tất cả API keys từ environment"""
        keys = []
        
        # Load các key đánh số: GEMINI_API_KEY_1, GEMINI_API_KEY_2, ...
        i = 1
        while True:
            key = os.getenv(f"GEMINI_API_KEY_{i}")
            if not key:
                break
            keys.append(key)
            i += 1
        
        # Nếu không có key đánh số, dùng key chính
        if not keys:
            fallback = primary_key or os.getenv("GEMINI_API_KEY")
            if fallback:
                keys.append(fallback)
        
        if not keys:
            raise ValueError("Không tìm thấy GEMINI_API_KEY nào trong .env")
        
        return keys
    
    def _rotate_key(self):
        """Chuyển sang key tiếp theo"""
        self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)
        self.api_key = self.api_keys[self.current_key_index]
        self.client = genai.Client(api_key=self.api_key)
        print(f"🔄 Switched to API key #{self.current_key_index + 1}")
    
    def _generate_with_retry(self, model: str, contents, config):
        """Gọi API với tự động xoay vòng key khi bị limit và retry khi gặp lỗi 503/429"""
        import time
        max_retries_per_key = 3
        last_error = None
        
        # Thử qua tất cả các key
        for _ in range(len(self.api_keys)):
            # Thử nhiều lần trên mỗi key
            for attempt in range(max_retries_per_key):
                try:
                    response = self.client.models.generate_content(
                        model=model,
                        contents=contents,
                        config=config
                    )
                    return response
                except Exception as e:
                    error_msg = str(e)
                    last_error = e
                    
                    is_quota_error = any(code in error_msg for code in [
                        "429", "503", "RESOURCE_EXHAUSTED", "UNAVAILABLE", "quota"
                    ])
                    
                    if is_quota_error:
                        wait_time = 2 ** attempt  # Backoff: 1s, 2s, 4s
                        print(f"⚠️ API báo lỗi quá tải (503/429). Chờ {wait_time}s rồi thử lại lần {attempt+1}/{max_retries_per_key} với key hiện tại...")
                        time.sleep(wait_time)
                    else:
                        # Lỗi khác (không phải do quá tải) thì throw luôn
                        raise e
            
            # Nếu đã hết số lần thử cho key này mà vẫn lỗi, chuyển sang key khác
            print(f"⚠️ Key #{self.current_key_index + 1} vẫn bị limit sau {max_retries_per_key} lần thử, chuyển sang key khác...")
            self._rotate_key()
        
        # Nếu đã thử qua tất cả các key mà vẫn lỗi
        raise last_error
    
    def _prepare_image(self, image_input: Union[str, bytes, Image.Image]) -> Image.Image:
        """Chuẩn bị ảnh"""
        if isinstance(image_input, Image.Image):
            return image_input
        
        if isinstance(image_input, str):
            if image_input.startswith('data:image'):
                image_input = image_input.split(',')[1]
            image_bytes = base64.b64decode(image_input)
            return Image.open(BytesIO(image_bytes))
        
        if isinstance(image_input, bytes):
            return Image.open(BytesIO(image_input))
        
        raise ValueError(f"Unsupported image input type: {type(image_input)}")
    
    async def extract_geometry_from_image(
        self,
        image: Union[str, bytes, Image.Image],
        additional_context: str = "",
        validate: bool = False
    ) -> GeometryExtraction:
        """Trích xuất dữ liệu hình học từ ảnh"""
        pil_image = self._prepare_image(image)
        
        # Convert RGBA to RGB
        if pil_image.mode == 'RGBA':
            rgb_image = Image.new('RGB', pil_image.size, (255, 255, 255))
            rgb_image.paste(pil_image, mask=pil_image.split()[3])
            pil_image = rgb_image
        elif pil_image.mode not in ('RGB', 'L'):
            pil_image = pil_image.convert('RGB')
        
        prompt = build_extraction_prompt(additional_context)
        
        # Lưu ảnh tạm
        import tempfile
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp_file:
            pil_image.save(tmp_file.name, format='JPEG')
            tmp_path = tmp_file.name
        
        try:
            # Chạy trong thread pool để không block async event loop
            import asyncio
            loop = asyncio.get_event_loop()

            uploaded_file = await loop.run_in_executor(
                None,
                lambda: self.client.files.upload(file=tmp_path)
            )

            response = await loop.run_in_executor(
                None,
                lambda: self._generate_with_retry(
                    model=self.model_name,
                    contents=[prompt, uploaded_file],
                    config=self.generation_config
                )
            )
        finally:
            # Xóa file tạm
            import os
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
        
        try:
            response_text = response.text
            
            # Extract JSON from markdown code blocks
            if "```json" in response_text:
                json_str = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                json_str = response_text.split("```")[1].split("```")[0].strip()
            else:
                json_str = response_text.strip()
            
            # Fix: Replace LaTeX escape sequences with Unicode
            import re
            # Replace \frac{a}{b} with a/b
            json_str = re.sub(r'\\frac\{([^}]+)\}\{([^}]+)\}', r'(\1)/(\2)', json_str)
            # Replace \sqrt{x} with √x
            json_str = re.sub(r'\\sqrt\{([^}]+)\}', r'√\1', json_str)
            # Replace remaining backslashes (except valid JSON escapes)
            json_str = re.sub(r'(?<!\\)\\(?!["\\/bfnrtu])', r'', json_str)
            
            # Fix incomplete JSON - add closing brackets if missing
            open_braces = json_str.count('{')
            close_braces = json_str.count('}')
            open_brackets = json_str.count('[')
            close_brackets = json_str.count(']')
            
            # Add missing closing brackets
            if open_braces > close_braces:
                json_str += '}' * (open_braces - close_braces)
            if open_brackets > close_brackets:
                json_str += ']' * (open_brackets - close_brackets)
            
            # Fix unterminated strings - find last quote and close it
            if json_str.count('"') % 2 != 0:
                json_str += '"'
            
            # Fix: Thay thế biến 'a' bằng giá trị số để parse được JSON
            # Thay thế a/số bằng 1.0/số (ví dụ: a/2 -> 0.5)
            json_str = re.sub(r'\ba/2\b', '0.5', json_str)
            json_str = re.sub(r'\ba/3\b', '0.333', json_str)
            json_str = re.sub(r'\ba/4\b', '0.25', json_str)
            # Thay thế 'a' đơn lẻ bằng 1.0
            json_str = re.sub(r':\s*\[a,', ': [1.0,', json_str)
            json_str = re.sub(r',\s*a,', ', 1.0,', json_str)
            json_str = re.sub(r',\s*a\]', ', 1.0]', json_str)
            json_str = re.sub(r'\[a\]', '[1.0]', json_str)
            json_str = re.sub(r':\s*"a"', ': "1.0"', json_str)
            
            data = json.loads(json_str)
            extraction = GeometryExtraction(**data)
            
            return extraction
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON: {e}\nResponse: {response.text}")
        except Exception as e:
            raise ValueError(f"Failed to create GeometryExtraction: {e}")
    
    async def extract_from_text(self, problem_text: str) -> GeometryExtraction:
        """Trích xuất dữ liệu hình học từ văn bản"""
        prompt = build_extraction_prompt()
        
        full_prompt = f"""{prompt}

BÀI TOÁN:
{problem_text}

Phân tích và trả về JSON.
"""
        
        import asyncio
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: self.client.models.generate_content(
                model=self.model_name,
                contents=full_prompt,
                config=self.generation_config
            )
        )
        
        try:
            response_text = response.text
            if "```json" in response_text:
                json_str = response_text.split("```json")[1].split("```")[0].strip()
            else:
                json_str = response_text.strip()
            
            # Fix: Replace LaTeX escape sequences with Unicode
            import re
            # Replace \frac{a}{b} with a/b
            json_str = re.sub(r'\\frac\{([^}]+)\}\{([^}]+)\}', r'(\1)/(\2)', json_str)
            # Replace \sqrt{x} with √x
            json_str = re.sub(r'\\sqrt\{([^}]+)\}', r'√\1', json_str)
            # Replace remaining backslashes (except valid JSON escapes)
            json_str = re.sub(r'(?<!\\)\\(?!["\\/bfnrtu])', r'', json_str)
            
            # Fix: Xử lý biến 'a'
            # Thay thế a/số bằng giá trị số
            json_str = re.sub(r'\ba/2\b', '0.5', json_str)
            json_str = re.sub(r'\ba/3\b', '0.333', json_str)
            json_str = re.sub(r'\ba/4\b', '0.25', json_str)
            # Thay thế 'a' đơn lẻ
            json_str = re.sub(r':\s*\[a,', ': [1.0,', json_str)
            json_str = re.sub(r',\s*a,', ', 1.0,', json_str)
            json_str = re.sub(r',\s*a\]', ', 1.0]', json_str)
            
            data = json.loads(json_str)
            return GeometryExtraction(**data)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON: {e}")
        except Exception as e:
            raise ValueError(f"Failed to create GeometryExtraction: {e}")
    
    async def estimate_coordinates(self, extraction: GeometryExtraction) -> GeometryExtraction:
        """Ước lượng tọa độ 3D"""
        return extraction


async def solve_with_ai(
    problem: Optional[str] = None,
    image: Optional[Union[str, bytes, Image.Image]] = None,
    api_key: Optional[str] = None
) -> GeometryExtraction:
    """Main function để giải bài toán hình học với AI"""
    if not problem and not image:
        raise ValueError("Either problem text or image must be provided")
    
    client = GeminiClient(api_key=api_key)
    
    if image:
        extraction = await client.extract_geometry_from_image(
            image=image,
            additional_context=problem or ""
        )
    else:
        extraction = await client.extract_from_text(problem)
    
    return extraction
