# 🚀 QUICK START GUIDE

## Bắt đầu nhanh trong 5 phút

### 1. Setup Backend

```bash
# Di chuyển vào thư mục backend
cd prototype-3d/backend

# Tạo virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Chạy server
uvicorn app.main:app --reload --port 8001
```

✅ Backend chạy tại: http://localhost:8001
📚 API docs: http://localhost:8001/docs

---

### 2. Setup Frontend

```bash
# Mở terminal mới
cd prototype-3d/frontend

# Install dependencies
npm install

# Chạy dev server
npm run dev
```

✅ Frontend chạy tại: http://localhost:5174

---

### 3. Test

1. Mở browser: http://localhost:5174
2. Select mock data từ dropdown
3. Click "Load" để render 3D
4. Dùng controls để play animation

---

## Workflow phát triển

### Backend Development

1. **Tạo solver mới**:
   ```bash
   cd backend/app/solver
   # Tạo file mới, ví dụ: tetrahedron_solver.py
   ```

2. **Test solver**:
   ```bash
   pytest tests/test_solver.py
   ```

3. **Thêm endpoint**:
   - Sửa `app/api/routes.py`
   - Thêm route mới

### Frontend Development

1. **Tạo component mới**:
   ```bash
   cd frontend/src/components/ui
   # Tạo file .tsx mới
   ```

2. **Test visual**:
   - Chạy `npm run dev`
   - Mở browser và test

3. **Update Three.js logic**:
   - Sửa files trong `src/three/`
   - SceneManager, GeometryBuilder, etc.

---

## Mock Data

### Tạo mock data mới

1. Tạo file JSON trong `backend/mock_data/`:
   ```json
   {
     "shape_type": "pyramid",
     "constraints": {
       "base": { "type": "square", "side": 1 },
       "apex": { "height": 1.414 }
     }
   }
   ```

2. Test với API:
   ```bash
   curl -X POST http://localhost:8001/api/solve \
     -H "Content-Type: application/json" \
     -d @mock_data/pyramid.json
   ```

3. Copy response vào `frontend/public/mock-data/`

---

## Debugging

### Backend không chạy
- Check Python version (3.10+)
- Check port 8001 có bị chiếm không
- Check virtual environment đã activate chưa

### Frontend không render
- Check console browser (F12)
- Check API endpoint trong `src/services/api.ts`
- Check backend có chạy không

### Three.js không hiển thị
- Check canvas ref trong ThreeCanvas.tsx
- Check SceneManager initialization
- Check geometry data format

---

## Tips

- **Hot reload**: Backend và frontend đều hỗ trợ hot reload
- **Console logs**: Dùng `console.log()` để debug
- **API testing**: Dùng Swagger UI tại http://localhost:8001/docs
- **Git**: Commit thường xuyên, mỗi feature 1 commit

---

## Next Steps

1. ✅ Setup xong → Đọc `ARCHITECTURE.md`
2. ✅ Hiểu kiến trúc → Đọc `IMPLEMENTATION_PLAN.md`
3. ✅ Bắt đầu code → Follow plan từng ngày
4. ✅ Hoàn thành → Demo và integrate vào dự án chính

---

## Troubleshooting

### Port đã bị chiếm
```bash
# Backend: Đổi port trong command
uvicorn app.main:app --reload --port 8002

# Frontend: Đổi port trong vite.config.ts
```

### Dependencies lỗi
```bash
# Backend
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall

# Frontend
rm -rf node_modules package-lock.json
npm install
```

### Virtual environment lỗi
```bash
# Xóa và tạo lại
rm -rf venv
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

---

## Liên hệ

Nếu gặp vấn đề, check:
1. README.md trong từng thư mục
2. ARCHITECTURE.md
3. Code comments
