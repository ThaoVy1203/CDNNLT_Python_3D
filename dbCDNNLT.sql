
-- ============================================================

IF EXISTS (SELECT * FROM sys.databases WHERE name = 'dbCDNNLT')
BEGIN
    USE master
    ALTER DATABASE dbCDNNLT SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
    DROP DATABASE dbCDNNLT
END;
GO

CREATE DATABASE [dbCDNNLT]
GO
USE [dbCDNNLT]
GO

CREATE TABLE NGUOIDUNG 
(
    maNguoiDung VARCHAR(100) PRIMARY KEY,
    tenDangNhap NVARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    matKhau VARCHAR(50) NOT NULL,
    vaiTro NVARCHAR(20) NOT NULL DEFAULT N'Thành viên'
        CHECK (vaiTro IN (N'Thành viên', N'Admin')),
    ngayTao DATETIME DEFAULT GETDATE()
);

CREATE TABLE BAITOAN 
(
    maBaiToan BIGINT IDENTITY(1,1) PRIMARY KEY,
    maNguoiDung VARCHAR(100),
    duongDan VARCHAR(255),
    deBaiTho NVARCHAR(MAX),          -- Văn bản thô Gemini trích xuất
    loaiHinh NVARCHAR(100),           -- Hình chóp, lăng trụ...
    tomTatDe NVARCHAR(MAX),
    ngayTao DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (maNguoiDung) REFERENCES NGUOIDUNG(maNguoiDung)
);

CREATE TABLE DULIEUHINHHOC 
(
    id BIGINT IDENTITY(1,1) PRIMARY KEY,
    maBaiToan BIGINT,
    toaDoDiem VARCHAR(MAX),     -- JSON: {"A": [0,0,0], ...}
    cacCanh VARCHAR(MAX),            -- JSON: [["A", "B"], ...]
    cacQuanHe NVARCHAR(MAX),         -- JSON: {"vuông góc": [...]}
    FOREIGN KEY (maBaiToan) REFERENCES BAITOAN(maBaiToan)
);

CREATE TABLE LOIGIAI (
    maLoiGiai BIGINT IDENTITY(1,1) PRIMARY KEY,
    maBaiToan BIGINT,
    cacBuocGiai NVARCHAR(MAX),       -- JSON mảng các bước
    ketQuaCuoi NVARCHAR(MAX),
    congThucSuDung NVARCHAR(MAX),   -- JSON danh sách công thức
    ngayTao DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (maBaiToan) REFERENCES BAITOAN(maBaiToan)
);

CREATE TABLE DUNGHINH3D (
    maDungHinh BIGINT IDENTITY(1,1) PRIMARY KEY,
    maBaiToan BIGINT,
    cacBuocVe NVARCHAR(MAX),        -- JSON: Thứ tự các bước vẽ
    hamThreeJS NVARCHAR(MAX),       -- JSON: Danh sách hàm Three.js cần dùng
    thamSo NVARCHAR(MAX),           -- JSON: Tham số cho từng hàm
    codeThreeJS NVARCHAR(MAX),      -- Code Three.js đầy đủ
    huongDanVe NVARCHAR(MAX),       -- Text: Hướng dẫn chi tiết
    ngayTao DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (maBaiToan) REFERENCES BAITOAN(maBaiToan)
);

-- ============================================================
-- BẢNG CACHE CHO TÌM BÀI TOÁN TƯƠNG TỰ
-- ============================================================
CREATE TABLE BAI_TOAN_TUONG_TU_CACHE (
    maCache INT IDENTITY(1,1) PRIMARY KEY,
    tuKhoa NVARCHAR(500) NOT NULL UNIQUE,  -- Keywords để search (vd: "hình chóp, góc, vuông góc")
    ketQua NVARCHAR(MAX),                   -- JSON array kết quả từ Gemini
    ngayTao DATETIME DEFAULT GETDATE(),
    lanCapNhat DATETIME DEFAULT GETDATE()
);

-- Index để tìm nhanh theo keywords
CREATE INDEX idx_tuKhoa ON BAI_TOAN_TUONG_TU_CACHE(tuKhoa);
-- Index để xóa cache cũ
CREATE INDEX idx_ngayTao ON BAI_TOAN_TUONG_TU_CACHE(ngayTao);
GO


select * from NGUOIDUNG;
SELECT * FROM DULIEUHINHHOC;
SELECT * FROM DUNGHINH3D;
SELECT * FROM BAITOAN;
SELECT * FROM BAI_TOAN_TUONG_TU_CACHE;
SELECT * FROM LOIGIAI;
