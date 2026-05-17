"""
Script tạo cache mẫu cho bài toán tương tự
Dùng để test mà không cần upload ảnh
"""
import json
from app.repositories.bai_toan_tuong_tu_cache_repository import BaiToanTuongTuCacheRepository

def seed_sample_cache():
    repo = BaiToanTuongTuCacheRepository()
    
    print("=" * 60)
    print("TẠO CACHE MẪU")
    print("=" * 60)
    
    # Cache mẫu 1: Hình chóp + góc
    sample1_keywords = "hình chóp, góc, vuông góc"
    sample1_data = [
        {
            "title": "Cho hình chóp S.ABC có đáy ABC là tam giác vuông tại B",
            "source": "khoahoc.vietjack.com",
            "url": "https://khoahoc.vietjack.com/question/448010/cho-hinh-chop-s-abc-co-day-abc-la-tam-giac-vuong-tai-b",
            "summary": "Cho hình chóp S.ABC có đáy ABC là tam giác vuông tại B, biết SA vuông góc với mặt phẳng đáy. Tính góc giữa SC và mặt phẳng (ABC).",
            "difficulty": "Trung bình"
        },
        {
            "title": "Hình chóp S.ABCD có đáy là hình vuông",
            "source": "hoidap247.com",
            "url": "https://hoidap247.com/cau-hoi/3314691",
            "summary": "Cho hình chóp S.ABCD có đáy ABCD là hình vuông cạnh a, SA vuông góc với đáy. Tính góc giữa hai mặt phẳng.",
            "difficulty": "Trung bình"
        },
        {
            "title": "Hình chóp tứ giác đều - Tính góc giữa cạnh bên và đáy",
            "source": "khoahoc.vietjack.com",
            "url": "https://khoahoc.vietjack.com/question/450000/hinh-chop-tu-giac-deu-tinh-goc",
            "summary": "Cho hình chóp tứ giác đều S.ABCD có cạnh đáy bằng a, cạnh bên bằng 2a. Tính góc giữa SA và (ABCD).",
            "difficulty": "Dễ"
        },
        {
            "title": "Góc giữa đường thẳng và mặt phẳng trong hình chóp",
            "source": "hoidap247.com",
            "url": "https://hoidap247.com/cau-hoi/3315000",
            "summary": "Cho hình chóp S.ABC có đáy là tam giác đều, SA ⊥ (ABC). Tính góc giữa SB và mặt phẳng đáy.",
            "difficulty": "Trung bình"
        },
        {
            "title": "Hình chóp có cạnh bên vuông góc với đáy",
            "source": "khoahoc.vietjack.com",
            "url": "https://khoahoc.vietjack.com/question/451000/hinh-chop-canh-ben-vuong-goc-day",
            "summary": "Cho hình chóp S.ABCD, đáy ABCD là hình chữ nhật, SA ⊥ (ABCD). Tính góc giữa SD và (ABCD).",
            "difficulty": "Dễ"
        }
    ]
    
    # Cache mẫu 2: Hình chóp + thể tích
    sample2_keywords = "hình chóp, thể tích"
    sample2_data = [
        {
            "title": "Bài 1: Tính thể tích hình chóp tứ giác đều",
            "source": "toanmath.com",
            "url": "https://toanmath.com/the-tich-hinh-chop",
            "summary": "Cho hình chóp đều S.ABCD có cạnh đáy a, chiều cao h. Tính thể tích.",
            "difficulty": "Dễ"
        },
        {
            "title": "Bài 2: Thể tích hình chóp có đáy là hình vuông",
            "source": "hoc247.net",
            "url": "https://hoc247.net/bai-tap-the-tich-hinh-chop",
            "summary": "Hình chóp S.ABCD có đáy ABCD là hình vuông cạnh a, SA ⊥ (ABCD), SA = 2a. Tính thể tích.",
            "difficulty": "Trung bình"
        },
        {
            "title": "Bài 3: Đề thi THPT QG 2022 - Thể tích hình chóp",
            "source": "vndoc.vn",
            "url": "https://vndoc.vn/de-thi-thpt-2022-toan",
            "summary": "Cho hình chóp S.ABC có đáy là tam giác vuông tại B, SA ⊥ (ABC). Tính thể tích khối chóp.",
            "difficulty": "Trung bình"
        }
    ]
    
    # Cache mẫu 3: Hình lăng trụ
    sample3_keywords = "hình lăng trụ, thể tích"
    sample3_data = [
        {
            "title": "Bài 1: Thể tích lăng trụ đứng tam giác",
            "source": "toanmath.com",
            "url": "https://toanmath.com/lang-tru-dung",
            "summary": "Cho lăng trụ đứng ABC.A'B'C' có đáy là tam giác vuông, tính thể tích.",
            "difficulty": "Dễ"
        },
        {
            "title": "Bài 2: Lăng trụ xiên và thể tích",
            "source": "hoc247.net",
            "url": "https://hoc247.net/lang-tru-xien",
            "summary": "Lăng trụ xiên có đáy là hình chữ nhật, tính thể tích khi biết chiều cao.",
            "difficulty": "Khó"
        }
    ]
    
    # Lưu cache
    samples = [
        (sample1_keywords, sample1_data),
        (sample2_keywords, sample2_data),
        (sample3_keywords, sample3_data)
    ]
    
    for keywords, data in samples:
        try:
            json_data = json.dumps(data, ensure_ascii=False)
            success = repo.create(keywords, json_data)
            
            if success:
                print(f"✅ Đã tạo cache: {keywords}")
            else:
                print(f"⚠️ Cache đã tồn tại: {keywords}")
        except Exception as e:
            print(f"❌ Lỗi khi tạo cache '{keywords}': {e}")
    
    print("\n" + "=" * 60)
    print("HOÀN THÀNH!")
    print("=" * 60)
    print("\n💡 Bây giờ bạn có thể:")
    print("   1. Chạy: python check_cache.py")
    print("   2. Hoặc test API: curl http://localhost:8000/bai-toan/1/similar")

if __name__ == "__main__":
    seed_sample_cache()
