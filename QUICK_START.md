# 🚀 Quick Start - Chạy Backend Nhanh

## Cách 1: Dùng Script (Đơn Giản Nhất)

### Windows

```bash
# Mở Command Prompt hoặc PowerShell
cd E:\CDNNLT\Project_CK\be
start.bat
```

Script sẽ tự động:
- ✅ Check Python
- ✅ Check dependencies
- ✅ Install nếu thiếu
- ✅ Start server

## Cách 2: Chạy Thủ Công

### Bước 1: Cài Dependencies

```bash
cd E:\CDNNLT\Project_CK\be
pip install -r requirements.txt
```

### Bước 2: Test Database

```bash
cd E:\CDNNLT\Project_CK\be
test_db.bat
```

Phải thấy: `✅ Database connection successful!`

### Bước 3: Start Server

```bash
cd E:\CDNNLT\Project_CK\be
py -m uvicorn main:app --reload --port 8000
```

## Kiểm Tra Server Đang Chạy

### Test 1: Health Check

Mở browser:
```
http://127.0.0.1:8000/health
```

Phải thấy:
```json
{"status":"healthy","version":"1.0.0"}
```

### Test 2: API Docs

```
http://127.0.0.1:8000/docs
```

Phải thấy Swagger UI

### Test 3: Frontend

```
http://127.0.0.1:8000/fe/pages/index.html
```

Phải thấy trang chủ

## Các Lệnh Hữu Ích

```bash
# Cài dependencies
cd be
pip install -r requirements.txt

# Test database
cd be
test_db.bat

# Test Gemini API
cd be
python test_gemini.py

# Start server
cd be
start.bat

# hoặc
cd be
py -m uvicorn main:app --reload --port 8000

# Stop server
Ctrl + C
```

## Troubleshooting Nhanh

### ❌ "Python not found"
**Fix**: Cài Python từ https://www.python.org/downloads/

### ❌ "pip not found"
**Fix**: 
```bash
python -m ensurepip --upgrade
```

### ❌ "Database connection failed"
**Fix**:
1. Check SQL Server đang chạy
2. Check file `.env`:
   ```env
   DB_SERVER=localhost
   DB_NAME=dbCDNNLT
   DB_USER=sa
   DB_PASSWORD=123456
   ```

### ❌ "Port 8000 already in use"
**Fix**:
```bash
# Kill process
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# hoặc dùng port khác
py -m uvicorn main:app --reload --port 8001
```

### ❌ "ModuleNotFoundError"
**Fix**:
```bash
cd be
pip install -r requirements.txt
```

## Checklist

- [ ] Python đã cài (3.8+)
- [ ] SQL Server đang chạy
- [ ] Database `dbCDNNLT` đã tạo
- [ ] File `.env` đã cấu hình
- [ ] Dependencies đã cài
- [ ] Test database thành công
- [ ] Server khởi động thành công

## URLs Quan Trọng

| URL | Mô tả |
|-----|-------|
| http://127.0.0.1:8000 | Root API |
| http://127.0.0.1:8000/health | Health check |
| http://127.0.0.1:8000/docs | API documentation |
| http://127.0.0.1:8000/fe/pages/index.html | Trang chủ |
| http://127.0.0.1:8000/fe/pages/solver.html | Giải bài |
| http://127.0.0.1:8000/fe/pages/history.html | Lịch sử |

## Cấu Trúc Thư Mục

```
be/
├── start.bat              ← Chạy file này để start server
├── test_db.bat           ← Test database connection
├── test_gemini.py        ← Test Gemini API
├── requirements.txt      ← Dependencies
├── .env                  ← Configuration
├── main.py              ← Entry point
└── app/
    ├── api/
    │   └── routes/      ← API endpoints
    ├── core/
    │   ├── config.py    ← Settings
    │   └── database.py  ← Database connection
    ├── models/          ← Database models
    ├── repositories/    ← Data access
    └── services/        ← Business logic
```

## Next Steps

Sau khi server chạy thành công:

1. ✅ Test upload ảnh
2. ✅ Test xem lịch sử
3. ✅ Test các tính năng khác

---

**Bắt đầu ngay:**
```bash
cd E:\CDNNLT\Project_CK\be
start.bat
```

🚀 **Good luck!**
