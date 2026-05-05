# Test Annotations Theo Từng Bước

## Tính năng mới

Các ký hiệu hình học giờ đây xuất hiện **theo từng bước** trong quá trình dựng hình, không phải hiển thị tất cả cùng lúc.

## Ví dụ: Hình chóp S.ABC với trung điểm M

### Đề bài
"Cho hình chóp S.ABC có đáy ABC là tam giác vuông tại B, AB = 3, BC = 4. SA vuông góc với mặt phẳng (ABC) và SA = 6. Gọi M là trung điểm của AB."

### Các bước dựng hình

#### Bước 1: Vẽ đáy ABC
**Objects hiển thị:**
- Điểm A, B, C
- Cạnh AB, BC, CA

**Annotations hiển thị:**
- ✅ Label "3" trên cạnh AB
- ✅ Label "4" trên cạnh BC
- ✅ Ký hiệu ∟ tại điểm B (góc vuông)

#### Bước 2: Dựng đỉnh S và nối SA
**Objects hiển thị:**
- Điểm S
- Cạnh SA

**Annotations hiển thị (tích lũy):**
- ✅ Label "3" trên AB (từ bước 1)
- ✅ Label "4" trên BC (từ bước 1)
- ✅ Ký hiệu ∟ tại B (từ bước 1)
- ✅ Label "6" trên cạnh SA (mới)
- ✅ Ký hiệu ⊥ tại SA (mới - vuông góc với đáy)

#### Bước 3: Nối các cạnh bên còn lại
**Objects hiển thị:**
- Cạnh SB, SC

**Annotations hiển thị (tích lũy):**
- Tất cả annotations từ bước 1 và 2

#### Bước 4: Xác định điểm M
**Objects hiển thị:**
- Điểm M

**Annotations hiển thị (tích lũy):**
- Tất cả annotations từ các bước trước
- ✅ Label "trung điểm AB" tại điểm M (mới)

#### Bước 5: Nối SM
**Objects hiển thị:**
- Cạnh SM

**Annotations hiển thị (tích lũy):**
- Tất cả annotations từ các bước trước

#### Bước 6: Hoàn thiện
**Objects hiển thị:**
- Tất cả objects

**Annotations hiển thị:**
- Tất cả annotations

---

## Cách test

### 1. Khởi động
```bash
# Terminal 1 - Backend
cd prototype-3d/backend
python -m uvicorn app.main:app --reload --port 8001

# Terminal 2 - Frontend
cd prototype-3d/frontend
npm run dev
```

### 2. Mở trình duyệt
```
http://localhost:5173
```

### 3. Test từng bước

1. **Chọn "Bài 2: Hình chóp S.ABC với trung điểm"**
2. **Click "🎨 Dựng hình 3D"**
3. **Sử dụng nút ◀ ▶ để chuyển step**

### 4. Kiểm tra từng bước

#### Bước 1 (Vẽ đáy):
- [ ] Thấy tam giác ABC
- [ ] Thấy số "3" trên AB
- [ ] Thấy số "4" trên BC
- [ ] Thấy ký hiệu ∟ tại B

#### Bước 2 (Dựng S và SA):
- [ ] Thấy điểm S xuất hiện
- [ ] Thấy cạnh SA
- [ ] Thấy số "6" trên SA
- [ ] Thấy ký hiệu ⊥ tại SA
- [ ] Vẫn thấy annotations từ bước 1

#### Bước 3 (Nối cạnh bên):
- [ ] Thấy SB, SC xuất hiện
- [ ] Vẫn thấy tất cả annotations trước đó

#### Bước 4 (Điểm M):
- [ ] Thấy điểm M xuất hiện giữa A và B
- [ ] Thấy label "trung điểm AB" tại M
- [ ] Vẫn thấy tất cả annotations trước đó

#### Bước 5 (Nối SM):
- [ ] Thấy cạnh SM
- [ ] Vẫn thấy tất cả annotations

#### Bước 6 (Hoàn thiện):
- [ ] Thấy toàn bộ hình chóp
- [ ] Thấy tất cả annotations

---

## Test với Bài 1 (Hình chóp S.ABCD)

### Đề bài
"Cho hình chóp S.ABCD có đáy ABCD là hình vuông cạnh a. SA vuông góc với mặt phẳng đáy và SA = a√2."

### Các bước

#### Bước 1: Vẽ đáy ABCD
**Annotations:**
- Label "a" trên các cạnh đáy (nếu được parse từ đề bài)

#### Bước 2: Dựng S và SA
**Annotations:**
- Label "a√2" trên SA
- Ký hiệu ⊥ tại SA

#### Bước 3: Nối cạnh bên
**Annotations:**
- Tích lũy từ các bước trước

#### Bước 4: Hoàn thiện
**Annotations:**
- Tất cả

---

## Kiểm tra API

### Test response có annotations trong steps
```bash
curl http://localhost:8001/api/problems/pyramid-2 | jq '.geometry.steps[1].annotations'
```

**Kỳ vọng:** Mỗi step có annotations riêng
```json
{
  "edges": [
    {"edge": "S-A", "label": "6", "type": "length"}
  ],
  "perpendicular": [
    {"line": "S-A", "symbol": "⊥", "type": "perpendicular_to_plane"}
  ]
}
```

---

## Logic hoạt động

### Backend (steps_generator.py)
```python
def distribute_annotations(steps, all_annotations):
    """Phân bổ annotations vào từng step"""
    for step in steps:
        step_objects = set(step["objects"])
        step_annotations = {}
        
        # Chỉ thêm annotations cho objects trong step này
        for edge_ann in all_annotations["edges"]:
            if edge_ann["edge"] in step_objects:
                step_annotations["edges"].append(edge_ann)
        
        step["annotations"] = step_annotations
```

### Frontend (SceneManager.ts)
```typescript
showAnnotationsUpToStep(currentStep) {
    // Tích lũy annotations từ step 0 đến currentStep
    const cumulative = { edges: [], points: [], ... };
    
    for (let i = 0; i <= currentStep; i++) {
        const step = this.geometryData.steps[i];
        if (step.annotations) {
            cumulative.edges.push(...step.annotations.edges);
            // ...
        }
    }
    
    this.annotationRenderer.renderAnnotations(cumulative);
}
```

---

## Debug

### Nếu annotations không xuất hiện theo step:

1. **Kiểm tra backend response:**
```javascript
fetch('http://localhost:8001/api/problems/pyramid-2')
  .then(r => r.json())
  .then(d => {
    d.geometry.steps.forEach((step, i) => {
      console.log(`Step ${i}:`, step.annotations);
    });
  });
```

2. **Kiểm tra frontend console:**
- Mở DevTools (F12)
- Chuyển step và xem logs
- Kiểm tra `showAnnotationsUpToStep` được gọi

3. **Kiểm tra objects trong step:**
```javascript
// Trong console
fetch('http://localhost:8001/api/problems/pyramid-2')
  .then(r => r.json())
  .then(d => {
    d.geometry.steps.forEach((step, i) => {
      console.log(`Step ${i} objects:`, step.objects);
    });
  });
```

---

## Lỗi thường gặp

### 1. Annotations xuất hiện tất cả ngay từ đầu
**Nguyên nhân:** Frontend không gọi `showAnnotationsUpToStep`

**Giải pháp:** Kiểm tra `goToStep()` trong SceneManager

### 2. Annotations không tích lũy
**Nguyên nhân:** Logic tích lũy bị lỗi

**Giải pháp:** Kiểm tra vòng lặp `for (let i = 0; i <= currentStep; i++)`

### 3. Annotations bị duplicate
**Nguyên nhân:** Không clear trước khi render

**Giải pháp:** Đảm bảo `this.annotationRenderer.clear()` được gọi

### 4. Annotations không khớp với objects
**Nguyên nhân:** Edge name không khớp (A-B vs B-A)

**Giải pháp:** Backend đã xử lý cả 2 chiều trong `distribute_annotations`

---

## Checklist hoàn chỉnh

- [ ] Backend khởi động thành công
- [ ] Frontend khởi động thành công
- [ ] API trả về steps với annotations
- [ ] Bước 1: Chỉ thấy annotations của đáy
- [ ] Bước 2: Thấy annotations tích lũy (đáy + SA)
- [ ] Bước 3: Thấy annotations tích lũy tiếp
- [ ] Bước 4: Thấy annotation của điểm M
- [ ] Bước 5: Thấy tất cả annotations
- [ ] Chuyển ngược lại (◀) vẫn đúng
- [ ] Annotations không bị duplicate
- [ ] Text rõ ràng, không bị che

---

## Kết quả mong đợi

✅ Khi chuyển từ bước 1 → 2 → 3 → 4 → 5 → 6:
- Annotations xuất hiện dần dần
- Annotations cũ vẫn hiển thị (tích lũy)
- Không có annotations bị mất
- Không có annotations bị duplicate

✅ Khi chuyển ngược 6 → 5 → 4 → 3 → 2 → 1:
- Annotations biến mất dần
- Chỉ hiển thị annotations của các bước đã qua
- Không có lỗi console
