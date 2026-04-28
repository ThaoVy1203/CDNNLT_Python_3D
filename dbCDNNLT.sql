
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
    maNguoiDung INT IDENTITY(1,1) PRIMARY KEY,
    tenDangNhap NVARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    matKhau VARCHAR(50) NOT NULL,
	vaiTro	NVARCHAR(20) NOT NULL DEFAULT N'Thành viên'
			CHECK (vaiTro IN (N'Thành viên', N'Admin')),
    ngayTao DATETIME DEFAULT GETDATE()
);

CREATE TABLE BAITOAN 
(
    maBaiToan INT IDENTITY(1,1) PRIMARY KEY,
	maNguoiDung INT,
    duongDan VARCHAR(255),
    deBaiTho NVARCHAR(MAX),          -- Văn bản thô Gemini trích xuất
    loaiHinh NVARCHAR(100),           -- Hình chóp, lăng trụ...
    tomTatDe NVARCHAR(MAX),
    ngayTao DATETIME DEFAULT GETDATE(),
	FOREIGN KEY (maNguoiDung) REFERENCES NGUOIDUNG(maNguoiDung)
);


CREATE TABLE DULIEUHINHHOC 
(
    id INT IDENTITY(1,1) PRIMARY KEY,
    maBaiToan INT,
    toaDoDiem VARCHAR(MAX),     -- JSON: {"A": [0,0,0], ...}
    cacCanh VARCHAR(MAX),            -- JSON: [["A", "B"], ...]
    cacQuanHe NVARCHAR(MAX),         -- JSON: {"vuông góc": [...]}
	FOREIGN KEY (maBaiToan) REFERENCES BAITOAN(maBaiToan)
);

CREATE TABLE LOIGIAI (
    maLoiGiai INT IDENTITY(1,1) PRIMARY KEY,
	maBaiToan INT,
    cacBuocGiai NVARCHAR(MAX),       -- JSON mảng các bước
    ketQuaCuoi NVARCHAR(MAX),
    congThucSuDung NVARCHAR(MAX),   -- JSON danh sách công thức
    ngayTao DATETIME DEFAULT GETDATE(),
	FOREIGN KEY (maBaiToan) REFERENCES BAITOAN(maBaiToan)
);

CREATE TABLE DUNGHINH3D (
    maDungHinh INT IDENTITY(1,1) PRIMARY KEY,
    maBaiToan INT,
    cacBuocVe NVARCHAR(MAX),        -- JSON: Thứ tự các bước vẽ
    hamThreeJS NVARCHAR(MAX),       -- JSON: Danh sách hàm Three.js cần dùng
    thamSo NVARCHAR(MAX),           -- JSON: Tham số cho từng hàm
    codeThreeJS NVARCHAR(MAX),      -- Code Three.js đầy đủ
    huongDanVe NVARCHAR(MAX),       -- Text: Hướng dẫn chi tiết
    ngayTao DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (maBaiToan) REFERENCES BAITOAN(maBaiToan)
);
GO
select * from NGUOIDUNG
SELECT * FROM BAITOAN;
SELECT * FROM DULIEUHINHHOC;
SELECT * FROM LOIGIAI;
SELECT * FROM DUNGHINH3D;
delete from DUNGHINH3D
where maDungHinh = 4
