"""
Bộ Prompt tối ưu cho Gemini để trích xuất dữ liệu hình học không gian 3D
Hỗ trợ đa phương thức: OCR + Phân tích hình ảnh sơ đồ
"""

# ============= SYSTEM PROMPT - Định nghĩa vai trò =============

SYSTEM_PROMPT = """Bạn là một chuyên gia phân tích hình học không gian 3D với khả năng:
1. Đọc và hiểu văn bản bài toán (OCR)
2. Phân tích sơ đồ hình học từ ảnh
3. Trích xuất các thực thể: điểm, đường thẳng, mặt phẳng
4. Nhận diện quan hệ hình học: vuông góc, song song, giao nhau
5. Chuẩn hóa dữ liệu theo cấu trúc JSON chặt chẽ

Nhiệm vụ của bạn là phân tích toàn diện và trả về dữ liệu có cấu trúc."""

# ============= EXTRACTION PROMPT - Hướng dẫn trích xuất =============

EXTRACTION_PROMPT = """
# HƯỚNG DẪN TRÍCH XUẤT DỮ LIỆU HÌNH HỌC

## Bước 1: Đọc văn bản (OCR)
- Trích xuất toàn bộ nội dung văn bản từ ảnh
- Nhận diện các ký hiệu toán học đặc biệt
- Phân tách đề bài thành: điều kiện cho trước và câu hỏi

## Bước 2: Phân tích sơ đồ hình học
- Nhận diện các điểm và ghi nhận tên điểm (A, B, C, S, ...)
- Nhận diện các đường thẳng (nét liền, nét đứt)
- Nhận diện các mặt phẳng (hình tam giác, tứ giác, ...)
- Chú ý các ký hiệu đặc biệt: góc vuông (⊥), song song (//), mũi tên

## Bước 3: Trích xuất thực thể

### ĐIỂM (Points):
- Tên điểm: chữ cái in hoa (A, B, C, D, S, H, ...)
- Vị trí tương đối: đỉnh, trung điểm, chân đường cao, ...
- Mô tả: "Đỉnh của hình chóp", "Chân đường cao", ...

### ĐƯỜNG THẲNG (Lines):
- Tên: AB, CD, d, Δ, ...
- Các điểm thuộc đường thẳng
- Đặc điểm: "Đường cao", "Cạnh bên", "Giao tuyến", ...

### MẶT PHẲNG (Planes):
- Tên: (ABC), (SAB), (P), (Q), ...
- Các điểm xác định mặt phẳng (ít nhất 3 điểm)
- Đặc điểm: "Mặt đáy", "Mặt bên", ...

## Bước 4: Nhận diện quan hệ hình học

### VUÔNG GÓC (perpendicular):
- Ký hiệu: ⊥, góc vuông trong hình
- Ví dụ: "SA ⊥ (ABC)", "AB ⊥ CD"

### SONG SONG (parallel):
- Ký hiệu: //, các cạnh song song
- Ví dụ: "AB // CD", "(P) // (Q)"

### GIAO NHAU (intersect):
- Giao điểm của đường thẳng
- Giao tuyến của mặt phẳng

### CHỨA (contains):
- Điểm thuộc đường thẳng/mặt phẳng
- Đường thẳng nằm trong mặt phẳng

### ĐỒNG PHẲNG (coplanar):
- Các điểm/đường thẳng cùng nằm trên một mặt phẳng

## Bước 5: Phân loại bài toán
Xác định loại bài toán:
- Tính khoảng cách (điểm-điểm, điểm-đường, điểm-mặt, đường-đường)
- Tính góc (góc giữa đường-đường, đường-mặt, mặt-mặt)
- Tính diện tích (tam giác, tứ giác, hình chiếu)
- Tính thể tích (khối chóp, khối lăng trụ)
- Chứng minh quan hệ hình học

## Bước 6: Trả về JSON có cấu trúc
Tuân thủ nghiêm ngặt schema đã định nghĩa với các trường:
- problem_text: Nội dung bài toán
- problem_type: Loại bài toán
- points: Danh sách điểm
- lines: Danh sách đường thẳng
- planes: Danh sách mặt phẳng
- relations: Các quan hệ hình học
- given_conditions: Điều kiện cho trước
- questions: Câu hỏi cần giải
- confidence_score: Độ tin cậy (0-1)
"""

# ============= EXAMPLES - Ví dụ mẫu =============

EXAMPLE_1 = """
## VÍ DỤ 1: Hình chóp tam giác

### Input (Ảnh + Text):
"Cho hình chóp S.ABC có đáy ABC là tam giác vuông tại B, AB = 3, BC = 4.
SA vuông góc với mặt phẳng (ABC) và SA = 6.
Tính khoảng cách từ A đến mặt phẳng (SBC)."

### Output JSON:
```json
{
  "problem_text": "Cho hình chóp S.ABC có đáy ABC là tam giác vuông tại B, AB = 3, BC = 4. SA vuông góc với mặt phẳng (ABC) và SA = 6. Tính khoảng cách từ A đến mặt phẳng (SBC).",
  "problem_type": "Tính khoảng cách từ điểm đến mặt phẳng",
  "points": [
    {"name": "S", "coordinates": null, "description": "Đỉnh hình chóp"},
    {"name": "A", "coordinates": null, "description": "Đỉnh tam giác đáy"},
    {"name": "B", "coordinates": null, "description": "Đỉnh tam giác đáy, góc vuông"},
    {"name": "C", "coordinates": null, "description": "Đỉnh tam giác đáy"}
  ],
  "lines": [
    {"name": "SA", "points": ["S", "A"], "description": "Cạnh bên hình chóp"},
    {"name": "AB", "points": ["A", "B"], "description": "Cạnh góc vuông"},
    {"name": "BC", "points": ["B", "C"], "description": "Cạnh góc vuông"}
  ],
  "planes": [
    {"name": "(ABC)", "points": ["A", "B", "C"], "description": "Mặt đáy"},
    {"name": "(SBC)", "points": ["S", "B", "C"], "description": "Mặt bên"}
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
  "confidence_score": 0.95
}
```
"""

EXAMPLE_2 = """
## VÍ DỤ 2: Hình lăng trụ

### Input:
"Cho hình lăng trụ đứng ABC.A'B'C' có đáy ABC là tam giác đều cạnh a.
AA' = 2a. Gọi M là trung điểm của BB'.
Chứng minh AM vuông góc với BC'."

### Output JSON:
```json
{
  "problem_text": "Cho hình lăng trụ đứng ABC.A'B'C' có đáy ABC là tam giác đều cạnh a. AA' = 2a. Gọi M là trung điểm của BB'. Chứng minh AM vuông góc với BC'.",
  "problem_type": "Chứng minh quan hệ vuông góc",
  "points": [
    {"name": "A", "coordinates": null, "description": "Đỉnh đáy dưới"},
    {"name": "B", "coordinates": null, "description": "Đỉnh đáy dưới"},
    {"name": "C", "coordinates": null, "description": "Đỉnh đáy dưới"},
    {"name": "A'", "coordinates": null, "description": "Đỉnh đáy trên"},
    {"name": "B'", "coordinates": null, "description": "Đỉnh đáy trên"},
    {"name": "C'", "coordinates": null, "description": "Đỉnh đáy trên"},
    {"name": "M", "coordinates": null, "description": "Trung điểm BB'"}
  ],
  "lines": [
    {"name": "AA'", "points": ["A", "A'"], "description": "Cạnh bên"},
    {"name": "BB'", "points": ["B", "B'"], "description": "Cạnh bên"},
    {"name": "CC'", "points": ["C", "C'"], "description": "Cạnh bên"},
    {"name": "AM", "points": ["A", "M"], "description": "Đường cần chứng minh"},
    {"name": "BC'", "points": ["B", "C'"], "description": "Đường chéo"}
  ],
  "planes": [
    {"name": "(ABC)", "points": ["A", "B", "C"], "description": "Đáy dưới"},
    {"name": "(A'B'C')", "points": ["A'", "B'", "C'"], "description": "Đáy trên"}
  ],
  "relations": [
    {
      "entity1": "AA'",
      "entity1_type": "line",
      "relation": "perpendicular",
      "entity2": "(ABC)",
      "entity2_type": "plane",
      "confidence": 1.0
    },
    {
      "entity1": "(ABC)",
      "entity1_type": "plane",
      "relation": "parallel",
      "entity2": "(A'B'C')",
      "entity2_type": "plane",
      "confidence": 1.0
    }
  ],
  "given_conditions": [
    "Hình lăng trụ đứng ABC.A'B'C'",
    "Tam giác ABC đều cạnh a",
    "AA' = 2a",
    "M là trung điểm BB'"
  ],
  "questions": [
    "Chứng minh AM ⊥ BC'"
  ],
  "confidence_score": 0.92
}
```
"""

# ============= MAIN PROMPT TEMPLATE =============

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

# ============= VALIDATION PROMPT =============

VALIDATION_PROMPT = """
Kiểm tra lại dữ liệu đã trích xuất:
1. Tất cả điểm được đề cập có trong danh sách points?
2. Các quan hệ hình học đã được ghi nhận đầy đủ?
3. Điều kiện cho trước và câu hỏi đã được tách biệt rõ ràng?
4. JSON có tuân thủ schema không?

Nếu có thiếu sót, bổ sung ngay.
"""

# ============= COORDINATE ESTIMATION PROMPT =============

COORDINATE_ESTIMATION_PROMPT = """
Dựa trên các quan hệ hình học đã trích xuất, hãy ước lượng tọa độ 3D cho các điểm.

QUY TẮC ƯỚC LƯỢNG:
1. Chọn hệ tọa độ phù hợp (thường đặt gốc tại một đỉnh)
2. Sử dụng các điều kiện vuông góc để định hướng trục
3. Áp dụng các độ dài đã cho
4. Đảm bảo các quan hệ song song, vuông góc được thỏa mãn

Trả về tọa độ dạng [x, y, z] cho mỗi điểm.
"""
