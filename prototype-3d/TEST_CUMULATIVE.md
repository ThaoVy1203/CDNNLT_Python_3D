# 🧪 TEST CUMULATIVE STEPS

## 🔄 REFRESH FRONTEND

Vì chỉ sửa frontend, **không cần restart backend**.

### Cách 1: Hard Refresh Browser
```
Nhấn: Ctrl + Shift + R
```

### Cách 2: Clear Cache
```
F12 → Application → Clear storage → Clear site data
```

### Cách 3: Restart Frontend (nếu cần)
```bash
# Stop: Ctrl+C
# Restart:
cd d:/Vy/CDNNLT/CK_NNLT_3D/prototype-3d/frontend
npm run dev
```

---

## ✅ TEST CHECKLIST

### Test 1: Hình Chóp (Pyramid)

1. **Load hình**:
   - Chọn "Hình chóp"
   - Click "Tải hình"

2. **Bước 1** - Click Next hoặc Play:
   - ✅ Thấy 4 điểm A, B, C, D
   - ✅ Thấy 4 cạnh đáy

3. **Bước 2** - Click Next:
   - ✅ Thấy điểm S xuất hiện
   - ✅ **Đáy ABCD vẫn còn** (QUAN TRỌNG!)

4. **Bước 3** - Click Next:
   - ✅ Thấy 4 cạnh bên S-A, S-B, S-C, S-D
   - ✅ **Đáy ABCD vẫn còn**
   - ✅ **Đỉnh S vẫn còn**

5. **Bước 4** - Click Next:
   - ✅ Toàn bộ hình chóp hoàn chỉnh

### Test 2: Lăng Trụ (Prism)

1. **Load hình**:
   - Chọn "Lăng trụ"
   - Click "Tải hình"

2. **Bước 1**:
   - ✅ Thấy tam giác ABC
   - ✅ Thấy 3 cạnh đáy

3. **Bước 2**:
   - ✅ Thấy tam giác A'B'C' xuất hiện
   - ✅ **Đáy ABC vẫn còn**

4. **Bước 3**:
   - ✅ Thấy 3 cạnh bên A-A', B-B', C-C'
   - ✅ **Đáy ABC vẫn còn**
   - ✅ **Đỉnh A'B'C' vẫn còn**

5. **Bước 4**:
   - ✅ Toàn bộ lăng trụ hoàn chỉnh

### Test 3: Auto Play

1. **Load hình bất kỳ**
2. **Click ▶ (Play)**
3. **Quan sát**:
   - ✅ Animation chạy tự động
   - ✅ Mỗi bước thêm objects mới
   - ✅ Objects cũ không biến mất
   - ✅ Mượt mà, không nhảy cóc

### Test 4: Jump giữa các bước

1. **Load hình**
2. **Click vào "Bước 3" trong danh sách**
3. **Kiểm tra**:
   - ✅ Hiện objects từ bước 1, 2, 3
   - ✅ Không chỉ hiện bước 3

4. **Click vào "Bước 1"**
5. **Kiểm tra**:
   - ✅ Chỉ hiện objects bước 1
   - ✅ Objects bước 2, 3 biến mất

---

## 📊 SO SÁNH TRƯỚC/SAU

### TRƯỚC KHI SỬA:

```
Bước 1: [Đáy ABCD]
        ↓
Bước 2: [Đỉnh S]  ← ❌ Đáy biến mất!
        ↓
Bước 3: [Cạnh bên]  ← ❌ Đáy + đỉnh biến mất!
```

### SAU KHI SỬA:

```
Bước 1: [Đáy ABCD]
        ↓
Bước 2: [Đáy ABCD] + [Đỉnh S]  ← ✅ Giữ đáy!
        ↓
Bước 3: [Đáy ABCD] + [Đỉnh S] + [Cạnh bên]  ← ✅ Giữ tất cả!
```

---

## 🎥 VISUAL TEST

### Bước 1 → Bước 2

**Mong đợi**:
- Điểm S xuất hiện từ từ
- Đáy ABCD **không nhấp nháy**, **không biến mất**
- Smooth transition

### Bước 2 → Bước 3

**Mong đợi**:
- 4 cạnh bên xuất hiện
- Đáy ABCD **vẫn còn**
- Đỉnh S **vẫn còn**
- Không có gì biến mất

### Bước 3 → Bước 4

**Mong đợi**:
- Không có thay đổi lớn (vì bước 4 là tổng hợp)
- Hoặc có thêm một số chi tiết nhỏ

---

## 🔍 DEBUG (Nếu vẫn lỗi)

### Lỗi: Objects vẫn biến mất

**Check 1**: File đã save chưa?
```
Kiểm tra file: frontend/src/three/GeometryBuilder.ts
Dòng: showObjectsForStep(step: number)
Phải có: for (let i = 0; i <= step; i++)
```

**Check 2**: Browser đã refresh chưa?
```
Ctrl + Shift + R (hard refresh)
```

**Check 3**: Console có error không?
```
F12 → Console tab
Không được có error màu đỏ
```

### Lỗi: Animation không mượt

**Nguyên nhân**: Có thể do performance

**Giải pháp**:
- Giảm số objects
- Tắt grid/axes
- Zoom out xa hơn

---

## ✅ THÀNH CÔNG KHI

- [x] Bước 2 vẫn thấy đáy
- [x] Bước 3 vẫn thấy đáy + đỉnh
- [x] Animation mượt mà
- [x] Không có objects biến mất đột ngột
- [x] Dễ theo dõi quá trình dựng hình

---

## 📝 NOTES

### Tại sao quan trọng?

1. **Giáo dục**: Học sinh thấy rõ quá trình xây dựng hình
2. **UX**: Không bị nhầm lẫn, không bị mất context
3. **Logic**: Giống như vẽ tay thực tế
4. **Professional**: Animation chuyên nghiệp hơn

### So với dự án chính

Dự án chính (`fe/pages/geo3d.html`) dùng SVG tĩnh, không có animation.

Prototype này **vượt trội** vì:
- ✅ Animation động
- ✅ Cumulative steps
- ✅ Tương tác 3D
- ✅ Dễ mở rộng

---

**Chúc bạn test thành công!** 🎉

Nếu OK, có thể integrate vào dự án chính rồi!
