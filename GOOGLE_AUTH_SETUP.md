# Hướng dẫn tích hợp Google Authentication

## Đã hoàn thành

### Backend
✅ **API Endpoint mới:** `POST /auth/google-login`
- Tự động tạo user trong database nếu chưa tồn tại
- Sử dụng Google ID làm `maNguoiDung`
- Lưu email, tên người dùng
- Trả về thông tin user

✅ **Repository method:** `get_or_create_google_user()`
- Kiểm tra user đã tồn tại chưa
- Tạo user mới nếu chưa có
- Hỗ trợ VARCHAR cho `maNguoiDung`

✅ **File đã tạo:**
- `be/app/api/routes/auth.py` - Authentication routes
- `fe/js/google-auth.js` - Google OAuth handler
- `be/main.py` - Đã đăng ký auth router

## Cách sử dụng

### 1. Cấu hình Google OAuth

Bạn cần có **Google Client ID** từ Google Cloud Console:

1. Truy cập https://console.cloud.google.com/
2. Tạo project mới hoặc chọn project có sẵn
3. Vào **APIs & Services** > **Credentials**
4. Tạo **OAuth 2.0 Client ID**
5. Thêm **Authorized JavaScript origins:**
   - `http://localhost:8000`
   - `http://127.0.0.1:8000`
6. Thêm **Authorized redirect URIs:**
   - `http://localhost:8000/pages/login.html`
   - `http://127.0.0.1:8000/pages/login.html`
7. Copy **Client ID**

### 2. Cập nhật Frontend

Trong file `fe/pages/login.html`, thêm:

```html
<!-- Google Sign-In SDK -->
<script src="https://accounts.google.com/gsi/client" async defer></script>
<script src="../js/google-auth.js"></script>

<!-- Google Sign-In Button -->
<div id="google-signin-button"></div>

<script>
  // Khởi tạo Google Sign-In khi trang load
  window.addEventListener('DOMContentLoaded', function() {
    initGoogleSignIn();
  });
</script>
```

### 3. Thay Client ID

Trong file `fe/js/google-auth.js`, dòng 67:
```javascript
client_id: 'YOUR_GOOGLE_CLIENT_ID', // Thay bằng Client ID thực
```

Thay `YOUR_GOOGLE_CLIENT_ID` bằng Client ID từ Google Cloud Console.

### 4. Test

1. **Khởi động backend:**
   ```bash
   cd be
   python main.py
   ```

2. **Mở trình duyệt:**
   ```
   http://127.0.0.1:8000/pages/login.html
   ```

3. **Click nút "Sign in with Google"**

4. **Kiểm tra database:**
   ```sql
   SELECT * FROM NGUOIDUNG WHERE maNguoiDung LIKE '%google%'
   ```

## API Endpoints

### POST /auth/google-login
Đăng nhập bằng Google OAuth

**Request:**
```json
{
  "googleId": "123456789",
  "email": "user@gmail.com",
  "name": "Nguyen Van A",
  "picture": "https://..."
}
```

**Response:**
```json
{
  "success": true,
  "message": "Đăng nhập thành công",
  "user": {
    "maNguoiDung": "123456789",
    "tenDangNhap": "Nguyen Van A",
    "email": "user@gmail.com",
    "vaiTro": "user"
  }
}
```

### GET /auth/check/{ma_nguoi_dung}
Kiểm tra user có tồn tại không

**Response:**
```json
{
  "exists": true,
  "user": {
    "maNguoiDung": "123456789",
    "tenDangNhap": "Nguyen Van A",
    "email": "user@gmail.com",
    "vaiTro": "user"
  }
}
```

## Database Schema

Bảng `NGUOIDUNG` đã hỗ trợ:
- `maNguoiDung` VARCHAR(100) - Có thể là "ND001" hoặc Google ID
- `tenDangNhap` VARCHAR(100)
- `email` VARCHAR(100)
- `matKhau` VARCHAR(255) - Để trống cho Google OAuth
- `vaiTro` VARCHAR(50)

## Flow đăng nhập Google

1. User click "Sign in with Google"
2. Google hiển thị popup đăng nhập
3. User chọn tài khoản Google
4. Google trả về JWT token
5. Frontend parse token, lấy thông tin user
6. Frontend gọi `POST /auth/google-login`
7. Backend kiểm tra user trong database:
   - Nếu chưa có → Tạo user mới
   - Nếu đã có → Lấy thông tin user
8. Backend trả về thông tin user
9. Frontend lưu vào localStorage
10. Redirect đến trang solver

## Lưu ý

### Bảo mật
- ✅ Google ID được dùng làm `maNguoiDung` (unique)
- ✅ Không lưu password cho Google OAuth users
- ✅ CORS đã được cấu hình
- ⚠️ Cần validate JWT token ở backend (TODO)

### Lịch sử bài toán
- ✅ Lịch sử sẽ tự động lưu với `maNguoiDung` = Google ID
- ✅ API `/bai-toan/user/{ma_nguoi_dung}` đã hỗ trợ VARCHAR
- ✅ Frontend đã tích hợp backend API

### Testing
Để test mà không cần Google OAuth thực:
```javascript
// Trong console browser
handleGoogleLogin({
  credential: 'fake-jwt-token'
});
```

Hoặc gọi API trực tiếp:
```bash
curl -X POST http://127.0.0.1:8000/auth/google-login \
  -H "Content-Type: application/json" \
  -d '{
    "googleId": "test123",
    "email": "test@gmail.com",
    "name": "Test User"
  }'
```

## Troubleshooting

### Lỗi: "User chưa được lưu vào database"
- Kiểm tra backend có chạy không
- Kiểm tra CORS settings
- Xem console log trong browser
- Xem log trong terminal backend

### Lỗi: "Failed to load history"
- Đảm bảo user đã được tạo trong database
- Kiểm tra `maNguoiDung` trong localStorage
- Test API endpoint: `GET /bai-toan/user/{ma_nguoi_dung}`

### Lỗi: "Google Sign-In button không hiển thị"
- Kiểm tra đã load Google SDK chưa
- Kiểm tra Client ID đã đúng chưa
- Xem console log có lỗi không

## Next Steps

1. ✅ Tạo API endpoint `/auth/google-login`
2. ✅ Tự động tạo user trong database
3. ✅ Tích hợp với lịch sử bài toán
4. ⏳ Thêm Google Sign-In button vào login page
5. ⏳ Validate JWT token ở backend
6. ⏳ Thêm refresh token mechanism
7. ⏳ Thêm logout functionality

## Support

Nếu gặp vấn đề, kiểm tra:
1. Backend logs: `python main.py`
2. Browser console: F12 → Console
3. Network tab: F12 → Network
4. Database: Query `SELECT * FROM NGUOIDUNG`
