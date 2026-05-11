# API Response Format - Lịch Sử Bài Toán

## Endpoint: GET /geometry/problem/{ma_bai_toan}

### Mục Đích
Lấy **đầy đủ thông tin** bài toán để hiển thị trong lịch sử, bao gồm:
- ✅ Hình ảnh được tải lên
- ✅ Đề bài đã nhận diện  
- ✅ Yếu tố hình học (5 items)
- ✅ Lời giải (nếu có)

### Response Format

```json
{
  "baiToan": {
    "maBaiToan": 123,
    "maNguoiDung": "ND001",
    "duongDan": "/uploads/20240510_143022_test.jpg",
    "deBaiTho": "Cho hình chóp S.ABCD có đáy ABCD là hình vuông cạnh a, cạnh bên SA vuông góc với mặt phẳng đáy. Gọi M là trung điểm của cạnh CD. Biết khoảng cách giữa BC và SM bằng a√3/4. Tính thể tích của khối chóp S.ABCD theo a.",
    "loaiHinh": "Hình chóp",
    "tomTatDe": "Tính thể tích khối chóp S.ABCD",
    "ngayTao": "2024-05-10T14:30:22"
  },
  
  "duLieuHinhHoc": {
    "maDuLieu": 456,
    "maBaiToan": 123,
    "toaDoDiem": "{\"S\":[0,0,2],\"A\":[0,0,0],\"B\":[1,0,0],\"C\":[1,1,0],\"D\":[0,1,0],\"M\":[0.5,1,0]}",
    "cacCanh": "[[\"S\",\"A\"],[\"S\",\"B\"],[\"S\",\"C\"],[\"S\",\"D\"],[\"A\",\"B\"],[\"B\",\"C\"],[\"C\",\"D\"],[\"D\",\"A\"]]",
    "cacQuanHe": "[{\"type\":\"perpendicular\",\"entities\":[\"SA\",\"ABCD\"]},{\"type\":\"midpoint\",\"entities\":[\"M\",\"CD\"]}]"
  },
  
  "loiGiai": {
    "maLoiGiai": 789,
    "maBaiToan": 123,
    "cacBuocGiai": "[\"Bước 1: Xác định SA vuông góc với đáy\",\"Bước 2: Tính khoảng cách từ BC đến SM\",\"Bước 3: Tính chiều cao SA\",\"Bước 4: Tính thể tích V = 1/3 * S_đáy * h\"]",
    "ketQuaCuoi": "V = a³/3",
    "congThucSuDung": "[\"V = 1/3 * S * h\",\"S_hình_vuông = a²\"]"
  },
  
  "extraction": {
    "problem_text": "Cho hình chóp S.ABCD có đáy ABCD là hình vuông cạnh a...",
    "problem_type": "Hình chóp",
    "given_conditions": [
      "ABCD là hình vuông cạnh a",
      "SA ⊥ (ABCD)",
      "M là trung điểm của CD",
      "Khoảng cách giữa BC và SM = a√3/4"
    ],
    "questions": [
      "Tính thể tích của khối chóp S.ABCD theo a"
    ],
    "points": ["S", "A", "B", "C", "D", "M"],
    "relationships": [
      {"type": "perpendicular", "entities": ["SA", "ABCD"]},
      {"type": "midpoint", "entities": ["M", "CD"]}
    ]
  }
}
```

## Cách Hiển Thị Trên Frontend

### 1. Hình Ảnh
```javascript
const imageUrl = `http://127.0.0.1:8000${data.baiToan.duongDan}`;
// Display: <img src="http://127.0.0.1:8000/uploads/20240510_143022_test.jpg">
```

### 2. Câu Hỏi
```javascript
const question = data.extraction.problem_text;
// Display: "Cho hình chóp S.ABCD có đáy ABCD là hình vuông..."
```

### 3. Đề Bài Đã Nhận Diện
```javascript
const recognizedText = data.baiToan.deBaiTho;
// Display: Full problem text
```

### 4. Yếu Tố Hình Học (5 Items)

#### Item 1: Hình Dạng
```javascript
const shape = data.extraction.problem_type;
// Display: "Hình chóp"
```

#### Item 2: Đáy
```javascript
const base = data.extraction.given_conditions.find(c => 
  c.includes('hình vuông') || c.includes('hình chữ nhật')
);
// Display: "ABCD là hình vuông cạnh a"
```

#### Item 3: Vuông Góc
```javascript
const perpendicular = data.extraction.given_conditions.find(c => 
  c.includes('⊥') || c.includes('vuông góc')
);
// Display: "SA ⊥ (ABCD)"
```

#### Item 4: Trung Điểm
```javascript
const midpoint = data.extraction.given_conditions.find(c => 
  c.includes('trung điểm')
);
// Display: "M là trung điểm của CD"
```

#### Item 5: Độ Dài / Khoảng Cách
```javascript
const distance = data.extraction.given_conditions.find(c => 
  c.includes('=') || c.includes('khoảng cách')
);
// Display: "Khoảng cách giữa BC và SM = a√3/4"
```

#### Item 6: Yêu Cầu
```javascript
const requirement = data.extraction.questions[0];
// Display: "Tính thể tích của khối chóp S.ABCD theo a"
```

### 5. Lời Giải (Nếu Có)
```javascript
if (data.loiGiai) {
  const steps = JSON.parse(data.loiGiai.cacBuocGiai);
  const result = data.loiGiai.ketQuaCuoi;
  
  // Display steps:
  steps.forEach(step => {
    console.log(step);
  });
  
  // Display result:
  console.log("Kết quả:", result);
}
```

## Frontend Implementation Example

```javascript
async function loadProblemFromHistory(problemId) {
  try {
    const response = await fetch(`http://127.0.0.1:8000/geometry/problem/${problemId}`);
    const data = await response.json();
    
    // 1. Display Image
    const imageUrl = `http://127.0.0.1:8000${data.baiToan.duongDan}`;
    document.getElementById('problemImage').src = imageUrl;
    
    // 2. Display Question
    document.getElementById('question').textContent = data.extraction.problem_text;
    
    // 3. Display Recognized Text
    document.getElementById('recognizedText').textContent = data.baiToan.deBaiTho;
    
    // 4. Display Geometry Elements (5 items)
    const elements = [
      { label: 'Hình dạng', value: data.extraction.problem_type },
      { label: 'Đáy', value: data.extraction.given_conditions.find(c => c.includes('hình vuông')) },
      { label: 'Vuông góc', value: data.extraction.given_conditions.find(c => c.includes('⊥')) },
      { label: 'Trung điểm', value: data.extraction.given_conditions.find(c => c.includes('trung điểm')) },
      { label: 'Độ dài', value: data.extraction.given_conditions.find(c => c.includes('=')) },
      { label: 'Yêu cầu', value: data.extraction.questions[0] }
    ];
    
    elements.forEach(el => {
      const html = `
        <div class="geometry-element">
          <span class="label">${el.label}</span>
          <span class="value">${el.value || 'N/A'}</span>
        </div>
      `;
      document.getElementById('geometryElements').innerHTML += html;
    });
    
    // 5. Display Solution (if available)
    if (data.loiGiai) {
      const steps = JSON.parse(data.loiGiai.cacBuocGiai);
      const result = data.loiGiai.ketQuaCuoi;
      
      let solutionHTML = '<ol>';
      steps.forEach(step => {
        solutionHTML += `<li>${step}</li>`;
      });
      solutionHTML += '</ol>';
      solutionHTML += `<div class="result">Kết quả: ${result}</div>`;
      
      document.getElementById('solution').innerHTML = solutionHTML;
    }
    
  } catch (error) {
    console.error('Error loading problem:', error);
  }
}
```

## Database Schema

### BAITOAN Table
```sql
CREATE TABLE BAITOAN (
    maBaiToan INT PRIMARY KEY IDENTITY(1,1),
    maNguoiDung VARCHAR(100),
    duongDan NVARCHAR(500),      -- "/uploads/20240510_143022_test.jpg"
    deBaiTho NVARCHAR(MAX),       -- Full problem text
    loaiHinh NVARCHAR(100),       -- "Hình chóp"
    tomTatDe NVARCHAR(500),       -- "Tính thể tích..."
    ngayTao DATETIME DEFAULT GETDATE()
);
```

### DULIEUHINHHOC Table
```sql
CREATE TABLE DULIEUHINHHOC (
    maDuLieu INT PRIMARY KEY IDENTITY(1,1),
    maBaiToan INT FOREIGN KEY REFERENCES BAITOAN(maBaiToan),
    toaDoDiem NVARCHAR(MAX),      -- JSON: {"S":[0,0,2],...}
    cacCanh NVARCHAR(MAX),        -- JSON: [["S","A"],...]
    cacQuanHe NVARCHAR(MAX)       -- JSON: [{"type":"perpendicular",...}]
);
```

### LOIGIAI Table
```sql
CREATE TABLE LOIGIAI (
    maLoiGiai INT PRIMARY KEY IDENTITY(1,1),
    maBaiToan INT FOREIGN KEY REFERENCES BAITOAN(maBaiToan),
    cacBuocGiai NVARCHAR(MAX),    -- JSON: ["Bước 1:...",...]
    ketQuaCuoi NVARCHAR(500),     -- "V = a³/3"
    congThucSuDung NVARCHAR(MAX)  -- JSON: ["V = 1/3 * S * h",...]
);
```

## Testing

### Test API
```bash
curl http://127.0.0.1:8000/geometry/problem/123
```

### Expected Response
- ✅ `baiToan` object with all fields
- ✅ `duLieuHinhHoc` object with geometry data
- ✅ `loiGiai` object with solution (if available)
- ✅ `extraction` object with parsed data

### Test Frontend
1. Upload a problem
2. Go to history page
3. Click on the problem
4. Verify all 5 elements display:
   - ✅ Hình dạng
   - ✅ Đáy
   - ✅ Vuông góc
   - ✅ Trung điểm
   - ✅ Độ dài
   - ✅ Yêu cầu

## Summary

✅ **Backend API đã hoàn thiện**:
- Endpoint: `GET /geometry/problem/{ma_bai_toan}`
- Returns: Full problem data with extraction
- Includes: Image path, problem text, geometry elements, solution

✅ **Frontend có thể hiển thị**:
- Hình ảnh từ `/uploads/`
- Đề bài đã nhận diện
- 5-6 yếu tố hình học
- Lời giải (nếu có)

✅ **Data flow**:
1. User clicks problem in history
2. Frontend calls API with problem ID
3. Backend returns full data
4. Frontend displays all information

---

**Ready to use!** 🚀
