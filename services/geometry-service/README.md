# Hệ Thống Hỗ Trợ Giải Toán Hình Học Không Gian 3D

API Backend sử dụng FastAPI + Gemini AI để phân tích ảnh, giải toán và render hình học 3D.

## Cấu Trúc Thư Mục

```
be/
├── app/                              # Application code
│   ├── api/                          # API layer
│   │   └── routes/                   # API endpoints
│   │       ├── nguoi_dung.py         # User management API
│   │       ├── bai_toan.py           # Problem management API
│   │       └── geometry.py           # Geometry AI API (main)
│   │
│   ├── core/                         # Core configuration
│   │   ├── config.py                 # Settings & environment variables
│   │   └── database.py               # Database connection (SQL Server)
│   │
│   ├── models/                       # Pydantic models (Data validation)
│   │   ├── nguoi_dung.py             # User model
│   │   ├── bai_toan.py               # Problem model
│   │   ├── du_lieu_hinh_hoc.py       # Geometry data model
│   │   ├── loi_giai.py               # Solution model
│   │   └── dung_hinh_3d.py           # 3D drawing guide model
│   │
│   ├── repositories/                 # Data access layer
│   │   ├── nguoi_dung_repository.py  # User CRUD operations
│   │   ├── bai_toan_repository.py    # Problem CRUD operations
│   │   ├── du_lieu_hinh_hoc_repository.py
│   │   ├── loi_giai_repository.py
│   │   └── dung_hinh_3d_repository.py
│   │
│   └── services/                     # Business logic layer
│       ├── gemini_service.py         # Main AI service (orchestrator)
│       │
│       ├── ai/                       # AI-related services
│       │   ├── gemini_client.py      # Gemini API client
│       │   └── prompt.py             # All AI prompts (centralized)
│       │
│       └── renderer/                 # 3D rendering services
│           └── transform.py          # Transform to 3D coordinates
│
├── .env                              # Environment variables (API keys, DB config)
├── .gitignore                        # Git ignore rules
├── Dockerfile                        # Docker configuration
├── main.py                           # Application entry point
├── requirements.txt                  # Python dependencies
├── README.md                         # This file
└── HOW_TO_TEST.md                    # Testing guide
```

## Kiến Trúc Hệ Thống

### Layered Architecture (Clean Architecture)
```
┌─────────────────────────────────────────────────────────┐
│  API Layer (routes/)                                    │
│  - Nhận HTTP requests                                   │
│  - Validate input                                       │
│  - Trả về HTTP responses                               │
└────────────────┬────────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────────┐
│  Service Layer (services/)                              │
│  - Business logic                                       │
│  - Gọi Gemini AI                                        │
│  - Xử lý dữ liệu                                        │
└────────────────┬────────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────────┐
│  Repository Layer (repositories/)                       │
│  - Data access                                          │
│  - SQL queries                                          │
│  - CRUD operations                                      │
└────────────────┬────────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────────┐
│  Database (SQL Server)                                  │
│  - BAITOAN, DULIEUHINHHOC, LOIGIAI, DUNGHINH3D         │
└─────────────────────────────────────────────────────────┘
```

## Kiến Trúc Hệ Thống

### Layered Architecture (Clean Architecture)
```
┌─────────────────────────────────────────────────────────┐
│  API Layer (routes/)                                    │
│  - Nhận HTTP requests                                   │
│  - Validate input                                       │
│  - Trả về HTTP responses                               │
└────────────────┬────────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────────┐
│  Service Layer (services/)                              │
│  - Business logic                                       │
│  - Gọi Gemini AI                                        │
│  - Xử lý dữ liệu                                        │
└────────────────┬────────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────────┐
│  Repository Layer (repositories/)                       │
│  - Data access                                          │
│  - SQL queries                                          │
│  - CRUD operations                                      │
└────────────────┬────────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────────┐
│  Database (SQL Server)                                  │
│  - BAITOAN, DULIEUHINHHOC, LOIGIAI, DUNGHINH3D         │
└─────────────────────────────────────────────────────────┘
```

## Cài Đặt

### 1. Cài đặt dependencies
```cmd
cd d:\CDNNLT\Project_CK\be
pip install -r requirements.txt
```

### 2. Cấu hình môi trường (.env)
```env
# Database
DB_SERVER=localhost
DB_NAME=dbCDNNLT
DB_USER=sa
DB_PASSWORD=123456

# Gemini AI
GEMINI_API_KEY=your_api_key_here
```

### 3. Chạy database script
Chạy `dbCDNNLT.sql` trong SQL Server Management Studio

### 4. Khởi động server
```cmd
python main.py
```

Server sẽ chạy tại: http://localhost:8000

## API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Người Dùng (`/nguoi-dung`)
- `POST /nguoi-dung/` - Tạo người dùng
- `GET /nguoi-dung/` - Danh sách người dùng
- `GET /nguoi-dung/{id}` - Chi tiết người dùng
- `DELETE /nguoi-dung/{id}` - Xóa người dùng

### Bài Toán (`/bai-toan`)
- `POST /bai-toan/` - Tạo bài toán
- `GET /bai-toan/` - Danh sách bài toán
- `GET /bai-toan/{id}` - Chi tiết bài toán
- `GET /bai-toan/user/{user_id}` - Bài toán theo user

### Hình Học 3D (`/geometry`) - MAIN API
- `POST /geometry/upload-and-save` - Upload ảnh, phân tích và lưu (Gemini AI)
- `GET /geometry/problem/{id}` - Lấy thông tin đầy đủ bài toán
- `GET /geometry/solution/{id}` - Lấy lời giải (nếu có)
- `POST /geometry/solve-problem/{id}` - Giải bài toán bằng Gemini AI
- `GET /geometry/drawing-guide/{id}` - Lấy hướng dẫn dựng hình (nếu có)
- `POST /geometry/render-3d/{id}` - Tạo hướng dẫn dựng hình + code Three.js

## Flow Hoạt Động

```
1. Upload ảnh
   ↓
2. Gemini AI phân tích ảnh → Trích xuất đề bài
   ↓
3. Lưu vào BAITOAN + DULIEUHINHHOC
   ↓
4. User bấm "Giải" → Gemini AI giải toán
   ↓
5. Lưu vào LOIGIAI
   ↓
6. User bấm "Dựng hình 3D" → Gemini AI tạo hướng dẫn
   ↓
7. Lưu vào DUNGHINH3D (code Three.js + hướng dẫn)
```

## Kiến Trúc

### Layered Architecture
1. **API Layer** (`app/api/routes/`) - HTTP endpoints
2. **Service Layer** (`app/services/`) - Business logic + AI integration
3. **Repository Layer** (`app/repositories/`) - Data access
4. **Model Layer** (`app/models/`) - Data structures
5. **Core Layer** (`app/core/`) - Configuration & utilities

### AI Integration
- **Gemini AI**: Phân tích ảnh, OCR, giải toán, tạo hướng dẫn dựng hình
- **3D Renderer**: Chuyển đổi dữ liệu hình học sang tọa độ 3D
- **Prompts**: Tất cả prompts tập trung tại `app/services/ai/prompt.py`

## Development

### Chạy với auto-reload
```cmd
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Three.js Integration

### Bảng DUNGHINH3D
Lưu trữ hướng dẫn dựng hình 3D cho Three.js:
- `cacBuocVe`: JSON thứ tự các bước vẽ
- `hamThreeJS`: JSON danh sách hàm Three.js cần dùng
- `thamSo`: JSON tham số cho từng hàm
- `codeThreeJS`: Code Three.js đầy đủ (có thể chạy ngay)
- `huongDanVe`: Text hướng dẫn chi tiết

### API Endpoint
- `POST /geometry/render-3d/{ma_bai_toan}` - Tạo hướng dẫn Three.js và code hoàn chỉnh

### Three.js Functions Used

#### 1. Scene Management
- `new THREE.Scene()` - Tạo scene chính chứa tất cả objects
- `new THREE.PerspectiveCamera(fov, aspect, near, far)` - Camera góc nhìn phối cảnh
- `new THREE.WebGLRenderer()` - Renderer WebGL để vẽ lên canvas

#### 2. Geometry Creation
- `new THREE.BufferGeometry()` - Tạo geometry hiệu năng cao
- `new THREE.Vector3(x, y, z)` - Tạo điểm 3D với tọa độ
- `geometry.setFromPoints(points)` - Tạo geometry từ mảng điểm

#### 3. Materials & Objects
- `new THREE.LineBasicMaterial(options)` - Material cho đường thẳng
  - Options: `{ color: 0x0000ff }`
- `new THREE.MeshBasicMaterial(options)` - Material cho mặt phẳng
  - Options: `{ color: 0x00ff00, transparent: true, opacity: 0.5 }`
- `new THREE.Line(geometry, material)` - Tạo đường thẳng
- `new THREE.Mesh(geometry, material)` - Tạo mesh (mặt 3D)

#### 4. Lighting
- `new THREE.AmbientLight(color, intensity)` - Ánh sáng môi trường đồng đều
  - Example: `new THREE.AmbientLight(0x404040, 0.6)`
- `new THREE.DirectionalLight(color, intensity)` - Ánh sáng định hướng (như mặt trời)
  - Example: `new THREE.DirectionalLight(0xffffff, 0.8)`
  - Set position: `light.position.set(x, y, z)`

#### 5. Controls
- `new THREE.OrbitControls(camera, domElement)` - Cho phép xoay, zoom camera
  - `controls.enableDamping = true` - Bật hiệu ứng mượt mà
  - `controls.update()` - Cập nhật trong animation loop

#### 6. Animation
- `requestAnimationFrame(callback)` - Tạo animation loop
- `renderer.render(scene, camera)` - Render scene với camera

### Usage Flow
1. Upload ảnh → Phân tích → Lưu BAITOAN + DULIEUHINHHOC
2. Gọi `POST /geometry/render-3d/{id}` → Tạo code Three.js
3. Frontend nhận code và render 3D trực tiếp

### Response Format
```json
{
  "success": true,
  "message": "Đã tạo hướng dẫn dựng hình Three.js",
  "data": {
    "dungHinhId": 1,
    "threejs": {
      "steps": ["Bước 1...", "Bước 2..."],
      "functions": ["THREE.Scene()", "THREE.Camera()", ...],
      "parameters": {
        "camera": {"fov": 75, "position": [3,3,3]},
        "lights": {...},
        "materials": {...}
      },
      "code": "// Full Three.js code...",
      "guide": "HƯỚNG DẪN DỰNG HÌNH...\n1. Tạo các điểm:\n   - Điểm A tại (0,0,0)\n   - Điểm B tại (1,0,0)\n2. Vẽ các cạnh:\n   - Vẽ đoạn thẳng AB\n   - AB vuông góc với CD\n..."
    }
  }
}
```

### Example Guide Output (Generated by Gemini AI)
```
HƯỚNG DẪN DỰNG HÌNH CHÓP S.ABCD

Bước 1: Vẽ đáy ABCD là hình vuông
   - Vẽ hình vuông ABCD với cạnh a
   - Đảm bảo AB = BC = CD = DA = a
   - Các góc đều là góc vuông

Bước 2: Xác định điểm S (đỉnh chóp)
   - Từ A, dựng đường thẳng vuông góc với mặt phẳng (ABCD)
   - Trên đường thẳng đó, lấy điểm S sao cho SA vuông góc với (ABCD)

Bước 3: Xác định điểm M (trung điểm CD)
   - Trên cạnh CD, lấy điểm M sao cho CM = MD = a/2

Bước 4: Vẽ các cạnh bên
   - Nối S với A, B, C, D để tạo các cạnh bên
   - Vẽ đoạn thẳng SM

Bước 5: Hoàn thiện
   - Kiểm tra SA ⊥ (ABCD)
   - Kiểm tra M là trung điểm của CD
   - Tô màu hoặc đánh dấu các mặt để dễ nhìn

Lưu ý:
   - SA vuông góc với mặt phẳng đáy ABCD
   - M là trung điểm của CD
   - Khoảng cách giữa BC và SM cần tính theo đề bài
```

Hướng dẫn được tạo tự động bởi Gemini AI dựa trên đề bài thực tế, đảm bảo logic và dễ hiểu cho học sinh.


