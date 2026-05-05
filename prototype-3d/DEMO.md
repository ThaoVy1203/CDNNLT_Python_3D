# 🎬 DEMO - Hướng dẫn sử dụng

## 🎯 Mục tiêu Demo

Demo này cho thấy hệ thống **dựng hình 3D từng bước** hoạt động như thế nào.

---

## 📸 Screenshots

### 1. Giao diện chính
```
┌─────────────────────────────────────────────────────┐
│  🧪 Prototype: Dựng hình 3D                         │
│  React + Geometry Engine + Three.js                 │
├──────────────┬──────────────────────────────────────┤
│              │                                       │
│  Controls    │         Canvas 3D                    │
│              │                                       │
│  [Chọn hình] │      [Hình chóp 3D]                 │
│  [Animation] │                                       │
│  [Settings]  │                                       │
│              │                                       │
└──────────────┴──────────────────────────────────────┘
```

---

## 🎮 Workflow Demo

### Demo 1: Hình Chóp S.ABCD

**Bước 1: Chọn hình**
- Click radio button "Hình chóp (Pyramid)"
- Click nút "Tải hình"
- ⏱️ Đợi 1-2 giây

**Bước 2: Xem hình 3D**
- Hình chóp xuất hiện trên canvas
- Dùng chuột:
  - Kéo trái: Xoay
  - Cuộn: Zoom
  - Kéo phải: Pan

**Bước 3: Xem animation**
- Click nút ▶ (Play)
- Quan sát các bước:
  1. Vẽ đáy ABCD (4 điểm + 4 cạnh xuất hiện)
  2. Dựng đỉnh S (điểm S xuất hiện)
  3. Nối các cạnh bên (4 cạnh từ S xuất hiện)
  4. Hoàn thiện (toàn bộ hình)

**Bước 4: Điều khiển thủ công**
- Click ⏸ để pause
- Click ⏩ để next step
- Click ⏪ để prev step
- Click vào từng bước trong danh sách

---

### Demo 2: Lăng Trụ ABC.A'B'C'

**Bước 1: Chọn hình**
- Click "Lăng trụ (Prism)"
- Click "Tải hình"

**Bước 2: Xem animation**
- Click ▶
- Quan sát:
  1. Vẽ đáy ABC (tam giác)
  2. Vẽ đỉnh A'B'C' (tam giác trên)
  3. Nối các cạnh bên
  4. Hoàn thiện

---

### Demo 3: Hình Lập Phương

**Bước 1: Chọn hình**
- Click "Hình lập phương (Cube)"
- Click "Tải hình"

**Bước 2: Xem animation**
- Click ▶
- Quan sát 4 bước dựng hình

---

## 🎨 Tính năng nổi bật

### 1. Animation từng bước
- ✅ Hiển thị từng bước dựng hình
- ✅ Smooth transitions
- ✅ Có thể pause/resume
- ✅ Có thể jump đến bất kỳ bước nào

### 2. Tương tác 3D
- ✅ Xoay 360° (OrbitControls)
- ✅ Zoom in/out
- ✅ Pan (di chuyển)
- ✅ Auto-fit camera

### 3. UI Controls
- ✅ Play/Pause
- ✅ Next/Previous step
- ✅ Progress bar
- ✅ Step list (click để jump)
- ✅ Toggle grid/axes

### 4. Responsive
- ✅ Hoạt động trên desktop
- ✅ Canvas tự động resize
- ⚠️ Mobile chưa optimize

---

## 📊 So sánh với dự án chính

| Tính năng | Prototype | Dự án chính (fe/) |
|-----------|-----------|-------------------|
| **3D Rendering** | ✅ Dynamic | ❌ Static SVG |
| **Animation** | ✅ Step-by-step | ❌ Hardcoded |
| **Data source** | ✅ API Backend | ❌ Hardcoded |
| **Tương tác** | ✅ Xoay/Zoom | ❌ Không có |
| **Dạng hình** | ✅ 3 dạng | ❌ 1 dạng |

---

## 🚀 Next Steps

### Integrate vào dự án chính

1. **Copy backend solver**:
   ```bash
   cp -r prototype-3d/backend/app/solver be/app/services/solver
   ```

2. **Copy frontend components**:
   ```bash
   cp -r prototype-3d/frontend/src/three fe/src/three
   cp -r prototype-3d/frontend/src/components/three fe/src/components/three
   ```

3. **Update API routes**:
   - Thêm endpoints vào `be/app/api/routes/geometry.py`

4. **Integrate vào solver.html**:
   - Option 1: Migrate sang React
   - Option 2: Embed React component vào HTML

---

## 💡 Tips Demo

### Để demo ấn tượng:

1. **Chuẩn bị trước**:
   - Chạy backend và frontend
   - Test 1 lần trước khi demo
   - Mở sẵn browser

2. **Trong khi demo**:
   - Bắt đầu với hình chóp (đơn giản nhất)
   - Giải thích từng bước animation
   - Show tương tác (xoay, zoom)
   - So sánh với HTML tĩnh

3. **Highlight**:
   - "Tự động tính tọa độ từ backend"
   - "Animation từng bước giúp học sinh hiểu"
   - "Có thể xoay để xem mọi góc độ"
   - "Dễ dàng thêm dạng hình mới"

---

## 🎥 Video Demo (Optional)

Nếu muốn record video:

1. **Tool**: OBS Studio hoặc Windows Game Bar
2. **Duration**: 2-3 phút
3. **Script**:
   - 0:00 - Giới thiệu
   - 0:30 - Chọn hình và load
   - 1:00 - Xem animation
   - 1:30 - Tương tác (xoay/zoom)
   - 2:00 - Thử hình khác
   - 2:30 - Kết luận

---

## 📝 Feedback

Sau khi demo, thu thập feedback về:
- [ ] Animation có mượt không?
- [ ] UI có dễ dùng không?
- [ ] Có bug gì không?
- [ ] Cần thêm tính năng gì?
