"""
Geometry API - Endpoints cho phân tích và giải toán hình học

Flow 3 bước (giống nhau cho cả guest và logged-in):
  Bước 1: POST /upload-and-save      → Phân tích ảnh
  Bước 2: POST /solve-problem/{id}   → Giải toán
  Bước 3: POST /render-3d/{id}       → Dựng hình 3D

Sự khác biệt:
  - Có ma_nguoi_dung → lưu vào DB, có lịch sử
  - Không có ma_nguoi_dung → không lưu DB, không có lịch sử
  - Cả 2 đều dùng chung maBaiToan tạm (session-based)
"""
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from app.services.gemini_service import GeminiService
from app.repositories.bai_toan_repository import BaiToanRepository
from app.repositories.du_lieu_hinh_hoc_repository import DuLieuHinhHocRepository
from app.repositories.loi_giai_repository import LoiGiaiRepository
from app.repositories.dung_hinh_3d_repository import DungHinh3DRepository
from pydantic import BaseModel
from typing import Optional
import json

router = APIRouter(prefix="/geometry", tags=["Hình học 3D"])
gemini_service = GeminiService()
bai_toan_repo = BaiToanRepository()
du_lieu_repo = DuLieuHinhHocRepository()
loi_giai_repo = LoiGiaiRepository()
dung_hinh_repo = DungHinh3DRepository()

# ============================================================
# BƯỚC 1: Upload và phân tích ảnh
# ============================================================

@router.post("/upload-and-save")
async def upload_and_save_problem(
    file: UploadFile = File(...),
    ma_nguoi_dung: Optional[str] = Form(None)
):
    """
    Bước 1: Upload ảnh, phân tích bài toán.

    - Có ma_nguoi_dung → lưu vào DB (có lịch sử)
    - Không có ma_nguoi_dung → không lưu DB (không có lịch sử)
    - Cả 2 đều trả về maBaiToan để dùng ở bước 2, 3
    """
    # Parse ma_nguoi_dung
    user_id: Optional[int] = None
    if ma_nguoi_dung and ma_nguoi_dung.strip():
        try:
            user_id = int(ma_nguoi_dung.strip())
        except ValueError:
            raise HTTPException(status_code=400, detail="ma_nguoi_dung phải là số nguyên")

    try:
        # Phân tích ảnh bằng Gemini AI
        print("Step 1: Analyzing image...")
        image_bytes = await file.read()

        try:
            extraction = await gemini_service.analyze_image(image_bytes)
        except Exception as e:
            error_msg = str(e)
            if "503" in error_msg or "UNAVAILABLE" in error_msg:
                raise HTTPException(status_code=503, detail="AI đang quá tải. Vui lòng thử lại sau 1-2 phút")
            elif "429" in error_msg:
                raise HTTPException(status_code=429, detail="Đã vượt quá giới hạn API. Vui lòng đợi vài phút")
            else:
                raise HTTPException(status_code=500, detail=f"Lỗi phân tích ảnh: {error_msg}")

        # Tạo visualization 3D
        try:
            geometry_data = {
                "points": extraction.get("points", []),
                "edges": [],
                "relations": extraction.get("relationships", [])
            }
            visualization = gemini_service.renderer.transform_to_3d(geometry_data)
        except Exception as e:
            print(f"Renderer error: {e}")
            visualization = {"points": {}, "edges": [], "faces": []}

        # Lưu vào DB (dù có hay không có user_id đều lưu để có maBaiToan)
        # Nếu không có user_id thì maNguoiDung = None (guest record)
        print("Step 2: Saving to BAITOAN...")
        try:
            ma_bai_toan = bai_toan_repo.create_from_dict({
                "maNguoiDung": user_id,  # None nếu không đăng nhập
                "duongDan": file.filename,
                "deBaiTho": extraction.get("problem_text", ""),
                "loaiHinh": extraction.get("problem_type", ""),
                "tomTatDe": ", ".join(extraction.get("questions", []))
            })
        except Exception as e:
            if "FOREIGN KEY" in str(e) or "FK__BAITOAN" in str(e):
                raise HTTPException(
                    status_code=400,
                    detail=f"Người dùng ID={user_id} không tồn tại. Vui lòng kiểm tra lại."
                )
            raise

        print("Step 3: Saving to DULIEUHINHHOC...")
        du_lieu_id = du_lieu_repo.create_from_dict({
            "maBaiToan": ma_bai_toan,
            "toaDoDiem": json.dumps(visualization.get("points", {}), ensure_ascii=False),
            "cacCanh": json.dumps(visualization.get("edges", []), ensure_ascii=False),
            "cacQuanHe": json.dumps(extraction.get("relationships", []), ensure_ascii=False)
        })

        return {
            "success": True,
            "message": "Đã phân tích xong. Bấm 'Giải' để xem đáp án.",
            "saved": user_id is not None,
            "data": {
                "maBaiToan": ma_bai_toan,
                "duLieuHinhHocId": du_lieu_id,
                "extraction": extraction,
                "visualization": visualization,
                "hasLoiGiai": False
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi hệ thống: {str(e)}")


# ============================================================
# BƯỚC 2: Giải toán
# ============================================================

@router.post("/solve-problem/{ma_bai_toan}")
async def solve_problem_with_ai(ma_bai_toan: int):
    """
    Bước 2: Giải bài toán bằng Gemini AI.
    Hoạt động với cả guest (maBaiToan từ bước 1) và logged-in user.
    Kết quả lưu vào LOIGIAI (dù guest hay không).
    """
    try:
        # Lấy bài toán từ DB
        bai_toan = bai_toan_repo.get_by_id(ma_bai_toan)
        if not bai_toan:
            raise HTTPException(status_code=404, detail="Không tìm thấy bài toán")

        # Kiểm tra đã có lời giải chưa (cache)
        existing_solution = loi_giai_repo.get_by_bai_toan(ma_bai_toan)
        if existing_solution:
            return {
                "success": True,
                "message": "Bài toán đã được giải trước đó",
                "data": {
                    "loiGiaiId": existing_solution.get("maLoiGiai"),
                    "solution": {
                        "steps": json.loads(existing_solution.get("cacBuocGiai", "[]")),
                        "result": existing_solution.get("ketQuaCuoi", ""),
                        "formulas_used": json.loads(existing_solution.get("congThucSuDung", "[]"))
                    },
                    "fromCache": True
                }
            }

        # Gọi Gemini AI giải toán
        problem_text = bai_toan.get("deBaiTho", "")
        try:
            solution = await gemini_service.solve_problem(problem_text)
        except Exception as e:
            error_msg = str(e)
            if "503" in error_msg or "UNAVAILABLE" in error_msg:
                raise HTTPException(status_code=503, detail="AI đang quá tải. Vui lòng thử lại sau 1-2 phút")
            elif "429" in error_msg:
                raise HTTPException(status_code=429, detail="Đã vượt quá giới hạn API. Vui lòng đợi vài phút")
            else:
                raise HTTPException(status_code=500, detail=f"Lỗi giải toán: {error_msg}")

        # Lưu lời giải vào DB
        loi_giai_id = loi_giai_repo.create_from_dict({
            "maBaiToan": ma_bai_toan,
            "cacBuocGiai": json.dumps(solution.get("steps", []), ensure_ascii=False),
            "ketQuaCuoi": solution.get("result", ""),
            "congThucSuDung": json.dumps(solution.get("formulas_used", []), ensure_ascii=False)
        })

        return {
            "success": True,
            "message": "Đã giải toán thành công",
            "data": {
                "loiGiaiId": loi_giai_id,
                "solution": solution,
                "fromCache": False
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi hệ thống: {str(e)}")


# ============================================================
# BƯỚC 3: Dựng hình 3D
# ============================================================

@router.post("/render-3d/{ma_bai_toan}")
async def generate_threejs_instructions(ma_bai_toan: int):
    """
    Bước 3: Tạo hướng dẫn dựng hình 3D bằng Three.js.
    Hoạt động với cả guest (maBaiToan từ bước 1) và logged-in user.
    """
    try:
        bai_toan = bai_toan_repo.get_by_id(ma_bai_toan)
        if not bai_toan:
            raise HTTPException(status_code=404, detail="Không tìm thấy bài toán")

        du_lieu = du_lieu_repo.get_by_bai_toan(ma_bai_toan)

        # Kiểm tra cache
        existing = dung_hinh_repo.get_by_bai_toan(ma_bai_toan)
        if existing:
            return {
                "success": True,
                "message": "Đã có hướng dẫn dựng hình Three.js",
                "data": {
                    "dungHinhId": existing.get("maDungHinh"),
                    "threejs": {
                        "steps": json.loads(existing.get("cacBuocVe", "[]")),
                        "functions": json.loads(existing.get("hamThreeJS", "[]")),
                        "parameters": json.loads(existing.get("thamSo", "{}")),
                        "code": existing.get("codeThreeJS", ""),
                        "guide": existing.get("huongDanVe", "")
                    },
                    "fromCache": True
                }
            }

        loai_hinh = bai_toan.get("loaiHinh", "").lower()
        de_bai = bai_toan.get("deBaiTho", "")

        points_data = {}
        if du_lieu:
            try:
                points_data = json.loads(du_lieu.get("toaDoDiem", "{}"))
            except:
                points_data = {}

        # Tạo hướng dẫn dựng hình bằng Gemini AI
        try:
            drawing_guide = await gemini_service.generate_drawing_guide(de_bai, loai_hinh)
        except Exception as e:
            drawing_guide = f"HƯỚNG DẪN DỰNG HÌNH {loai_hinh.upper()}\n\nBước 1: Vẽ các điểm theo đề bài\nBước 2: Nối các cạnh\nBước 3: Hoàn thiện hình vẽ"

        threejs_instructions = {
            "steps": [
                "1. Khởi tạo Scene, Camera, Renderer",
                "2. Tạo các điểm (Points) từ tọa độ",
                "3. Vẽ các cạnh (Lines) nối các điểm",
                "4. Tạo các mặt (Faces) nếu cần",
                "5. Thêm ánh sáng (Lights)",
                "6. Thêm OrbitControls để xoay hình",
                "7. Render và animate"
            ],
            "functions": [
                "THREE.Scene()",
                "THREE.PerspectiveCamera(fov, aspect, near, far)",
                "THREE.WebGLRenderer()",
                "THREE.Vector3(x, y, z)",
                "THREE.BufferGeometry()",
                "THREE.LineBasicMaterial()",
                "THREE.Line(geometry, material)",
                "THREE.MeshBasicMaterial()",
                "THREE.Mesh(geometry, material)",
                "THREE.AmbientLight(color, intensity)",
                "THREE.DirectionalLight(color, intensity)",
                "THREE.OrbitControls(camera, renderer.domElement)"
            ],
            "parameters": {
                "camera": {"fov": 75, "position": [3, 3, 3], "lookAt": [0, 0, 0]},
                "lights": {
                    "ambient": {"color": "0x404040", "intensity": 0.6},
                    "directional": {"color": "0xffffff", "intensity": 0.8, "position": [1, 1, 1]}
                },
                "materials": {
                    "line": {"color": "0x0000ff"},
                    "face": {"color": "0x00ff00", "transparent": True, "opacity": 0.5}
                }
            },
            "code": f"""const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({{ antialias: true }});
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);
const points = {json.dumps(points_data, indent=2)};
const vectors = {{}};
for (const [name, coords] of Object.entries(points)) {{
    vectors[name] = new THREE.Vector3(coords[0], coords[1], coords[2]);
}}
const edgeMaterial = new THREE.LineBasicMaterial({{ color: 0x0000ff }});
for (const [name1, vec1] of Object.entries(vectors)) {{
    for (const [name2, vec2] of Object.entries(vectors)) {{
        if (name1 < name2) {{
            const geometry = new THREE.BufferGeometry().setFromPoints([vec1, vec2]);
            scene.add(new THREE.Line(geometry, edgeMaterial));
        }}
    }}
}}
scene.add(new THREE.AmbientLight(0x404040, 0.6));
const dirLight = new THREE.DirectionalLight(0xffffff, 0.8);
dirLight.position.set(1, 1, 1);
scene.add(dirLight);
camera.position.set(3, 3, 3);
camera.lookAt(0, 0, 0);
const controls = new THREE.OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
function animate() {{ requestAnimationFrame(animate); controls.update(); renderer.render(scene, camera); }}
animate();
""",
            "guide": drawing_guide
        }

        dung_hinh_id = dung_hinh_repo.create_from_dict({
            "maBaiToan": ma_bai_toan,
            "cacBuocVe": json.dumps(threejs_instructions["steps"], ensure_ascii=False),
            "hamThreeJS": json.dumps(threejs_instructions["functions"], ensure_ascii=False),
            "thamSo": json.dumps(threejs_instructions["parameters"], ensure_ascii=False),
            "codeThreeJS": threejs_instructions["code"],
            "huongDanVe": drawing_guide
        })

        return {
            "success": True,
            "message": "Đã tạo hướng dẫn dựng hình Three.js",
            "data": {
                "dungHinhId": dung_hinh_id,
                "threejs": threejs_instructions,
                "fromCache": False
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================
# GET endpoints (xem lại kết quả)
# ============================================================

@router.get("/problem/{ma_bai_toan}")
async def get_full_problem(ma_bai_toan: int):
    """Lấy đầy đủ thông tin bài toán"""
    try:
        bai_toan = bai_toan_repo.get_by_id(ma_bai_toan)
        if not bai_toan:
            raise HTTPException(status_code=404, detail="Không tìm thấy bài toán")
        du_lieu = du_lieu_repo.get_by_bai_toan(ma_bai_toan)
        loi_giai = loi_giai_repo.get_by_bai_toan(ma_bai_toan)
        return {"baiToan": bai_toan, "duLieuHinhHoc": du_lieu, "loiGiai": loi_giai}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/solution/{ma_bai_toan}")
async def get_solution(ma_bai_toan: int):
    """Lấy lời giải của bài toán"""
    try:
        bai_toan = bai_toan_repo.get_by_id(ma_bai_toan)
        if not bai_toan:
            raise HTTPException(status_code=404, detail="Không tìm thấy bài toán")
        loi_giai = loi_giai_repo.get_by_bai_toan(ma_bai_toan)
        if not loi_giai:
            return {"success": False, "message": "Chưa có lời giải", "data": None}
        return {
            "success": True,
            "message": "Đã tìm thấy lời giải",
            "data": {
                "loiGiaiId": loi_giai.get("maLoiGiai"),
                "maBaiToan": loi_giai.get("maBaiToan"),
                "solution": {
                    "steps": json.loads(loi_giai.get("cacBuocGiai", "[]")),
                    "result": loi_giai.get("ketQuaCuoi", ""),
                    "formulas_used": json.loads(loi_giai.get("congThucSuDung", "[]"))
                },
                "ngayTao": loi_giai.get("ngayTao")
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/drawing-guide/{ma_bai_toan}")
async def get_drawing_guide(ma_bai_toan: int):
    """Lấy hướng dẫn dựng hình"""
    try:
        bai_toan = bai_toan_repo.get_by_id(ma_bai_toan)
        if not bai_toan:
            raise HTTPException(status_code=404, detail="Không tìm thấy bài toán")
        dung_hinh = dung_hinh_repo.get_by_bai_toan(ma_bai_toan)
        if not dung_hinh:
            return {"success": False, "message": "Chưa có hướng dẫn dựng hình", "data": None}
        return {
            "success": True,
            "message": "Đã tìm thấy hướng dẫn dựng hình",
            "data": {
                "dungHinhId": dung_hinh.get("maDungHinh"),
                "maBaiToan": dung_hinh.get("maBaiToan"),
                "guide": dung_hinh.get("huongDanVe", ""),
                "threejs": {
                    "steps": json.loads(dung_hinh.get("cacBuocVe", "[]")),
                    "functions": json.loads(dung_hinh.get("hamThreeJS", "[]")),
                    "parameters": json.loads(dung_hinh.get("thamSo", "{}")),
                    "code": dung_hinh.get("codeThreeJS", "")
                },
                "ngayTao": dung_hinh.get("ngayTao")
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
