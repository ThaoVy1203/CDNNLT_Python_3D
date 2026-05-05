# 🚀 HƯỚNG DẪN CHẠY PROTOTYPE

## ✅ YÊU CẦU HỆ THỐNG

- **Python**: 3.10 trở lên
- **Node.js**: 18 trở lên
- **Git Bash** hoặc **PowerShell** (Windows)

---

## 📦 BƯỚC 1: SETUP BACKEND (5 phút)

### 1.1. Mở Git Bash hoặc PowerShell

```bash
# Di chuyển vào thư mục backend
cd d:/Vy/CDNNLT/CK_NNLT_3D/prototype-3d/backend
```

### 1.2. Tạo Virtual Environment

```bash
# Tạo venv
python -m venv venv

# Activate (Git Bash)
source venv/Scripts/activate

# Hoặc Activate (PowerShell)
venv\Scripts\activate
```

**Kiểm tra**: Bạn sẽ thấy `(venv)` ở đầu dòng lệnh

### 1.3. Install Dependencies

```bash
pip install -r requirements.txt
```

**Chờ khoảng 1-2 phút** để cài đặt các packages

### 1.4. Chạy Backend Server

```bash
uvicorn app.main:app --reload --port 8001
```

**✅ Thành công khi thấy**:
```
INFO:     Uvicorn running on http://127.0.0.1:8001 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### 1.5. Test Backend

Mở browser: **http://localhost:8001**

Bạn sẽ thấy:
```json
{
  "message": "Geometry Engine API",
  "version": "0.1.0",
  "docs": "/docs"
}
```

**Test API docs**: http://localhost:8001/docs

---

## ⚛️ BƯỚC 2: SETUP FRONTEND (5 phút)

### 2.1. Mở Terminal MỚI (giữ backend chạy)

```bash
# Di chuyển vào thư mục frontend
cd d:/Vy/CDNNLT/CK_NNLT_3D/prototype-3d/frontend
```

### 2.2. Install Dependencies (nếu chưa cài)

```bash
npm install
```

**Chờ khoảng 2-3 phút** để cài đặt

### 2.3. Chạy Frontend Dev Server

```bash
npm run dev
```

**✅ Thành công khi thấy**:
```
VITE v5.0.8  ready in 500 ms

➜  Local:   http://localhost:5174/
➜  Network: use --host to expose
➜  press h + enter to show help
```

### 2.4. Mở Browser

Mở: **http://localhost:5174**

Bạn sẽ thấy giao diện với:
- Sidebar bên trái: Controls
- Canvas bên phải: Vùng render 3D

---

## 🧪 BƯỚC 3: TEST API (Không cần frontend)

### 3.1. Test với Browser

Mở: **http://localhost:8001/api/mock/pyramid**

Bạn sẽ thấy JSON response với tọa độ hình chóp

### 3.2. Test với Swagger UI

1. Mở: **http://localhost:8001/docs**
2. Click vào **POST /api/solve**
3. Click **Try it out**
4. Paste JSON này:

```json
{
  "shape_type": "pyramid",
  "constraints": {
    "base": {
      "type": "square",
      "side": 1.0
    },
    "apex": {
      "height": 1.414,
      "perpendicular_to_base": true
    }
  }
}
```

5. Click **Execute**
6. Xem response bên dưới

### 3.3. Test với curl (Optional)

```bash
curl -X POST http://localhost:8001/api/solve \
  -H "Content-Type: application/json" \
  -d '{
    "shape_type": "pyramid",
    "constraints": {
      "base": {"type": "square", "side": 1.0},
      "apex": {"height": 1.414, "perpendicular_to_base": true}
    }
  }'
```

---

## 🎉 BƯỚC 4: SỬ DỤNG ỨNG DỤNG

### 4.1. Chọn hình học

1. Trong sidebar, chọn một trong 3 loại:
   - ⭕ Hình chóp (Pyramid)
   - ⭕ Lăng trụ (Prism)
   - ⭕ Hình lập phương (Cube)

2. Click nút **"Tải hình"**

3. Đợi 1-2 giây, hình 3D sẽ xuất hiện

### 4.2. Xem animation từng bước

1. Click nút **▶ (Play)** để xem animation tự động

2. Hoặc dùng các nút:
   - **⏮** - Về đầu
   - **⏪** - Bước trước
   - **⏸** - Tạm dừng
   - **⏩** - Bước sau
   - **⏭** - Đến cuối

3. Hoặc click trực tiếp vào từng bước trong danh sách

### 4.3. Tương tác với hình 3D

- **Xoay**: Kéo chuột trái
- **Zoom**: Cuộn chuột
- **Pan**: Kéo chuột phải (hoặc Shift + kéo trái)

### 4.4. Tùy chỉnh hiển thị

Trong sidebar, bật/tắt:
- ☑️ Hiện lưới (Grid)
- ☑️ Hiện trục tọa độ (Axes)

---

## 📊 DEMO WORKFLOW

### Ví dụ: Dựng hình chóp

1. **Chọn "Hình chóp"** → Click "Tải hình"
2. **Bước 1**: Vẽ đáy ABCD (hình vuông xuất hiện)
3. **Bước 2**: Dựng đỉnh S (điểm S xuất hiện phía trên)
4. **Bước 3**: Nối các cạnh bên (các đường từ S đến ABCD)
5. **Bước 4**: Hoàn thiện (toàn bộ hình chóp)

### Ví dụ: Dựng lăng trụ

1. **Chọn "Lăng trụ"** → Click "Tải hình"
2. **Bước 1**: Vẽ đáy ABC (tam giác)
3. **Bước 2**: Vẽ đỉnh A'B'C' (tam giác trên)
4. **Bước 3**: Nối các cạnh bên
5. **Bước 4**: Hoàn thiện

---

### Test Hình Chóp
```
http://localhost:8001/api/mock/pyramid
```

### Test Lăng Trụ
```
http://localhost:8001/api/mock/prism
```

### Test Hình Lập Phương
```
http://localhost:8001/api/mock/cube
```

---

## ❌ XỬ LÝ LỖI THƯỜNG GẶP

### Lỗi 1: "python: command not found"
**Giải pháp**: 
- Cài Python từ python.org
- Hoặc dùng `python3` thay vì `python`

### Lỗi 2: "Port 8001 already in use"
**Giải pháp**:
```bash
# Đổi port khác
uvicorn app.main:app --reload --port 8002
```

### Lỗi 3: "No module named 'app'"
**Giải pháp**:
```bash
# Đảm bảo đang ở thư mục backend/
cd d:/Vy/CDNNLT/CK_NNLT_3D/prototype-3d/backend

# Activate venv
source venv/Scripts/activate

# Chạy lại
uvicorn app.main:app --reload --port 8001
```

### Lỗi 4: "venv\Scripts\activate: command not found"
**Giải pháp** (Git Bash):
```bash
source venv/Scripts/activate
```

**Giải pháp** (PowerShell):
```powershell
venv\Scripts\activate
```

### Lỗi 5: "Cannot import name 'routes'"
**Giải pháp**:
```bash
# Kiểm tra file có tồn tại không
ls app/api/routes.py

# Nếu không có, tạo lại file
```

---

## 📊 KIỂM TRA BACKEND HOẠT ĐỘNG

### Checklist:
- [ ] Backend chạy tại http://localhost:8001
- [ ] Swagger UI mở được tại http://localhost:8001/docs
- [ ] API `/api/mock/pyramid` trả về JSON
- [ ] API `/api/mock/prism` trả về JSON
- [ ] API `/api/mock/cube` trả về JSON
- [ ] POST `/api/solve` hoạt động

---

## 🎉 THÀNH CÔNG!

Nếu tất cả checklist đều ✅, backend đã sẵn sàng!

**Tiếp theo**:
1. Tạo frontend React app (tôi sẽ hướng dẫn tiếp)
2. Hoặc test API với Postman/Insomnia
3. Hoặc viết Python script để test

---

## 📝 GHI CHÚ

- **Backend port**: 8001 (khác với dự án chính là 8000)
- **Frontend port**: 5174 (khác với dự án chính là 5173)
- **Không ảnh hưởng**: Code trong `be/` và `fe/` không bị thay đổi
- **Tắt server**: Nhấn `Ctrl+C` trong terminal

---

## 🆘 CẦN TRỢ GIÚP?

Nếu gặp lỗi:
1. Copy toàn bộ error message
2. Check file `app/main.py` có tồn tại không
3. Check Python version: `python --version`
4. Check pip version: `pip --version`
