# Ký hiệu toán học trong hình học không gian 3D

## 🎯 Mục tiêu

Hiển thị đầy đủ các ký hiệu toán học trên hình 3D:
- Độ dài cạnh (AB = 4, SA = 6)
- Ký hiệu vuông góc (⊥)
- Ký hiệu góc (∠, ∟)
- Ký hiệu đoạn bằng nhau (dấu gạch)
- Ghi chú điểm đặc biệt (tâm, trung điểm)

---

## 📐 Các loại ký hiệu

### 1. **Độ dài cạnh** (`annotations.edges`)

Ghi độ dài thực tế lên cạnh (nếu đề bài cho)

**Ví dụ:**
```json
{
  "edge": "A-B",
  "label": "4",
  "position": "bottom",
  "color": "black"
}
```

**Quy tắc:**
- Nếu đề bài cho "AB = 4" → ghi "4"
- Nếu đề bài cho "cạnh a" → ghi "a"
- Nếu không cho → không ghi (hoặc ghi "a")

**Vị trí:**
- `bottom`: Phía dưới cạnh
- `top`: Phía trên cạnh
- `left`: Bên trái cạnh
- `right`: Bên phải cạnh
- `center`: Giữa cạnh

### 2. **Ký hiệu vuông góc** (`annotations.perpendicular`)

Ký hiệu ⊥ tại đỉnh khi 2 đường vuông góc

**Ví dụ:**
```json
{
  "vertex": "A",
  "line1": "S-A",
  "line2": "A-B",
  "symbol": "⊥",
  "description": "SA ⊥ (ABCD)"
}
```

**Hiển thị:**
- Vẽ hình vuông nhỏ tại đỉnh A
- Hoặc vẽ ký hiệu ⊥ gần đỉnh A

**Các trường hợp:**
- SA ⊥ đáy → ký hiệu tại A (SA ⊥ AB, SA ⊥ AD)
- AB ⊥ BC → ký hiệu tại B (góc vuông)

### 3. **Ký hiệu góc** (`annotations.angles`)

Ký hiệu góc tại đỉnh

**Ví dụ:**
```json
{
  "vertex": "A",
  "line1": "A-B",
  "line2": "A-D",
  "angle": 90,
  "symbol": "∟",
  "description": "Góc vuông tại A"
}
```

**Hiển thị:**
- Vẽ cung tròn nhỏ tại đỉnh
- Ghi ký hiệu ∟ (góc vuông) hoặc số độ (60°, 90°)

**Các loại góc:**
- Góc vuông: `∟` hoặc hình vuông nhỏ
- Góc nhọn/tù: Cung tròn + số độ

### 4. **Ký hiệu đoạn bằng nhau** (`annotations.equal_segments`)

Dấu gạch trên các đoạn bằng nhau

**Ví dụ:**
```json
{
  "segments": ["A-B", "B-C", "C-D", "D-A"],
  "mark": "single",
  "description": "Các cạnh đáy bằng nhau"
}
```

**Hiển thị:**
- `single`: 1 gạch (|)
- `double`: 2 gạch (||)
- `triple`: 3 gạch (|||)

**Các trường hợp:**
- Hình vuông: AB = BC = CD = DA → 1 gạch trên mỗi cạnh
- Trung điểm: CM = MD → 2 gạch trên CM và MD

### 5. **Ghi chú điểm** (`annotations.points`)

Tên và mô tả điểm đặc biệt

**Ví dụ:**
```json
{
  "point": "O",
  "label": "O",
  "description": "Tâm đáy",
  "color": "purple"
}
```

**Hiển thị:**
- Tên điểm: O, M, H...
- Mô tả: "Tâm đáy", "Trung điểm", "Hình chiếu"

### 6. **Ghi chú khoảng cách** (`annotations.distances`)

Thông tin bổ sung về quan hệ

**Ví dụ:**
```json
{
  "description": "O là giao điểm của AC và BD",
  "related_points": ["O", "A", "C", "B", "D"]
}
```

---

## 🎨 Màu sắc

| Loại ký hiệu | Màu | Ví dụ |
|-------------|-----|-------|
| Độ dài cạnh đáy | Đen | AB = 4 |
| Độ dài cạnh bên | Teal | SA = 6 |
| Ký hiệu vuông góc | Đen | ⊥ |
| Ký hiệu góc | Đen | ∟, 90° |
| Điểm tâm | Tím | O |
| Điểm trung điểm | Vàng | M |
| Đường phụ trợ | Xám | AC, BD |

---

## 📋 Ví dụ đầy đủ

### Đề bài: "Hình chóp S.ABCD có đáy ABCD là hình vuông cạnh 4, SA = 6, SA ⊥ (ABCD), M là trung điểm CD"

**Annotations:**
```json
{
  "edges": [
    {
      "edge": "A-B",
      "label": "4",
      "position": "bottom",
      "color": "black"
    },
    {
      "edge": "S-A",
      "label": "6",
      "position": "left",
      "color": "teal"
    },
    {
      "edge": "S-M",
      "label": "SM",
      "position": "right",
      "color": "gold"
    }
  ],
  "points": [
    {
      "point": "A",
      "label": "A",
      "color": "black"
    },
    {
      "point": "M",
      "label": "M",
      "description": "Trung điểm",
      "color": "gold"
    }
  ],
  "perpendicular": [
    {
      "vertex": "A",
      "line1": "S-A",
      "line2": "A-B",
      "symbol": "⊥",
      "description": "SA ⊥ (ABCD)"
    },
    {
      "vertex": "A",
      "line1": "S-A",
      "line2": "A-D",
      "symbol": "⊥"
    }
  ],
  "angles": [
    {
      "vertex": "A",
      "line1": "A-B",
      "line2": "A-D",
      "angle": 90,
      "symbol": "∟",
      "description": "Góc vuông tại A"
    },
    {
      "vertex": "B",
      "line1": "B-A",
      "line2": "B-C",
      "angle": 90,
      "symbol": "∟"
    },
    {
      "vertex": "C",
      "line1": "C-B",
      "line2": "C-D",
      "angle": 90,
      "symbol": "∟"
    },
    {
      "vertex": "D",
      "line1": "D-C",
      "line2": "D-A",
      "angle": 90,
      "symbol": "∟"
    }
  ],
  "equal_segments": [
    {
      "segments": ["A-B", "B-C", "C-D", "D-A"],
      "mark": "single",
      "description": "Các cạnh đáy bằng nhau"
    },
    {
      "segments": ["C-M", "M-D"],
      "mark": "double",
      "description": "CM = MD"
    }
  ],
  "distances": [
    {
      "description": "M là trung điểm của CD",
      "related_points": ["M", "C", "D"]
    }
  ]
}
```

---

## 🔧 Implementation

### Backend (GeometrySolver)

```python
def _extract_actual_lengths(self, constraints: Dict) -> Dict[str, float]:
    """Trích xuất độ dài thực tế từ constraints"""
    lengths = {}
    
    # Từ base
    base = constraints.get("base", {})
    if "side" in base:
        lengths["AB"] = base["side"]
    
    # Từ apex
    apex = constraints.get("apex", {})
    if "height" in apex:
        lengths["SA"] = apex["height"]
    
    # Từ given_conditions
    for condition in constraints.get("given_conditions", []):
        # Parse "AB = 4", "SA = 6"
        match = re.search(r'([A-Z]{2})\s*=\s*(\d+\.?\d*)', condition)
        if match:
            lengths[match.group(1)] = float(match.group(2))
    
    return lengths

def _solve_pyramid(self, constraints: Dict):
    # ... tính toán points, edges ...
    
    # Lấy độ dài thực tế
    actual_lengths = self._extract_actual_lengths(constraints)
    
    # Tạo annotations
    annotations = {
        "edges": [],
        "points": [],
        "perpendicular": [],
        "angles": [],
        "equal_segments": [],
        "distances": []
    }
    
    # Ghi độ dài cạnh
    base_length = actual_lengths.get("AB", a)
    annotations["edges"].append({
        "edge": "A-B",
        "label": f"{base_length}" if base_length != 1.0 else "a",
        "position": "bottom"
    })
    
    # Ghi độ dài chiều cao
    height_value = actual_lengths.get("SA", h)
    annotations["edges"].append({
        "edge": "S-A",
        "label": f"{height_value}" if height_value != 1.414 else "h",
        "position": "left",
        "color": "teal"
    })
    
    # Ký hiệu vuông góc
    annotations["perpendicular"].append({
        "vertex": "A",
        "line1": "S-A",
        "line2": "A-B",
        "symbol": "⊥"
    })
    
    # Ký hiệu góc vuông (hình vuông)
    if base.get("type") == "square":
        for vertex in ["A", "B", "C", "D"]:
            annotations["angles"].append({
                "vertex": vertex,
                "angle": 90,
                "symbol": "∟"
            })
    
    # Ký hiệu cạnh bằng nhau
    annotations["equal_segments"].append({
        "segments": ["A-B", "B-C", "C-D", "D-A"],
        "mark": "single"
    })
    
    # Trung điểm
    if "M" in points:
        annotations["equal_segments"].append({
            "segments": ["C-M", "M-D"],
            "mark": "double"
        })
    
    return {
        "points": points,
        "edges": edges,
        "faces": faces,
        "annotations": annotations
    }
```

### Frontend (Three.js)

```typescript
class AnnotationRenderer {
  renderEdgeLabel(edge: Edge, label: string, position: string) {
    // Tính vị trí giữa 2 điểm
    const midpoint = edge.getMidpoint();
    
    // Tạo CSS2DObject cho label
    const div = document.createElement('div');
    div.className = 'edge-label';
    div.textContent = label;
    
    const labelObject = new CSS2DObject(div);
    labelObject.position.copy(midpoint);
    
    // Điều chỉnh vị trí theo position
    if (position === 'bottom') {
      labelObject.position.y -= 0.1;
    } else if (position === 'top') {
      labelObject.position.y += 0.1;
    }
    
    this.scene.add(labelObject);
  }
  
  renderPerpendicularSymbol(vertex: Vector3, line1: Vector3, line2: Vector3) {
    // Vẽ hình vuông nhỏ tại vertex
    const size = 0.1;
    const geometry = new PlaneGeometry(size, size);
    const material = new MeshBasicMaterial({ color: 0x000000, side: DoubleSide });
    const square = new Mesh(geometry, material);
    
    square.position.copy(vertex);
    // Xoay để vuông góc với 2 đường
    
    this.scene.add(square);
  }
  
  renderAngleSymbol(vertex: Vector3, angle: number) {
    // Vẽ cung tròn nhỏ
    const radius = 0.15;
    const curve = new EllipseCurve(0, 0, radius, radius, 0, Math.PI / 2);
    const points = curve.getPoints(20);
    const geometry = new BufferGeometry().setFromPoints(points);
    const material = new LineBasicMaterial({ color: 0x000000 });
    const arc = new Line(geometry, material);
    
    arc.position.copy(vertex);
    
    this.scene.add(arc);
  }
  
  renderEqualSegmentMarks(segments: string[], mark: string) {
    // Vẽ dấu gạch trên các đoạn
    const numMarks = mark === 'single' ? 1 : mark === 'double' ? 2 : 3;
    
    segments.forEach(segment => {
      const [start, end] = segment.split('-');
      const midpoint = this.getMidpoint(start, end);
      
      for (let i = 0; i < numMarks; i++) {
        // Vẽ gạch nhỏ vuông góc với đoạn
        const offset = (i - (numMarks - 1) / 2) * 0.05;
        // ...
      }
    });
  }
}
```

---

## ✅ Checklist

- [ ] Ghi độ dài cạnh đáy (AB = 4)
- [ ] Ghi độ dài cạnh bên (SA = 6)
- [ ] Ký hiệu vuông góc tại A (SA ⊥ đáy)
- [ ] Ký hiệu góc vuông tại các đỉnh đáy (∟)
- [ ] Ký hiệu cạnh bằng nhau (dấu gạch)
- [ ] Ghi chú điểm tâm O
- [ ] Ghi chú điểm trung điểm M
- [ ] Ký hiệu CM = MD (2 gạch)

---

## 🎯 Kết quả mong đợi

Khi render hình chóp S.ABCD với AB = 4, SA = 6, M là trung điểm CD:

```
         S (6)
        /|\
       / | \
      /  |  \
     /   |   \
    /    |    \
   /     |     \
  A------B------C
  |      |      |
  |      O      M
  |      |      |
  D------+------+
     (4)
     
Ký hiệu:
- AB = 4 (ghi dưới cạnh AB)
- SA = 6 (ghi bên trái SA)
- ⊥ tại A (SA vuông góc đáy)
- ∟ tại A, B, C, D (góc vuông)
- | trên AB, BC, CD, DA (cạnh bằng nhau)
- || trên CM, MD (đoạn bằng nhau)
- O: Tâm đáy (màu tím)
- M: Trung điểm (màu vàng)
```

---

## 📝 Lưu ý

1. **Độ ưu tiên hiển thị:**
   - Độ dài cạnh > Ký hiệu vuông góc > Ký hiệu góc > Dấu gạch

2. **Tránh chồng chéo:**
   - Điều chỉnh vị trí label để không che các ký hiệu khác
   - Sử dụng offset phù hợp

3. **Màu sắc nhất quán:**
   - Cạnh đáy: Đen
   - Cạnh bên: Teal (nếu là đường cao)
   - Điểm đặc biệt: Tím (tâm), Vàng (trung điểm)

4. **Font và size:**
   - Font: Arial, sans-serif
   - Size: 14px cho độ dài, 12px cho ký hiệu
   - Bold cho độ dài quan trọng
