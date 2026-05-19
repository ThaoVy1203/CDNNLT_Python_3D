# 🚀 Hướng Dẫn Chạy Backend

## Bước 1: Cài Đặt Dependencies

### Option 1: Cài Từng Package (Recommended)

```bash
cd be

# Core packages
pip install fastapi==0.115.0
pip install uvicorn[standard]==0.32.0
pip install pydantic==2.10.0
pip install python-dotenv==1.0.1
pip install email-validator==2.2.0

# Database
pip install pymssql

# Google Gemini AI
pip install google-genai

# Image processing
pip install Pillow
```

### Option 2: Cài Từ requirements.txt

```bash
cd be
pip install -r requirements.txt
```

## Bước 2: Kiểm Tra Cấu Hình

### 2.1. Kiểm Tra .env File

File: `be/.env`

```env
# Database Configuration
DB_SERVER=localhost
DB_NAME=dbCDNNLT
DB_USER=sa
DB_PASSWORD=123456

# Gemini AI API Key
GEMINI_API_KEY=AIzaSyBi9TFRtH4O-KwdLAaOg_3Ngh3mPSQ61Q0

# Gemini Model
GEMINI_MODEL=gemini-1.5-flash

# CORS Origins
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

### 2.2. Test Database Connection

```bash
cd be
python -c "from app.core.database import DatabaseConnection; db = DatabaseConnection(); print('✅ Database connection successful!')"
```

**Kết quả mong đợi**:
```
✅ Database connection successful!
```

**Nếu lỗi**:
- Check SQL Server đang chạy
- Check DB_SERVER, DB_NAME, DB_USER, DB_PASSWORD trong .env
- Check database `dbCDNNLT` đã tạo chưa

### 2.3. Test Gemini API

```bash
cd be
python test_gemini.py
```

**Kết quả mong đợi**:
```
============================================================
GEMINI API TEST
============================================================

1. Checking API key...
✅ API key found: AIzaSyBi9TFRtH4O-Kwd...

2. Configuring Gemini...
✅ Gemini configured with model: gemini-1.5-flash

3. Listing available models...
Available models:
  - models/gemini-1.5-flash
  - models/gemini-1.5-pro

4. Testing text generation...
✅ Response: Hello, Gemini API is working!

============================================================
TEST COMPLETE
============================================================
```

## Bước 3: Khởi Động Backend

### Option 1: Development Mode (Recommended)

```bash
cd be
py -m uvicorn main:app --reload --port 8000
```

hoặc

```bash
cd be
python -m uvicorn main:app --reload --port 8000
```

### Option 2: Production Mode

```bash
cd be
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Bước 4: Kiểm Tra Backend Đang Chạy

### 4.1. Xem Terminal Output

Phải thấy:
```
🤖 Using Gemini model: gemini-1.5-flash
INFO:     Will watch for changes in these directories: ['E:\\CDNNLT\\Project_CK\\be']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxxx] using WatchFiles
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
✅ Serving frontend from: E:\CDNNLT\Project_CK\fe
✅ Serving uploads from: E:\CDNNLT\Project_CK\be\uploads
```

### 4.2. Test Health Endpoint

Mở browser hoặc dùng curl:
```
http://127.0.0.1:8000/health
```

**Kết quả mong đợi**:
```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

### 4.3. Test API Docs

Mở browser:
```
http://127.0.0.1:8000/docs
```

Phải thấy Swagger UI với tất cả endpoints.

## Bước 5: Test Frontend

### 5.1. Mở Trang Chủ

```
http://127.0.0.1:8000/fe/pages/index.html
```

### 5.2. Mở Trang Giải Bài

```
http://127.0.0.1:8000/fe/pages/solver.html
```

### 5.3. Test Upload

1. Click "Chọn ảnh"
2. Chọn một ảnh hình học
3. Đợi phân tích
4. Phải thấy: "Đã phân tích thành công!"

## Troubleshooting

### Lỗi 1: "ModuleNotFoundError: No module named 'fastapi'"

**Giải pháp**:
```bash
pip install fastapi uvicorn
```

### Lỗi 2: "ModuleNotFoundError: No module named 'pymssql'"

**Giải pháp**:
```bash
pip install pymssql
```

### Lỗi 3: "ModuleNotFoundError: No module named 'google.genai'"

**Giải pháp**:
```bash
pip install google-genai
```

### Lỗi 4: "Database connection failed"

**Giải pháp**:
1. Check SQL Server đang chạy
2. Check .env file
3. Test connection:
   ```bash
   python -c "from app.core.database import DatabaseConnection; db = DatabaseConnection(); print('OK')"
   ```

### Lỗi 5: "Port 8000 already in use"

**Giải pháp**:
```bash
# Dùng port khác
py -m uvicorn main:app --reload --port 8001
```

hoặc kill process đang dùng port 8000:
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Lỗi 6: "GEMINI_API_KEY not found"

**Giải pháp**:
1. Check file `.env` có tồn tại không
2. Check có dòng `GEMINI_API_KEY=...`
3. Restart backend

## Quick Start Script

Tạo file `start.bat` (Windows):

```batch
@echo off
echo ========================================
echo Starting Geo3D Backend Server
echo ========================================

cd /d "%~dp0"

echo.
echo Checking Python...
python --version
if errorlevel 1 (
    echo ERROR: Python not found!
    pause
    exit /b 1
)

echo.
echo Starting server...
python -m uvicorn main:app --reload --port 8000

pause
```

Hoặc `start.sh` (Linux/Mac):

```bash
#!/bin/bash
echo "========================================"
echo "Starting Geo3D Backend Server"
echo "========================================"

cd "$(dirname "$0")"

echo ""
echo "Checking Python..."
python3 --version || { echo "ERROR: Python not found!"; exit 1; }

echo ""
echo "Starting server..."
python3 -m uvicorn main:app --reload --port 8000
```

## Checklist

- [ ] Python đã cài (version 3.8+)
- [ ] Pip đã cài
- [ ] SQL Server đang chạy
- [ ] Database `dbCDNNLT` đã tạo
- [ ] File `.env` đã cấu hình đúng
- [ ] Dependencies đã cài (pip install -r requirements.txt)
- [ ] Database connection test thành công
- [ ] Gemini API test thành công
- [ ] Backend khởi động thành công
- [ ] Health endpoint trả về OK
- [ ] Frontend accessible qua /fe

## Useful Commands

```bash
# Stop server
Ctrl + C

# Restart server
Ctrl + C
py -m uvicorn main:app --reload --port 8000

# Check running processes
netstat -ano | findstr :8000

# View logs
# Logs hiển thị trực tiếp trong terminal

# Clear Python cache
find . -type d -name __pycache__ -exec rm -rf {} +
# hoặc Windows:
for /d /r . %d in (__pycache__) do @if exist "%d" rd /s /q "%d"
```

## Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| DB_SERVER | SQL Server host | localhost | Yes |
| DB_NAME | Database name | dbCDNNLT | Yes |
| DB_USER | Database user | sa | Yes |
| DB_PASSWORD | Database password | 123456 | Yes |
| GEMINI_API_KEY | Google Gemini API key | - | Yes |
| GEMINI_MODEL | Gemini model name | gemini-1.5-flash | No |
| CORS_ORIGINS | Allowed CORS origins | * | No |

## Production Deployment

### Using Gunicorn (Linux)

```bash
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Using Docker

```bash
docker build -t geo3d-backend .
docker run -p 8000:8000 geo3d-backend
```

### Using systemd (Linux)

Create `/etc/systemd/system/geo3d.service`:

```ini
[Unit]
Description=Geo3D Backend
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/Project_CK/be
Environment="PATH=/usr/bin"
ExecStart=/usr/bin/python3 -m uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

Then:
```bash
sudo systemctl enable geo3d
sudo systemctl start geo3d
sudo systemctl status geo3d
```

---

**Ready to start? Run:**
```bash
cd be
py -m uvicorn main:app --reload --port 8000
```

🚀 **Happy coding!**
