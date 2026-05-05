# 🧪 TEST SAU KHI SỬA

## 🔄 RESTART ỨNG DỤNG

### 1. Stop Backend (nếu đang chạy)
Nhấn `Ctrl+C` trong terminal backend

### 2. Restart Backend
```bash
cd d:/Vy/CDNNLT/CK_NNLT_3D/prototype-3d/backend
uvicorn app.main:app --reload --port 8001
```

### 3. Refresh Frontend
Trong browser, nhấn `Ctrl+Shift+R` (hard refresh)

Hoặc stop và restart:
```bash
# Stop: Ctrl+C
# Restart:
npm run dev
```

---

## ✅ CHECKLIST TEST

### Test Hình Chóp (Pyramid)

1. **Chọn "Hình chóp"** → Click "Tải hình"
2. **Bước 1**: 
   - ✅ 4 điểm A, B, C, D xuất hiện
   - ✅ 4 cạnh đáy xuất hiện (A-B, B-C, C-D, D-A)
3. **Bước 2**:
   - ✅ Điểm S xuất hiện phía trên
4. **Bước 3** (QUAN TRỌNG):
   - ✅ 4 cạnh bên xuất hiện (S-A, S-B, S-C, S-D)
   - ✅ Nối từ S đến 4 điểm đáy
5. **Bước 4**:
   - ✅ Toàn bộ hình chóp hoàn chỉnh

### Test Lăng Trụ (Prism)

1. **Chọn "Lăng trụ"** → Click "Tải hình"
2. **Bước 1**:
   - ✅ 3 điểm A, B, C xuất hiện
   - ✅ 3 cạnh đáy xuất hiện
3. **Bước 2**:
   - ✅ 3 điểm A', B', C' xuất hiện
   - ✅ 3 cạnh đỉnh xuất hiện
4. **Bước 3** (QUAN TRỌNG):
   - ✅ 3 cạnh bên xuất hiện (A-A', B-B', C-C')
5. **Bước 4**:
   - ✅ Toàn bộ lăng trụ hoàn chỉnh

### Test Hình Lập Phương (Cube)

1. **Chọn "Hình lập phương"** → Click "Tải hình"
2. **Bước 1**:
   - ✅ 4 điểm đáy xuất hiện
   - ✅ 4 cạnh đáy xuất hiện
3. **Bước 2**:
   - ✅ 4 điểm đỉnh xuất hiện
   - ✅ 4 cạnh đỉnh xuất hiện
4. **Bước 3** (QUAN TRỌNG):
   - ✅ 4 cạnh bên xuất hiện
5. **Bước 4**:
   - ✅ Toàn bộ hình lập phương hoàn chỉnh

---

## 🎮 TEST ANIMATION

### Auto Play
1. Click nút **▶ (Play)**
2. Quan sát animation tự động chạy qua 4 bước
3. Kiểm tra:
   - ✅ Mỗi bước hiện đúng objects
   - ✅ Không bị nhảy cóc
   - ✅ Smooth transitions

### Manual Control
1. Click **⏮** (Restart) → Về bước 1
2. Click **⏩** (Next) → Từng bước một
3. Kiểm tra:
   - ✅ Bước 3 có cạnh bên
   - ✅ Bước 4 có tất cả

### Click vào Steps List
1. Click trực tiếp vào "Bước 3: Nối các cạnh bên"
2. Kiểm tra:
   - ✅ Cạnh bên xuất hiện ngay lập tức

---

## 🔍 DEBUG (Nếu vẫn lỗi)

### 1. Check Backend Response

Mở: http://localhost:8001/api/mock/pyramid

Kiểm tra JSON response:
```json
{
  "steps": [
    {
      "order": 3,
      "description": "Nối các cạnh bên",
      "objects": ["S-A", "S-B", "S-C", "S-D"],  // ← Phải có dấu "-"
      "highlight": ["S-A", "S-B", "S-C", "S-D"]
    }
  ]
}
```

### 2. Check Browser Console

Nhấn `F12` → Tab Console

Kiểm tra:
- ❌ Không có error màu đỏ
- ✅ Có log "Geometry updated" (nếu có)

### 3. Check Network Tab

Nhấn `F12` → Tab Network

Kiểm tra:
- ✅ Request đến `/api/mock/pyramid` thành công (200)
- ✅ Response có đúng data

---

## 📊 KẾT QUẢ MONG ĐỢI

### Trước khi sửa:
```
Bước 3: Nối các cạnh bên
→ ❌ Không có gì xuất hiện
→ ❌ Chỉ thấy đáy + đỉnh
```

### Sau khi sửa:
```
Bước 3: Nối các cạnh bên
→ ✅ 4 cạnh từ S đến ABCD xuất hiện
→ ✅ Hình chóp gần hoàn chỉnh
```

---

## 🆘 NẾU VẪN LỖI

### Lỗi 1: Cạnh bên vẫn không hiện

**Giải pháp**:
```bash
# Clear cache backend
cd backend
rm -rf __pycache__ app/__pycache__ app/**/__pycache__

# Restart
uvicorn app.main:app --reload --port 8001
```

### Lỗi 2: Frontend không update

**Giải pháp**:
```bash
# Hard refresh browser
Ctrl+Shift+R

# Hoặc clear cache
Ctrl+Shift+Delete → Clear cache
```

### Lỗi 3: Vẫn không work

**Giải pháp**:
1. Check file `steps_generator.py` đã save chưa
2. Check file `GeometryBuilder.ts` đã save chưa
3. Restart cả backend và frontend
4. Hard refresh browser

---

## ✅ THÀNH CÔNG KHI

- [x] Bước 3 có cạnh bên xuất hiện
- [x] Animation mượt mà
- [x] Tất cả 3 dạng hình đều work
- [x] Không có error trong console

---

**Chúc bạn test thành công!** 🎉
