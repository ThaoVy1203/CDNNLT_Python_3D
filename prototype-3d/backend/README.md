# 🔧 Backend - Geometry Engine

## Mục đích
Backend tính toán tọa độ 3D chính xác từ ràng buộc hình học bằng SymPy.

## Cài đặt

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

## Chạy server

```bash
uvicorn app.main:app --reload --port 8001
```

Server chạy tại: http://localhost:8001

## API Documentation

Swagger UI: http://localhost:8001/docs

## Cấu trúc

```
backend/
├── app/
│   ├── main.py              # FastAPI app
│   ├── api/
│   │   └── routes.py        # API endpoints
│   ├── solver/
│   │   ├── sympy_solver.py  # SymPy solver
│   │   └── steps_generator.py
│   └── models/
│       └── schemas.py       # Pydantic models
├── tests/
├── mock_data/               # Mock JSON files
└── requirements.txt
```

## API Endpoints

### POST /api/solve
Giải bài toán hình học và trả về tọa độ 3D.

**Request**:
```json
{
  "shape_type": "pyramid",
  "constraints": {
    "base": {
      "type": "square",
      "side": 1
    },
    "apex": {
      "height": 1.414,
      "perpendicular_to_base": true
    }
  }
}
```

**Response**:
```json
{
  "points": {
    "A": [0, 0, 0],
    "B": [1, 0, 0],
    "C": [1, 0, 1],
    "D": [0, 0, 1],
    "S": [0, 1.414, 0]
  },
  "edges": [
    { "start": "A", "end": "B" },
    { "start": "B", "end": "C" },
    ...
  ],
  "faces": [
    { "vertices": ["A", "B", "C", "D"] }
  ],
  "steps": [
    {
      "order": 1,
      "description": "Vẽ đáy ABCD",
      "objects": ["A", "B", "C", "D", "AB", "BC", "CD", "DA"]
    },
    ...
  ]
}
```

## Testing

```bash
pytest tests/
```

## Mock Data

Thư mục `mock_data/` chứa các file JSON mẫu:
- `pyramid.json` - Hình chóp
- `prism.json` - Lăng trụ
- `cube.json` - Hình lập phương

## Development

1. Tạo solver mới trong `app/solver/`
2. Thêm endpoint trong `app/api/routes.py`
3. Test với mock data
4. Update documentation
