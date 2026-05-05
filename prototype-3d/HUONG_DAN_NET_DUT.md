# Hướng Dẫn Vẽ Cạnh Nét Đứt

## Tổng quan

Các cạnh phụ (như SM khi M là trung điểm) giờ được vẽ dạng **nét đứt** thay vì nét liền để phân biệt với các cạnh chính của hình.

## Các loại đường

### 1. Solid (Nét liền) - Mặc định
Dùng cho các cạnh chính của hình:
- Cạnh đáy: AB, BC, CD, DA
- Cạnh bên: SA, SB, SC, SD

```typescript
{"start": "A", "end": "B", "style": "solid", "type": "main"}
```

### 2. Dashed (Nét đứt)
Dùng cho các cạnh phụ:
- Cạnh đến điểm đặc biệt: SM (M là trung điểm)
- Đường cao
- Đường phụ

```typescript
{"start": "S", "end": "M", "style": "dashed", "type": "auxiliary"}
```

**Thông số:**
- `dashSize`: 0.1 (độ dài mỗi đoạn)
- `gapSize`: 0.05 (khoảng cách giữa các đoạn)
- Màu: #2c3e50

### 3. Dotted (Nét chấm)
Dùng cho các đường đặc biệt khác:

```typescript
{"start": "A", "end": "I", "style": "dotted", "type": "projection"}
```

**Thông số:**
- `dashSize`: 0.02 (độ dài mỗi chấm)
- `gapSize`: 0.08 (khoảng cách giữa các chấm)

---

## Ví dụ: Hình chóp S.ABCD với trung điểm M

### Đề bài
"Cho hình chóp S.ABCD có đáy ABCD là hình vuông cạnh a. SA vuông góc với mặt phẳng đáy. Gọi M là trung điểm của CD."

### Edges được tạo

```json
{
  "edges": [
    // Cạnh đáy - NÉT LIỀN
    {"start": "A", "end": "B", "style": "solid", "type": "main"},
    {"start": "B", "end": "C", "style": "solid", "type": "main"},
    {"start": "C", "end": "D", "style": "solid", "type": "main"},
    {"start": "D", "end": "A", "style": "solid", "type": "main"},
    
    // Cạnh bên - NÉT LIỀN
    {"start": "S", "end": "A", "style": "solid", "type": "main"},
    {"start": "S", "end": "B", "style": "solid", "type": "main"},
    {"start": "S", "end": "C", "style": "solid", "type": "main"},
    {"start": "S", "end": "D", "style": "solid", "type": "main"},
    
    // Cạnh đến trung điểm - NÉT ĐỨT
    {"start": "S", "end": "M", "style": "dashed", "type": "auxiliary"}
  ]
}
```

### Kết quả
- Các cạnh AB, BC, CD, DA, SA, SB, SC, SD: **nét liền** (xanh dương đậm)
- Cạnh SM: **nét đứt** (xám đen)

---

## Logic tự động

### Backend (Python)

```python
# File: backend/app/solver/sympy_solver.py

def solve_pyramid(self, constraints: Dict) -> Dict:
    # ... tạo points ...
    
    special_point_names = []
    
    # Thêm điểm đặc biệt
    if special_points:
        for sp in special_points:
            if sp.get("type") == "midpoint":
                # ... tính tọa độ ...
                special_point_names.append(sp["name"])
    
    # Cạnh chính - solid
    edges = [
        {"start": "A", "end": "B", "style": "solid", "type": "main"},
        # ...
    ]
    
    # Cạnh đến điểm đặc biệt - dashed
    for sp_name in special_point_names:
        edges.append({
            "start": "S",
            "end": sp_name,
            "style": "dashed",
            "type": "auxiliary"
        })
```

### Frontend (TypeScript)

```typescript
// File: frontend/src/three/GeometryBuilder.ts

private createEdge(
  start: [number, number, number],
  end: [number, number, number],
  name: string,
  style: 'solid' | 'dashed' | 'dotted' = 'solid'
): THREE.Line {
  const geometry = new THREE.BufferGeometry().setFromPoints(points);
  
  if (style === 'dashed') {
    const material = new THREE.LineDashedMaterial({
      color: 0x2c3e50,
      dashSize: 0.1,
      gapSize: 0.05
    });
    const line = new THREE.Line(geometry, material);
    line.computeLineDistances();  // Quan trọng!
    return line;
  }
  
  // ... solid hoặc dotted ...
}
```

---

## Cách sử dụng

### 1. Thêm điểm đặc biệt trong constraints

```json
{
  "shape_type": "pyramid",
  "constraints": {
    "base": {"type": "square", "side": 1.0},
    "apex": {"height": 1.414},
    "special_points": [
      {
        "name": "M",
        "type": "midpoint",
        "segment": ["C", "D"]
      }
    ]
  }
}
```

### 2. Backend tự động tạo cạnh dashed

Khi có `special_points`, backend sẽ:
1. Tính tọa độ điểm M
2. Thêm cạnh SM với `"style": "dashed"`

### 3. Frontend render nét đứt

GeometryBuilder nhận edge với `style: "dashed"` và vẽ bằng `LineDashedMaterial`.

---

## Test

```bash
# Terminal 1
cd prototype-3d\backend
python -m uvicorn app.main:app --reload --port 8001

# Terminal 2
cd prototype-3d\frontend
npm run dev
```

### Test case

1. Chọn **"Bài 2: Hình chóp S.ABC với trung điểm"**
2. Click **"🎨 Dựng hình 3D"**
3. Chuyển đến **Bước 4** (Xác định điểm M)
4. Chuyển đến **Bước 5** (Nối SM)

### Kỳ vọng

✅ Bước 1-3: Các cạnh chính vẽ nét liền  
✅ Bước 4: Điểm M xuất hiện  
✅ Bước 5: Cạnh SM xuất hiện dạng **nét đứt**  

---

## Phân biệt các loại cạnh

| Loại cạnh | Style | Màu | Ví dụ |
|-----------|-------|-----|-------|
| Cạnh chính | solid | #0000ff | AB, BC, SA, SB |
| Cạnh phụ | dashed | #2c3e50 | SM, AI |
| Hình chiếu | dotted | #2c3e50 | Đường chiếu |

---

## Mở rộng

### Thêm loại cạnh khác

```python
# Đường cao
edges.append({
    "start": "A",
    "end": "H",
    "style": "dashed",
    "type": "height"
})

# Đường trung tuyến
edges.append({
    "start": "A",
    "end": "M",
    "style": "dashed",
    "type": "median"
})

# Hình chiếu
edges.append({
    "start": "A",
    "end": "I",
    "style": "dotted",
    "type": "projection"
})
```

---

## Lưu ý

### 1. computeLineDistances()
**Quan trọng!** Phải gọi `line.computeLineDistances()` sau khi tạo LineDashedMaterial, nếu không nét đứt sẽ không hiển thị.

```typescript
const line = new THREE.Line(geometry, dashedMaterial);
line.computeLineDistances();  // BẮT BUỘC!
```

### 2. linewidth
`linewidth` trong Three.js không hoạt động trên tất cả platform. Nếu muốn đường dày hơn, dùng `THREE.Line2` từ `three/examples/jsm/lines/Line2.js`.

### 3. Màu sắc
Có thể tùy chỉnh màu cho từng loại:
- Cạnh chính: xanh dương (#0000ff)
- Cạnh phụ: xám đen (#2c3e50)
- Đường cao: xanh lá (#00aa00)

---

## Kết luận

Hệ thống giờ tự động vẽ các cạnh phụ dạng nét đứt:

✅ Cạnh đến điểm đặc biệt (SM) - nét đứt  
✅ Cạnh chính (AB, SA) - nét liền  
✅ Hỗ trợ 3 loại: solid, dashed, dotted  
✅ Tự động nhận diện từ special_points  
✅ Xuất hiện theo từng bước dựng hình  
