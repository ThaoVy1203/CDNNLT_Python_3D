"""
Solution Geometry Service
Sinh lệnh vẽ bổ sung dựa trên lời giải (cacBuocGiai) và hình ban đầu (DUNGHINH3D).
Kết quả lưu vào DUNGHINH3D_LOIGIAI.
"""
import json
import re
import asyncio
from typing import Optional

from app.services.gemini_service import GeminiService
from app.repositories.dunghinh3d_loigiai_repository import DungHinh3DLoiGiaiRepository
from app.repositories.dung_hinh_3d_repository import DungHinh3DRepository
from app.repositories.loi_giai_repository import LoiGiaiRepository


class SolutionGeometryService:
    """Service xử lý dựng hình bổ sung theo lời giải."""

    def __init__(self):
        self.gemini_service = GeminiService()
        self.dunghinh_loigiai_repo = DungHinh3DLoiGiaiRepository()
        self.dunghinh_repo = DungHinh3DRepository()
        self.loigiai_repo = LoiGiaiRepository()

    async def generate_solution_geometry(self, ma_loi_giai: int, ma_bai_toan: int) -> dict:
        """
        Sinh lệnh vẽ bổ sung từ lời giải.

        Flow:
        1. Lấy cacBuocGiai từ LOIGIAI
        2. Lấy existing_commands từ DUNGHINH3D
        3. Gọi Gemini với prompt solution_geometry
        4. Lưu kết quả vào DUNGHINH3D_LOIGIAI
        5. Trả về commands bổ sung

        Args:
            ma_loi_giai: Mã lời giải
            ma_bai_toan: Mã bài toán (để lấy hình ban đầu)

        Returns:
            dict chứa commands bổ sung và metadata
        """
        # 1. Lấy lời giải
        loi_giai = self.loigiai_repo.get_by_bai_toan(ma_bai_toan)
        if not loi_giai:
            raise Exception(f"Không tìm thấy lời giải cho bài toán {ma_bai_toan}")

        cac_buoc_giai = json.loads(loi_giai.get("cacBuocGiai", "[]"))
        if not cac_buoc_giai:
            return {"commands": [], "message": "Lời giải không có bước nào"}

        # 2. Lấy hình ban đầu
        dung_hinh = self.dunghinh_repo.get_by_bai_toan(ma_bai_toan)
        if not dung_hinh:
            raise Exception(f"Không tìm thấy hình ban đầu cho bài toán {ma_bai_toan}")

        existing_commands = json.loads(dung_hinh.get("cacBuocVe", "[]"))
        if not existing_commands:
            raise Exception("Hình ban đầu không có lệnh vẽ nào")

        # 3. Kiểm tra cache
        existing_solution_geo = self.dunghinh_loigiai_repo.get_by_loi_giai(ma_loi_giai)
        if existing_solution_geo:
            cached_commands = json.loads(existing_solution_geo.get("cacBuocVe", "[]"))
            return {
                "commands": cached_commands,
                "dungHinhLoiGiaiId": existing_solution_geo.get("maDungHinhLoiGiai"),
                "fromCache": True,
                "message": "Đã có dữ liệu dựng hình bổ sung"
            }

        # 4. Gọi Gemini sinh lệnh vẽ bổ sung
        additional_commands = await self._call_gemini_for_solution_geometry(
            cac_buoc_giai, existing_commands
        )

        # 5. Trích danh sách hàm đã dùng
        seen = set()
        ham_three_js = []
        for c in additional_commands:
            fn = c.get("fn")
            if fn and fn not in seen:
                seen.add(fn)
                ham_three_js.append(fn)

        # 6. Trích tọa độ điểm mới
        new_points = {}
        for c in additional_commands:
            if c.get("fn") == "drawPoint":
                a = c.get("args", {})
                if a.get("name") is not None:
                    new_points[a["name"]] = [a.get("x", 0), a.get("y", 0), a.get("z", 0)]

        tham_so = {"new_points": new_points}

        # 7. Tạo hướng dẫn vẽ bổ sung
        huong_dan = self._commands_to_guide(additional_commands)

        # 8. Lưu vào DB
        dung_hinh_loi_giai_id = self.dunghinh_loigiai_repo.create_from_dict({
            "maLoiGiai": ma_loi_giai,
            "cacBuocVe": json.dumps(additional_commands, ensure_ascii=False),
            "hamThreeJS": json.dumps(ham_three_js, ensure_ascii=False),
            "thamSo": json.dumps(tham_so, ensure_ascii=False),
            "codeThreeJS": json.dumps(additional_commands, ensure_ascii=False),
            "huongDanVe": huong_dan,
        })

        return {
            "commands": additional_commands,
            "dungHinhLoiGiaiId": dung_hinh_loi_giai_id,
            "newPoints": new_points,
            "hamThreeJS": ham_three_js,
            "huongDanVe": huong_dan,
            "fromCache": False,
            "message": "Đã sinh lệnh vẽ bổ sung từ lời giải"
        }

    async def _call_gemini_for_solution_geometry(
        self, cac_buoc_giai: list, existing_commands: list
    ) -> list:
        """Gọi Gemini AI để sinh mảng lệnh vẽ bổ sung."""
        from app.services.ai.prompt import build_solution_geometry_prompt

        prompt = build_solution_geometry_prompt(cac_buoc_giai, existing_commands)

        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: self.gemini_service.gemini_client._generate_with_retry(
                model=self.gemini_service.gemini_client.model_name,
                contents=prompt,
                config=self.gemini_service.gemini_client.generation_config,
            ),
        )

        text = (response.text or "").strip()

        # Parse JSON response
        cleaned = text
        if "```" in cleaned:
            m = re.search(r"```(?:json)?\s*([\s\S]+?)\s*```", cleaned)
            if m:
                cleaned = m.group(1).strip()

        try:
            commands = json.loads(cleaned)
        except json.JSONDecodeError as e:
            # Fallback: tìm mảng [ ... ] đầu tiên
            m = re.search(r"\[[\s\S]+\]", cleaned)
            if not m:
                # Nếu Gemini trả về rỗng hoặc không parse được → trả mảng rỗng
                print(f"⚠️ [solution_geometry] Gemini không trả về JSON hợp lệ: {e}")
                return []
            commands = json.loads(m.group(0))

        if isinstance(commands, dict):
            commands = commands.get("commands") or commands.get("steps") or []

        if not isinstance(commands, list):
            return []

        # Validate
        ALLOWED_FN = {
            "drawPoint", "drawEdge", "drawLabel",
            "drawRightAngle", "drawEqualMark", "drawAngle",
        }
        valid_commands = []
        for cmd in commands:
            if not isinstance(cmd, dict):
                continue
            fn = cmd.get("fn")
            args = cmd.get("args") or {}
            if fn not in ALLOWED_FN:
                print(f"⚠️ [solution_geometry] Bỏ qua lệnh: {fn}")
                continue
            valid_commands.append({"fn": fn, "args": args})

        return valid_commands

    def get_merged_geometry(self, ma_loi_giai: int, ma_bai_toan: int) -> dict:
        """
        Merge hình ban đầu (DUNGHINH3D) + hình bổ sung (DUNGHINH3D_LOIGIAI).

        Returns:
            dict chứa:
            - base_commands: lệnh vẽ hình ban đầu
            - additional_commands: lệnh vẽ bổ sung
            - merged_commands: tất cả lệnh đã merge
            - all_points: dict tất cả điểm (base + new)
        """
        # Lấy hình ban đầu
        dung_hinh = self.dunghinh_repo.get_by_bai_toan(ma_bai_toan)
        base_commands = []
        if dung_hinh:
            base_commands = json.loads(dung_hinh.get("cacBuocVe", "[]"))

        # Lấy hình bổ sung
        additional_commands = []
        solution_geo = self.dunghinh_loigiai_repo.get_by_loi_giai(ma_loi_giai)
        if solution_geo:
            additional_commands = json.loads(solution_geo.get("cacBuocVe", "[]"))

        # Merge: base trước, additional sau (nhưng trước setCamera)
        merged = []
        set_camera_cmd = None

        for cmd in base_commands:
            if cmd.get("fn") == "setCamera":
                set_camera_cmd = cmd
            else:
                merged.append(cmd)

        # Thêm lệnh bổ sung
        for cmd in additional_commands:
            merged.append(cmd)

        # setCamera cuối cùng
        if set_camera_cmd:
            merged.append(set_camera_cmd)

        # Trích tất cả điểm
        all_points = {}
        for cmd in merged:
            if cmd.get("fn") == "drawPoint":
                a = cmd.get("args", {})
                if a.get("name"):
                    all_points[a["name"]] = [a.get("x", 0), a.get("y", 0), a.get("z", 0)]

        return {
            "base_commands": base_commands,
            "additional_commands": additional_commands,
            "merged_commands": merged,
            "all_points": all_points,
            "has_additional": len(additional_commands) > 0,
        }

    def _commands_to_guide(self, commands: list) -> str:
        """Chuyển mảng lệnh bổ sung thành hướng dẫn text."""
        if not commands:
            return "Không cần vẽ thêm gì."

        lines = ["HƯỚNG DẪN VẼ BỔ SUNG (theo lời giải):", ""]
        step = 1

        for cmd in commands:
            fn = cmd.get("fn", "")
            args = cmd.get("args", {})

            if fn == "drawPoint":
                name = args.get("name", "?")
                x = args.get("x", 0)
                y = args.get("y", 0)
                z = args.get("z", 0)
                lines.append(f"Bước {step}: Vẽ điểm {name} tại ({x:.2f}, {y:.2f}, {z:.2f})")
                step += 1
            elif fn == "drawEdge":
                fr = args.get("from", "?")
                to = args.get("to", "?")
                opts = args.get("opts", {})
                style = opts.get("style", "solid")
                desc = f"nét đứt" if style == "dashed" else "nét liền"
                lines.append(f"Bước {step}: Vẽ đoạn {fr}{to} ({desc})")
                step += 1
            elif fn == "drawRightAngle":
                vertex = args.get("vertex", "?")
                lines.append(f"Bước {step}: Ký hiệu góc vuông tại {vertex}")
                step += 1
            elif fn == "drawEqualMark":
                fr = args.get("from", "?")
                to = args.get("to", "?")
                lines.append(f"Bước {step}: Ký hiệu đoạn bằng nhau {fr}-{to}")
                step += 1
            elif fn == "drawLabel":
                text = args.get("text", "")
                lines.append(f"Bước {step}: Ghi nhãn \"{text}\"")
                step += 1

        return "\n".join(lines)
