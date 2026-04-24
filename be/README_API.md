# Hướng Dẫn Chạy API FastAPI

## Yêu Cầu Hệ Thống

1. Python 3.8+
2. SQL Server với database `dbCDNNLT` đã được tạo
3. ODBC Driver 17 for SQL Server

## Cài Đặt ODBC Driver (nếu chưa có)

Tải và cài đặt từ: https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server

## Các Bước Chạy

### 1. Cài đặt dependencies

```cmd
cd d:\CDNNLT\Project_CK\be
pip install -r requirements.txt
```

### 2. Cấu hình database

Kiểm tra file `.env` và cập nhật thông tin kết nối nếu cần:
```
DB_SERVER=localhost
DB_NAME=dbCDNNLT
DB_USER=sa
DB_PASSWORD=123456
DB_DRIVER=ODBC Driver 17 for SQL Server
```

### 3. Chạy database script

Chạy file `dbCDNNLT.sql` trong SQL Server Management Studio để tạo database và tables.

### 4. Khởi động server

```cmd
cd d:\CDNNLT\Project_CK\be
python main.py
```

Hoặc sử dụng uvicorn trực tiếp:
```cmd
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 5. Truy cập API Documentation

Mở trình duyệt và truy cập:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 6. Test API bằng script

Mở terminal mới và chạy:
```cmd
cd d:\CDNNLT\Project_CK\be
python test_api.py
```

## Cấu Trúc Thư Mục

```
be/
├── database/
│   ├── config.py          # Cấu hình database
│   └── connection.py      # Quản lý kết nối
├── models/
│   ├── nguoi_dung.py      # Model người dùng
│   ├── bai_toan.py        # Model bài toán
│   ├── du_lieu_hinh_hoc.py
│   └── loi_giai.py
├── repositories/
│   ├── nguoi_dung_repository.py
│   └── bai_toan_repository.py
├── routes/
│   ├── nguoi_dung_routes.py
│   └── bai_toan_routes.py
├── .env                   # Cấu hình môi trường
├── main.py               # Entry point
└── test_api.py           # Script test API
```

## API Endpoints

### Người Dùng
- `POST /nguoi-dung/` - Tạo người dùng mới
- `GET /nguoi-dung/` - Lấy danh sách người dùng
- `GET /nguoi-dung/{id}` - Lấy thông tin người dùng
- `DELETE /nguoi-dung/{id}` - Xóa người dùng

### Bài Toán
- `POST /bai-toan/` - Tạo bài toán mới
- `GET /bai-toan/` - Lấy danh sách bài toán
- `GET /bai-toan/{id}` - Lấy thông tin bài toán
- `GET /bai-toan/user/{user_id}` - Lấy bài toán theo người dùng

## Test với cURL

### Tạo người dùng:
```cmd
curl -X POST "http://localhost:8000/nguoi-dung/" -H "Content-Type: application/json" -d "{\"tenDangNhap\":\"user1\",\"email\":\"user1@test.com\",\"matKhau\":\"pass123\",\"vaiTro\":\"Thành viên\"}"
```

### Lấy danh sách người dùng:
```cmd
curl -X GET "http://localhost:8000/nguoi-dung/"
```

### Tạo bài toán:
```cmd
curl -X POST "http://localhost:8000/bai-toan/" -H "Content-Type: application/json" -d "{\"maNguoiDung\":1,\"deBaiTho\":\"Cho hình chóp\",\"loaiHinh\":\"Hình chóp\",\"tomTatDe\":\"Tính thể tích\"}"
```

## Troubleshooting

### Lỗi kết nối database:
- Kiểm tra SQL Server đang chạy
- Kiểm tra username/password trong `.env`
- Kiểm tra ODBC Driver đã được cài đặt

### Lỗi import module:
```cmd
set PYTHONPATH=d:\CDNNLT\Project_CK\be
```

### Port 8000 đã được sử dụng:
Thay đổi port trong `main.py` hoặc khi chạy uvicorn:
```cmd
uvicorn main:app --port 8001
```
