# Hướng Dẫn Ký Hiệu Mới Theo Hình Mẫu

## Các ký hiệu đã thêm dựa trên hình mẫu

### 1. Trục tọa độ (Axis)
**Từ hình 1:** Trục Y màu xanh lá với mũi tên

```typescript
{
  "axes": [
    {"name": "Y", "color": "#00ff00", "length": 3, "showLabel": true}
  ]
}
```

**Hiển thị:**
- Đường thẳng từ gốc tọa độ
- Mũi tên ở đầu
- Label tên trục (X, Y, Z)

### 2. Đường đứt nét (Dashed Line)
**Từ hình 2:** Đường cao AI, đường phụ IH

```typescript
{
  "dashedLines": [
    {"start": "A", "end": "I", "type": "height"},
    {"start": "I", "end": "H", "type": "auxiliary"}
  ]
}
```

**Loại đường:**
- `height`: Đường cao (màu xanh lá #00aa00)
- `projection`: Hình chiếu (màu xanh dương #0066cc)
- `auxiliary`: Đường phụ (màu xám #666666)

### 3. Độ dài cạnh với công thức
**Từ hình 1:** `2a`, `a√3`, `a√5`, `2a√2`

```typescript
{
  "edges": [
    {"edge": "A-B", "label": "2a", "type": "length"},
    {"edge": "B-C", "label": "a√3", "type": "length"},
    {"edge": "C-D", "label": "a√5", "type": "length"}
  ]
}
```

### 4. Điểm với tọa độ
**Từ hình 1:** `C(z=a√3)`

```typescript
{
  "points": [
    {"point": "C", "label": "z=a√3", "type": "special", "showCoordinates": true}
  ]
}
```

**Hiển thị:** `C(z=a√3)`

### 5. Hình vuông góc vuông
**Từ hình 2:** Hình vuông nhỏ tại H

```typescript
{
  "perpendicular": [
    {"line": "A-I", "symbol": "⊥", "showSquare": true}
  ]
}
```

**Hiển thị:**
- Hình vuông nhỏ 0.1 x 0.1
- Ký hiệu ⊥

---

## Ví dụ đầy đủ theo hình mẫu

### Hình 1: Tứ diện với trục Y

```json
{
  "points": {
    "A": [0, 2, 0],
    "B": [2, 0, 0],
    "C": [0, 0, 1.732],
    "Y_origin": [0, 0, 0]
  },
  "edges": [
    {"start": "A", "end": "B"},
    {"start": "B", "end": "C"},
    {"start": "C", "end": "A"}
  ],
  "annotations": {
    "edges": [
      {"edge": "A-B", "label": "2a√2", "type": "length"},
      {"edge": "B-C", "label": "2a", "type": "length"},
      {"edge": "C-A", "label": "a√5", "type": "length"}
    ],
    "points": [
      {"point": "C", "label": "z=a√3", "type": "special", "showCoordinates": true}
    ],
    "axes": [
      {"name": "Y", "color": "#00ff00", "length": 3, "showLabel": true}
    ]
  }
}
```

### Hình 2: Tứ diện ABCD với đường cao

```json
{
  "points": {
    "A": [0, 2, 0],
    "B": [-1, 0, -1],
    "C": [1, 0, -1],
    "D": [0, 0, 1],
    "I": [0, 0, 0],
    "H": [0, 0, -0.5]
  },
  "edges": [
    {"start": "A", "end": "B"},
    {"start": "A", "end": "C"},
    {"start": "A", "end": "D"},
    {"start": "B", "end": "C"},
    {"start": "C", "end": "D"},
    {"start": "D", "end": "B"}
  ],
  "annotations": {
    "dashedLines": [
      {"start": "A", "end": "I", "type": "height"},
      {"start": "I", "end": "H", "type": "auxiliary"},
      {"start": "B", "end": "C", "type": "auxiliary"}
    ],
    "perpendicular": [
      {"line": "A-I", "symbol": "⊥", "showSquare": true}
    ],
    "points": [
      {"point": "I", "label": "I", "type": "projection"},
      {"point": "H", "label": "H", "type": "intersection"}
    ]
  }
}
```

---

## Cách sử dụng

### 1. Thêm trục tọa độ

```python
# Backend
annotations["axes"] = [
    {"name": "X", "color": "#ff0000", "length": 2, "showLabel": True},
    {"name": "Y", "color": "#00ff00", "length": 3, "showLabel": True},
    {"name": "Z", "color": "#0000ff", "length": 2, "showLabel": True}
]
```

### 2. Thêm đường đứt nét

```python
# Đường cao từ A xuống I
annotations["dashedLines"] = [
    {"start": "A", "end": "I", "type": "height"}
]
```

### 3. Thêm độ dài với công thức

```python
# Parse từ đề bài hoặc thêm thủ công
annotations["edges"] = [
    {"edge": "A-B", "label": "2a√2", "type": "length"},
    {"edge": "B-C", "label": "a√3", "type": "length"}
]
```

### 4. Thêm điểm với tọa độ

```python
annotations["points"] = [
    {
        "point": "C",
        "label": "z=a√3",
        "type": "special",
        "showCoordinates": True
    }
]
```

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

### Test cases

1. **Trục Y:** Thấy trục màu xanh lá với mũi tên và label "Y"
2. **Đường đứt nét:** Thấy đường cao AI dạng đứt nét
3. **Độ dài:** Thấy `2a√2`, `a√3` trên các cạnh
4. **Điểm tọa độ:** Thấy `C(z=a√3)`
5. **Hình vuông góc:** Thấy hình vuông nhỏ tại chân vuông góc

---

## Màu sắc

| Thành phần | Màu | Hex |
|------------|-----|-----|
| Trục X | Đỏ | #ff0000 |
| Trục Y | Xanh lá | #00ff00 |
| Trục Z | Xanh dương | #0000ff |
| Đường cao | Xanh lá đậm | #00aa00 |
| Hình chiếu | Xanh dương | #0066cc |
| Đường phụ | Xám | #666666 |
| Độ dài cạnh | Nâu | #a07840 |
| Điểm đặc biệt | Xanh lá | #2a7a62 |
| Vuông góc | Xanh dương đậm | #3d52a0 |

---

## Kết luận

Hệ thống giờ hỗ trợ đầy đủ các ký hiệu theo hình mẫu:

✅ Trục tọa độ với mũi tên  
✅ Đường đứt nét (đường cao, hình chiếu, phụ)  
✅ Độ dài cạnh với công thức (2a√2, a√3,...)  
✅ Điểm với tọa độ C(z=a√3)  
✅ Hình vuông góc vuông  
✅ Tất cả ký hiệu xuất hiện theo từng bước!
