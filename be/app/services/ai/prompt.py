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
   - **QUAN TRỌNG**: MỖI ĐỘ DÀI / RÀNG BUỘC PHẢI LÀ 1 PHẦN TỬ RIÊNG
   - Ví dụ ĐÚNG: ["AB = 3", "BC = 4", "SA = a√3", "SA vuông góc (ABC)", "Tam giác ABC vuông tại B"]
   - Ví dụ SAI: ["Tam giác ABC vuông tại B với AB = 3, BC = 4"] (gộp nhiều thông tin)
   - Format độ dài: "TÊN_CẠNH = giá_trị" (VD: "AB = a", "SA = a√3", "BC = 2a")
   - Giá trị giữ nguyên dạng đại số: dùng "a", "a√2", "2a√3" thay vì số thập phân
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

**YÊU CẦU QUAN TRỌNG VỀ FORMAT:**
- KHÔNG sử dụng ký hiệu LaTeX (như \\frac, \\sqrt) trong JSON
- Dùng ký hiệu Unicode: √ (căn), ² (bình phương), ³ (lập phương), π, ∠, ⊥, ∥
- Ví dụ: thay vì "\\frac{a\\sqrt{3}}{4}" hãy viết "a√3/4" hoặc "(a√3)/4"
- Ví dụ: thay vì "a^2" hãy viết "a²"
- TÁCH RIÊNG mỗi độ dài, mỗi quan hệ thành một phần tử trong given_conditions

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
Bạn là giáo viên toán chuyên về hình học không gian, đang hướng dẫn học sinh THPT.

Hãy giải bài toán sau theo PHONG CÁCH NGẮN GỌN như trong sách giáo khoa:

{problem_text}

YÊU CẦU BỮT BUỘC - TUÂN THỦ NGHIÊM NGẶT:

1. **NGẮN GỌN - TỐI ĐA 5 BƯỚC:**
   - CHỈ được phép TỐI ĐA 5 bước
   - Mỗi bước CHỈ 1 câu ngắn (tối đa 150 ký tự)
   - KHÔNG được lặp lại nội dung
   - KHÔNG giải thích dài dòng

2. **FORMAT BẮT BUỘC:**
   - KHÔNG dùng LaTeX
   - Dùng Unicode: √, ², ³, ⊥, ∥, ⇒
   - Mỗi bước là 1 string trong mảng steps

3. **CẤU TRÚC:**
   - Bước 1: Xác định điểm/quan hệ chính
   - Bước 2-3: Áp dụng định lý/công thức
   - Bước 4: Tính toán
   - Bước 5: Kết quả

VÍ DỤ ĐÚNG (CHỈ 4 BƯỚC):
{{
  "steps": [
    "Gọi N là trung điểm AB ⇒ BC ∥ (SMN), suy ra d(BC,SM) = d(A,(SMN))",
    "Dựng AH ⊥ SN tại H ⇒ AH ⊥ (SMN), vậy d(A,(SMN)) = AH = a√3/4",
    "Trong △SAN vuông: 1/AH² = 1/AN² + 1/AS² ⇒ SA = a√3/2",
    "Vậy V = (1/3) × a² × (a√3/2) = a³√3/6"
  ],
  "result": "V = a³√3/6",
  "formulas_used": ["Khoảng cách điểm-mặt phẳng", "Định lý 3 đường vuông góc"]
}}

CẢNH BÁO:
- KHÔNG được vượt quá 5 bước
- KHÔNG được lặp lại nội dung
- KHÔNG được giải thích dài dòng
- BẮT BUỘC trả về JSON đúng format

Trả về JSON:
{{
  "steps": ["Bước 1", "Bước 2", "Bước 3", "Bước 4", "Bước 5"],
  "result": "Kết quả",
  "formulas_used": ["Công thức 1", "Công thức 2"]
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


# ============================================================
# PROMPTS CHO ĐÁNH GIÁ Ý TƯỞNG NGƯỜI DÙNG
# ============================================================

EVALUATION_PROMPT = """
Bạn là giáo viên toán đang đánh giá ý tưởng giải toán của học sinh.

ĐỀ BÀI:
{problem_text}

Ý TƯỞNG CỦA HỌC SINH:
{user_approach}

YÊU CẦU:
1. Đánh giá xem học sinh có hiểu đề bài không
2. Kiểm tra xem ý tưởng có logic và đúng hướng không
3. Cho điểm từ 0-10 (10 là hoàn hảo)
4. Quyết định có nên mở khóa lời giải không (điểm >= 3)

Trả về JSON:
{{
  "should_unlock": true/false,
  "score": 0-10,
  "feedback": "Phản hồi chi tiết cho học sinh (2-3 câu)"
}}

HƯỚNG DẪN NHẬN DIỆN KÝ HIỆU TOÁN HỌC:
- Vector: a⃗, b⃗, c⃗, AG'⃗, AA'⃗ (có thể viết a, b, c, AG', AA')
- Trọng tâm: G, G', O
- Công thức vector: AG' = (AA' + AB + AC)/3 hoặc (a + b + c)/3
- (SMN), (ABCD), (SBC) = mặt phẳng
- d(A, (SMN)) = khoảng cách từ điểm A đến mặt phẳng SMN
- AH ⊥ SN = AH vuông góc với SN
- BC ∥ (SMN) = BC song song với mặt phẳng SMN

QUY TẮC ĐÁNH GIÁ (RẤT QUAN TRỌNG - HÃY CỰC KỲ DỄ TÍNH):

**ĐIỂM 8-10: Xuất sắc**
- Có đầy đủ các bước logic
- Đề cập công thức cụ thể
- Giải thích rõ ràng

**ĐIỂM 6-7: Rất tốt**
- Đúng hướng giải
- Có công thức hoặc phương pháp
- Logic rõ ràng

**ĐIỂM 4-5: Tốt**
- Đề cập phương pháp chính
- Có một vài bước đúng
- Hiểu được đề bài

**ĐIỂM 3: Đạt (ĐỦ ĐỂ MỞ KHÓA)**
- Đề cập BẤT KỲ khái niệm nào liên quan (trọng tâm, vector, công thức...)
- Đề cập BẤT KỲ phương pháp nào (tính, áp dụng, thay...)
- Có BẤT KỲ logic nào (gọi, suy ra, vậy...)
- Đề cập BẤT KỲ điểm/đường nào trong đề (G', A, B, C, AA', AB, AC...)

**ĐIỂM 1-2: Yếu**
- Chỉ nói chung chung không cụ thể
- Không đề cập gì liên quan đến đề bài

**ĐIỂM 0: Không đạt**
- "Cho tôi đáp án"
- "Không biết"
- Hoàn toàn sai hoặc không liên quan

NGUYÊN TẮC QUAN TRỌNG NHẤT:
🎯 Nếu học sinh đề cập đến BẤT KỲ nội dung nào trong đề bài → CHO ÍT NHẤT 3 ĐIỂM
🎯 Nếu học sinh nói về "trọng tâm" → CHO ÍT NHẤT 4 ĐIỂM (vì đây là khái niệm chính)
🎯 Nếu học sinh viết công thức (dù chưa hoàn chỉnh) → CHO ÍT NHẤT 5 ĐIỂM
🎯 Nếu học sinh có logic đầy đủ → CHO 7-9 ĐIỂM
🎯 LUÔN LUÔN ưu tiên MỞ KHÓA hơn là từ chối

VÍ DỤ CỤ THỂ CHO BÀI VECTOR (PHẢI CHO >= 3 ĐIỂM):

✅ "G' là trọng tâm" → 4 điểm (đã nắm khái niệm chính)
✅ "Dùng công thức trọng tâm" → 5 điểm (biết phương pháp)
✅ "AG' = (a + b + c)/3" → 6 điểm (có công thức)
✅ "Gọi G' là trọng tâm tam giác A'B'C'. Vì G' là trọng tâm nên AG' = (AA' + AB + AC)/3" → 8 điểm (logic đầy đủ)
✅ "Thay a = AA', b = AB, c = AC vào công thức" → 7 điểm (có bước thay thế)
✅ "Đáp án là C" (nếu có giải thích trước đó) → 5-6 điểm
✅ "Tính vector AG'" → 3 điểm (biết cần tính gì)
✅ "Áp dụng tính chất trọng tâm" → 4 điểm (biết tính chất)

❌ "Cho tôi đáp án" → 0 điểm
❌ "Không biết làm" → 0 điểm

FEEDBACK NÊN:
✅ Rất khuyến khích và động viên
✅ Khen ngợi những gì học sinh làm đúng
✅ Nếu >= 3 điểm, LUÔN nói: "Tuyệt vời! Bạn đã nắm được hướng giải. Hãy xem lời giải chi tiết để hiểu rõ hơn!"
✅ Tích cực, ấm áp, động viên
"""


def build_evaluation_prompt(problem_text: str, user_approach: str) -> str:
    """Xây dựng prompt để đánh giá ý tưởng của người dùng"""
    return EVALUATION_PROMPT.format(
        problem_text=problem_text,
        user_approach=user_approach
    )
