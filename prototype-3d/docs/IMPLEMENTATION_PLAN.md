# 📅 KẾ HOẠCH TRIỂN KHAI

## Timeline: 3 tuần

---

## 🔵 WEEK 1: Backend Geometry Engine

### Day 1-2: Setup & SymPy Solver cơ bản
- [ ] Setup Python project với FastAPI
- [ ] Install dependencies: sympy, numpy, fastapi, uvicorn
- [ ] Tạo `sympy_solver.py` với class `SymPySolver`
- [ ] Implement solver cho **hình chóp đơn giản**:
  - Đáy hình vuông
  - Đỉnh vuông góc đáy
  - Test với 1 bài toán mẫu

**Output**: API endpoint `/api/solve` trả về tọa độ cho 1 hình chóp

### Day 3-4: Mở rộng Solver
- [ ] Implement solver cho **lăng trụ**
- [ ] Implement solver cho **hình lập phương**
- [ ] Xử lý điểm đặc biệt:
  - Trung điểm
  - Chân đường cao
  - Giao điểm
- [ ] Test với 5 bài toán khác nhau

**Output**: Solver hỗ trợ 3 dạng hình cơ bản

### Day 5: Steps Generator
- [ ] Tạo `steps_generator.py`
- [ ] Logic tạo thứ tự dựng hình:
  - Phân tích topology
  - Sắp xếp theo dependency
  - Generate description cho mỗi step
- [ ] Test với 3 hình đã có

**Output**: API trả về cả `steps` array

### Day 6-7: Testing & Documentation
- [ ] Viết unit tests
- [ ] Tạo 10 mock data files (JSON)
- [ ] Document API với Swagger
- [ ] README cho backend

**Output**: Backend hoàn chỉnh, tested, documented

---

## 🟢 WEEK 2: Frontend Three.js Renderer

### Day 1-2: Setup React + Three.js
- [ ] Create React app với Vite + TypeScript
- [ ] Install dependencies: three, @types/three, zustand
- [ ] Setup project structure (folders)
- [ ] Tạo `SceneManager.ts` (vanilla Three.js):
  - Init scene, camera, renderer
  - Lights, grid, axes
  - OrbitControls
  - Animation loop
- [ ] Tạo `ThreeCanvas.tsx` (React wrapper)
- [ ] Test render 1 cube đơn giản

**Output**: React app render được Three.js scene cơ bản

### Day 3-4: GeometryBuilder
- [ ] Tạo `GeometryBuilder.ts`
- [ ] Implement methods:
  - `createPoint()` - sphere + label
  - `createEdge()` - line
  - `createFace()` - mesh
- [ ] Tạo `MaterialLibrary.ts` (quản lý materials)
- [ ] Test với mock data hardcoded

**Output**: Render được geometry từ JSON data

### Day 5: Dynamic Data Loading
- [ ] Tạo `api.ts` service
- [ ] Connect với backend API
- [ ] Tạo `DataInput` component (select mock data)
- [ ] Zustand store setup
- [ ] Test load data từ backend

**Output**: Frontend fetch và render data từ backend

### Day 6-7: UI & Controls
- [ ] Tạo `ControlPanel` component
- [ ] Tạo `AnimationControls` component:
  - Play/Pause button
  - Next/Prev buttons
  - Step indicator
- [ ] Styling với CSS
- [ ] Responsive layout

**Output**: UI hoàn chỉnh, có thể control animation

---

## 🟡 WEEK 3: Animation & Polish

### Day 1-2: Animation System
- [ ] Tạo `AnimationController.ts`
- [ ] Implement step-by-step animation:
  - Filter objects theo step
  - Fade in/out animations
  - Smooth transitions
- [ ] Connect với UI controls
- [ ] Test animation flow

**Output**: Animation hoạt động mượt mà

### Day 3: Camera & Interactions
- [ ] Auto-fit camera (bounding box)
- [ ] Click handlers:
  - Click point → highlight
  - Hover edge → change color
- [ ] Tooltips (tên điểm, tọa độ)

**Output**: Tương tác tốt, camera tự động

### Day 4: Labels & Annotations
- [ ] Improve text labels (canvas texture)
- [ ] Add measurement lines (optional)
- [ ] Add angle indicators (optional)
- [ ] Color coding (base vs apex vs special points)

**Output**: Visualization rõ ràng, dễ hiểu

### Day 5: Testing & Bug Fixes
- [ ] Test với tất cả 10 mock data
- [ ] Fix bugs
- [ ] Performance optimization
- [ ] Cross-browser testing

**Output**: Stable, no major bugs

### Day 6-7: Documentation & Demo
- [ ] README cho frontend
- [ ] User guide (cách sử dụng)
- [ ] Record demo video
- [ ] Prepare presentation

**Output**: Prototype hoàn chỉnh, ready to demo

---

## 📊 Milestones

### Milestone 1 (End of Week 1)
✅ Backend API hoạt động, trả về tọa độ chính xác cho 3 dạng hình

### Milestone 2 (End of Week 2)
✅ Frontend render được geometry từ backend, có UI controls

### Milestone 3 (End of Week 3)
✅ Prototype hoàn chỉnh với animation, interactions, documentation

---

## 🎯 Success Criteria

- [ ] Backend solver tính đúng tọa độ cho ít nhất 3 dạng hình
- [ ] Frontend render chính xác geometry từ JSON
- [ ] Animation step-by-step hoạt động mượt
- [ ] UI responsive, dễ sử dụng
- [ ] Code clean, có comments
- [ ] Documentation đầy đủ

---

## 🚀 Next Steps (Sau prototype)

1. **Integration vào dự án chính**:
   - Copy solver vào `be/app/services/solver/`
   - Copy Three.js classes vào `fe/src/`
   - Update API routes

2. **Mở rộng**:
   - Thêm nhiều dạng hình hơn
   - Gemini AI integration
   - Database persistence
   - User authentication

3. **Production**:
   - Deploy backend
   - Deploy frontend
   - CI/CD setup
   - Monitoring

---

## 📝 Notes

- Ưu tiên **hoàn thành core features** trước khi polish
- Test thường xuyên với mock data
- Commit code mỗi ngày
- Document khi code, không để sau
