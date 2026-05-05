# Demo: Annotations Theo Từng Bước

## Khởi động nhanh

```bash
# Terminal 1
cd prototype-3d/backend && python -m uvicorn app.main:app --reload --port 8001

# Terminal 2
cd prototype-3d/frontend && npm run dev
```

Mở: `http://localhost:5173`

---

## Demo ngay

1. Chọn **"Bài 2: Hình chóp S.ABC với trung điểm"**
2. Click **"🎨 Dựng hình 3D"**
3. Dùng nút **◀ ▶** để chuyển step

---

## Xem annotations xuất hiện từng bước

### 🔹 Bước 1: Vẽ đáy ABC
Thấy:
- Số **3** trên AB
- Số **4** trên BC
- Ký hiệu **∟** tại B

### 🔹 Bước 2: Dựng S và SA
Thấy thêm:
- Số **6** trên SA
- Ký hiệu **⊥** tại SA
- (Vẫn thấy annotations bước 1)

### 🔹 Bước 3: Nối cạnh bên
- Thấy SB, SC
- Annotations tích lũy từ bước 1, 2

### 🔹 Bước 4: Điểm M
Thấy thêm:
- Điểm **M** giữa A và B
- Label **"trung điểm AB"**

### 🔹 Bước 5: Nối SM
- Thấy cạnh SM
- Tất cả annotations vẫn hiển thị

### 🔹 Bước 6: Hoàn thiện
- Toàn bộ hình chóp
- Tất cả annotations

---

## Kiểm tra nhanh

### Annotations có xuất hiện từng bước?
✅ Bước 1: Chỉ thấy annotations của đáy  
✅ Bước 2: Thấy thêm annotations của SA  
✅ Bước 4: Thấy thêm annotation của M  

### Annotations có tích lũy?
✅ Chuyển từ bước 1→2→3: Annotations cũ vẫn hiển thị  
✅ Chuyển ngược 3→2→1: Annotations biến mất đúng  

### Không có lỗi?
✅ Console không có lỗi đỏ  
✅ Annotations không bị duplicate  
✅ Text rõ ràng, dễ đọc  

---

## Thành công! 🎉

Nếu thấy annotations xuất hiện từng bước theo đúng objects → Tính năng hoạt động!

---

## Nếu có vấn đề

### Annotations xuất hiện tất cả ngay từ đầu?
→ Kiểm tra `showAnnotationsUpToStep()` trong SceneManager

### Annotations không tích lũy?
→ Kiểm tra vòng lặp `for (let i = 0; i <= currentStep; i++)`

### Annotations bị duplicate?
→ Đảm bảo `clear()` được gọi trước `renderAnnotations()`

### Debug:
```javascript
// Trong browser console
fetch('http://localhost:8001/api/problems/pyramid-2')
  .then(r => r.json())
  .then(d => console.log(d.geometry.steps.map(s => s.annotations)))
```
