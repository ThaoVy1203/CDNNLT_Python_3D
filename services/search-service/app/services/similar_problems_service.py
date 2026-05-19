"""
Service tìm bài toán tương tự
Flow: Keywords → Web Search → Validate → Gemini Filter → Cache
"""
import json
from typing import List, Dict
from app.services.ai.gemini_client import GeminiClient
from app.services.web_search_service import WebSearchService
from app.repositories.bai_toan_tuong_tu_cache_repository import BaiToanTuongTuCacheRepository


class SimilarProblemsService:
    """Service tìm bài toán tương tự với web search thật"""
    
    def __init__(self):
        self.gemini = GeminiClient()
        self.web_search = WebSearchService()
        self.cache_repo = BaiToanTuongTuCacheRepository()
    
    def extract_keywords(self, de_bai: str) -> str:
        """
        Trích xuất keywords từ đề bài để tìm kiếm
        
        Args:
            de_bai: Đề bài đã phân tích
        
        Returns:
            String keywords ngăn cách bởi dấu phẩy
        """
        keywords = []
        de_bai_lower = de_bai.lower()
        
        # Hình dạng
        if "hình chóp" in de_bai_lower:
            keywords.append("hình chóp")
        if "hình lăng trụ" in de_bai_lower or "lăng trụ" in de_bai_lower:
            keywords.append("hình lăng trụ")
        if "hình hộp" in de_bai_lower:
            keywords.append("hình hộp")
        if "hình nón" in de_bai_lower:
            keywords.append("hình nón")
        if "hình trụ" in de_bai_lower:
            keywords.append("hình trụ")
        if "hình cầu" in de_bai_lower:
            keywords.append("hình cầu")
        
        # Yêu cầu tính toán
        if "góc" in de_bai_lower:
            keywords.append("góc")
        if "khoảng cách" in de_bai_lower:
            keywords.append("khoảng cách")
        if "thể tích" in de_bai_lower:
            keywords.append("thể tích")
        if "diện tích" in de_bai_lower:
            keywords.append("diện tích")
        
        # Điều kiện đặc biệt
        if "vuông góc" in de_bai_lower or "⊥" in de_bai:
            keywords.append("vuông góc")
        if "song song" in de_bai_lower or "//" in de_bai:
            keywords.append("song song")
        if "trung điểm" in de_bai_lower:
            keywords.append("trung điểm")
        if "hình vuông" in de_bai_lower:
            keywords.append("đáy hình vuông")
        if "tam giác" in de_bai_lower:
            keywords.append("tam giác")
        
        # Nếu không tìm thấy keyword nào, dùng mặc định
        if not keywords:
            keywords.append("hình học không gian")
        
        return ", ".join(keywords)
    
    async def find_similar(self, de_bai: str, use_cache: bool = True) -> List[Dict]:
        """
        Tìm bài toán tương tự với flow mới:
        1. Extract keywords
        2. Check cache
        3. Web search thật (DuckDuckGo)
        4. Validate URLs
        5. Gemini filter & analyze
        6. Save cache
        
        Args:
            de_bai: Đề bài đã phân tích
            use_cache: Có dùng cache không (default: True)
        
        Returns:
            List các bài toán tương tự (max 5 bài)
        """
        # 1. Trích keywords
        keywords = self.extract_keywords(de_bai)
        print(f"🔍 Extracted keywords: {keywords}")
        
        # 2. Check cache
        if use_cache:
            cached = self.cache_repo.get_by_keywords(keywords, max_age_days=7)
            if cached:
                print(f"✅ Cache hit for keywords: {keywords}")
                try:
                    return json.loads(cached.ket_qua)
                except json.JSONDecodeError as e:
                    print(f"❌ Error parsing cached JSON: {e}")
                    pass
        
        # 3. Web search thật
        print(f"🌐 Cache miss, searching web for: {keywords}")
        search_results = self.web_search.search(keywords, max_results=20)
        
        if not search_results:
            print("❌ No search results found")
            return []
        
        print(f"📊 Got {len(search_results)} search results")
        
        # 4. Gemini filter & analyze
        filtered_results = await self._filter_with_gemini(search_results, de_bai, keywords)
        
        # 5. Lưu cache
        if filtered_results:
            try:
                results_json = json.dumps(filtered_results, ensure_ascii=False)
                self.cache_repo.create(keywords, results_json)
                print(f"💾 Saved to cache: {keywords}")
            except Exception as e:
                print(f"❌ Error saving cache: {e}")
        
        return filtered_results
    
    async def _filter_with_gemini(self, search_results: List[Dict], de_bai: str, keywords: str) -> List[Dict]:
        """
        Dùng Gemini để filter và phân tích kết quả search
        
        Args:
            search_results: Kết quả từ web search
            de_bai: Đề bài gốc
            keywords: Keywords đã trích xuất
        
        Returns:
            List 5 bài toán phù hợp nhất từ 5 nguồn khác nhau
        """
        # Chuẩn bị danh sách URL cho Gemini
        urls_info = []
        for i, result in enumerate(search_results[:15], 1):  # Chỉ lấy 15 kết quả đầu
            urls_info.append(f"{i}. {result['title']}\n   URL: {result['url']}\n   Snippet: {result['snippet'][:150]}...")
        
        urls_text = "\n\n".join(urls_info)
        
        prompt = f"""
Bạn là chuyên gia toán học. Từ kết quả tìm kiếm web, hãy chọn 5 bài toán THẬT SỰ TƯƠNG TỰ với đề bài gốc.

ĐỀ BÀI GỐC:
{de_bai[:500]}

KEYWORDS: {keywords}

KẾT QUẢ TÌM KIẾM WEB (ĐÃ VALIDATE):
{urls_text}

YÊU CẦU:
1. Chọn 5 bài toán TƯƠNG TỰ NHẤT với đề bài gốc
2. Ưu tiên các bài từ khoahoc.vietjack.com và hoidap247.com
3. Bài toán phải cùng dạng, cùng chủ đề
4. **QUAN TRỌNG: Mỗi bài phải từ DOMAIN/PATH KHÁC NHAU**
   - ✅ ĐÚNG: vietjack.com/question/123, hoidap247.com/cau-hoi/456, toanmath.com/bai-1
   - ❌ SAI: vietjack.com/question/123, vietjack.com/question/456 (cùng domain/path)
5. Đánh giá độ khó: Dễ/Trung bình/Khó
6. Viết tóm tắt ngắn gọn (max 120 ký tự)

Trả về ĐÚNG format JSON (không thêm markdown):

[
  {{
    "title": "Tiêu đề bài toán (max 80 ký tự)",
    "source": "Tên nguồn (ví dụ: khoahoc.vietjack.com)",
    "url": "URL CHÍNH XÁC từ danh sách trên",
    "summary": "Tóm tắt ngắn gọn (max 120 ký tự)",
    "difficulty": "Dễ hoặc Trung bình hoặc Khó"
  }}
]

CHÚ Ý:
- CHỈ trả về JSON array, KHÔNG thêm text giải thích
- KHÔNG thêm markdown code blocks
- URL phải CHÍNH XÁC từ danh sách trên
- **KHÔNG chọn 2 bài từ cùng 1 domain/path** (ví dụ: không chọn 2 bài từ vietjack.com/question/)
- Nếu không đủ 5 bài từ 5 nguồn khác nhau, trả về ít hơn
"""
        
        try:
            import asyncio
            loop = asyncio.get_event_loop()
            
            response = await loop.run_in_executor(
                None,
                lambda: self.gemini.client.models.generate_content(
                    model=self.gemini.model_name,
                    contents=prompt,
                    config=self.gemini.generation_config
                )
            )
            
            if not response or not response.text:
                print("❌ Gemini returned empty response")
                return []
            
            # Parse JSON
            text = response.text.strip()
            
            # Remove markdown nếu có
            if text.startswith("```json"):
                text = text[7:]
            elif text.startswith("```"):
                text = text[3:]
            
            if text.endswith("```"):
                text = text[:-3]
            
            text = text.strip()
            
            # Parse JSON
            results = json.loads(text)
            
            if not isinstance(results, list):
                print("❌ Invalid response format")
                return []
            
            # Validate results
            valid_results = []
            for item in results:
                if all(k in item for k in ["title", "source", "url", "summary"]):
                    if item["url"].startswith("http"):
                        valid_results.append(item)
                        print(f"   ✅ Gemini selected: {item['url']}")
                    else:
                        print(f"   ❌ Invalid URL from Gemini: {item.get('url', 'N/A')}")
            
            # Deduplicate by domain/path (loại bỏ các URL từ cùng domain/path)
            deduplicated = self._deduplicate_by_domain_path(valid_results)
            
            print(f"✅ Gemini filtered to {len(deduplicated)} unique problems from different sources")
            return deduplicated[:5]
            
        except json.JSONDecodeError as e:
            print(f"❌ Error parsing JSON from Gemini: {e}")
            return []
        except Exception as e:
            print(f"❌ Error filtering with Gemini: {e}")
            return []
    
    def _deduplicate_by_domain_path(self, results: List[Dict]) -> List[Dict]:
        """
        Loại bỏ các bài toán từ cùng domain/path HOẶC URL trùng hoàn toàn
        Ví dụ: Chỉ giữ 1 bài từ vietjack.com/question/, 1 bài từ hoidap247.com/cau-hoi/
        
        Args:
            results: List kết quả đã filter
        
        Returns:
            List đã loại bỏ trùng lặp domain/path và URL
        """
        from urllib.parse import urlparse
        
        seen_urls = set()  # Track exact URLs
        seen_paths = set()  # Track domain/path patterns
        unique_results = []
        
        for result in results:
            url = result.get('url', '')
            
            # Skip nếu URL trùng hoàn toàn
            if url in seen_urls:
                print(f"⚠️ Skipping exact duplicate URL: {url[:80]}")
                continue
            
            try:
                parsed = urlparse(url)
                # Lấy domain + path chính (không bao gồm ID cuối)
                # Ví dụ: vietjack.com/question/123 → vietjack.com/question
                domain = parsed.netloc
                path_parts = parsed.path.split('/')
                
                # Lấy 2 phần đầu của path (domain + section)
                if len(path_parts) >= 2:
                    base_path = f"{domain}/{path_parts[1]}"
                else:
                    base_path = domain
                
                # Chỉ thêm nếu chưa có domain/path này
                if base_path not in seen_paths:
                    seen_paths.add(base_path)
                    seen_urls.add(url)
                    unique_results.append(result)
                else:
                    print(f"⚠️ Skipping duplicate path: {base_path} - {result.get('title', '')[:50]}")
                    
            except Exception as e:
                # Nếu parse lỗi, check URL trùng
                if url not in seen_urls:
                    seen_urls.add(url)
                    unique_results.append(result)
        
        return unique_results
    
    def clear_cache(self, keywords: str = None):
        """
        Xóa cache (for debugging/maintenance)
        
        Args:
            keywords: Nếu có, chỉ xóa cache của keywords này. Nếu None, xóa tất cả cache cũ
        """
        if keywords:
            print(f"Clear cache for: {keywords}")
        else:
            deleted = self.cache_repo.delete_old_cache(days=30)
            print(f"Cleared {deleted} old cache entries")
