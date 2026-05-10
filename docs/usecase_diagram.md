# Use Cases - 3D Geometry Problem Solving System

## Actors and Their Use Cases

### 👤 Guest User
**Description:** User without login, using the system temporarily

**Use Cases:**

#### 1. Upload Problem Image
- **Input:** Image file (JPG, PNG, max 10MB), optional user ID
- **Output:** 
  - Success: `{maBaiToan, extraction data, visualization, saved: false}`
  - Error: Error message (invalid format, file too large, AI error)

#### 2. View Extracted Problem
- **Input:** `maBaiToan` (from upload step)
- **Output:** 
  - Problem text
  - Problem type (pyramid, prism, tetrahedron, cube)
  - List of points: `[{name: "A", coordinates: [x,y,z]}, ...]`
  - Relationships: `[{type: "perpendicular", entities: ["SA", "(ABC)"]}, ...]`
  - Given conditions: `["AB = 3", "SA ⊥ (ABC)", ...]`
  - Questions: `["Calculate volume", "Find distance", ...]`

#### 3. Generate 3D Model
- **Input:** `maBaiToan`
- **Output:**
  - 3D coordinates: `{A: [0,0,0], B: [1,0,0], ...}`
  - Edges: `[{start: "A", end: "B", style: "solid"}, ...]`
  - Faces: `[{vertices: ["A","B","C"], color: "#fff"}, ...]`
  - Camera position: `[5, 5, 5]`
  - Construction steps: `["Step 1: Draw base ABCD", ...]`

#### 4. Rotate or Zoom 3D Model
- **Input:** Mouse/touch gestures (drag, scroll, pinch)
- **Output:** Updated camera position and orientation in real-time

#### 5. Solve Problem with AI
- **Input:** `maBaiToan`
- **Output:**
  - Solution steps: `["Step 1: Analyze...", "Step 2: Apply formula...", ...]`
  - Final result: `"Volume = 24 cm³"`
  - Formulas used: `["V = (1/3) × S × h", "S = a²", ...]`
  - LaTeX formulas for rendering

#### 6. View Detailed Solution
- **Input:** `maBaiToan`
- **Output:**
  - Step-by-step solution with LaTeX formulas
  - Intermediate calculations
  - Final answer highlighted
  - Formulas explanation

#### 7. View Drawing Guide
- **Input:** `maBaiToan`
- **Output:**
  - Step-by-step drawing instructions
  - Order of construction: `["1. Draw base square ABCD", "2. Draw apex S above A", ...]`
  - Tips and notes for each step

#### 8. Register Account
- **Input:** 
  - Username (3-50 characters)
  - Email (valid format)
  - Password (min 6 characters)
  - Role: "Member" (default)
- **Output:**
  - Success: `{maNguoiDung: "ND001", message: "Account created"}`
  - Error: "Username/email already exists"

**Limitations:**
- ❌ Cannot save problem history
- ❌ Cannot review past problems
- ❌ Data lost when closing browser

---

### 👤 Registered User
**Description:** User with account, can save and review history

**Use Cases:**

#### 1. Login
- **Input:** 
  - Username or Email
  - Password
- **Output:**
  - Success: `{maNguoiDung, tenDangNhap, email, vaiTro, token}`
  - Error: "Invalid credentials"

#### 2-8. Same as Guest User (Upload, View, Generate, etc.)
- **Difference:** All actions are saved with `maNguoiDung`
- **Output includes:** `saved: true` flag

#### 9. View Problem History
- **Input:** `maNguoiDung` (from session)
- **Output:**
  - List of problems: `[{maBaiToan, loaiHinh, tomTatDe, ngayTao, hasLoiGiai, hasDungHinh}, ...]`
  - Sorted by date (newest first)
  - Pagination: page number, items per page

#### 10. Review Past Problems
- **Input:** `maBaiToan` (from history)
- **Output:**
  - Complete problem data (extraction, 3D model, solution)
  - All previously generated content
  - Cached data (no AI call needed)

#### 11. Delete Own Problems
- **Input:** `maBaiToan` (must belong to user)
- **Output:**
  - Success: `{message: "Problem deleted"}`
  - Error: "Not authorized" or "Problem not found"

#### 12. Logout
- **Input:** Session token
- **Output:** 
  - Success: `{message: "Logged out"}`
  - Session cleared

**Advantages:**
- ✅ Save all completed problems
- ✅ Review anytime
- ✅ Track learning progress

---

### 👥 Admin
**Description:** System administrator with highest privileges

**Use Cases:**

#### 1. Admin Login
- **Input:** 
  - Username (admin account)
  - Password
- **Output:**
  - Success: `{maNguoiDung, vaiTro: "Admin", token}`
  - Error: "Invalid credentials" or "Not authorized"

#### 2. View User List
- **Input:** 
  - Optional: page number, search query, filter by role
- **Output:**
  - List of users: `[{maNguoiDung, tenDangNhap, email, vaiTro, ngayTao}, ...]`
  - Total count
  - Pagination info

#### 3. Create New User
- **Input:**
  - Username
  - Email
  - Password
  - Role: "Member" or "Admin"
- **Output:**
  - Success: `{maNguoiDung: "ND001", message: "User created"}`
  - Auto-generated ID: ND001, ND002, ND003...

#### 4. View User Details
- **Input:** `maNguoiDung`
- **Output:**
  - User info: `{maNguoiDung, tenDangNhap, email, vaiTro, ngayTao}`
  - Statistics: total problems, total solutions
  - Recent activity

#### 5. Delete User
- **Input:** `maNguoiDung`
- **Output:**
  - Success: `{message: "User deleted"}`
  - Cascade: All user's problems set to `maNguoiDung = NULL`

#### 6. Change User Role
- **Input:** 
  - `maNguoiDung`
  - New role: "Member" or "Admin"
- **Output:**
  - Success: `{message: "Role updated to Admin"}`

#### 7. View All Problems
- **Input:** 
  - Optional: filter by user, date range, problem type
- **Output:**
  - List of all problems from all users
  - `[{maBaiToan, maNguoiDung, loaiHinh, ngayTao}, ...]`

#### 8. Delete Any Problem
- **Input:** `maBaiToan` (any user's problem)
- **Output:**
  - Success: `{message: "Problem deleted"}`
  - Cascade: Delete related data (DULIEUHINHHOC, LOIGIAI, DUNGHINH3D)

#### 9. View System Statistics
- **Input:** Optional date range
- **Output:**
  - Total users: `{total, members, admins}`
  - Total problems: `{total, by_type: {pyramid: 50, prism: 30, ...}}`
  - Total solutions generated
  - API usage: `{gemini_calls, cache_hits, cache_misses}`
  - Storage: `{database_size, image_storage}`

**Privileges:**
- ✅ Manage all users
- ✅ Access all data
- ✅ Delete/edit any information

---

### 🤖 Gemini AI (External System)
**Description:** External AI system providing intelligent features

**Use Cases (called by system):**

#### 1. Analyze Problem Image
- **Input:** 
  - Image file (JPEG/PNG, converted to RGB)
  - Prompt with extraction instructions
- **Output:**
  - JSON with structured data:
    ```json
    {
      "problem_text": "Cho hình chóp S.ABCD...",
      "problem_type": "Hình chóp tứ giác",
      "confidence_score": 0.95,
      "given_conditions": ["ABCD là hình vuông", "AB = 4", ...],
      "questions": ["Tính thể tích", ...],
      "points": [{"name": "A", "coordinates": null}, ...],
      "relationships": [{"type": "perpendicular", "entities": ["SA", "(ABCD)"]}, ...]
    }
    ```

#### 2. Extract Points and Relationships
- **Input:** Problem text or image
- **Output:**
  - Points: `[{name: "A", coordinates: [x,y,z]}, ...]`
  - Lines: `[{point1: "A", point2: "B"}, ...]`
  - Relations: `[{type: "perpendicular", entities: ["AB", "CD"]}, ...]`

#### 3. Solve Problem Step-by-Step
- **Input:** 
  - Problem text
  - Prompt with solving instructions
- **Output:**
  - JSON with solution:
    ```json
    {
      "steps": [
        "Bước 1: Xác định đáy ABCD là hình vuông cạnh 4",
        "Bước 2: Tính diện tích đáy: $S = 4^2 = 16$ cm²",
        "Bước 3: Chiều cao h = SA = 6 cm",
        "Bước 4: Áp dụng công thức: $V = \\frac{1}{3} S h$",
        "Bước 5: $V = \\frac{1}{3} \\times 16 \\times 6 = 32$ cm³"
      ],
      "result": "Thể tích hình chóp S.ABCD là 32 cm³",
      "formulas_used": [
        "$S_{\\text{hình vuông}} = a^2$",
        "$V_{\\text{chóp}} = \\frac{1}{3} S h$"
      ]
    }
    ```

#### 4. Generate Drawing Guide
- **Input:** 
  - Problem text
  - Shape type
- **Output:**
  - Step-by-step drawing instructions:
    ```
    HƯỚNG DẪN DỰNG HÌNH CHÓP S.ABCD
    
    Bước 1: Vẽ hình vuông ABCD cạnh 4cm trên mặt phẳng ngang
    - Đặt A tại gốc tọa độ
    - Vẽ AB = 4cm theo trục x
    - Vẽ AD = 4cm theo trục z
    - Hoàn thành hình vuông ABCD
    
    Bước 2: Dựng đỉnh S
    - Từ A, vẽ đường thẳng vuông góc với mặt phẳng (ABCD)
    - Lấy điểm S sao cho SA = 6cm
    
    Bước 3: Nối các cạnh bên
    - Nối S với B, C, D
    - Các cạnh SA, SB, SC, SD là cạnh bên của hình chóp
    ```

---

## Use Case Details Summary

### Data Flow Example: Complete Problem Solving

**Step 1: Upload**
```
Input:  image.jpg, ma_nguoi_dung="ND001"
Output: {maBaiToan: 1, extraction: {...}, saved: true}
```

**Step 2: Generate 3D**
```
Input:  maBaiToan=1
Output: {points: {A:[0,0,0], ...}, edges: [...], fromCache: false}
```

**Step 3: Solve**
```
Input:  maBaiToan=1
Output: {steps: [...], result: "32 cm³", fromCache: false}
```

**Step 4: Review Later**
```
Input:  maBaiToan=1
Output: {extraction: {...}, 3d: {...}, solution: {...}, fromCache: true}
```

---

## Input/Output Validation Rules

### Image Upload
- **Accepted formats:** JPG, JPEG, PNG
- **Max size:** 10MB
- **Min dimensions:** 100x100 pixels
- **Max dimensions:** 4096x4096 pixels

### User Registration
- **Username:** 3-50 characters, alphanumeric + underscore
- **Email:** Valid email format, unique
- **Password:** Min 6 characters

### Problem ID
- **maBaiToan:** Positive integer (auto-increment)
- **maNguoiDung:** Format "ND001", "ND002", ... or NULL (guest)

---

**Document Version:** 2.0  
**Last Updated:** 2026-05-07  
**Status:** ✅ Complete with Input/Output

---

## Use Case Details

### 1. Upload Problem Image
- **Actor:** Guest, Registered User
- **Input:** Image file (JPG, PNG)
- **Output:** Problem text, points, relationships
- **AI:** Gemini analyzes image

### 2. Generate 3D Model
- **Actor:** Guest, Registered User
- **Input:** Extracted geometry data
- **Output:** Three.js 3D model
- **Logic:** GeometrySolver calculates 3D coordinates

### 3. Solve Problem with AI
- **Actor:** Guest, Registered User
- **Input:** Problem text
- **Output:** Solution steps, formulas, result
- **AI:** Gemini solves problem

### 4. View Problem History
- **Actor:** Registered User, Admin
- **Input:** maNguoiDung (User ID)
- **Output:** Problem list (type, date, status)
- **Database:** Query BAITOAN table

### 5. Manage Users
- **Actor:** Admin
- **Operations:** 
  - Create user (auto-generate ID: ND001, ND002...)
  - View user list
  - Delete user
  - Change role (Member ↔ Admin)

---

## Use Case Priority

### High Priority (Must Have)
1. ✅ Upload problem image
2. ✅ Generate 3D model
3. ✅ Solve problem with AI
4. ✅ View solution
5. ✅ Register/Login

### Medium Priority (Should Have)
6. ✅ View problem history
7. ✅ Rotate/zoom 3D model
8. ✅ View drawing guide
9. ✅ Manage users (Admin)

### Low Priority (Nice to Have)
10. ⏳ Export solution as PDF
11. ⏳ Share problem
12. ⏳ Practice mode
13. ⏳ Learning statistics

---

## Comparison: Guest vs Registered User

| Feature | Guest | Registered User |
|---------|-------|-----------------|
| Upload image | ✅ | ✅ |
| Generate 3D model | ✅ | ✅ |
| Solve with AI | ✅ | ✅ |
| View solution | ✅ | ✅ |
| Save history | ❌ | ✅ |
| Review past problems | ❌ | ✅ |
| Delete problems | ❌ | ✅ (own only) |
| Manage users | ❌ | ❌ |

---

**Document Version:** 1.0  
**Last Updated:** 2026-05-07  
**Status:** ✅ Complete
