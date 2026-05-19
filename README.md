# Hệ Thống Hỗ Trợ Giải Toán Hình Học Không Gian 3D

Hệ thống microservices sử dụng FastAPI + Gemini AI để phân tích ảnh đề bài, giải toán hình học không gian và render mô hình 3D trực tiếp trên trình duyệt với Three.js.

---

## Cấu Trúc Thư Mục

```
📦 geo3d/
├── 🔒 .env
├── 🔒 .env.example
├── 🙈 .gitignore
├── 🐳 docker-compose.yml
├── 🗄️  dbCDNNLT.sql
├── 📖 README.md
│
├── 📂 services/
│   ├── 📂 auth-service/
│   │   ├── 📂 app/
│   │   │   ├── 🐍 __init__.py
│   │   │   ├── 📂 api/
│   │   │   │   ├── 🐍 __init__.py
│   │   │   │   └── 📂 routes/
│   │   │   │       ├── 🐍 __init__.py
│   │   │   │       ├── 🐍 auth.py
│   │   │   │       └── 🐍 nguoi_dung.py
│   │   │   ├── 📂 core/
│   │   │   │   ├── 🐍 __init__.py
│   │   │   │   ├── 🐍 config.py
│   │   │   │   └── 🐍 database.py
│   │   │   ├── 📂 models/
│   │   │   │   ├── 🐍 __init__.py
│   │   │   │   └── 🐍 nguoi_dung.py
│   │   │   └── 📂 repositories/
│   │   │       ├── 🐍 __init__.py
│   │   │       └── 🐍 nguoi_dung_repository.py
│   │   ├── 🐍 main.py
│   │   ├── 📄 requirements.txt
│   │   └── 🐳 Dockerfile
│   │
│   ├── 📂 geometry-service/
│   │   ├── 📂 app/
│   │   │   ├── 📂 api/
│   │   │   │   └── 📂 routes/
│   │   │   │       ├── 🐍 geometry.py
│   │   │   │       └── 🐍 bai_toan.py
│   │   │   ├── 📂 core/
│   │   │   │   ├── 🐍 config.py
│   │   │   │   └── 🐍 database.py
│   │   │   ├── 📂 models/
│   │   │   │   ├── 🐍 bai_toan.py
│   │   │   │   ├── 🐍 du_lieu_hinh_hoc.py
│   │   │   │   ├── 🐍 loi_giai.py
│   │   │   │   ├── 🐍 dung_hinh_3d.py
│   │   │   │   └── 🐍 dung_hinh_3d_loi_giai.py
│   │   │   ├── 📂 repositories/
│   │   │   │   ├── 🐍 bai_toan_repository.py
│   │   │   │   ├── 🐍 du_lieu_hinh_hoc_repository.py
│   │   │   │   ├── 🐍 loi_giai_repository.py
│   │   │   │   ├── 🐍 dung_hinh_3d_repository.py
│   │   │   │   └── 🐍 dunghinh3d_loigiai_repository.py
│   │   │   └── 📂 services/
│   │   │       ├── 🐍 gemini_service.py
│   │   │       ├── 🐍 solution_geometry_service.py
│   │   │       ├── 🐍 file_search_service.py
│   │   │       ├── 📂 ai/
│   │   │       │   ├── 🐍 gemini_client.py
│   │   │       │   └── 🐍 prompt.py
│   │   │       └── 📂 renderer/
│   │   │           └── 🐍 transform.py
│   │   ├── 📂 Documents/
│   │   │   ├── 📕 Tom_tat_ly_thuyet_Hinh_khong_gian.pdf
│   │   │   └── 📕 tong-hop-ly-thuyet-va-cong-thuc-tinh-nhanh-hinh-hoc-12.pdf
│   │   ├── 📂 uploads/
│   │   ├── 🐍 main.py
│   │   ├── 📄 requirements.txt
│   │   ├── 🐳 Dockerfile
│   │   ├── 🐍 check_models.py
│   │   ├── 🐍 check_quota.py
│   │   ├── 🖥️  start.bat
│   │   ├── 🖥️  test_db.bat
│   │   ├── 🗃️  .file_search_cache.json
│   │   ├── 🙈 .gitignore
│   │   ├── 📖 README.md
│   │   └── 📖 START_BACKEND.md
│   │
│   └── 📂 search-service/
│       ├── 📂 app/
│       │   ├── 🐍 __init__.py
│       │   ├── 📂 api/
│       │   │   ├── 🐍 __init__.py
│       │   │   └── 📂 routes/
│       │   │       ├── 🐍 __init__.py
│       │   │       └── 🐍 search.py
│       │   ├── 📂 core/
│       │   │   ├── 🐍 __init__.py
│       │   │   ├── 🐍 config.py
│       │   │   └── 🐍 database.py
│       │   ├── 📂 models/
│       │   │   ├── 🐍 __init__.py
│       │   │   └── 🐍 bai_toan_tuong_tu_cache.py
│       │   ├── 📂 repositories/
│       │   │   ├── 🐍 __init__.py
│       │   │   └── 🐍 bai_toan_tuong_tu_cache_repository.py
│       │   └── 📂 services/
│       │       ├── 🐍 __init__.py
│       │       ├── 🐍 similar_problems_service.py
│       │       ├── 🐍 web_search_service.py
│       │       ├── 🐍 file_search_service.py
│       │       └── 📂 ai/
│       │           ├── 🐍 __init__.py
│       │           ├── 🐍 gemini_client.py
│       │           └── 🐍 prompt.py
│       ├── 📂 Documents/
│       │   ├── 📕 Tom_tat_ly_thuyet_Hinh_khong_gian.pdf
│       │   └── 📕 tong-hop-ly-thuyet-va-cong-thuc-tinh-nhanh-hinh-hoc-12.pdf
│       ├── 🐍 main.py
│       ├── 📄 requirements.txt
│       ├── 🐳 Dockerfile
│       └── 🗃️  .file_search_cache.json
│
└── 📂 fe/
    ├── 📂 pages/
    │   ├── 🌐 index.html
    │   ├── 🌐 login.html
    │   ├── 🌐 solver.html
    │   ├── 🌐 history.html
    │   ├── 🌐 profile.html
    │   ├── 🌐 practice.html
    │   ├── 🌐 docs.html
    │   ├── 🌐 test_history_load.html
    │   └── 🌐 test_similar.html
    ├── 📂 src/
    │   ├── ⚛️  main.tsx
    │   ├── ⚛️  App.tsx
    │   ├── 📂 components/
    │   │   ├── ⚛️  ThreeScene.tsx
    │   │   └── ⚛️  Pyramid.tsx
    │   ├── 📂 three/
    │   │   ├── 🟦 index.ts
    │   │   ├── 🟦 ThreeViewer.ts
    │   │   ├── 🟦 SceneManager.ts
    │   │   ├── 🟦 GeometryBuilder.ts
    │   │   ├── 🟦 MaterialLibrary.ts
    │   │   ├── 🟦 AnnotationRenderer.ts
    │   │   ├── 🟦 AnnotationAdapter.ts
    │   │   └── 🟦 types.ts
    │   ├── 📂 services/
    │   │   └── 🟦 api.ts
    │   └── 📂 types/
    │       └── 🟦 geometry.ts
    ├── 📂 js/
    │   ├── 🟨 api.js
    │   ├── 🟨 auth.js
    │   ├── 🟨 google-auth.js
    │   ├── 🟨 config.js
    │   ├── 🟨 topbar.js
    │   ├── 🟨 home.js
    │   ├── 🟨 history.js
    │   ├── 🟨 script.js
    │   ├── 🟨 three-viewer.js
    │   ├── 🟨 three.min.js
    │   ├── 🟨 OrbitControls.js
    │   └── 📂 components/
    │       └── 📂 home/
    │           ├── 🟨 hero.js
    │           ├── 🟨 features.js
    │           ├── 🟨 benefits.js
    │           ├── 🟨 pricing.js
    │           └── 🟨 testimonials.js
    ├── 📂 css/
    │   ├── 🎨 home.css
    │   ├── 🎨 history.css
    │   ├── 🎨 practice.css
    │   ├── 🎨 profile.css
    │   ├── 🎨 docs.css
    │   └── 🎨 three-viewer.css
    ├── 📂 assets/
    │   └── 📂 images/
    │       ├── 🖼️  banner.jpg
    │       ├── 🎬 bg_hero.mp4
    │       ├── 🎬 bg_card2.mp4
    │       ├── 🖼️  bg_static.avif
    │       └── 🎬 video.mp4
    ├── 🌐 index.html
    ├── 🎨 styles.css
    ├── 📦 package.json
    ├── 📦 package-lock.json
    ├── 🟦 tsconfig.json
    ├── 🟦 tsconfig.node.json
    ├── ⚙️  vite.config.ts
    ├── ⚙️  vite.config.three.ts
    └── 🐳 Dockerfile
```

---

## Kiến Trúc Hệ Thống

### Microservices Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  Frontend  (fe/ — cổng 5173)                                │
│  TypeScript + React + Three.js + Vite                       │
└──────┬──────────────┬──────────────┬───────────────────────┘
       │              │              │
       ▼              ▼              ▼
┌────────────┐ ┌────────────┐ ┌────────────────────────────┐
│auth-service│ │search-     │ │geometry-service (cổng 8000)│
│(cổng 8003) │ │service     │ │  - Upload & phân tích ảnh  │
│  - Đăng    │ │(cổng 8002) │ │  - Giải toán (Gemini AI)   │
│    nhập    │ │  - Tìm bài │ │  - Sinh hướng dẫn dựng hình│
│  - Google  │ │    tương tự│ │  - Render 3D (Three.js)    │
│    OAuth   │ │  - Web     │ │  - File search (PDF)       │
│  - CRUD    │ │    search  │ └────────────────────────────┘
│    user    │ └────────────┘
└────────────┘
       │              │              │
       └──────────────┴──────────────┘
                      │
              ┌───────▼────────┐
              │  SQL Server    │
              │  dbCDNNLT      │
              └────────────────┘
```

### Layered Architecture (mỗi service)

```
┌─────────────────────────────────────────────────────────┐
│  API Layer  (app/api/routes/)                           │
│  Nhận HTTP request · Validate input · Trả response      │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│  Service Layer  (app/services/)                         │
│  Business logic · Gọi Gemini AI · Xử lý dữ liệu        │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│  Repository Layer  (app/repositories/)                  │
│  Data access · SQL queries · CRUD operations            │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│  Database  (SQL Server)                                 │
│  NGUOIDUNG · BAITOAN · DULIEUHINHHOC                    │
│  LOIGIAI · DUNGHINH3D · DUNGHINH3D_LOIGIAI              │
│  BAI_TOAN_TUONG_TU_CACHE                                │
└─────────────────────────────────────────────────────────┘
```

---

## Cơ Sở Dữ Liệu

```
NGUOIDUNG ──────────────────────────────────────────────────┐
  maNguoiDung (PK) · tenDangNhap · email · matKhau · vaiTro │
                                                             │
BAITOAN ─────────────────────────────────────────────────── ┤
  maBaiToan (PK) · maNguoiDung (FK) · duongDan              │
  deBaiTho · loaiHinh · tomTatDe · ngayTao                  │
       │                                                     │
       ├──► DULIEUHINHHOC                                    │
       │      toaDoDiem (JSON) · cacCanh (JSON)              │
       │      cacQuanHe (JSON)                               │
       │                                                     │
       ├──► DUNGHINH3D                                       │
       │      cacBuocVe · hamThreeJS · thamSo                │
       │      codeThreeJS · huongDanVe                       │
       │                                                     │
       └──► LOIGIAI                                          │
              cacBuocGiai (JSON) · ketQuaCuoi                │
              congThucSuDung (JSON)                          │
                   │                                         │
                   └──► DUNGHINH3D_LOIGIAI                   │
                          cacBuocVe · codeThreeJS            │
                          huongDanVe (bổ sung theo lời giải) │
                                                             │
BAI_TOAN_TUONG_TU_CACHE ────────────────────────────────────┘
  tuKhoa (UNIQUE) · ketQua (JSON) · ngayTao · lanCapNhat
```

---

## Flow Hoạt Động

```
1. Upload ảnh đề bài
   ↓
2. geometry-service: Gemini AI phân tích ảnh → trích xuất đề bài
   ↓
3. Lưu vào BAITOAN + DULIEUHINHHOC (tọa độ điểm, cạnh, quan hệ)
   ↓
4. Frontend render mô hình 3D cơ bản từ DULIEUHINHHOC
   ↓
5. User bấm "Giải" → Gemini AI sinh lời giải từng bước
   ↓
6. Lưu vào LOIGIAI
   ↓
7. User bấm "Dựng hình 3D" → Gemini AI sinh code Three.js + hướng dẫn
   ↓
8. Lưu vào DUNGHINH3D + DUNGHINH3D_LOIGIAI
   ↓
9. Frontend phát lại dựng hình từng bước + hiển thị annotation
   ↓
10. search-service: Tìm bài toán tương tự (cache + Gemini + web search)
```

---

## Cài Đặt & Khởi Động

### Yêu cầu
- Docker & Docker Compose
- SQL Server (local hoặc cloud)
- Google Gemini API key

### 1. Cấu hình môi trường

Sao chép `.env.example` thành `.env` và điền các giá trị:

```env
# Database
DB_SERVER=localhost
DB_NAME=dbCDNNLT
DB_USER=sa
DB_PASSWORD=your_password

# Gemini AI
GEMINI_API_KEY=your_api_key_here

# Google OAuth (auth-service)
GOOGLE_CLIENT_ID=your_google_client_id
```

### 2. Khởi tạo database

Chạy `dbCDNNLT.sql` trong SQL Server Management Studio.

### 3. Chạy với Docker Compose

```bash
docker-compose up --build
```

| Service           | URL                        |
|-------------------|----------------------------|
| geometry-service  | http://localhost:8000       |
| geometry-service docs | http://localhost:8000/docs |
| search-service    | http://localhost:8002       |
| auth-service      | http://localhost:8003       |
| frontend          | http://localhost:5173       |

### 4. Chạy từng service thủ công (development)

```bash
# geometry-service
cd services/geometry-service
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# search-service
cd services/search-service
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8002

# auth-service
cd services/auth-service
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8003

# frontend
cd fe
npm install
npm run dev
```

---

## API Endpoints

### geometry-service (`/geometry`) — API chính

| Method | Endpoint | Mô tả |
|--------|----------|-------|
| `POST` | `/geometry/upload-and-save` | Upload ảnh, Gemini phân tích và lưu bài toán |
| `GET`  | `/geometry/problem/{id}` | Lấy thông tin đầy đủ bài toán |
| `POST` | `/geometry/solve-problem/{id}` | Giải bài toán bằng Gemini AI |
| `GET`  | `/geometry/solution/{id}` | Lấy lời giải |
| `POST` | `/geometry/render-3d/{id}` | Sinh hướng dẫn dựng hình + code Three.js |
| `GET`  | `/geometry/drawing-guide/{id}` | Lấy hướng dẫn dựng hình |

### geometry-service (`/bai-toan`)

| Method | Endpoint | Mô tả |
|--------|----------|-------|
| `POST` | `/bai-toan/` | Tạo bài toán |
| `GET`  | `/bai-toan/` | Danh sách bài toán |
| `GET`  | `/bai-toan/{id}` | Chi tiết bài toán |
| `GET`  | `/bai-toan/user/{user_id}` | Bài toán theo user |

### auth-service

| Method | Endpoint | Mô tả |
|--------|----------|-------|
| `POST` | `/auth/login` | Đăng nhập |
| `POST` | `/auth/register` | Đăng ký |
| `POST` | `/auth/google` | Đăng nhập Google OAuth |
| `GET`  | `/nguoi-dung/` | Danh sách người dùng |
| `GET`  | `/nguoi-dung/{id}` | Chi tiết người dùng |

### search-service

| Method | Endpoint | Mô tả |
|--------|----------|-------|
| `POST` | `/search/similar` | Tìm bài toán tương tự |

---

## Three.js Module Architecture

```
fe/src/three/
├── ThreeViewer.ts          # Điểm vào: khởi tạo renderer, vòng lặp animation
├── SceneManager.ts         # Quản lý scene, camera (PerspectiveCamera), ánh sáng
├── GeometryBuilder.ts      # Tạo điểm, đoạn thẳng, mặt phẳng, đa diện
├── MaterialLibrary.ts      # Vật liệu: màu sắc, độ trong suốt, wireframe
├── AnnotationRenderer.ts   # Render nhãn 2D (screen-space projection)
├── AnnotationAdapter.ts    # Chuyển đổi dữ liệu annotation từ API response
└── types.ts                # Định nghĩa kiểu dữ liệu hình học
```

### AI Integration

- **Gemini AI**: Phân tích ảnh (OCR + parse hình học), sinh lời giải từng bước, sinh code Three.js và hướng dẫn dựng hình
- **File Search**: Tìm kiếm trong tài liệu PDF lý thuyết hình học để bổ sung ngữ cảnh cho AI
- **Web Search**: DuckDuckGo search để tìm bài toán tương tự trên internet
- **Prompts**: Tập trung tại `app/services/ai/prompt.py` trong mỗi service
