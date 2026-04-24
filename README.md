# Hệ thống hỗ trợ giải bài toán hình học không gian 3D

## Cấu trúc project

```
cdnnlt-ck-hinhhoc-3d/
├── fe/                    # Frontend (React + R3F)
├── be/                    # Backend (FastAPI)
├── docker-compose.yml
└── README.md
```

## Chạy frontend

```bash
cd fe
npm install
npm run dev
```

Mở: http://localhost:5173

## Chạy backend

```bash
cd be
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn api_gateway.main:app --reload
```

Mở: http://localhost:8000

## Chạy với Docker

```bash
docker-compose up --build
```

## Công nghệ sử dụng

- Frontend: React, TypeScript, Three.js, React Three Fiber
- Backend: FastAPI, Python
- 3D Rendering: @react-three/fiber, @react-three/drei
