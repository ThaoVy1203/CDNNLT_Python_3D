# 🧪 PROTOTYPE: React + Geometry Engine + Three.js

## 📋 Mục đích
Thư mục này dùng để **test và phát triển** hệ thống dựng hình 3D động, **KHÔNG ảnh hưởng** đến code chính ở `be/` và `fe/`.

## ⚡ CHẠY NGAY (2 phút)

### Terminal 1: Backend
```bash
cd prototype-3d/backend
python -m venv venv
source venv/Scripts/activate  # Git Bash
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
```
✅ http://localhost:8001

### Terminal 2: Frontend
```bash
cd prototype-3d/frontend
npm install
npm run dev
```
✅ http://localhost:5174

## 🎮 Sử dụng

1. Mở http://localhost:5174
2. Chọn hình (Pyramid/Prism/Cube)
3. Click "Tải hình"
4. Click ▶ để xem animation từng bước
5. Dùng chuột xoay/zoom hình 3D

## 🏗️ Kiến trúc

```
prototype-3d/
├── backend/          # Python backend với SymPy solver
├── frontend/         # React + Three.js app
└── docs/             # Tài liệu thiết kế
```

## 🎯 Mục tiêu

### ✅ Đã hoàn thành
- [x] Backend API với SymPy solver
- [x] Tính tọa độ 3D cho 3 dạng hình (pyramid, prism, cube)
- [x] Generate steps dựng hình logic
- [x] Frontend React + Three.js
- [x] Render 3D động từ API
- [x] Animation từng bước
- [x] UI controls (play, pause, next, prev)
- [x] Tương tác (xoay, zoom)

### 🚧 Đang phát triển
- [ ] Thêm nhiều dạng hình hơn
- [ ] Cải thiện animation (fade in/out)
- [ ] Thêm labels động
- [ ] Export hình ảnh

## 📦 Tech Stack

**Backend**:
- Python 3.10+
- FastAPI
- SymPy (symbolic math)
- NumPy (numerical computation)

**Frontend**:
- React 18
- TypeScript
- Three.js (vanilla, không dùng R3F)
- Zustand (state management)
- Vite (build tool)

## 🔗 Kết nối với dự án chính

Sau khi prototype hoàn thiện:
1. Copy backend solver vào `be/app/services/solver/`
2. Copy frontend components vào `fe/src/components/three/`
3. Update API routes trong `be/app/api/routes/geometry.py`
4. Integrate vào `fe/pages/solver.html` hoặc migrate sang React

## ⚠️ Lưu ý

- **KHÔNG** sửa code trong `be/` và `fe/`
- **KHÔNG** connect với database `dbCDNNLT`
- Dùng mock data hoặc SQLite local
- Commit riêng branch `prototype-3d`

## 📝 Ghi chú

- Tạo ngày: 2026-05-05
- Mục đích: Test và phát triển hệ thống 3D rendering
- Trạng thái: 🚧 Đang xây dựng
