# Hệ thống Trích xuất Dữ liệu Hình học với Gemini AI

## Tổng quan

Hệ thống sử dụng Google Gemini API để trích xuất dữ liệu hình học không gian 3D từ ảnh và văn bản, hỗ trợ:

- **OCR**: Đọc văn bản bài toán từ ảnh
- **Image Analysis**: Phân tích sơ đồ hình học
- **Entity Extraction**: Trích xuất điểm, đường thẳng, mặt phẳng
- **Relation Detection**: Nhận diện quan hệ vuông góc, song song, giao nhau
- **Structured Output**: Chuẩn hóa dữ liệu với Pydantic schemas

## Kiến trúc

```
be/ai_service/
├── gemini_client.py      # Client tương tác với Gemini API
├── prompt.py             # Bộ prompt engineering tối ưu
└── README.md            # Tài liệu này
```

## Cài đặt

### 1. Cài đặt dependencies

```bash
cd be
pip install -r requirements.txt
```

### 2. Cấu hình API Key

Lấy API key từ [Google AI Studio](https://makersuite.google.com/app/apikey)

**Cách 1: Biến môi trường**
```bash
export GEMINI_API_KEY="your-api-key-here"
```

**Cách 2: File .env**
```bash
echo "GEMINI_API_KEY=your-api-key-here" > .env
```

**Cách 3: Truyền trực tiếp**
```python
client = GeminiClient(api_key="your-api-key-here")
```

## Sử dụng

### 1. Trích xuất từ ảnh (Multimodal)

```python
from be.ai_service.gemini_client import solve_with_ai
from PIL import Image

# Từ file ảnh
image = Image.open("geometry_problem.jpg")
result = await solve_with_ai(image=image)

# Từ base64
image_base64 = "data:image/jpeg;base64,/9j/4AAQ..."
result = await solve_with_ai(image=image_base64)

# Với thông tin bổ sung
result = await solve_with_ai(
    image=image,
    problem="Bài toán về hình chóp tam giác"
)
```

### 2. Trích xuất từ văn bản

```python
problem = """
Cho hình chóp S.ABC có đáy ABC là tam giác vuông tại B, AB = 3, BC = 4.
SA vuông góc với mặt phẳng (ABC) và SA = 6.
Tính khoảng cách từ A đến mặt phẳng (SBC).
"""

result = await solve_with_ai(problem=problem)
```

### 3. Sử dụng GeminiClient trực tiếp

```python
from be.ai_service.gemini_client import GeminiClient

client = GeminiClient(api_key="your-key")

# Trích xuất từ ảnh
extraction = await client.extract_geometry_from_image(
    image=image,
    additional_context="Hình chóp tam giác",
    validate=True  # Bật validation
)

# Ước lượng tọa độ
extraction_with_coords = await client.estimate_coordinates(extraction)

# Trích xuất từ text
extraction = await client.extract_from_text(problem_text)
```

## Cấu trúc dữ liệu đầu ra

### GeometryExtraction Schema

```python
{
  "problem_text": str,           # Nội dung bài toán
  "problem_type": str,           # Loại bài toán
  
  "points": [                    # Danh sách điểm
    {
      "name": str,               # Tên điểm (A, B, C, ...)
      "coordinates": [x, y, z],  # Tọa độ 3D (optional)
      "description": str         # Mô tả vị trí
    }
  ],
  
  "lines": [                     # Danh sách đường thẳng
    {
      "name": str,               # Tên đường (AB, d, ...)
      "points": [str],           # Các điểm thuộc đường
      "direction_vector": [x, y, z],  # Vector chỉ phương (optional)
      "description": str
    }
  ],
  
  "planes": [                    # Danh sách mặt phẳng
    {
      "name": str,               # Tên mặt phẳng ((ABC), (P), ...)
      "points": [str],           # Các điểm xác định mặt phẳng
      "normal_vector": [x, y, z],     # Vector pháp tuyến (optional)
      "description": str
    }
  ],
  
  "relations": [                 # Quan hệ hình học
    {
      "entity1": str,            # Tên thực thể 1
      "entity1_type": str,       # Loại: point/line/plane
      "relation": str,           # perpendicular/parallel/intersect/contains/coplanar
      "entity2": str,            # Tên thực thể 2
      "entity2_type": str,
      "confidence": float        # Độ tin cậy 0-1
    }
  ],
  
  "given_conditions": [str],     # Điều kiện cho trước
  "questions": [str],            # Câu hỏi cần giải
  
  "confidence_score": float,     # Độ tin cậy tổng thể 0-1
  "extraction_notes": str        # Ghi chú
}
```

## Ví dụ đầu ra

### Input
Ảnh bài toán: Hình chóp S.ABC với SA ⊥ (ABC), AB = 3, BC = 4, SA = 6

### Output
```json
{
  "problem_text": "Cho hình chóp S.ABC có đáy ABC là tam giác vuông tại B, AB = 3, BC = 4. SA vuông góc với mặt phẳng (ABC) và SA = 6. Tính khoảng cách từ A đến mặt phẳng (SBC).",
  "problem_type": "Tính khoảng cách từ điểm đến mặt phẳng",
  
  "points": [
    {"name": "S", "coordinates": [0, 0, 6], "description": "Đỉnh hình chóp"},
    {"name": "A", "coordinates": [0, 0, 0], "description": "Gốc tọa độ"},
    {"name": "B", "coordinates": [3, 0, 0], "description": "Góc vuông"},
    {"name": "C", "coordinates": [3, 4, 0], "description": "Đỉnh thứ 3"}
  ],
  
  "lines": [
    {"name": "SA", "points": ["S", "A"], "direction_vector": [0, 0, 1]},
    {"name": "AB", "points": ["A", "B"], "direction_vector": [1, 0, 0]},
    {"name": "BC", "points": ["B", "C"], "direction_vector": [0, 1, 0]}
  ],
  
  "planes": [
    {"name": "(ABC)", "points": ["A", "B", "C"], "normal_vector": [0, 0, 1]},
    {"name": "(SBC)", "points": ["S", "B", "C"], "normal_vector": null}
  ],
  
  "relations": [
    {
      "entity1": "SA",
      "entity1_type": "line",
      "relation": "perpendicular",
      "entity2": "(ABC)",
      "entity2_type": "plane",
      "confidence": 1.0
    },
    {
      "entity1": "AB",
      "entity1_type": "line",
      "relation": "perpendicular",
      "entity2": "BC",
      "entity2_type": "line",
      "confidence": 1.0
    }
  ],
  
  "given_conditions": [
    "Tam giác ABC vuông tại B",
    "AB = 3",
    "BC = 4",
    "SA ⊥ (ABC)",
    "SA = 6"
  ],
  
  "questions": [
    "Tính khoảng cách từ A đến mặt phẳng (SBC)"
  ],
  
  "confidence_score": 0.95,
  "extraction_notes": "Tọa độ đã được ước lượng dựa trên hệ trục Oxyz với A là gốc"
}
```

## Tối ưu hóa Prompt

### 1. Cấu trúc Prompt

Hệ thống sử dụng prompt engineering 3 tầng:

1. **System Prompt**: Định nghĩa vai trò và khả năng
2. **Extraction Prompt**: Hướng dẫn chi tiết từng bước
3. **Examples**: Ví dụ mẫu với input/output

### 2. Kỹ thuật sử dụng

- **Few-shot learning**: Cung cấp 2-3 ví dụ mẫu
- **Chain-of-thought**: Hướng dẫn từng bước phân tích
- **Structured output**: Yêu cầu JSON theo schema chặt chẽ
- **Validation**: Kiểm tra lại kết quả với confidence thấp

### 3. Tùy chỉnh Prompt

Chỉnh sửa file `prompt.py`:

```python
# Thêm ví dụ mới
EXAMPLE_3 = """..."""

# Tùy chỉnh hướng dẫn
EXTRACTION_PROMPT = """
Thêm hướng dẫn đặc biệt cho loại bài toán của bạn...
"""

# Xây dựng prompt với context
prompt = build_extraction_prompt(
    additional_context="Chú ý đặc biệt đến góc vuông"
)
```

## Xử lý lỗi

### 1. API Key không hợp lệ
```python
ValueError: GEMINI_API_KEY not found
```
→ Kiểm tra lại API key và biến môi trường

### 2. JSON parsing error
```python
ValueError: Failed to parse JSON from Gemini response
```
→ Response không đúng format, kiểm tra prompt hoặc tăng temperature

### 3. Pydantic validation error
```python
ValidationError: Field required
```
→ Dữ liệu thiếu trường bắt buộc, cải thiện prompt hoặc bật validation

## Best Practices

### 1. Chất lượng ảnh đầu vào
- Độ phân giải tối thiểu: 800x600
- Ảnh rõ nét, không bị mờ
- Sơ đồ hình học rõ ràng, có nhãn điểm

### 2. Tối ưu hiệu suất
- Cache kết quả cho cùng một ảnh
- Sử dụng batch processing cho nhiều ảnh
- Giảm temperature (0.1-0.2) cho output ổn định

### 3. Độ tin cậy
- Kiểm tra `confidence_score` trước khi sử dụng
- Bật validation cho confidence < 0.8
- Review `extraction_notes` để hiểu hạn chế

### 4. Xử lý edge cases
- Ảnh không có sơ đồ → Trích xuất từ text only
- Ký hiệu đặc biệt → Cung cấp additional_context
- Bài toán phức tạp → Chia nhỏ thành các bước

## Tích hợp với API

Xem file `be/api_gateway/routes/` để tích hợp vào FastAPI endpoint:

```python
from fastapi import UploadFile
from be.ai_service.gemini_client import solve_with_ai

@app.post("/api/analyze")
async def analyze_geometry(file: UploadFile):
    image_bytes = await file.read()
    result = await solve_with_ai(image=image_bytes)
    return result.model_dump()
```

## Troubleshooting

### Gemini API Quota
- Free tier: 60 requests/minute
- Nếu vượt quota, đợi 1 phút hoặc upgrade plan

### Model không khả dụng
- Kiểm tra region: Gemini chưa khả dụng ở một số quốc gia
- Sử dụng VPN nếu cần

### Output không đúng format
- Tăng số lượng examples trong prompt
- Giảm temperature xuống 0.1
- Thêm validation step

## Roadmap

- [ ] Hỗ trợ batch processing
- [ ] Cache và rate limiting
- [ ] Fine-tuning cho domain cụ thể
- [ ] Hỗ trợ thêm loại hình học (ellipse, parabola, ...)
- [ ] Export sang LaTeX/TikZ
- [ ] Tích hợp với symbolic math solver

## Tài liệu tham khảo

- [Google Gemini API Documentation](https://ai.google.dev/docs)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Prompt Engineering Guide](https://www.promptingguide.ai/)
