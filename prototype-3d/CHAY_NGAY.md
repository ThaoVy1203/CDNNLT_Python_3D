# ⚡ CHẠY NGAY - QUICK START

## 🎯 Chạy trong 2 phút

### Terminal 1: Backend

```bash
cd d:/Vy/CDNNLT/CK_NNLT_3D/prototype-3d/backend
python -m venv venv
source venv/Scripts/activate  # Git Bash
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
```

✅ Backend: http://localhost:8001

---

### Terminal 2: Frontend

```bash
cd d:/Vy/CDNNLT/CK_NNLT_3D/prototype-3d/frontend
npm install
npm run dev
```

✅ Frontend: http://localhost:5174

---

## 🎮 Sử dụng

1. Mở browser: **http://localhost:5174**
2. Chọn hình (Pyramid/Prism/Cube)
3. Click **"Tải hình"**
4. Click **▶ Play** để xem animation
5. Dùng chuột xoay/zoom hình 3D

---

## ✅ Checklist

- [ ] Backend chạy tại port 8001
- [ ] Frontend chạy tại port 5174
- [ ] Có thể tải hình thành công
- [ ] Animation hoạt động
- [ ] Có thể xoay/zoom hình 3D

---

## 🆘 Lỗi thường gặp

### Backend không chạy
```bash
# Check Python
python --version

# Activate venv
source venv/Scripts/activate

# Reinstall
pip install -r requirements.txt --force-reinstall
```

### Frontend không chạy
```bash
# Clear cache
rm -rf node_modules package-lock.json
npm install

# Check Node
node --version
```

### Không load được hình
- Check backend có chạy không: http://localhost:8001
- Check console browser (F12)
- Check CORS error

---

## 📚 Tài liệu đầy đủ

Xem file **HUONG_DAN_CHAY.md** để biết chi tiết hơn.
