# 🔧 FIX: Các bước liên kết với nhau (Cumulative Steps)

## ❌ VẤN ĐỀ TRƯỚC ĐÓ

Khi chuyển sang bước mới, các objects từ bước trước **biến mất**:

```
Bước 1: Vẽ đáy ABCD
→ Hiện: A, B, C, D + 4 cạnh đáy

Bước 2: Dựng đỉnh S
→ Hiện: CHỈ có S
→ ❌ Đáy ABCD biến mất!

Bước 3: Nối các cạnh bên
→ Hiện: CHỈ có 4 cạnh bên
→ ❌ Đáy và đỉnh biến mất!
```

## ✅ MONG MUỐN

Các bước phải **tích lũy** (cumulative):

```
Bước 1: Vẽ đáy ABCD
→ Hiện: A, B, C, D + 4 cạnh đáy

Bước 2: Dựng đỉnh S
→ Hiện: A, B, C, D + 4 cạnh đáy + S
→ ✅ Giữ nguyên đáy!

Bước 3: Nối các cạnh bên
→ Hiện: A, B, C, D + 4 cạnh đáy + S + 4 cạnh bên
→ ✅ Giữ nguyên đáy + đỉnh!

Bước 4: Hoàn thiện
→ Hiện: Tất cả
```

## 🔧 GIẢI PHÁP

### Sửa `GeometryBuilder.ts`

**Logic cũ** (chỉ hiện bước hiện tại):
```typescript
showObjectsForStep(step: number) {
  const currentStep = this.geometryData.steps[step];
  
  // Hide all
  this.objects.forEach(obj => obj.visible = false);
  
  // Show ONLY current step objects
  currentStep.objects.forEach(objName => {
    const obj = this.objects.get(objName);
    if (obj) obj.visible = true;
  });
}
```

**Logic mới** (tích lũy từ bước 0 đến bước hiện tại):
```typescript
showObjectsForStep(step: number) {
  // Hide all first
  this.objects.forEach(obj => obj.visible = false);
  
  // Show objects from ALL steps up to current step
  for (let i = 0; i <= step; i++) {
    const currentStep = this.geometryData.steps[i];
    if (!currentStep) continue;
    
    currentStep.objects.forEach(objName => {
      const obj = this.objects.get(objName);
      if (obj) {
        obj.visible = true;
      }
    });
  }
}
```

## 📊 SO SÁNH

### Trước khi sửa:

| Bước | Hiển thị |
|------|----------|
| 1 | Đáy ABCD |
| 2 | ❌ CHỈ đỉnh S (đáy biến mất) |
| 3 | ❌ CHỈ cạnh bên (đáy + đỉnh biến mất) |
| 4 | Tất cả |

### Sau khi sửa:

| Bước | Hiển thị |
|------|----------|
| 1 | Đáy ABCD |
| 2 | ✅ Đáy ABCD + Đỉnh S |
| 3 | ✅ Đáy ABCD + Đỉnh S + Cạnh bên |
| 4 | ✅ Tất cả |

## 🎬 DEMO WORKFLOW

### Hình chóp S.ABCD

**Bước 1**: Vẽ đáy ABCD
```
Visible: [A, B, C, D, A-B, B-C, C-D, D-A]
```

**Bước 2**: Dựng đỉnh S
```
Visible: [A, B, C, D, A-B, B-C, C-D, D-A, S]
         └─────── Từ bước 1 ────────┘  └─ Bước 2 ─┘
```

**Bước 3**: Nối các cạnh bên
```
Visible: [A, B, C, D, A-B, B-C, C-D, D-A, S, S-A, S-B, S-C, S-D]
         └─────── Từ bước 1 ────────┘  └─ Bước 2 ─┘ └── Bước 3 ──┘
```

**Bước 4**: Hoàn thiện
```
Visible: [Tất cả objects]
```

## ✅ KẾT QUẢ

### Animation mượt mà:
- ✅ Bước 1: Đáy xuất hiện
- ✅ Bước 2: Đỉnh xuất hiện, đáy vẫn còn
- ✅ Bước 3: Cạnh bên xuất hiện, đáy + đỉnh vẫn còn
- ✅ Bước 4: Toàn bộ hình hoàn chỉnh

### Trải nghiệm người dùng:
- ✅ Dễ theo dõi quá trình dựng hình
- ✅ Không bị nhảy cóc
- ✅ Hiểu rõ từng bước xây dựng
- ✅ Giống như vẽ tay thực tế

## 🧪 TEST

### Test Hình Chóp

1. Click "Tải hình" → Chọn Pyramid
2. Click ▶ (Play)
3. Quan sát:
   - Bước 1: Đáy xuất hiện ✅
   - Bước 2: Đỉnh xuất hiện, **đáy vẫn còn** ✅
   - Bước 3: Cạnh bên xuất hiện, **đáy + đỉnh vẫn còn** ✅
   - Bước 4: Hoàn chỉnh ✅

### Test Lăng Trụ

1. Click "Tải hình" → Chọn Prism
2. Click ▶ (Play)
3. Quan sát:
   - Bước 1: Đáy ABC xuất hiện ✅
   - Bước 2: Đỉnh A'B'C' xuất hiện, **đáy vẫn còn** ✅
   - Bước 3: Cạnh bên xuất hiện, **đáy + đỉnh vẫn còn** ✅
   - Bước 4: Hoàn chỉnh ✅

## 📝 NOTES

### Tại sao cần cumulative?

1. **Giống vẽ tay thực tế**: Khi vẽ hình, ta không xóa đi vẽ lại
2. **Dễ hiểu**: Học sinh thấy rõ quá trình xây dựng
3. **Không bị nhầm lẫn**: Không bị mất context
4. **UX tốt hơn**: Animation mượt mà, logic

### Alternative approach (không dùng)

Có thể dùng `steps[step].objects` chứa **tất cả** objects từ đầu:
```python
# Backend
steps = [
  {"order": 1, "objects": ["A", "B", "C", "D", ...]},
  {"order": 2, "objects": ["A", "B", "C", "D", ..., "S"]},  # Lặp lại
  {"order": 3, "objects": ["A", "B", "C", "D", ..., "S", "S-A", ...]},  # Lặp lại
]
```

**Nhược điểm**: Lặp lại nhiều, JSON lớn

**Ưu điểm của cách hiện tại**: 
- JSON nhỏ gọn
- Logic rõ ràng (mỗi step chỉ chứa objects mới)
- Frontend xử lý cumulative

## ✅ STATUS

**FIXED** - Animation bây giờ là cumulative, giữ lại objects từ các bước trước.

---

**Ngày sửa**: 2026-05-05  
**File thay đổi**: `frontend/src/three/GeometryBuilder.ts`  
**Thay đổi**: Logic `showObjectsForStep()` từ "replace" sang "cumulative"
