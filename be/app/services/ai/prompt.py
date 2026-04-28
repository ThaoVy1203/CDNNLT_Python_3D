"""
AI Prompts for Gemini - Hệ thống prompt cho phân tích hình học
"""

SYSTEM_PROMPT = """
Bạn là trợ lý AI chuyên về hình học không gian 3D.
Nhiệm vụ: Phân tích bài toán hình học và trích xuất thông tin có cấu trúc.
"""

EXTRACTION_PROMPT = """
Trích xuất các thông tin sau từ bài toán hình học:

1. **problem_text**: Nội dung đầy đủ của bài toán
2. **problem_type**: Loại hình học (hình chóp, lăng trụ, tứ diện, hình hộp...)
3. **confidence_score**: Độ tin cậy của việc trích xuất (0.0 - 1.0)
4. **given_conditions**: Danh sách các điều kiện cho trước
   - Ví dụ: ["AB = 3", "BC = 4", "SA vuông góc (ABC)"]
5. **questions**: Danh sách câu hỏi cần giải quyết
   - Ví dụ: ["Tính thể tích", "Tính khoảng cách từ A đến (SBC)"]
6. **points**: Danh sách các điểm
   - Format: [{"name": "A", "coordinates": [x, y, z]}]
   - Nếu chưa có tọa độ, để coordinates = null
7. **lines**: Danh sách các cạnh/đường thẳng
   - Format: [{"point1": "A", "point2": "B"}]
8. **relations**: Các quan hệ hình học
   - Format: [{"type": "vuông góc", "entities": ["AB", "CD"]}]
   - Các loại: "vuông góc", "song song", "bằng nhau", "thuộc"

Trả về JSON với cấu trúc trên.
"""

VALIDATION_PROMPT = """
Kiểm tra và xác thực dữ liệu hình học đã trích xuất.
Sửa các lỗi nếu có và trả về JSON đã được cải thiện.
"""

COORDINATE_ESTIMATION_PROMPT = """
Dựa trên các điều kiện hình học đã cho, ước lượng tọa độ 3D cho các điểm.

Quy tắc:
- Đặt hệ trục tọa độ Oxyz phù hợp
- Tính toán tọa độ dựa trên các quan hệ vuông góc, song song, độ dài
- Đảm bảo tính nhất quán của hệ tọa độ

Trả về JSON với trường coordinates đã được điền cho mỗi điểm.
"""

EXAMPLE_1 = """
VÍ DỤ 1:
Bài toán: "Cho hình chóp S.ABC có đáy ABC là tam giác vuông tại B, AB = 3, BC = 4. 
SA vuông góc với mặt phẳng (ABC) và SA = 6. Tính thể tích hình chóp."

JSON output:
```json
{
  "problem_text": "Cho hình chóp S.ABC có đáy ABC là tam giác vuông tại B, AB = 3, BC = 4. SA vuông góc với mặt phẳng (ABC) và SA = 6. Tính thể tích hình chóp.",
  "problem_type": "Hình chóp tam giác",
  "confidence_score": 0.95,
  "given_conditions": [
    "ABC là tam giác vuông tại B",
    "AB = 3",
    "BC = 4",
    "SA vuông góc (ABC)",
    "SA = 6"
  ],
  "questions": ["Tính thể tích hình chóp S.ABC"],
  "points": [
    {"name": "S", "coordinates": [0, 0, 6]},
    {"name": "A", "coordinates": [0, 0, 0]},
    {"name": "B", "coordinates": [3, 0, 0]},
    {"name": "C", "coordinates": [3, 4, 0]}
  ],
  "lines": [
    {"point1": "S", "point2": "A"},
    {"point1": "S", "point2": "B"},
    {"point1": "S", "point2": "C"},
    {"point1": "A", "point2": "B"},
    {"point1": "B", "point2": "C"},
    {"point1": "C", "point2": "A"}
  ],
  "relations": [
    {"type": "vuông góc", "entities": ["SA", "(ABC)"]},
    {"type": "vuông góc", "entities": ["AB", "BC"]}
  ]
}
```
"""

EXAMPLE_2 = """
VÍ DỤ 2:
Bài toán: "Cho hình lập phương ABCD.A'B'C'D' cạnh a. 
Tính khoảng cách từ A đến mặt phẳng (BDC')."

JSON output:
```json
{
  "problem_text": "Cho hình lập phương ABCD.A'B'C'D' cạnh a. Tính khoảng cách từ A đến mặt phẳng (BDC').",
  "problem_type": "Hình lập phương",
  "confidence_score": 0.9,
  "given_conditions": [
    "ABCD.A'B'C'D' là hình lập phương",
    "Cạnh = a"
  ],
  "questions": ["Tính khoảng cách từ A đến (BDC')"],
  "points": [
    {"name": "A", "coordinates": [0, 0, 0]},
    {"name": "B", "coordinates": [1, 0, 0]},
    {"name": "C", "coordinates": [1, 1, 0]},
    {"name": "D", "coordinates": [0, 1, 0]},
    {"name": "A'", "coordinates": [0, 0, 1]},
    {"name": "B'", "coordinates": [1, 0, 1]},
    {"name": "C'", "coordinates": [1, 1, 1]},
    {"name": "D'", "coordinates": [0, 1, 1]}
  ],
  "lines": [],
  "relations": [
    {"type": "song song", "entities": ["AB", "CD"]},
    {"type": "vuông góc", "entities": ["AB", "AD"]}
  ]
}
```
"""

def build_extraction_prompt(additional_context: str = "") -> str:
    """Xây dựng prompt hoàn chỉnh cho việc trích xuất"""
    
    prompt = f"""{SYSTEM_PROMPT}

{EXTRACTION_PROMPT}

{EXAMPLE_1}

{EXAMPLE_2}

## YÊU CẦU QUAN TRỌNG:
1. Phân tích CẢ văn bản VÀ hình ảnh (nếu có)
2. Trích xuất ĐẦY ĐỦ tất cả thực thể và quan hệ
3. Trả về JSON tuân thủ CHÍNH XÁC schema đã định nghĩa
4. Đánh giá confidence_score dựa trên độ rõ ràng của ảnh/text
5. Ghi chú vào extraction_notes nếu có điểm không chắc chắn
"""
    
    if additional_context:
        prompt += f"\n## THÔNG TIN BỔ SUNG:\n{additional_context}\n"
    
    prompt += "\n## BẮT ĐẦU PHÂN TÍCH:\n"
    
    return prompt


# ============================================================
# PROMPTS CHO GIẢI TOÁN
# ============================================================

SOLVE_PROBLEM_PROMPT = """
Bạn là giáo viên toán chuyên về hình học không gian.
Hãy giải chi tiết bài toán sau:

{problem_text}

YÊU CẦU QUAN TRỌNG:
- Trong JSON, các công thức LaTeX phải escape đúng: dùng \\\\ thay vì \\
- Ví dụ: "\\\\frac{{a}}{{2}}" thay vì "\\frac{{a}}{{2}}"
- Hoặc dùng text thuần không có LaTeX

Trả về JSON với format:
{{
  "steps": ["Bước 1: ...", "Bước 2: ...", ...],
  "result": "Kết quả cuối cùng",
  "formulas_used": ["Công thức 1", "Công thức 2", ...]
}}
"""


# ============================================================
# PROMPTS CHO DỰNG HÌNH 3D
# ============================================================

DRAWING_GUIDE_PROMPT = """
Bạn là giáo viên toán chuyên về hình học không gian.
Hãy tạo hướng dẫn DỰNG HÌNH cho học sinh dựa trên đề bài sau:

ĐỀ BÀI:
{problem_text}

LOẠI HÌNH: {shape_type}

YÊU CẦU:
1. Hướng dẫn phải theo thứ tự logic (vẽ đáy trước, sau đó các điểm đặc biệt, rồi nối các cạnh)
2. Chỉ rõ quan hệ hình học khi vẽ (vuông góc, song song, trung điểm, v.v.)
3. Ngôn ngữ đơn giản, dễ hiểu cho học sinh
4. Không đề cập đến kỹ thuật lập trình hay Three.js

Trả về hướng dẫn theo format:

HƯỚNG DẪN DỰNG HÌNH [TÊN HÌNH]

Bước 1: [Mô tả bước đầu tiên - thường là vẽ đáy]
   - [Chi tiết 1]
   - [Chi tiết 2]

Bước 2: [Mô tả bước tiếp theo]
   - [Chi tiết 1]
   - [Chi tiết 2]

...

Lưu ý:
   - [Các quan hệ hình học quan trọng]
"""


def build_solve_prompt(problem_text: str) -> str:
    """Xây dựng prompt để giải bài toán"""
    return SOLVE_PROBLEM_PROMPT.format(problem_text=problem_text)


def build_drawing_guide_prompt(problem_text: str, shape_type: str) -> str:
    """Xây dựng prompt để tạo hướng dẫn dựng hình"""
    return DRAWING_GUIDE_PROMPT.format(
        problem_text=problem_text,
        shape_type=shape_type
    )
