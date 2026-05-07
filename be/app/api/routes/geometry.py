"""
Geometry API - Endpoints cho phân tích và giải toán hình học

Flow 3 bước (giống nhau cho cả guest và logged-in):
  Bước 1: POST /upload-and-save      → Phân tích ảnh
  Bước 2: POST /render-3d/{id}       → Dựng hình 3D (TRƯỚC)
  Bước 3: POST /solve-problem/{id}   → Giải toán (SAU)

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
    user_id: Optional[str] = None  # Đổi thành str thay vì int
    if ma_nguoi_dung and ma_nguoi_dung.strip():
        user_id = str(ma_nguoi_dung.strip())  # Giữ dạng string

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
            data_to_save = {
                "maNguoiDung": user_id,  # None nếu không đăng nhập, hoặc Google ID
                "duongDan": file.filename,
                "deBaiTho": extraction.get("problem_text", ""),
                "loaiHinh": extraction.get("problem_type", ""),
                "tomTatDe": ", ".join(extraction.get("questions", []))
            }
            print(f"Data to save: maNguoiDung={data_to_save['maNguoiDung']}, duongDan={data_to_save['duongDan']}, loaiHinh={data_to_save['loaiHinh']}")
            print(f"deBaiTho length: {len(data_to_save['deBaiTho'])}, tomTatDe length: {len(data_to_save['tomTatDe'])}")
            ma_bai_toan = bai_toan_repo.create_from_dict(data_to_save)
        except Exception as e:
            import traceback
            print(f"ERROR saving to BAITOAN: {e}")
            print(traceback.format_exc())
            # Bỏ check FOREIGN KEY - cho phép lưu dù user không tồn tại
            raise HTTPException(status_code=500, detail=f"Lỗi lưu bài toán: {str(e)}")

        print("Step 3: Saving to DULIEUHINHHOC...")
        try:
            du_lieu_id = du_lieu_repo.create_from_dict({
                "maBaiToan": ma_bai_toan,
                "toaDoDiem": json.dumps(visualization.get("points", {}), ensure_ascii=False),
                "cacCanh": json.dumps(visualization.get("edges", []), ensure_ascii=False),
                "cacQuanHe": json.dumps(extraction.get("relationships", []), ensure_ascii=False)
            })
        except Exception as e:
            import traceback
            print(f"ERROR saving to DULIEUHINHHOC: {e}")
            print(traceback.format_exc())
            raise HTTPException(status_code=500, detail=f"Lỗi lưu dữ liệu hình học: {str(e)}")

        return {
            "success": True,
            "message": "Đã phân tích xong. Bấm 'Dựng hình 3D' để xem mô hình.",
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
# BƯỚC 3: Giải toán (SAU khi dựng hình 3D)
# ============================================================

@router.post("/solve-problem/{ma_bai_toan}")
async def solve_problem_with_ai(ma_bai_toan: int):
    """
    Bước 3: Giải bài toán bằng Gemini AI.
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
# BƯỚC 2: Render 3D với GeometrySolver (TRƯỚC khi giải toán)
# ============================================================

@router.post("/render-3d/{ma_bai_toan}")
async def render_3d_geometry(ma_bai_toan: int):
    """
    Bước 2: Tạo dữ liệu dựng hình 3D từ bài toán đã phân tích.
    
    Tích hợp GeometrySolver để render hình học không gian 3D.
    SỬ DỤNG DỮ LIỆU GEMINI AI EXTRACTION thay vì parse lại text.
    
    Returns:
        - geometry: points, edges, faces, steps, annotations, camera
        - threejs: code và parameters cho Three.js
    """
    try:
        from app.services.geometry_solver import GeometrySolver
        
        # Lấy thông tin bài toán từ DB
        bai_toan = bai_toan_repo.get_by_id(ma_bai_toan)
        if not bai_toan:
            raise HTTPException(status_code=404, detail="Không tìm thấy bài toán")
        
        # Kiểm tra cache
        existing = dung_hinh_repo.get_by_bai_toan(ma_bai_toan)
        if existing:
            return {
                "success": True,
                "message": "Đã có dữ liệu dựng hình 3D",
                "data": {
                    "dungHinhId": existing.get("maDungHinh"),
                    "geometry": json.loads(existing.get("thamSo", "{}")),
                    "threejs": {
                        "steps": json.loads(existing.get("cacBuocVe", "[]")),
                        "functions": json.loads(existing.get("hamThreeJS", "[]")),
                        "code": existing.get("codeThreeJS", ""),
                        "guide": existing.get("huongDanVe", "")
                    },
                    "fromCache": True
                }
            }
        
        # Lấy dữ liệu hình học từ DULIEUHINHHOC (Gemini extraction)
        du_lieu = du_lieu_repo.get_by_bai_toan(ma_bai_toan)
        
        # Prepare extraction data for GeometrySolver
        extraction_data = {
            "problem_text": bai_toan.get('deBaiTho', ''),
            "problem_type": bai_toan.get('loaiHinh', ''),
            "given_conditions": [],
            "questions": [],
            "points": [],
            "relationships": []
        }
        
        # Parse data from DULIEUHINHHOC if available
        if du_lieu:
            try:
                # Parse toaDoDiem (points from Gemini)
                toa_do_diem = json.loads(du_lieu.get("toaDoDiem", "{}"))
                if toa_do_diem:
                    extraction_data["points"] = list(toa_do_diem.keys())
                
                # Parse cacQuanHe (relationships from Gemini)
                cac_quan_he = json.loads(du_lieu.get("cacQuanHe", "[]"))
                if cac_quan_he:
                    extraction_data["relationships"] = cac_quan_he
            except json.JSONDecodeError as e:
                print(f"Warning: Could not parse DULIEUHINHHOC data: {e}")
        
        # Extract given_conditions and questions from problem_text
        # This is a simple extraction - Gemini should have done this better
        problem_text = extraction_data["problem_text"]
        if problem_text:
            # Split by sentences
            sentences = problem_text.split('.')
            for sentence in sentences:
                sentence = sentence.strip()
                if not sentence:
                    continue
                
                # Check if it's a question
                if '?' in sentence or 'tính' in sentence.lower() or 'tìm' in sentence.lower():
                    extraction_data["questions"].append(sentence)
                # Check if it's a given condition
                elif '=' in sentence or 'vuông góc' in sentence.lower() or '⊥' in sentence:
                    extraction_data["given_conditions"].append(sentence)
                elif 'hình' in sentence.lower() or 'cạnh' in sentence.lower():
                    extraction_data["given_conditions"].append(sentence)
                elif 'trung điểm' in sentence.lower() or 'tâm' in sentence.lower():
                    extraction_data["given_conditions"].append(sentence)
        
        print(f"📊 [API] Extraction data prepared:")
        print(f"   - Problem type: {extraction_data['problem_type']}")
        print(f"   - Given conditions: {len(extraction_data['given_conditions'])} items")
        print(f"   - Points: {extraction_data['points']}")
        print(f"   - Relationships: {len(extraction_data['relationships'])} items")
        
        # Solve geometry using Gemini extraction data
        solver = GeometrySolver()
        geometry_data = solver.solve_from_extraction(extraction_data, extraction_data['problem_type'])
        
        # Tạo hướng dẫn dựng hình
        guide = _generate_drawing_guide(geometry_data)
        
        # Tạo dữ liệu Three.js
        threejs_data = {
            "steps": [step["description"] for step in geometry_data.get("steps", [])],
            "functions": ["THREE.Scene()", "THREE.PerspectiveCamera()", "THREE.WebGLRenderer()", "THREE.OrbitControls()"],
            "code": "// Three.js code will be generated by frontend",
            "guide": guide
        }
        
        # Lưu vào DB (bảng DUNGHINH3D)
        dung_hinh_id = dung_hinh_repo.create_from_dict({
            "maBaiToan": ma_bai_toan,
            "cacBuocVe": json.dumps(geometry_data.get("steps", []), ensure_ascii=False),
            "hamThreeJS": json.dumps(threejs_data["functions"], ensure_ascii=False),
            "thamSo": json.dumps(geometry_data, ensure_ascii=False),
            "codeThreeJS": threejs_data["code"],
            "huongDanVe": guide
        })
        
        print(f"✅ [API] 3D geometry saved to DUNGHINH3D with ID: {dung_hinh_id}")
        
        return {
            "success": True,
            "message": "Đã tạo dữ liệu dựng hình 3D từ Gemini extraction",
            "data": {
                "dungHinhId": dung_hinh_id,
                "geometry": geometry_data,
                "threejs": threejs_data,
                "fromCache": False
            }
        }
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Lỗi render 3D: {str(e)}")


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
        
        # Parse geometry data from thamSo
        geometry_data = json.loads(dung_hinh.get("thamSo", "{}"))
        
        return {
            "success": True,
            "message": "Đã tìm thấy hướng dẫn dựng hình",
            "data": {
                "dungHinhId": dung_hinh.get("maDungHinh"),
                "maBaiToan": dung_hinh.get("maBaiToan"),
                "geometry": geometry_data,
                "guide": dung_hinh.get("huongDanVe", ""),
                "threejs": {
                    "steps": json.loads(dung_hinh.get("cacBuocVe", "[]")),
                    "functions": json.loads(dung_hinh.get("hamThreeJS", "[]")),
                    "code": dung_hinh.get("codeThreeJS", "")
                },
                "ngayTao": dung_hinh.get("ngayTao")
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/evaluate-approach")
async def evaluate_user_approach(request: dict):
    """Đánh giá ý tưởng giải toán của người dùng bằng AI"""
    try:
        problem_id = request.get("problemId")
        user_approach = request.get("userApproach", "")
        problem_text = request.get("problemText", "")
        
        if not user_approach or len(user_approach) < 10:
            return {
                "success": False,
                "message": "Ý tưởng quá ngắn"
            }
        
        # Build evaluation prompt
        prompt = f"""Bạn là giáo viên toán học. Đánh giá ý tưởng giải toán của học sinh.

ĐỀ BÀI:
{problem_text}

Ý TƯỞNG CỦA HỌC SINH:
{user_approach}

Hãy đánh giá:
1. Học sinh có hiểu đúng đề bài không?
2. Hướng giải có hợp lý không?
3. Có đề cập đến các yếu tố quan trọng không?

Trả về JSON với format:
{{
  "score": <điểm từ 0-10>,
  "feedback": "<phản hồi chi tiết>",
  "should_unlock": <true nếu score >= 6, false nếu không>
}}
"""
        
        try:
            response = await gemini_service.gemini_client.generate_content_async(prompt)
            response_text = response.text.strip()
            
            # Extract JSON from response
            if "```json" in response_text:
                json_str = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                json_str = response_text.split("```")[1].split("```")[0].strip()
            else:
                json_str = response_text
            
            evaluation = json.loads(json_str)
            
            return {
                "success": True,
                "evaluation": {
                    "shouldUnlock": evaluation.get("should_unlock", False),
                    "feedback": evaluation.get("feedback", ""),
                    "score": evaluation.get("score", 0)
                }
            }
        except Exception as e:
            print(f"Gemini evaluation error: {e}")
            # Fallback to keyword-based evaluation
            score = 0
            keywords = ['pythagore', 'pytago', 'trung điểm', 'vuông góc', 'sin', 'cos', 'tan', 'góc', 'hình chiếu']
            for keyword in keywords:
                if keyword in user_approach.lower():
                    score += 1
            
            score = min(10, score * 2)
            feedback = "Ý tưởng của bạn có đề cập đến một số yếu tố quan trọng." if score >= 6 else "Hãy phân tích kỹ hơn các yếu tố đã cho trong đề bài."
            
            return {
                "success": True,
                "evaluation": {
                    "shouldUnlock": score >= 6,
                    "feedback": feedback,
                    "score": score
                }
            }
        
    except Exception as e:
        print(f"Evaluation error: {e}")
        return {
            "success": False,
            "message": str(e)
        }


def _generate_drawing_guide(geometry_data: dict) -> str:
    """Tạo hướng dẫn dựng hình từ geometry data"""
    steps = geometry_data.get("steps", [])
    points = geometry_data.get("points", {})
    
    guide = "HƯỚNG DẪN DỰNG HÌNH 3D\n\n"
    
    for step in steps:
        guide += f"Bước {step['order']}: {step['description']}\n"
        guide += f"   - Các đối tượng: {', '.join(step.get('objects', []))}\n"
        if step.get('highlight'):
            guide += f"   - Highlight: {', '.join(step['highlight'])}\n"
        guide += "\n"
    
    guide += "\nTỌA ĐỘ CÁC ĐIỂM:\n"
    for name, coords in points.items():
        guide += f"   {name}: ({coords[0]:.2f}, {coords[1]:.2f}, {coords[2]:.2f})\n"
    
    return guide

