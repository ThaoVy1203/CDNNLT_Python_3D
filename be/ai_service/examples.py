"""
Ví dụ sử dụng Gemini Client cho trích xuất dữ liệu hình học
"""

import asyncio
import base64
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

from gemini_client import GeminiClient, solve_with_ai
from be.api_gateway.schemas.geometry import GeometryExtraction


# ============= VÍ DỤ 1: Trích xuất từ văn bản =============

async def example_text_extraction():
    """Ví dụ trích xuất từ văn bản thuần túy"""
    
    print("=" * 60)
    print("VÍ DỤ 1: TRÍCH XUẤT TỪ VĂN BẢN")
    print("=" * 60)
    
    problem = """
    Cho hình chóp S.ABC có đáy ABC là tam giác vuông tại B, AB = 3, BC = 4.
    SA vuông góc với mặt phẳng (ABC) và SA = 6.
    Tính khoảng cách từ A đến mặt phẳng (SBC).
    """
    
    try:
        result = await solve_with_ai(problem=problem)
        
        print(f"\n✓ Trích xuất thành công!")
        print(f"  - Loại bài toán: {result.problem_type}")
        print(f"  - Số điểm: {len(result.points)}")
        print(f"  - Số đường thẳng: {len(result.lines)}")
        print(f"  - Số mặt phẳng: {len(result.planes)}")
        print(f"  - Số quan hệ: {len(result.relations)}")
        print(f"  - Độ tin cậy: {result.confidence_score:.2f}")
        
        print("\n📍 Các điểm:")
        for point in result.points:
            coords = point.coordinates if point.coordinates else "chưa xác định"
            print(f"  - {point.name}: {coords} ({point.description})")
        
        print("\n📏 Các quan hệ hình học:")
        for rel in result.relations:
            print(f"  - {rel.entity1} {rel.relation} {rel.entity2} (confidence: {rel.confidence})")
        
        print("\n❓ Câu hỏi:")
        for q in result.questions:
            print(f"  - {q}")
        
        return result
        
    except Exception as e:
        print(f"\n✗ Lỗi: {e}")
        return None


# ============= VÍ DỤ 2: Trích xuất từ ảnh =============

async def example_image_extraction():
    """Ví dụ trích xuất từ ảnh (cần có file ảnh thực tế)"""
    
    print("\n" + "=" * 60)
    print("VÍ DỤ 2: TRÍCH XUẤT TỪ ẢNH")
    print("=" * 60)
    
    # Tạo ảnh mẫu (trong thực tế, dùng ảnh thật)
    image = create_sample_geometry_image()
    
    try:
        result = await solve_with_ai(
            image=image,
            problem="Hình chóp tam giác đều"
        )
        
        print(f"\n✓ Trích xuất từ ảnh thành công!")
        print(f"  - OCR text: {result.problem_text[:100]}...")
        print(f"  - Độ tin cậy: {result.confidence_score:.2f}")
        
        if result.extraction_notes:
            print(f"  - Ghi chú: {result.extraction_notes}")
        
        return result
        
    except Exception as e:
        print(f"\n✗ Lỗi: {e}")
        return None


# ============= VÍ DỤ 3: Sử dụng GeminiClient trực tiếp =============

async def example_advanced_usage():
    """Ví dụ sử dụng nâng cao với GeminiClient"""
    
    print("\n" + "=" * 60)
    print("VÍ DỤ 3: SỬ DỤNG NÂNG CAO")
    print("=" * 60)
    
    client = GeminiClient()
    
    problem = """
    Cho hình lăng trụ đứng ABC.A'B'C' có đáy ABC là tam giác đều cạnh a.
    AA' = 2a. Gọi M là trung điểm của BB'.
    Chứng minh AM vuông góc với BC'.
    """
    
    try:
        # Bước 1: Trích xuất cơ bản
        print("\n[1/3] Trích xuất thực thể...")
        extraction = await client.extract_from_text(problem)
        print(f"  ✓ Tìm thấy {len(extraction.points)} điểm")
        
        # Bước 2: Ước lượng tọa độ
        print("\n[2/3] Ước lượng tọa độ...")
        extraction = await client.estimate_coordinates(extraction)
        
        coords_count = sum(1 for p in extraction.points if p.coordinates)
        print(f"  ✓ Đã ước lượng tọa độ cho {coords_count}/{len(extraction.points)} điểm")
        
        # Bước 3: Hiển thị kết quả
        print("\n[3/3] Kết quả cuối cùng:")
        for point in extraction.points:
            if point.coordinates:
                print(f"  - {point.name} = {point.coordinates}")
        
        return extraction
        
    except Exception as e:
        print(f"\n✗ Lỗi: {e}")
        return None


# ============= VÍ DỤ 4: Xử lý batch =============

async def example_batch_processing():
    """Ví dụ xử lý nhiều bài toán cùng lúc"""
    
    print("\n" + "=" * 60)
    print("VÍ DỤ 4: XỬ LÝ BATCH")
    print("=" * 60)
    
    problems = [
        "Cho hình chóp S.ABC có SA = SB = SC = a. Tính thể tích.",
        "Cho hình lập phương ABCD.A'B'C'D' cạnh a. Tính khoảng cách AC và BD'.",
        "Cho tứ diện ABCD có AB = CD = a, AC = BD = b, AD = BC = c. Tính thể tích."
    ]
    
    print(f"\nXử lý {len(problems)} bài toán...\n")
    
    tasks = [solve_with_ai(problem=p) for p in problems]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    for i, result in enumerate(results, 1):
        if isinstance(result, Exception):
            print(f"[{i}] ✗ Lỗi: {result}")
        else:
            print(f"[{i}] ✓ {result.problem_type}")
            print(f"     Điểm: {len(result.points)}, Độ tin cậy: {result.confidence_score:.2f}")
    
    return results


# ============= VÍ DỤ 5: Validation và error handling =============

async def example_validation():
    """Ví dụ về validation và xử lý lỗi"""
    
    print("\n" + "=" * 60)
    print("VÍ DỤ 5: VALIDATION VÀ ERROR HANDLING")
    print("=" * 60)
    
    # Bài toán mơ hồ, khó trích xuất
    ambiguous_problem = "Tính khoảng cách giữa hai đường thẳng."
    
    try:
        client = GeminiClient()
        result = await client.extract_from_text(ambiguous_problem)
        
        print(f"\nĐộ tin cậy: {result.confidence_score:.2f}")
        
        if result.confidence_score < 0.5:
            print("⚠️  Cảnh báo: Độ tin cậy thấp!")
            print(f"   Lý do: {result.extraction_notes}")
            print("   → Cần bổ sung thông tin hoặc ảnh minh họa")
        elif result.confidence_score < 0.8:
            print("⚠️  Cảnh báo: Độ tin cậy trung bình")
            print("   → Nên kiểm tra lại kết quả")
        else:
            print("✓ Độ tin cậy cao, kết quả đáng tin cậy")
        
        return result
        
    except ValueError as e:
        print(f"\n✗ Lỗi validation: {e}")
        print("   → Kiểm tra lại format dữ liệu đầu vào")
    except Exception as e:
        print(f"\n✗ Lỗi không xác định: {e}")


# ============= VÍ DỤ 6: Export sang các format khác =============

def example_export_formats(extraction: GeometryExtraction):
    """Ví dụ export dữ liệu sang các format khác"""
    
    print("\n" + "=" * 60)
    print("VÍ DỤ 6: EXPORT SANG CÁC FORMAT")
    print("=" * 60)
    
    # 1. JSON
    print("\n[1] JSON:")
    json_str = extraction.model_dump_json(indent=2)
    print(json_str[:200] + "...")
    
    # 2. Dictionary
    print("\n[2] Python Dict:")
    data_dict = extraction.model_dump()
    print(f"  Keys: {list(data_dict.keys())}")
    
    # 3. LaTeX (simplified)
    print("\n[3] LaTeX (simplified):")
    latex = generate_latex(extraction)
    print(latex[:200] + "...")
    
    # 4. Plain text summary
    print("\n[4] Plain Text Summary:")
    summary = generate_summary(extraction)
    print(summary)


# ============= Helper Functions =============

def create_sample_geometry_image() -> Image.Image:
    """Tạo ảnh mẫu cho demo (trong thực tế dùng ảnh thật)"""
    
    img = Image.new('RGB', (800, 600), color='white')
    draw = ImageDraw.Draw(img)
    
    # Vẽ tam giác ABC
    points = [(200, 400), (600, 400), (400, 200)]
    draw.polygon(points, outline='black', width=2)
    
    # Vẽ điểm S (đỉnh chóp)
    draw.ellipse((390, 90, 410, 110), fill='black')
    
    # Vẽ các cạnh bên
    draw.line([(400, 100), (200, 400)], fill='black', width=2)
    draw.line([(400, 100), (600, 400)], fill='black', width=2)
    draw.line([(400, 100), (400, 200)], fill='black', width=2)
    
    # Thêm nhãn (cần font, bỏ qua nếu không có)
    try:
        font = ImageFont.truetype("arial.ttf", 20)
        draw.text((190, 410), "A", fill='black', font=font)
        draw.text((610, 410), "B", fill='black', font=font)
        draw.text((410, 190), "C", fill='black', font=font)
        draw.text((410, 80), "S", fill='black', font=font)
    except:
        pass
    
    return img


def generate_latex(extraction: GeometryExtraction) -> str:
    """Generate LaTeX code từ extraction data"""
    
    latex = "\\begin{tikzpicture}\n"
    
    # Vẽ các điểm
    for point in extraction.points:
        if point.coordinates:
            x, y, z = point.coordinates
            latex += f"  \\coordinate ({point.name}) at ({x},{y},{z});\n"
    
    # Vẽ các đường thẳng
    for line in extraction.lines:
        if len(line.points) >= 2:
            latex += f"  \\draw ({line.points[0]}) -- ({line.points[1]});\n"
    
    latex += "\\end{tikzpicture}"
    
    return latex


def generate_summary(extraction: GeometryExtraction) -> str:
    """Generate plain text summary"""
    
    summary = f"BÀI TOÁN: {extraction.problem_type}\n\n"
    summary += f"Cho trước:\n"
    for cond in extraction.given_conditions:
        summary += f"  - {cond}\n"
    
    summary += f"\nCâu hỏi:\n"
    for q in extraction.questions:
        summary += f"  - {q}\n"
    
    summary += f"\nCác thực thể:\n"
    summary += f"  - {len(extraction.points)} điểm\n"
    summary += f"  - {len(extraction.lines)} đường thẳng\n"
    summary += f"  - {len(extraction.planes)} mặt phẳng\n"
    summary += f"  - {len(extraction.relations)} quan hệ hình học\n"
    
    return summary


# ============= Main =============

async def main():
    """Chạy tất cả các ví dụ"""
    
    print("\n" + "=" * 60)
    print("GEMINI GEOMETRY EXTRACTION - EXAMPLES")
    print("=" * 60)
    
    # Kiểm tra API key
    import os
    if not os.getenv("GEMINI_API_KEY"):
        print("\n⚠️  Cảnh báo: GEMINI_API_KEY chưa được set!")
        print("   Set bằng: export GEMINI_API_KEY='your-key-here'")
        print("\n   Các ví dụ sẽ không chạy được.\n")
        return
    
    # Chạy các ví dụ
    try:
        # Ví dụ 1: Text extraction
        result1 = await example_text_extraction()
        
        # Ví dụ 2: Image extraction (cần ảnh thật)
        # result2 = await example_image_extraction()
        
        # Ví dụ 3: Advanced usage
        result3 = await example_advanced_usage()
        
        # Ví dụ 4: Batch processing
        # results4 = await example_batch_processing()
        
        # Ví dụ 5: Validation
        result5 = await example_validation()
        
        # Ví dụ 6: Export formats
        if result1:
            example_export_formats(result1)
        
        print("\n" + "=" * 60)
        print("HOÀN THÀNH TẤT CẢ VÍ DỤ")
        print("=" * 60 + "\n")
        
    except Exception as e:
        print(f"\n✗ Lỗi khi chạy examples: {e}")


if __name__ == "__main__":
    # Chạy async main
    asyncio.run(main())
