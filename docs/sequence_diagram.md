# Sequence Diagrams - 3D Geometry Problem Solving System

## 1. Overall Flow

```mermaid
sequenceDiagram
    actor User as 👤 User
    participant FE as 🖥️ Frontend
    participant API as ⚡ FastAPI
    participant Gemini as 🤖 Gemini AI
    participant DB as 🗄️ SQL Server

    User->>FE: Upload problem image
    FE->>API: POST /geometry/upload-and-save
    API->>Gemini: Analyze image (OCR + Extract)
    Gemini-->>API: Return problem + points + relationships
    API->>DB: Save BAITOAN + DULIEUHINHHOC
    DB-->>API: maBaiToan
    API-->>FE: extraction + visualization + maBaiToan

    User->>FE: Click "Render 3D"
    FE->>API: POST /geometry/render-3d/{id}
    API->>DB: Get BAITOAN + DULIEUHINHHOC
    API->>API: GeometrySolver.solve_from_extraction()
    API->>DB: Save DUNGHINH3D
    API-->>FE: geometry data + Three.js code

    User->>FE: Click "Solve Problem"
    FE->>API: POST /geometry/solve-problem/{id}
    API->>DB: Get BAITOAN
    API->>Gemini: Solve problem from text
    Gemini-->>API: steps + result + formulas
    API->>DB: Save LOIGIAI
    API-->>FE: detailed solution
```

---

## 2. Step 1: Upload and Image Analysis

```mermaid
sequenceDiagram
    actor User as 👤 User
    participant FE as 🖥️ Frontend
    participant API as ⚡ FastAPI /upload-and-save
    participant GeminiSvc as 🔧 GeminiService
    participant GeminiClient as 📡 GeminiClient
    participant GeminiAPI as 🤖 Gemini API
    participant Renderer as 🎨 GeometryRenderer
    participant DB as 🗄️ SQL Server

    User->>FE: Select image + (optional) enter user ID
    FE->>API: POST /upload-and-save\n(file, ma_nguoi_dung?)

    Note over API: Parse ma_nguoi_dung\n"" or None → user_id = None\n"1" → user_id = 1

    API->>GeminiSvc: analyze_image(image_bytes)
    GeminiSvc->>GeminiClient: extract_geometry_from_image(image)

    Note over GeminiClient: Prepare image\nConvert RGBA→RGB\nSave temp .jpg file

    GeminiClient->>GeminiAPI: files.upload(tmp_path)
    GeminiAPI-->>GeminiClient: uploaded_file

    GeminiClient->>GeminiAPI: models.generate_content\n(prompt + uploaded_file)
    GeminiAPI-->>GeminiClient: JSON response

    Note over GeminiClient: Parse JSON\nFix LaTeX escapes\nFix variable 'a'\nCreate GeometryExtraction

    GeminiClient-->>GeminiSvc: GeometryExtraction object
    GeminiSvc-->>API: dict {problem_text, points, relationships, ...}

    API->>Renderer: transform_to_3d(geometry_data)
    Renderer-->>API: {points, edges, faces, camera_position}

    API->>DB: INSERT INTO BAITOAN\n(maNguoiDung, duongDan, deBaiTho, loaiHinh, tomTatDe)
    DB-->>API: maBaiToan (auto-increment)

    API->>DB: INSERT INTO DULIEUHINHHOC\n(maBaiToan, toaDoDiem, cacCanh, cacQuanHe)
    DB-->>API: duLieuId

    API-->>FE: {success, maBaiToan, extraction, visualization, saved}

    alt No ma_nguoi_dung (Guest)
        Note over FE: saved = false\nNo history
    else Has ma_nguoi_dung (Logged-in)
        Note over FE: saved = true\nHas history
    end
```

---

## 3. Step 2: 3D Rendering

```mermaid
sequenceDiagram
    actor User as 👤 User
    participant FE as 🖥️ Frontend
    participant API as ⚡ FastAPI /render-3d/{id}
    participant GeomSolver as 🔢 GeometrySolver
    participant DB as 🗄️ SQL Server

    User->>FE: Click "Render 3D"
    FE->>API: POST /geometry/render-3d/{maBaiToan}

    API->>DB: SELECT * FROM BAITOAN WHERE maBaiToan = ?
    DB-->>API: bai_toan data

    API->>DB: SELECT * FROM DUNGHINH3D WHERE maBaiToan = ?
    DB-->>API: existing (if any)

    alt Already cached
        API-->>FE: {fromCache: true, geometry, threejs}
    else Not cached
        API->>DB: SELECT * FROM DULIEUHINHHOC WHERE maBaiToan = ?
        DB-->>API: du_lieu (toaDoDiem, cacCanh, cacQuanHe)

        Note over API: Prepare extraction_data\nfrom BAITOAN + DULIEUHINHHOC

        API->>GeomSolver: solve_from_extraction(extraction_data, problem_type)

        Note over GeomSolver: Analyze shape type\nCalculate 3D coordinates\nCreate edges, faces\nGenerate instruction steps

        GeomSolver-->>API: geometry_data\n{points, edges, faces, steps, annotations}

        Note over API: Create rendering guide\nGenerate Three.js data

        API->>DB: INSERT INTO DUNGHINH3D\n(maBaiToan, cacBuocVe, hamThreeJS,\nthamSo, codeThreeJS, huongDanVe)
        DB-->>API: dungHinhId

        API-->>FE: {success, geometry, threejs, fromCache: false}
    end

    FE->>FE: Render 3D with React Three Fiber\nOrbitControls (rotate, zoom)
```

---

## 4. Step 3: Problem Solving

```mermaid
sequenceDiagram
    actor User as 👤 User
    participant FE as 🖥️ Frontend
    participant API as ⚡ FastAPI /solve-problem/{id}
    participant GeminiSvc as 🔧 GeminiService
    participant GeminiAPI as 🤖 Gemini API
    participant DB as 🗄️ SQL Server

    User->>FE: Click "Solve Problem"
    FE->>API: POST /geometry/solve-problem/{maBaiToan}

    API->>DB: SELECT * FROM BAITOAN WHERE maBaiToan = ?
    DB-->>API: bai_toan (deBaiTho, loaiHinh, ...)

    API->>DB: SELECT * FROM LOIGIAI WHERE maBaiToan = ?
    DB-->>API: existing_solution (if any)

    alt Solution exists (cached)
        API-->>FE: {fromCache: true, solution}
    else No solution yet
        API->>GeminiSvc: solve_problem(problem_text)
        GeminiSvc->>GeminiAPI: generate_content(solve_prompt)

        Note over GeminiAPI: Analyze problem\nApply formulas\nCalculate step by step

        GeminiAPI-->>GeminiSvc: JSON {steps, result, formulas_used}

        Note over GeminiSvc: Parse JSON\nFix LaTeX escapes

        GeminiSvc-->>API: {steps, result, formulas_used}

        API->>DB: INSERT INTO LOIGIAI\n(maBaiToan, cacBuocGiai,\nketQuaCuoi, congThucSuDung)
        DB-->>API: loiGiaiId

        API-->>FE: {success, loiGiaiId, solution, fromCache: false}
    end

    FE->>FE: Display step-by-step solution
```

---

## 5. User Management

```mermaid
sequenceDiagram
    actor Admin as 👤 Admin/User
    participant FE as 🖥️ Frontend
    participant API as ⚡ FastAPI /nguoi-dung
    participant DB as 🗄️ SQL Server

    Admin->>FE: Create account
    FE->>API: POST /nguoi-dung/\n{tenDangNhap, email, matKhau, vaiTro}
    API->>DB: INSERT INTO NGUOIDUNG
    DB-->>API: maNguoiDung
    API-->>FE: {message, maNguoiDung}

    Admin->>FE: View list
    FE->>API: GET /nguoi-dung/
    API->>DB: SELECT * FROM NGUOIDUNG
    DB-->>API: list users
    API-->>FE: [{maNguoiDung, tenDangNhap, email, ...}]

    Admin->>FE: View details
    FE->>API: GET /nguoi-dung/{id}
    API->>DB: SELECT * FROM NGUOIDUNG WHERE maNguoiDung = ?
    DB-->>API: user data
    API-->>FE: user object

    Admin->>FE: Delete user
    FE->>API: DELETE /nguoi-dung/{id}
    API->>DB: DELETE FROM NGUOIDUNG WHERE maNguoiDung = ?
    DB-->>API: rowcount
    API-->>FE: {message: "Deleted successfully"}
```

---

## 6. View History (Logged-in User)

```mermaid
sequenceDiagram
    actor User as 👤 Logged-in User
    participant FE as 🖥️ Frontend
    participant API as ⚡ FastAPI
    participant DB as 🗄️ SQL Server

    User->>FE: View problem history
    FE->>API: GET /bai-toan/user/{maNguoiDung}
    API->>DB: SELECT * FROM BAITOAN\nWHERE maNguoiDung = ?
    DB-->>API: list bai_toan
    API-->>FE: [{maBaiToan, loaiHinh, tomTatDe, ngayTao, ...}]

    User->>FE: Select old problem
    FE->>API: GET /geometry/problem/{maBaiToan}
    API->>DB: SELECT BAITOAN + DULIEUHINHHOC + LOIGIAI
    DB-->>API: full problem data
    API-->>FE: {baiToan, duLieuHinhHoc, loiGiai}

    User->>FE: View solution again
    FE->>API: GET /geometry/solution/{maBaiToan}
    API->>DB: SELECT * FROM LOIGIAI WHERE maBaiToan = ?
    DB-->>API: loi_giai
    API-->>FE: {steps, result, formulas_used}

    User->>FE: View 3D rendering again
    FE->>API: GET /geometry/drawing-guide/{maBaiToan}
    API->>DB: SELECT * FROM DUNGHINH3D WHERE maBaiToan = ?
    DB-->>API: dung_hinh
    API-->>FE: {geometry, guide, threejs}
```

---

## 7. Comparison: Guest vs Logged-in

```mermaid
sequenceDiagram
    actor Guest as 👤 Guest
    actor LoggedIn as 👤 Logged-in User
    participant API as ⚡ FastAPI
    participant DB as 🗄️ SQL Server

    Note over Guest, DB: GUEST FLOW

    Guest->>API: POST /upload-and-save\n(file, ma_nguoi_dung=None)
    API->>DB: INSERT BAITOAN (maNguoiDung=NULL)
    DB-->>API: maBaiToan=5
    API-->>Guest: {saved: false, maBaiToan: 5}

    Guest->>API: POST /render-3d/5
    API-->>Guest: geometry data ✅

    Guest->>API: POST /solve-problem/5
    API-->>Guest: solution ✅

    Note over Guest: No history\nCannot review later

    Note over LoggedIn, DB: LOGGED-IN FLOW

    LoggedIn->>API: POST /upload-and-save\n(file, ma_nguoi_dung=1)
    API->>DB: INSERT BAITOAN (maNguoiDung=1)
    DB-->>API: maBaiToan=6
    API-->>LoggedIn: {saved: true, maBaiToan: 6}

    LoggedIn->>API: POST /render-3d/6
    API-->>LoggedIn: geometry data ✅

    LoggedIn->>API: POST /solve-problem/6
    API-->>LoggedIn: solution ✅

    Note over LoggedIn: Has history\nCan review anytime ✅
```

---

## 8. Layered Architecture

```mermaid
sequenceDiagram
    participant Route as 📍 API Route Layer
    participant Service as 🔧 Service Layer
    participant Repo as 📦 Repository Layer
    participant DB as 🗄️ Database Layer

    Note over Route, DB: Example: solve-problem/{id}

    Route->>Repo: bai_toan_repo.get_by_id(id)
    Repo->>DB: execute_query(SELECT...)
    DB-->>Repo: dict result
    Repo-->>Route: bai_toan dict

    Route->>Service: gemini_service.solve_problem(text)
    Service->>Service: build_solve_prompt(text)
    Service->>Service: gemini_client.generate_content(prompt)
    Service-->>Route: {steps, result, formulas}

    Route->>Repo: loi_giai_repo.create_from_dict(data)
    Repo->>DB: execute_query(INSERT...)
    DB-->>Repo: new id
    Repo-->>Route: loiGiaiId

    Route-->>Route: return JSON response
```
