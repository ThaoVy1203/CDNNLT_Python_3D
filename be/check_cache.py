"""
Script kiểm tra cache bài toán tương tự
"""
from app.repositories.bai_toan_tuong_tu_cache_repository import BaiToanTuongTuCacheRepository

def check_cache():
    repo = BaiToanTuongTuCacheRepository()
    
    print("=" * 60)
    print("KIỂM TRA CACHE BÀI TOÁN TƯƠNG TỰ")
    print("=" * 60)
    
    try:
        all_cache = repo.get_all()
        
        if not all_cache:
            print("\n❌ Cache trống - chưa có dữ liệu")
            print("\n💡 Cache sẽ được tạo tự động khi:")
            print("   1. User upload ảnh bài toán")
            print("   2. AI phân tích và tìm bài tương tự")
            print("   3. Kết quả được lưu vào database")
        else:
            print(f"\n✅ Tìm thấy {len(all_cache)} cache entries:\n")
            
            for i, cache in enumerate(all_cache, 1):
                print(f"{i}. Keywords: {cache.tu_khoa}")
                print(f"   Ngày tạo: {cache.ngay_tao}")
                print(f"   Số bài: {cache.ket_qua.count('title')}")
                print()
    
    except Exception as e:
        print(f"\n❌ Lỗi khi kiểm tra cache: {e}")
        print("\n💡 Có thể bảng chưa được tạo. Chạy:")
        print("   sqlcmd -S localhost -U sa -P 123456 -i dbCDNNLT.sql")

if __name__ == "__main__":
    check_cache()
