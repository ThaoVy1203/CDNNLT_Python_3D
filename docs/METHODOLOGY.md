# Phương Pháp Luận - 3D Geometry Problem Solving System

## 📚 Tổng Quan Giải Pháp

Hệ thống giải toán hình học 3D từ ảnh sử dụng **phương pháp kết hợp AI và thuật toán hình học** để chuyển đổi bài toán từ ảnh sang mô hình 3D tương tác và lời giải chi tiết.

---

## 🎯 Phương Pháp Luận Chính

### **1. AI-Driven Extraction (Trích Xuất Dữ Liệu Bằng AI)**

#### **Mục tiêu:**
Chuyển đổi ảnh bài toán thành dữ liệu có cấu trúc (structured data)

#### **Công nghệ:**
- **Google Gemini AI** (Vision + Language Model)
- **OCR + Semantic Understanding**

#### **Quy trình:**

```
Ảnh đề bài
    ↓
[Gemini Vision API]
    ↓
Prompt Engineering (Structured Extraction)
    ↓
JSON Output:
  - problem_text: Đề bài dạng text
  - problem_type: Loại hình (chóp, lăng trụ, tứ diện...)
  - given_conditions: Điều kiện cho trước
  - questions: Câu hỏi cần giải
  - points: Danh sách điểm
  - relationships: Quan hệ hình học
```

#### **Kỹ thuật Prompt Engineering:**

**a) Structured Output Prompting:**
```python
EXTRACTION_PROMPT = """
Trích xuất các thông tin sau từ bài toán hình học:
1. problem_text: Nội dung đầy đủ
2. problem_type: Loại hình học
3. given_conditions: Điều kiện cho trước
4. questions: Câu hỏi cần giải
5. points: Danh sách điểm với tọa độ
6. relationships: Quan hệ hình học

Trả về JSON với cấu trúc trên.
"""
```

**b) Few-Shot Learning:**
- Cung cấp 2-3 ví dụ mẫu trong prompt
- Hướng dẫn AI format output đúng chuẩn

**c) Constraint Specification:**
- Không dùng LaTeX trong JSON
- Dùng Unicode: √, ², ³, ⊥, ∥
- Format số rõ ràng: "a√3/4" thay vì "\frac{a\sqrt{3}}{4}"

#### **Xử lý lỗi AI:**

```python
# 1. Parse JSON từ markdown code blocks
if "```json" in response_text:
    json_str = response_text.split("```json")[1].split("```")[0]

# 2. Fix LaTeX escapes
json_str = re.sub(r'\\frac\{([^}]+)\}\{([^}]+)\}', r'(\1)/(\2)', json_str)
json_str = re.sub(r'\\sqrt\{([^}]+)\}', r'√\1', json_str)

# 3. Fix biến 'a' → số
json_str = re.sub(r'\ba/2\b', '0.5', json_str)
json_str = re.sub(r':\s*\[a,', ': [1.0,', json_str)

# 4. Fix incomplete JSON
if open_braces > close_braces:
    json_str += '}' * (open_braces - close_braces)
```

---

### **2. Constraint-Based Geometry Solving (Giải Hình Học Dựa Trên Ràng Buộc)**

#### **Mục tiêu:**
Tính toán tọa độ 3D chính xác từ điều kiện hình học

#### **Phương pháp:**

**a) Pattern Recognition (Nhận Dạng Mẫu):**
```python
def _detect_shape_type(extraction_data, problem_type):
    """
    Phát hiện loại hình từ:
    1. problem_type từ AI
    2. Keywords trong problem_text
    3. Số lượng điểm và quan hệ
    """
    if "tứ diện" in text or "tetrahedron" in text:
        return "tetrahedron"
    elif "chóp" in text or "pyramid" in text:
        return "pyramid"
    # ...
```

**b) Constraint Extraction (Trích Xuất Ràng Buộc):**
```python
def _extract_constraints_from_gemini(extraction_data, shape_type):
    """
    Parse điều kiện từ given_conditions:
    - Base type: hình vuông, tam giác đều, tam giác vuông
    - Dimensions: AB = 3, SA = 6
    - Special points: M là trung điểm AB
    - Relationships: SA ⊥ (ABC)
    """
    constraints = {
        "base": {"type": "square", "side": 3.0},
        "apex": {"height": 6.0, "perpendicular_to_base": True},
        "special_points": {"M": {"type": "midpoint", "of": "AB"}}
    }
    return constraints
```

**c) Coordinate Calculation (Tính Toán Tọa Độ):**

**Hệ tọa độ chuẩn:**
- Mặt đáy nằm trên mặt phẳng XZ (y = 0)
- Trục Y hướng lên (chiều cao)
- Gốc tọa độ tại điểm A

**Ví dụ: Hình chóp S.ABCD đáy vuông:**
```python
def _solve_pyramid(constraints):
    a = constraints["base"]["side"]  # Cạnh đáy
    h = constraints["apex"]["height"]  # Chiều cao
    
    # Tọa độ đáy ABCD (hình vuông trên mặt phẳng y=0)
    points = {
        "A": [0, 0, 0],
        "B": [a, 0, 0],
        "C": [a, 0, a],
        "D": [0, 0, a],
        "S": [0, h, 0]  # Đỉnh ở trên A (nếu SA ⊥ đáy)
    }
    
    # Thêm điểm đặc biệt
    if "M" in special_points and M là trung điểm AB:
        points["M"] = [(A[0] + B[0])/2, (A[1] + B[1])/2, (A[2] + B[2])/2]
    
    return points
```

**d) Edge Classification (Phân Loại Cạnh):**

**Quy tắc vẽ:**
- **Nét liền (solid)**: Cạnh thật của hình (nhìn thấy)
- **Nét đứt (dashed)**: Cạnh bị che khuất hoặc đường phụ

```python
# Cạnh hình (nét liền)
base_edges = [("A", "B"), ("B", "C"), ("C", "D"), ("D", "A")]
lateral_edges = [("S", "A"), ("S", "B"), ("S", "C"), ("S", "D")]

# Đường phụ (nét đứt)
auxiliary_lines = [("A", "C"), ("B", "D")]  # Đường chéo đáy
if "M" in points:
    auxiliary_lines.append(("S", "M"))  # Đường từ đỉnh đến trung điểm
```

---

### **3. 3D Visualization Pipeline (Quy Trình Hiển Thị 3D)**

#### **Mục tiêu:**
Chuyển đổi dữ liệu hình học sang định dạng Three.js

#### **Quy trình:**

```
Geometry Data (points, edges, faces)
    ↓
[GeometryRenderer]
    ↓
Transform to 3D JSON:
  - points: {A: [0,0,0], B: [1,0,0], ...}
  - edges: [{start: "A", end: "B", style: "solid"}, ...]
  - faces: [{vertices: ["A","B","C"], color: "#fff"}, ...]
  - camera_position: [5, 5, 5]
    ↓
[React Three Fiber]
    ↓
Interactive 3D Model
```

#### **Kỹ thuật:**

**a) Coordinate Transformation:**
```python
def transform_to_3d(geometry_data):
    # 1. Transform points
    points_3d = {name: coords for name, coords in points}
    
    # 2. Transform edges
    edges_3d = [
        {
            "start": p1,
            "end": p2,
            "start_coords": points[p1],
            "end_coords": points[p2],
            "style": "solid" | "dashed"
        }
    ]
    
    # 3. Generate faces (optional)
    faces_3d = [
        {
            "vertices": ["A", "B", "C"],
            "coordinates": [points["A"], points["B"], points["C"]]
        }
    ]
    
    return {points_3d, edges_3d, faces_3d, camera_position}
```

**b) Camera Positioning:**
```python
def _calculate_camera_position(points):
    # Tính bounding box
    min_x, max_x = min(p[0]), max(p[0])
    min_y, max_y = min(p[1]), max(p[1])
    min_z, max_z = min(p[2]), max(p[2])
    
    # Center
    center = [(min_x + max_x)/2, (min_y + max_y)/2, (min_z + max_z)/2]
    
    # Distance = 2 * max_dimension
    size = max(max_x - min_x, max_y - min_y, max_z - min_z)
    distance = size * 2
    
    # Camera ở góc 45° so với các trục
    return [center[0] + distance, center[1] + distance, center[2] + distance]
```

---

### **4. AI-Powered Problem Solving (Giải Toán Bằng AI)**

#### **Mục tiêu:**
Tạo lời giải chi tiết từng bước với công thức LaTeX

#### **Phương pháp:**

**a) Prompt Engineering cho Giải Toán:**
```python
def build_solve_prompt(problem_text):
    return f"""
Giải bài toán hình học sau:

{problem_text}

Yêu cầu:
1. Phân tích đề bài
2. Xác định công thức cần dùng
3. Tính toán từng bước
4. Trả về JSON:
{{
  "steps": ["Bước 1: ...", "Bước 2: ...", ...],
  "result": "Kết quả cuối cùng",
  "formulas_used": ["V = (1/3) * S * h", ...]
}}

Dùng LaTeX cho công thức: $V = \\frac{{1}}{{3}} S h$
"""
```

**b) LaTeX Processing:**
```python
# Fix LaTeX escapes trong JSON
json_str = re.sub(r'(?<!\\)\\(?!["\\/bfnrtu])', r'\\\\', json_str)

# Parse JSON
solution = json.loads(json_str)

# Frontend render LaTeX với KaTeX/MathJax
```

---

### **5. Caching Strategy (Chiến Lược Cache)**

#### **Mục tiêu:**
Tối ưu hiệu năng, giảm chi phí API

#### **Phương pháp:**

**a) Database Caching:**
```python
# Bước 1: Upload → Lưu BAITOAN + DULIEUHINHHOC
ma_bai_toan = bai_toan_repo.create(...)
du_lieu_id = du_lieu_repo.create(...)

# Bước 2: Render 3D → Check cache
existing_3d = dung_hinh_repo.get_by_bai_toan(ma_bai_toan)
if existing_3d:
    return {"fromCache": True, "data": existing_3d}
else:
    # Generate mới và lưu
    geometry = solver.solve(...)
    dung_hinh_repo.create(geometry)

# Bước 3: Solve → Check cache
existing_solution = loi_giai_repo.get_by_bai_toan(ma_bai_toan)
if existing_solution:
    return {"fromCache": True, "solution": existing_solution}
```

**b) Cache Invalidation:**
- Không có invalidation (immutable data)
- Mỗi bài toán mới = record mới
- Guest user: Không lưu cache (maNguoiDung = NULL)

---

### **6. Error Handling & Fallback (Xử Lý Lỗi & Dự Phòng)**

#### **Chiến lược:**

**a) AI Service Errors:**
```python
try:
    extraction = await gemini_service.analyze_image(image)
except Exception as e:
    if "503" in str(e) or "UNAVAILABLE" in str(e):
        raise HTTPException(503, "AI đang quá tải. Thử lại sau 1-2 phút")
    elif "429" in str(e):
        raise HTTPException(429, "Vượt quá giới hạn API. Đợi vài phút")
    else:
        raise HTTPException(500, f"Lỗi phân tích ảnh: {e}")
```

**b) Geometry Solver Fallback:**
```python
try:
    result = self.solve_from_extraction(extraction_data, problem_type)
except Exception as e:
    print(f"❌ Error: {e}")
    # Fallback: Trả về hình chóp mặc định
    return self._solve_pyramid({
        "base": {"type": "square", "side": 1.0},
        "apex": {"height": 1.414, "perpendicular_to_base": True}
    })
```

**c) JSON Parsing Fallback:**
```python
try:
    solution = json.loads(json_str)
except json.JSONDecodeError:
    # Fallback: Lời giải đơn giản
    solution = {
        "steps": ["Bước 1: Phân tích đề bài", ...],
        "result": "Vui lòng xem lại đề bài",
        "formulas_used": []
    }
```

---

## 🏗️ Kiến Trúc Tổng Thể

### **Layered Architecture:**

```
┌─────────────────────────────────────────────┐
│         Presentation Layer                   │
│  - React Frontend                            │
│  - Three.js Visualization                    │
│  - User Interface                            │
└──────────────┬──────────────────────────────┘
               │ HTTP/REST API
┌──────────────▼──────────────────────────────┐
│         API Layer (FastAPI)                  │
│  - Routes: geometry, auth, users             │
│  - Request validation                        │
│  - Response formatting                       │
└──────────────┬──────────────────────────────┘
               │
┌──────────────▼──────────────────────────────┐
│         Service Layer                        │
│  - GeminiService: AI integration             │
│  - GeometrySolver: Coordinate calculation    │
│  - GeometryRenderer: 3D transformation       │
└──────────────┬──────────────────────────────┘
               │
┌──────────────▼──────────────────────────────┐
│         Repository Layer                     │
│  - BaiToanRepository                         │
│  - DuLieuHinhHocRepository                   │
│  - LoiGiaiRepository                         │
│  - DungHinh3DRepository                      │
└──────────────┬──────────────────────────────┘
               │
┌──────────────▼──────────────────────────────┐
│         Data Layer                           │
│  - SQL Server Database                       │
│  - Tables: BAITOAN, DULIEUHINHHOC, ...       │
└─────────────────────────────────────────────┘

External Services:
┌─────────────────────────────────────────────┐
│         Gemini AI API                        │
│  - Vision API: Image analysis                │
│  - Language API: Problem solving             │
└─────────────────────────────────────────────┘
```

---

## 🔬 Các Kỹ Thuật Đặc Biệt

### **1. Regex-Based Parsing:**
```python
# Parse "M là trung điểm AB"
patterns = [
    r'([A-Z])\s+(?:là\s+)?trung điểm\s+của\s+([A-Z]{2})',
    r'([A-Z])\s+(?:là\s+)?trung điểm\s+([A-Z]{2})',
    r'gọi\s+([A-Z])\s+là\s+trung điểm\s+của\s+([A-Z]{2})'
]
```

### **2. Number Extraction with Units:**
```python
def _extract_number(text, default=1.0):
    # Hỗ trợ: "a", "2a", "a√2", "√2", "1.5"
    if "√" in text:
        match = re.search(r'(\d*\.?\d*)\s*a?\s*√(\d+\.?\d*)', text)
        coef = float(match.group(1)) if match.group(1) else 1.0
        sqrt_val = float(match.group(2))
        return coef * math.sqrt(sqrt_val)
```

### **3. Trigger-Based Auto ID Generation:**
```sql
CREATE TRIGGER trg_AutoGenerateMaNguoiDung
ON NGUOIDUNG
INSTEAD OF INSERT
AS
BEGIN
    -- Tạo mã ND001, ND002, ND003...
    SELECT @maxNumber = MAX(CAST(SUBSTRING(maNguoiDung, 3, LEN(maNguoiDung)) AS INT))
    FROM NGUOIDUNG
    WHERE maNguoiDung LIKE 'ND%';
    
    SET @newMaNguoiDung = 'ND' + RIGHT('000' + CAST(@maxNumber + 1 AS VARCHAR), 3);
    
    INSERT INTO NGUOIDUNG (maNguoiDung, ...)
    SELECT @newMaNguoiDung, ...
    FROM inserted;
END;
```

---

## 📊 Data Flow

### **Complete Flow:**

```
1. User uploads image
   ↓
2. Gemini AI extracts structured data
   ↓
3. Save to BAITOAN + DULIEUHINHHOC
   ↓
4. User clicks "Generate 3D"
   ↓
5. GeometrySolver calculates coordinates
   ↓
6. GeometryRenderer transforms to 3D JSON
   ↓
7. Save to DUNGHINH3D
   ↓
8. Frontend renders with Three.js
   ↓
9. User clicks "Solve Problem"
   ↓
10. Gemini AI generates solution
   ↓
11. Save to LOIGIAI
   ↓
12. Frontend displays step-by-step solution
```

---

## 🎯 Ưu Điểm Của Phương Pháp

### **1. AI-First Approach:**
- Tận dụng sức mạnh của LLM
- Linh hoạt với nhiều dạng bài toán
- Không cần training model riêng

### **2. Constraint-Based Solving:**
- Chính xác về mặt toán học
- Có thể verify kết quả
- Dễ debug và maintain

### **3. Layered Architecture:**
- Separation of concerns
- Dễ test từng layer
- Dễ mở rộng

### **4. Caching Strategy:**
- Giảm chi phí API
- Tăng tốc độ response
- Hỗ trợ offline (với cached data)

---

## 🚀 Khả Năng Mở Rộng

### **1. Thêm Loại Hình Mới:**
```python
def _solve_new_shape(constraints):
    # Implement logic cho hình mới
    pass
```

### **2. Tích Hợp AI Khác:**
```python
class OpenAIClient:
    # Alternative AI provider
    pass
```

### **3. Thêm Tính Năng:**
- Export PDF
- Animation
- Step-by-step construction
- Interactive quiz

---

**Document Version:** 1.0  
**Last Updated:** 2026-05-07  
**Status:** ✅ Complete
