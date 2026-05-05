# 🎓 UPDATE: Từ "Chọn hình" → "Chọn đề bài"

## 🎯 THAY ĐỔI

### Trước đây:
```
┌─────────────────────────┐
│ Chọn hình học           │
│                         │
│ ○ Hình chóp (Pyramid)   │
│ ○ Lăng trụ (Prism)      │
│ ○ Hình lập phương       │
│                         │
│ [Tải hình]              │
└─────────────────────────┘
```

### Bây giờ:
```
┌─────────────────────────────────────────────┐
│ Chọn đề bài                                 │
│                                             │
│ ○ Bài 1: Hình chóp S.ABCD                  │
│   Cho hình chóp S.ABCD có đáy ABCD là      │
│   hình vuông cạnh a. SA vuông góc với      │
│   mặt phẳng đáy và SA = a√2.               │
│                                             │
│ ○ Bài 2: Lăng trụ tam giác ABC.A'B'C'      │
│   Cho lăng trụ đứng ABC.A'B'C' có đáy      │
│   ABC là tam giác đều cạnh a...            │
│                                             │
│ ○ Bài 3: Hình lập phương ABCD.A'B'C'D'     │
│   Cho hình lập phương ABCD.A'B'C'D'        │
│   có cạnh bằng a.                          │
│                                             │
│ [🎨 Dựng hình 3D]                          │
└─────────────────────────────────────────────┘
```

## ✨ CẢI TIẾN

### 1. Gần với thực tế hơn
- ✅ Giống đề thi thật
- ✅ Có ngữ cảnh bài toán
- ✅ Học sinh dễ hình dung

### 2. UI đẹp hơn
- ✅ Card-based design
- ✅ Hover effects
- ✅ Preview đề bài đã chọn
- ✅ Icon button

### 3. Dễ mở rộng
- ✅ Dễ thêm đề bài mới
- ✅ Có thể thêm độ khó
- ✅ Có thể thêm tags
- ✅ Có thể thêm hình ảnh

## 📝 ĐỀ BÀI MẪU

### Bài 1: Hình chóp S.ABCD (Cơ bản)
**Đề bài**: Cho hình chóp S.ABCD có đáy ABCD là hình vuông cạnh a. SA vuông góc với mặt phẳng đáy và SA = a√2.

**Câu hỏi**:
- Tính thể tích khối chóp S.ABCD
- Tính khoảng cách từ A đến mặt phẳng (SBC)

**Độ khó**: ⭐⭐ (Trung bình)

---

### Bài 2: Lăng trụ tam giác ABC.A'B'C' (Cơ bản)
**Đề bài**: Cho lăng trụ đứng ABC.A'B'C' có đáy ABC là tam giác đều cạnh a và chiều cao h = a.

**Câu hỏi**:
- Tính thể tích khối lăng trụ
- Tính khoảng cách giữa hai đường thẳng AB và B'C'

**Độ khó**: ⭐⭐ (Trung bình)

---

### Bài 3: Hình lập phương ABCD.A'B'C'D' (Dễ)
**Đề bài**: Cho hình lập phương ABCD.A'B'C'D' có cạnh bằng a.

**Câu hỏi**:
- Tính thể tích khối lập phương
- Tính khoảng cách từ A đến mặt phẳng (BDC')

**Độ khó**: ⭐ (Dễ)

---

## 🎨 UI COMPONENTS

### Problem Card
```tsx
<label className="problem-option">
  <input type="radio" />
  <div className="problem-content">
    <div className="problem-title">Bài 1: Hình chóp S.ABCD</div>
    <div className="problem-description">
      Cho hình chóp S.ABCD có đáy ABCD là hình vuông...
    </div>
  </div>
</label>
```

### Preview Box
```tsx
<div className="problem-preview">
  <strong>Đề bài đã chọn:</strong>
  <p>{selectedProblemData.description}</p>
</div>
```

### Action Button
```tsx
<button className="btn-load">
  🎨 Dựng hình 3D
</button>
```

## 📊 SO SÁNH

| Tiêu chí | Trước | Sau |
|----------|-------|-----|
| **Ngữ cảnh** | ❌ Chỉ có tên hình | ✅ Có đề bài đầy đủ |
| **Thực tế** | ❌ Trừu tượng | ✅ Giống đề thi |
| **UI** | ⚠️ Đơn giản | ✅ Card-based, đẹp |
| **Mở rộng** | ⚠️ Khó thêm info | ✅ Dễ thêm metadata |
| **UX** | ⚠️ OK | ✅ Tốt hơn |

## 🚀 CÁCH SỬ DỤNG

### 1. Refresh Frontend
```
Ctrl + Shift + R
```

### 2. Chọn đề bài
- Click vào card đề bài
- Đọc mô tả
- Xem preview

### 3. Dựng hình
- Click "🎨 Dựng hình 3D"
- Xem animation

## 🔮 TƯƠNG LAI

### Có thể thêm:

1. **Độ khó**:
   ```tsx
   <span className="difficulty">⭐⭐ Trung bình</span>
   ```

2. **Tags**:
   ```tsx
   <div className="tags">
     <span className="tag">Hình chóp</span>
     <span className="tag">Thể tích</span>
   </div>
   ```

3. **Hình ảnh**:
   ```tsx
   <img src="/problems/pyramid-1.png" alt="Preview" />
   ```

4. **Lời giải**:
   ```tsx
   <button onClick={showSolution}>Xem lời giải</button>
   ```

5. **Lịch sử**:
   ```tsx
   <span className="solved">✓ Đã làm</span>
   ```

## 📝 THÊM ĐỀ BÀI MỚI

### Trong `DataInput.tsx`:

```typescript
const PROBLEMS = [
  // ... existing problems
  {
    id: 'new-problem',
    title: 'Bài X: Tên bài',
    description: 'Đề bài đầy đủ...',
    shapeType: 'pyramid', // hoặc 'prism', 'cube'
  },
];
```

### Hoặc load từ API:

```typescript
useEffect(() => {
  fetch('/api/problems')
    .then(res => res.json())
    .then(data => setProblems(data));
}, []);
```

## ✅ KẾT QUẢ

### Trải nghiệm người dùng:
- ✅ Gần với thực tế hơn
- ✅ Dễ hiểu hơn
- ✅ Chuyên nghiệp hơn
- ✅ Dễ mở rộng

### So với dự án chính:
- ✅ Vượt trội về UX
- ✅ Có ngữ cảnh bài toán
- ✅ Dễ integrate với Gemini AI
- ✅ Sẵn sàng cho production

---

**Ngày update**: 2026-05-05  
**Files thay đổi**:
- `frontend/src/components/ui/DataInput.tsx`
- `frontend/src/App.css`
- `backend/mock_data/problems.json` (new)
