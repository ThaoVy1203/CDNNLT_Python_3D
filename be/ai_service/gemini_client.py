"""
Gemini Client - Tích hợp Google Gemini API cho phân tích hình học đa phương thức
Hỗ trợ: OCR, Image Analysis, Structured Output với Pydantic
"""

import os
import json
import base64
from typing import Optional, Union
from io import BytesIO
from PIL import Image

try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False
    print("Warning: google-generativeai not installed. Install with: pip install google-generativeai")

from be.api_gateway.schemas.geometry import GeometryExtraction
from be.ai_service.prompt import (
    build_extraction_prompt,
    VALIDATION_PROMPT,
    COORDINATE_ESTIMATION_PROMPT
)


class GeminiClient:
    """Client để tương tác với Gemini API"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Khởi tạo Gemini client
        
        Args:
            api_key: Google API key. Nếu None, sẽ lấy từ biến môi trường GEMINI_API_KEY
        """
        if not GENAI_AVAILABLE:
            raise ImportError("google-generativeai package is required. Install with: pip install google-generativeai")
        
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found. Set it as environment variable or pass to constructor.")
        
        genai.configure(api_key=self.api_key)
        
        # Sử dụng Gemini 1.5 Pro cho khả năng multimodal tốt nhất
        self.model = genai.GenerativeModel('gemini-1.5-pro-latest')
        
        # Generation config cho structured output
        self.generation_config = {
            'temperature': 0.1,  # Thấp để output ổn định hơn
            'top_p': 0.95,
            'top_k': 40,
            'max_output_tokens': 8192,
        }
    
    def _prepare_image(self, image_input: Union[str, bytes, Image.Image]) -> Image.Image:
        """
        Chuẩn bị ảnh từ nhiều định dạng khác nhau
        
        Args:
            image_input: Base64 string, bytes, hoặc PIL Image
            
        Returns:
            PIL Image object
        """
        if isinstance(image_input, Image.Image):
            return image_input
        
        if isinstance(image_input, str):
            # Giả sử là base64
            if image_input.startswith('data:image'):
                # Remove data URL prefix
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
        validate: bool = True
    ) -> GeometryExtraction:
        """
        Trích xuất dữ liệu hình học từ ảnh (OCR + Image Analysis)
        
        Args:
            image: Ảnh đầu vào (base64, bytes, hoặc PIL Image)
            additional_context: Thông tin bổ sung về bài toán
            validate: Có chạy bước validation không
            
        Returns:
            GeometryExtraction object với dữ liệu đã trích xuất
        """
        # Chuẩn bị ảnh
        pil_image = self._prepare_image(image)
        
        # Xây dựng prompt
        prompt = build_extraction_prompt(additional_context)
        
        # Gọi Gemini API với multimodal input
        response = self.model.generate_content(
            [prompt, pil_image],
            generation_config=self.generation_config
        )
        
        # Parse JSON response
        try:
            # Trích xuất JSON từ response (có thể có markdown code block)
            response_text = response.text
            if "```json" in response_text:
                json_str = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                json_str = response_text.split("```")[1].split("```")[0].strip()
            else:
                json_str = response_text.strip()
            
            # Parse thành dict
            data = json.loads(json_str)
            
            # Validate với Pydantic
            extraction = GeometryExtraction(**data)
            
            # Validation step (optional)
            if validate and extraction.confidence_score < 0.8:
                extraction = await self._validate_extraction(extraction, pil_image)
            
            return extraction
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON from Gemini response: {e}\nResponse: {response.text}")
        except Exception as e:
            raise ValueError(f"Failed to create GeometryExtraction: {e}\nData: {data if 'data' in locals() else 'N/A'}")
    
    async def _validate_extraction(
        self,
        extraction: GeometryExtraction,
        image: Image.Image
    ) -> GeometryExtraction:
        """
        Validation step - kiểm tra lại dữ liệu đã trích xuất
        
        Args:
            extraction: Dữ liệu đã trích xuất ban đầu
            image: Ảnh gốc
            
        Returns:
            GeometryExtraction đã được validate/sửa
        """
        validation_prompt = f"""{VALIDATION_PROMPT}

DỮ LIỆU HIỆN TẠI:
```json
{extraction.model_dump_json(indent=2)}
```

Kiểm tra và trả về JSON đã được sửa (nếu cần) hoặc giữ nguyên nếu đã đúng.
"""
        
        response = self.model.generate_content(
            [validation_prompt, image],
            generation_config=self.generation_config
        )
        
        try:
            response_text = response.text
            if "```json" in response_text:
                json_str = response_text.split("```json")[1].split("```")[0].strip()
            else:
                json_str = response_text.strip()
            
            data = json.loads(json_str)
            return GeometryExtraction(**data)
        except:
            # Nếu validation fail, trả về bản gốc
            return extraction
    
    async def estimate_coordinates(
        self,
        extraction: GeometryExtraction
    ) -> GeometryExtraction:
        """
        Ước lượng tọa độ 3D cho các điểm dựa trên quan hệ hình học
        
        Args:
            extraction: Dữ liệu hình học đã trích xuất
            
        Returns:
            GeometryExtraction với tọa độ đã được ước lượng
        """
        prompt = f"""{COORDINATE_ESTIMATION_PROMPT}

DỮ LIỆU HÌNH HỌC:
```json
{extraction.model_dump_json(indent=2)}
```

Trả về JSON với trường coordinates đã được điền cho mỗi điểm.
"""
        
        response = self.model.generate_content(
            prompt,
            generation_config=self.generation_config
        )
        
        try:
            response_text = response.text
            if "```json" in response_text:
                json_str = response_text.split("```json")[1].split("```")[0].strip()
            else:
                json_str = response_text.strip()
            
            data = json.loads(json_str)
            return GeometryExtraction(**data)
        except:
            # Nếu estimation fail, trả về bản gốc
            return extraction
    
    async def extract_from_text(
        self,
        problem_text: str
    ) -> GeometryExtraction:
        """
        Trích xuất dữ liệu hình học từ văn bản (không có ảnh)
        
        Args:
            problem_text: Nội dung bài toán dạng text
            
        Returns:
            GeometryExtraction object
        """
        prompt = f"""{build_extraction_prompt()}

BÀI TOÁN:
{problem_text}

Phân tích và trả về JSON theo schema đã định nghĩa.
"""
        
        response = self.model.generate_content(
            prompt,
            generation_config=self.generation_config
        )
        
        try:
            response_text = response.text
            if "```json" in response_text:
                json_str = response_text.split("```json")[1].split("```")[0].strip()
            else:
                json_str = response_text.strip()
            
            data = json.loads(json_str)
            return GeometryExtraction(**data)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON: {e}\nResponse: {response.text}")
        except Exception as e:
            raise ValueError(f"Failed to create GeometryExtraction: {e}")


# ============= Helper Functions =============

async def solve_with_ai(
    problem: Optional[str] = None,
    image: Optional[Union[str, bytes, Image.Image]] = None,
    api_key: Optional[str] = None
) -> GeometryExtraction:
    """
    Main function để giải bài toán hình học với AI
    
    Args:
        problem: Nội dung bài toán dạng text (optional nếu có ảnh)
        image: Ảnh bài toán (optional nếu có text)
        api_key: Gemini API key
        
    Returns:
        GeometryExtraction với dữ liệu đã trích xuất
    """
    if not problem and not image:
        raise ValueError("Either problem text or image must be provided")
    
    client = GeminiClient(api_key=api_key)
    
    if image:
        # Multimodal: ảnh + text (nếu có)
        extraction = await client.extract_geometry_from_image(
            image=image,
            additional_context=problem or ""
        )
    else:
        # Text only
        extraction = await client.extract_from_text(problem)
    
    # Ước lượng tọa độ nếu chưa có
    if extraction.points and not any(p.coordinates for p in extraction.points):
        extraction = await client.estimate_coordinates(extraction)
    
    return extraction


# ============= Example Usage =============

if __name__ == "__main__":
    import asyncio
    
    async def test_extraction():
        """Test function"""
        
        # Test với text only
        problem = """
        Cho hình chóp S.ABC có đáy ABC là tam giác vuông tại B, AB = 3, BC = 4.
        SA vuông góc với mặt phẳng (ABC) và SA = 6.
        Tính khoảng cách từ A đến mặt phẳng (SBC).
        """
        
        try:
            result = await solve_with_ai(problem=problem)
            print("Extraction Result:")
            print(result.model_dump_json(indent=2))
        except Exception as e:
            print(f"Error: {e}")
    
    # Run test
    # asyncio.run(test_extraction())
