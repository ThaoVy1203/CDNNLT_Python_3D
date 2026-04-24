from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api_gateway.routes.solve import router

app = FastAPI(title="Hình học 3D API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/")
def root():
    return {"message": "Hệ thống hỗ trợ giải bài toán hình học không gian 3D"}
