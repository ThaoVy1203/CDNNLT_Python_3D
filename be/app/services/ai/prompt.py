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


# ============================================================
# PROMPTS CHO DỰNG HÌNH 3D (Gemini sinh mảng lệnh vẽ)
# ============================================================

RENDER_3D_SYSTEM = """
Bạn là hệ thống dựng hình 3D cho bài toán hình học không gian.
Bạn sẽ ĐỌC đề bài rồi sinh ra MỘT MẢNG JSON CÁC LỆNH VẼ để frontend Three.js
thực thi. Mỗi lệnh có dạng { "fn": "...", "args": { ... } }.
"""

RENDER_3D_API = """
## DANH SÁCH HÀM VẼ CÓ SẴN (chỉ được dùng đúng các hàm này):

1. drawPoint(name, x, y, z, opts?)
   - args: { "name": str, "x": num, "y": num, "z": num, "opts"?: { "color"?: "#rrggbb", "radius"?: num } }
   - Vẽ 1 điểm + nhãn tên.

2. drawEdge(from, to, opts?)
   - args: { "from": str, "to": str, "opts"?: { "style"?: "solid"|"dashed", "color"?: "#rrggbb", "label"?: str } }
   - Vẽ cạnh nối 2 điểm. Nếu opts.label có thì hiển thị nhãn độ dài giữa cạnh.
   - QUY ƯỚC: 'from'/'to' phải là tên điểm đã drawPoint TRƯỚC.

3. drawFace(points[], opts?)
   - args: { "points": [str, str, ...], "opts"?: { "opacity"?: num, "color"?: "#rrggbb" } }
   - Vẽ mặt phẳng trong suốt từ danh sách tên điểm.

4. drawLabel(text, x, y, z, opts?)
   - args: { "text": str, "x": num, "y": num, "z": num, "opts"?: { "color"?: "#rrggbb", "scale"?: num } }
   - Nhãn văn bản tự do tại 1 vị trí.

5. drawRightAngle(vertex, edge1, edge2)
   - args: { "vertex": str, "edge1": "X-Y", "edge2": "X-Z" }
   - Vẽ ô vuông nhỏ tại đỉnh vertex để ký hiệu góc vuông giữa 2 cạnh.

6. drawEqualMark(from, to, mark?)
   - args: { "from": str, "to": str, "mark"?: "single"|"double"|"triple" }
   - Vẽ tick gạch trên đoạn để ký hiệu các đoạn bằng nhau.

7. drawAngle(vertex, edge1, edge2, value?)
   - args: { "vertex": str, "edge1": str, "edge2": str, "value"?: num }
   - Vẽ cung góc + nhãn giá trị (nếu có).

8. setCamera(x, y, z, lx?, ly?, lz?)
   - args: { "x": num, "y": num, "z": num, "lx"?: num, "ly"?: num, "lz"?: num }
   - Đặt vị trí camera nhìn vào hình.
"""

RENDER_3D_RULES = """
## QUY TẮC SINH LỆNH VẼ - TUÂN THỦ NGHIÊM NGẶT:

A. CHỌN HỆ TỌA ĐỘ:
   - Coi tham số "a" của đề bài là 1 đơn vị (a = 1). MỌI tọa độ dùng đơn vị này.
   - Đáy nằm trên mặt phẳng y = 0 (XZ).
   - Trục Y hướng lên trên (chiều cao của hình chóp / lăng trụ).

A2. ĐẶT TÊN ĐIỂM:
   - Tên điểm phải là 1 KÝ TỰ DUY NHẤT (có thể kèm dấu phẩy upper như A',
     B', C', D'). VD: "A", "B", "S", "M", "O", "G", "H", "A'".
   - TUYỆT ĐỐI KHÔNG dùng tên dài kiểu "M_AB", "M_BC", "Mab", "trungdiem"...
   - Khi cần điểm phụ, chọn 1 ký tự CHƯA xuất hiện theo thứ tự ưu tiên:
     M, N, P, Q, K, I, J, T, U, V (sau khi A,B,C,D,S,O,G,H đã dùng).

B. CHỈ VẼ NHỮNG GÌ ĐỀ BÀI CHO TRỰC TIẾP:
   - KHÔNG tự thêm điểm phụ trợ (trung điểm cạnh khác, hình chiếu...) khi đề
     không yêu cầu. Những thứ cần dựng thêm khi giải toán không thuộc bước vẽ.
   - KHÔNG tự gán độ dài cho cạnh nếu đề không cho. VD: đề chỉ nói "SA vuông
     góc đáy" mà không cho SA = bao nhiêu thì cạnh SA KHÔNG có drawEdge.opts.label.

C. NHÃN ĐỘ DÀI (drawEdge.opts.label):
   - Chỉ gắn cho cạnh đại diện khi đề thực sự cho biết độ dài.
   - Hình vuông cạnh a → CHỈ gắn label "a" cho 1 cạnh (VD: A-B). Các cạnh còn
     lại không gắn nữa (vì hình vuông nhìn là biết bằng nhau).
   - Tam giác có cạnh khác nhau → gắn label cho từng cạnh có dữ liệu.
   - "Khoảng cách giữa BC và SM = a√3/4" → KHÔNG gắn label lên cạnh nào, chỉ
     storeData với type="distance".

D. KÝ HIỆU GÓC VUÔNG (drawRightAngle):
   - Hình vuông đáy → CHỈ vẽ 1 ký hiệu tại 1 đỉnh đại diện (VD: A giữa A-B
     và A-D). KHÔNG vẽ cả 4 đỉnh.
   - "SA ⊥ đáy" → vẽ 1 ký hiệu tại A giữa S-A và A-B (hoặc A-D).
   - Tam giác vuông tại B → 1 ký hiệu tại B giữa B-A và B-C.

E. KÝ HIỆU TRUNG ĐIỂM (drawEqualMark):
   - "M là trung điểm CD" → 2 lệnh drawEqualMark cho C-M và M-D, mark="double".
   - KHÔNG dùng "single" cho trung điểm vì trùng với ký hiệu cạnh đáy bằng nhau.

F. KÝ HIỆU CẠNH BẰNG NHAU (drawEqualMark mark="single"):
   - CHỈ dùng khi đề nói rõ "AB = BC" hoặc "tam giác đều"/"tam giác cân"...
   - TAM GIÁC ĐỀU cạnh a:
     • Khi hình ĐƠN GIẢN (chỉ có tam giác): ký hiệu 3 cạnh ở đáy ABC.
     • Khi hình PHỨC TẠP (có thêm trung tuyến / trọng tâm / hình chiếu...
       làm đáy ABC bị nhiều ký hiệu chồng chéo): ĐẶT 3 KÝ HIỆU "single"
       LÊN ĐÁY TRÊN (A'B'C') để mặt đáy dưới đỡ rối. Đáy 2 đáy bằng nhau
       nên chỉ cần ký hiệu 1 nơi.
   - TAM GIÁC CÂN tại A (AB = AC) → drawEqualMark mark="single" cho A-B và A-C.
   - Hình thoi → 4 cạnh đều có drawEqualMark mark="single".
   - Hình vuông không cần (nhìn là biết).
   - Trong lăng trụ có 2 đáy bằng nhau, CHỈ ký hiệu ở MỘT đáy (chọn đáy nào
     ít ký hiệu hơn để dễ nhìn).

F2. LĂNG TRỤ (phân biệt đứng và xiên): * Quan trọng nhớ kĩ
   - "Lăng trụ ĐỨNG ABC.A'B'C'" → đáy trên trùng vị trí XZ với đáy dưới,
     chỉ khác y. Tức A' ở trên đỉnh A, B' ở trên B, C' ở trên C.
     PHẢI có drawRightAngle tại A giữa A-A' và A-B (hoặc tương tự),
     vì cạnh bên vuông góc đáy.
   - "Lăng trụ" KHÔNG có chữ "đứng" → mặc định LĂNG TRỤ XIÊN.
     Đáy trên dịch ngang so với đáy dưới (VD: A' = A + offset_x ≈ 0.35,
     offset_z ≈ 0.20). KHÔNG vẽ ký hiệu vuông góc cho cạnh bên.
   - "Lăng trụ đều" = lăng trụ đứng có đáy đa giác đều → vẫn áp quy tắc đứng.
   - Nhận diện: chỉ cần xuất hiện cụm "lăng trụ đứng" trong đề là coi là đứng.

F3. TÂM ĐÁY (O hoặc bất kỳ tên nào):
   - Khi đề có "O là tâm đáy", "O là tâm hình vuông ABCD", "O = AC ∩ BD"...
     PHẢI vẽ HAI ĐƯỜNG CHÉO TRƯỚC để hiển thị cách xác định tâm:
        drawEdge A-C với opts={ "style": "dashed", "color": "#888888" }
        drawEdge B-D với opts={ "style": "dashed", "color": "#888888" }
     RỒI MỚI drawPoint O tại giao điểm 2 đường chéo.
   - Với tam giác (tâm trọng tâm G): vẽ 2 trung tuyến dạng dashed rồi mới drawPoint G.
   - Mặt phẳng tâm tròn → vẽ đường kính dashed rồi tâm.
   - Đường chéo dùng style "dashed" + color "#888888" để phân biệt với cạnh thật.

F4. TRỌNG TÂM TAM GIÁC (G):
   "G là trọng tâm tam giác ABC" → trọng tâm = giao điểm 3 đường trung tuyến.
   PHẢI thực hiện đúng các bước sau, theo đúng thứ tự:
   1) Tính tọa độ trung điểm 3 cạnh: Mab = (A+B)/2, Mbc = (B+C)/2, Mca = (C+A)/2.
   2) drawPoint cho 2 trung điểm cần thiết với tên 1 KÝ TỰ DUY NHẤT chưa
      xuất hiện (VD: dùng "M", "N", "P", "Q", "K"... thay vì "M_BC", "M_CA").
   3) Vẽ 2 trung tuyến dạng dashed/gray (đủ xác định G):
        drawEdge A-M  style="dashed" color="#888888"   (M là trung điểm BC)
        drawEdge B-N  style="dashed" color="#888888"   (N là trung điểm CA)
   4) drawEqualMark cho các đoạn bằng nhau ở mỗi cạnh có trung điểm.
      QUY ƯỚC QUAN TRỌNG VỀ TICK:
      - Nếu đáy là TAM GIÁC ĐỀU (tất cả các cạnh đều bằng nhau, các nửa
        trung tuyến cũng bằng nhau với cùng độ dài a/2):
        DÙNG CHUNG mark="single" cho TẤT CẢ — cả cạnh đáy + các nửa
        cạnh do trung điểm chia ra. Vì cạnh đều = 2 nửa cạnh đều = chung
        1 lớp ký hiệu.
        VD: drawEqualMark B-M mark="single", drawEqualMark M-C mark="single",
            drawEqualMark C-N mark="single", drawEqualMark N-A mark="single".
      - Nếu đáy KHÔNG đều (tam giác thường, hình chữ nhật...):
        DÙNG mark khác nhau cho từng cặp:
            drawEqualMark B-M mark="double",  drawEqualMark M-C mark="double"
            drawEqualMark C-N mark="triple",  drawEqualMark N-A mark="triple"
        → Để phân biệt CM = MD vs cạnh khác.
   5) Nếu đáy là TAM GIÁC ĐỀU thì trung tuyến cũng là đường cao →
      BẮT BUỘC drawRightAngle tại trung điểm M giữa edge A-M và B-C.
      Tương tự: drawRightAngle tại N giữa B-N và C-A (nếu vẽ trung tuyến từ B).
   6) drawPoint G tại tọa độ ((Ax+Bx+Cx)/3, (Ay+By+Cy)/3, (Az+Bz+Cz)/3).
   - KHÔNG vẽ G mà thiếu các trung tuyến trước đó. Học sinh cần thấy cách xác định.

F5. HÌNH CHIẾU VUÔNG GÓC (X' là hình chiếu của X lên mặt phẳng P):
   "Hình chiếu vuông góc của A' lên mặt phẳng (ABC) là điểm H/G/O..."
   QUY TRÌNH BẮT BUỘC, KHÔNG ĐƯỢC BỎ BƯỚC NÀO:
   1) Xác định điểm chiếu H (hoặc trùng với điểm có sẵn như G, O, trung điểm M...)
      NẰM TRÊN mặt phẳng đáy. Tọa độ H có y = 0 nếu đáy là mp y=0.
   2) Tọa độ X (đỉnh được chiếu) phải có:
        x = H.x, z = H.z (nằm thẳng đứng phía trên H)
        y = chiều cao của X (giả định = 1 nếu đề không cho)
   3) drawPoint cho H trước (nếu chưa có). Nếu H trùng G/O đã vẽ thì bỏ qua.
   4) drawPoint cho X.
   5) drawEdge X-H với opts = { "style": "dashed", "color": "#2a7a62" }
      → đường vuông góc thể hiện chiều cao thực sự của khối.
   6) BẮT BUỘC drawRightAngle tại H để thể hiện X-H ⊥ đáy. KHÔNG được bỏ.
      Cách chọn 2 cạnh:
      - Nếu H là 1 đỉnh đáy (VD H = A): drawRightAngle vertex="A"
        edge1="X-A" edge2="A-B" (hoặc cạnh đáy bất kỳ qua A).
      - Nếu H là trung điểm cạnh đáy: drawRightAngle vertex="H"
        edge1="X-H" edge2 = cạnh đáy đi qua H.
      - Nếu H nằm trong miền tam giác (như trọng tâm G):
        chọn 1 đường phụ đã vẽ đi qua H (VD trung tuyến A-M qua G):
        drawRightAngle vertex="G" edge1="A'-G" edge2="A-M".
        (Hoặc edge2 = "G-M" nếu A-M không trùng tên).

F6. TRỰC TÂM TAM GIÁC (H_truc):
   "H là trực tâm tam giác ABC" → trực tâm = giao điểm 3 đường cao.
   - Vẽ 2-3 đường cao dạng dashed/gray:
        drawEdge A-foot_a style="dashed" color="#888888"  (foot_a là chân đường cao từ A xuống BC)
   - Sau đó drawPoint H_truc tại giao điểm.
   Lưu ý: tính toán chân đường cao phức tạp, nếu đề chỉ ám chỉ chung chung,
   có thể bỏ qua việc vẽ đường cao chính xác — chỉ cần drawPoint H ở vị trí trực tâm.

F7. TÂM ĐƯỜNG TRÒN NGOẠI TIẾP (I):
   "I là tâm đường tròn ngoại tiếp ABC" → giao điểm 3 đường trung trực.
   - Tam giác đều: trùng với trọng tâm → áp dụng F4.
   - Tam giác vuông: trùng với trung điểm cạnh huyền.
   - Trường hợp khác: drawPoint I, bỏ qua đường trung trực nếu phức tạp.

G. THÔNG TIN KHÔNG VẼ (khoảng cách, góc giữa, thể tích...):
   - "Khoảng cách giữa X và Y = ...", "Góc giữa X và Y = ...", "Thể tích = ..."
     → KHÔNG cần xử lý gì cả. Dữ liệu này đã có sẵn trong DULIEUHINHHOC
       (cột cacQuanHe / given_conditions từ bước upload-and-save).
   - Tuyệt đối KHÔNG gắn nhãn lên cạnh cho các phát biểu này.

H. VẼ MẶT (drawFace) - QUY TẮC TÔ MÀU:
   - CHỈ vẽ các mặt BAO BỌC HÌNH (mặt ngoài cùng tạo nên khối kín).
     Hình chóp S.ABCD → 5 mặt: 1 đáy ABCD + 4 mặt bên SAB, SBC, SCD, SDA.
     Lăng trụ ABC.A'B'C' → 5 mặt: 2 đáy + 3 mặt bên.
     Lập phương ABCD.A'B'C'D' → 6 mặt.
     Tứ diện ABCD → 4 mặt.
   - MỖI MẶT CHỈ VẼ 1 LẦN. Không vẽ ABCD rồi vẽ thêm DCBA, không vẽ mặt
     không tồn tại như mặt cắt khi đề không yêu cầu.
   - KHÔNG vẽ mặt phụ trợ chứa điểm trung gian (VD: SAM, SCM khi đề chỉ
     có S.ABCD và M là trung điểm CD). Mặt phụ chỉ vẽ khi đề bài hoặc
     câu hỏi nói tới mặt phẳng đó.
   - TẤT CẢ mặt dùng CÙNG opts để màu sắc đồng nhất, tránh hiện tượng
     mặt này đậm hơn mặt kia gây bóng giả:
        opacity: 0.12
        color:   "#3d52a0"   (xanh chàm — dùng cho MỌI mặt, kể cả đáy)

I. THỨ TỰ LỆNH (mỗi lệnh là 1 bước vẽ):
   1) drawPoint cho TẤT CẢ điểm đáy (theo thứ tự A, B, C, D...)
   2) drawEdge cho các cạnh đáy
   3) drawRightAngle cho 1 góc đại diện ở đáy (nếu có)
   4) NẾU đề có TÂM/TRỌNG TÂM/TRỰC TÂM ở đáy → vẽ các đường phụ dashed
      (đường chéo / trung tuyến / đường cao) TRƯỚC, RỒI drawPoint tâm.
      (Áp dụng quy tắc F3, F4, F6, F7).
   5) drawPoint cho đỉnh trên (S, A', B'...) sau khi đã có đáy.
      - Lăng trụ ĐỨNG: A' thẳng đứng trên A, ...
      - Lăng trụ XIÊN: A' = A + offset (offset_x ≈ 0.35, offset_z ≈ 0.20).
      - NẾU đề nói "hình chiếu vuông góc của A' lên đáy là H/G/O..." →
        đặt A' thẳng đứng trên điểm H đó (A'.x = H.x, A'.z = H.z, A'.y = chiều cao).
        ÁP DỤNG quy tắc F5.
   6) drawEdge cho cạnh đứng / cạnh bên
   7) drawRightAngle cho ⊥ với đáy:
      - Hình chóp có "SA ⊥ đáy" → bắt buộc.
      - Lăng trụ ĐỨNG → bắt buộc tại 1 đỉnh đáy.
      - Lăng trụ XIÊN → KHÔNG vẽ (cạnh bên không vuông góc đáy).
      - "Hình chiếu A' lên đáy là H" → vẽ drawEdge A'-H dashed/teal +
        drawRightAngle tại H (nếu H trùng đỉnh đáy/cạnh đáy).
   8) drawPoint điểm đặc biệt khác (M trung điểm, ...) + drawEqualMark nếu cần.
   9) drawEdge các cạnh phụ liên quan đến điểm đặc biệt
   10) drawFace các mặt bao bọc hình (mỗi mặt 1 lệnh, cùng opts)
   11) setCamera

J. KHÔNG dùng LaTeX trong nhãn. Dùng Unicode: a, a√2, a√3/4, 2a, ²...
"""

RENDER_3D_EXAMPLE = """
## VÍ DỤ ĐẦY ĐỦ:

Đề: "Cho hình chóp S.ABCD có đáy ABCD là hình vuông cạnh a, SA vuông góc với
mặt phẳng đáy. Gọi M là trung điểm của CD. Biết khoảng cách giữa hai đường
thẳng BC và SM bằng a√3/4."

Output (JSON, KHÔNG có markdown bao quanh):
[
  { "fn": "drawPoint", "args": { "name": "A", "x": 0, "y": 0, "z": 0 } },
  { "fn": "drawPoint", "args": { "name": "B", "x": 1, "y": 0, "z": 0 } },
  { "fn": "drawPoint", "args": { "name": "C", "x": 1, "y": 0, "z": 1 } },
  { "fn": "drawPoint", "args": { "name": "D", "x": 0, "y": 0, "z": 1 } },
  { "fn": "drawEdge",  "args": { "from": "A", "to": "B", "opts": { "label": "a" } } },
  { "fn": "drawEdge",  "args": { "from": "B", "to": "C" } },
  { "fn": "drawEdge",  "args": { "from": "C", "to": "D" } },
  { "fn": "drawEdge",  "args": { "from": "D", "to": "A" } },
  { "fn": "drawRightAngle", "args": { "vertex": "A", "edge1": "A-B", "edge2": "A-D" } },
  { "fn": "drawPoint", "args": { "name": "S", "x": 0, "y": 1, "z": 0 } },
  { "fn": "drawEdge",  "args": { "from": "S", "to": "A", "opts": { "color": "#2a7a62" } } },
  { "fn": "drawRightAngle", "args": { "vertex": "A", "edge1": "S-A", "edge2": "A-B" } },
  { "fn": "drawEdge",  "args": { "from": "S", "to": "B" } },
  { "fn": "drawEdge",  "args": { "from": "S", "to": "C" } },
  { "fn": "drawEdge",  "args": { "from": "S", "to": "D" } },
  { "fn": "drawPoint", "args": { "name": "M", "x": 0.5, "y": 0, "z": 1 } },
  { "fn": "drawEqualMark", "args": { "from": "C", "to": "M", "mark": "double" } },
  { "fn": "drawEqualMark", "args": { "from": "M", "to": "D", "mark": "double" } },
  { "fn": "drawEdge",  "args": { "from": "S", "to": "M", "opts": { "color": "#a07840" } } },
  { "fn": "drawFace",  "args": { "points": ["A","B","C","D"], "opts": { "opacity": 0.12, "color": "#3d52a0" } } },
  { "fn": "drawFace",  "args": { "points": ["S","A","B"],     "opts": { "opacity": 0.12, "color": "#3d52a0" } } },
  { "fn": "drawFace",  "args": { "points": ["S","B","C"],     "opts": { "opacity": 0.12, "color": "#3d52a0" } } },
  { "fn": "drawFace",  "args": { "points": ["S","C","D"],     "opts": { "opacity": 0.12, "color": "#3d52a0" } } },
  { "fn": "drawFace",  "args": { "points": ["S","D","A"],     "opts": { "opacity": 0.12, "color": "#3d52a0" } } },
  { "fn": "setCamera", "args": { "x": 2.5, "y": 2, "z": 2.5, "lx": 0.5, "ly": 0.5, "lz": 0.5 } }
]

## Bạn có thể tham khảo VÍ DỤ 2 nhưng không được lạm dụng, phải đọc đề mà vẽ đứng hay xiên(lăng trụ xiên + trọng tâm + hình chiếu vuông góc):

Đề: "Cho hình lăng trụ ABC.A'B'C' có đáy là tam giác đều cạnh a. Hình chiếu
vuông góc của A' lên (ABC) trùng với trọng tâm tam giác ABC. Biết khoảng cách
giữa AA' và BC bằng a√3/4."

Phân tích:
- Đáy ABC tam giác đều cạnh a → A=(0,0,0), B=(1,0,0), C=(0.5, 0, √3/2 ≈ 0.866).
- Trọng tâm G = ((0+1+0.5)/3, 0, (0+0+0.866)/3) = (0.5, 0, 0.289).
- Đề KHÔNG nói "đứng" → lăng trụ XIÊN. A' nằm thẳng đứng trên G:
    A' = (0.5, 1, 0.289).  Cạnh bên AA' xiên.
- B' = B + (A'-A) = (1.5, 1, 0.289).
- C' = C + (A'-A) = (1, 1, 1.155).
- Trung điểm M của BC = (0.75, 0, 0.433); trung điểm N của CA = (0.25, 0, 0.433).

Output:
[
  { "fn": "drawPoint", "args": { "name": "A", "x": 0,   "y": 0, "z": 0 } },
  { "fn": "drawPoint", "args": { "name": "B", "x": 1,   "y": 0, "z": 0 } },
  { "fn": "drawPoint", "args": { "name": "C", "x": 0.5, "y": 0, "z": 0.866 } },
  { "fn": "drawEdge",  "args": { "from": "A", "to": "B", "opts": { "label": "a" } } },
  { "fn": "drawEdge",  "args": { "from": "B", "to": "C" } },
  { "fn": "drawEdge",  "args": { "from": "C", "to": "A" } },

  // Trọng tâm G: vẽ 2 trung tuyến dashed/gray TRƯỚC, đặt tên trung điểm
  // bằng 1 ký tự (M, N) chưa dùng. RỒI mới drawPoint G.
  { "fn": "drawPoint", "args": { "name": "M", "x": 0.75, "y": 0, "z": 0.433 } },
  { "fn": "drawEdge",  "args": { "from": "A", "to": "M", "opts": { "style": "dashed", "color": "#888888" } } },
  // Tam giác đều → các nửa cạnh BM = MC bằng nhau VÀ bằng các cạnh khác sau khi chia.
  // DÙNG CHUNG "single" cho TẤT CẢ tick ở đáy (không phân biệt double/triple).
  { "fn": "drawEqualMark", "args": { "from": "B", "to": "M", "mark": "single" } },
  { "fn": "drawEqualMark", "args": { "from": "M", "to": "C", "mark": "single" } },
  // Tam giác đều → trung tuyến A-M cũng là đường cao → vuông góc với BC tại M
  { "fn": "drawRightAngle", "args": { "vertex": "M", "edge1": "A-M", "edge2": "B-C" } },

  { "fn": "drawPoint", "args": { "name": "N", "x": 0.25, "y": 0, "z": 0.433 } },
  { "fn": "drawEdge",  "args": { "from": "B", "to": "N", "opts": { "style": "dashed", "color": "#888888" } } },
  { "fn": "drawEqualMark", "args": { "from": "C", "to": "N", "mark": "single" } },
  { "fn": "drawEqualMark", "args": { "from": "N", "to": "A", "mark": "single" } },
  { "fn": "drawRightAngle", "args": { "vertex": "N", "edge1": "B-N", "edge2": "C-A" } },

  // G = giao của 2 trung tuyến (cũng là trọng tâm)
  { "fn": "drawPoint", "args": { "name": "G", "x": 0.5, "y": 0, "z": 0.289 } },

  // A' nằm thẳng đứng trên G (vì hình chiếu A' lên đáy = G).
  { "fn": "drawPoint", "args": { "name": "A'", "x": 0.5, "y": 1, "z": 0.289 } },
  // Đường vuông góc A'-G dashed/teal
  { "fn": "drawEdge",  "args": { "from": "A'", "to": "G", "opts": { "style": "dashed", "color": "#2a7a62" } } },
  // BẮT BUỘC drawRightAngle tại G giữa A'-G và trung tuyến A-M (đi qua G).
  // Đây là ký hiệu hình chiếu vuông góc của A' lên đáy.
  { "fn": "drawRightAngle", "args": { "vertex": "G", "edge1": "A'-G", "edge2": "A-M" } },

  { "fn": "drawPoint", "args": { "name": "B'", "x": 1.5, "y": 1, "z": 0.289 } },
  { "fn": "drawPoint", "args": { "name": "C'", "x": 1,   "y": 1, "z": 1.155 } },

  // Cạnh bên (xiên) — KHÔNG drawRightAngle vì lăng trụ xiên.
  { "fn": "drawEdge",  "args": { "from": "A", "to": "A'" } },
  { "fn": "drawEdge",  "args": { "from": "B", "to": "B'" } },
  { "fn": "drawEdge",  "args": { "from": "C", "to": "C'" } },

  // Cạnh đáy trên
  { "fn": "drawEdge",  "args": { "from": "A'", "to": "B'" } },
  { "fn": "drawEdge",  "args": { "from": "B'", "to": "C'" } },
  { "fn": "drawEdge",  "args": { "from": "C'", "to": "A'" } },

  // Tam giác đều → 3 cạnh bằng nhau. Đặt ký hiệu Ở ĐÁY TRÊN (A'B'C')
  // vì đáy dưới đã có nhiều ký hiệu của trung tuyến / trọng tâm rồi.
  { "fn": "drawEqualMark", "args": { "from": "A'", "to": "B'", "mark": "double" } },
  { "fn": "drawEqualMark", "args": { "from": "B'", "to": "C'", "mark": "double" } },
  { "fn": "drawEqualMark", "args": { "from": "C'", "to": "A'", "mark": "double" } },

  // Mặt
  { "fn": "drawFace",  "args": { "points": ["A","B","C"],       "opts": { "opacity": 0.12, "color": "#3d52a0" } } },
  { "fn": "drawFace",  "args": { "points": ["A'","B'","C'"],    "opts": { "opacity": 0.12, "color": "#3d52a0" } } },
  { "fn": "drawFace",  "args": { "points": ["A","B","B'","A'"], "opts": { "opacity": 0.12, "color": "#3d52a0" } } },
  { "fn": "drawFace",  "args": { "points": ["B","C","C'","B'"], "opts": { "opacity": 0.12, "color": "#3d52a0" } } },
  { "fn": "drawFace",  "args": { "points": ["C","A","A'","C'"], "opts": { "opacity": 0.12, "color": "#3d52a0" } } },

  { "fn": "setCamera", "args": { "x": 2.5, "y": 2, "z": 2.5, "lx": 0.5, "ly": 0.5, "lz": 0.5 } }
]
"""

def build_render_3d_prompt(problem_text: str) -> str:
    """Prompt yêu cầu Gemini sinh mảng lệnh vẽ Three.js cho 1 bài toán."""
    return f"""{RENDER_3D_SYSTEM}

{RENDER_3D_API}

{RENDER_3D_RULES}

{RENDER_3D_EXAMPLE}

## ĐỀ BÀI:
{problem_text}

## YÊU CẦU:
- Trả về DUY NHẤT 1 mảng JSON các lệnh vẽ. KHÔNG bao quanh bằng ```json``` hay markdown.
- KHÔNG kèm giải thích, chỉ JSON.
- Mọi tọa độ tính theo a = 1.
- Tuân thủ tuyệt đối quy tắc B (chỉ vẽ cái đề cho).
- Bỏ qua các phát biểu khoảng cách / góc giữa / thể tích — đã có sẵn trong DULIEUHINHHOC.
"""
