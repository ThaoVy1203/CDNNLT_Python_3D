# 🏷️ TÍNH NĂNG: KÝ HIỆU HÌNH HỌC (ANNOTATIONS)

## 🎯 MỤC TIÊU

Hiển thị các ký hiệu hình học trên hình 3D:
- ✅ Độ dài cạnh (a, 2a, a√2...)
- ✅ Ký hiệu trung điểm (M là trung điểm CD)
- ✅ Ký hiệu vuông góc (⊥)
- ✅ Ký hiệu góc (∠, α, β...)
- ✅ Ký hiệu song song (∥)
- ✅ Ký hiệu bằng nhau (=)

## 📊 DATA STRUCTURE

### Backend Response
```json
{
  "points": {...},
  "edges": [...],
  "faces": [...],
  "steps": [...],
  "annotations": {
    "edges": [
      {
        "edge": "A-B",
        "label": "a",
        "type": "length",
        "position": "middle"
      },
      {
        "edge": "S-A",
        "label": "a√2",
        "type": "length",
        "position": "middle"
      }
    ],
    "points": [
      {
        "point": "M",
        "label": "M (trung điểm CD)",
        "type": "midpoint"
      }
    ],
    "angles": [
      {
        "vertex": "A",
        "edges": ["S-A", "A-B"],
        "label": "90°",
        "type": "right_angle"
      }
    ],
    "perpendicular": [
      {
        "line": "S-A",
        "plane": "ABCD",
        "symbol": "⊥"
      }
    ]
  }
}
```

## 🎨 VISUAL EXAMPLES

### 1. Độ dài cạnh
```
    S
   /|
  / | a√2
 /  |
A---B
  a
```

### 2. Trung điểm
```
D-------M-------C
    ← M (trung điểm)
```

### 3. Vuông góc
```
    S
    |
    | ⊥
    |
A---+---B
   (ABCD)
```

### 4. Góc
```
    S
   /
  / α
 /___
A    B
```

## 🔧 IMPLEMENTATION PLAN

### Phase 1: Backend (Đơn giản)
Trả về annotations cố định cho mỗi loại hình

### Phase 2: Frontend (Quan trọng)
Render annotations lên Three.js:
- Text labels
- Symbols (⊥, ∥, ∠)
- Lines/arrows

### Phase 3: Dynamic (Nâng cao)
Parse đề bài tự động để tạo annotations

## 📝 EXAMPLES

### Bài 1: Hình chóp cơ bản
```json
"annotations": {
  "edges": [
    {"edge": "A-B", "label": "a"},
    {"edge": "B-C", "label": "a"},
    {"edge": "S-A", "label": "a√2"}
  ],
  "perpendicular": [
    {"line": "S-A", "plane": "ABCD"}
  ]
}
```

### Bài 2: Hình chóp với M
```json
"annotations": {
  "edges": [
    {"edge": "A-B", "label": "a"},
    {"edge": "S-A", "label": "a√2"}
  ],
  "points": [
    {"point": "M", "label": "trung điểm CD"}
  ],
  "perpendicular": [
    {"line": "S-A", "plane": "ABCD"}
  ]
}
```

## 🚀 ROADMAP

### Milestone 1: Basic Labels (1 ngày)
- [ ] Backend trả về annotations
- [ ] Frontend render text labels cơ bản
- [ ] Test với 1 bài

### Milestone 2: Symbols (1 ngày)
- [ ] Render ký hiệu ⊥
- [ ] Render ký hiệu góc vuông
- [ ] Position labels đúng chỗ

### Milestone 3: All Annotations (2 ngày)
- [ ] Độ dài cạnh
- [ ] Trung điểm
- [ ] Góc
- [ ] Song song

### Milestone 4: Polish (1 ngày)
- [ ] Styling đẹp
- [ ] Toggle on/off
- [ ] Responsive với camera

---

**Status**: 📋 Planning  
**Priority**: ⭐⭐⭐ High  
**Complexity**: 🔴 Medium-High
