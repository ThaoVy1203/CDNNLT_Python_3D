"""
Service tìm kiếm web với Serper.dev (Google Search API)
Thay thế DuckDuckGo để có kết quả chính xác hơn
"""
import requests
import os
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()


class WebSearchService:
    """Service tìm kiếm web với Serper.dev"""
    
    def __init__(self):
        self.api_key = os.getenv('SERPER_API_KEY')
        self.api_url = 'https://google.serper.dev/search'
        self.priority_domains = [
            "khoahoc.vietjack.com",
            "hoidap247.com",
            "toanmath.com",
            "vndoc.vn",
            "hoc247.net"
        ]
        
        if not self.api_key:
            print("⚠️ SERPER_API_KEY not found in .env")
    
    def search(self, keywords: str, max_results: int = 20) -> List[Dict]:
        """
        Tìm kiếm web với Serper.dev (Google Search)
        
        Args:
            keywords: Keywords để search
            max_results: Số kết quả tối đa (default: 20)
        
        Returns:
            List các kết quả search với URL thật
        """
        try:
            # Tạo query tối ưu cho bài toán hình học
            query = f"{keywords} hình học không gian lớp 11 12"
            
            print(f"🔍 Searching Google via Serper for: {query}")
            
            # Call Serper API
            headers = {
                'X-API-KEY': self.api_key,
                'Content-Type': 'application/json'
            }
            
            payload = {
                'q': query,
                'num': max_results,
                'gl': 'vn',  # Vietnam
                'hl': 'vi'   # Vietnamese
            }
            
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=10
            )
            
            if response.status_code != 200:
                print(f"❌ Serper API error: {response.status_code}")
                print(f"Response: {response.text}")
                return []
            
            data = response.json()
            organic_results = data.get('organic', [])
            
            print(f"📊 Found {len(organic_results)} results from Google")
            
            # Convert to standard format
            valid_results = []
            for result in organic_results:
                url = result.get('link', '')
                title = result.get('title', '')
                snippet = result.get('snippet', '')
                
                # Validate URL
                if self._is_valid_url(url):
                    valid_results.append({
                        'url': url,
                        'title': title,
                        'snippet': snippet,
                        'domain': self._extract_domain(url)
                    })
            
            print(f"✅ Found {len(valid_results)} valid results")
            
            # Sắp xếp theo priority domains
            sorted_results = self._sort_by_priority(valid_results)
            
            return sorted_results
            
        except requests.exceptions.Timeout:
            print("❌ Serper API timeout")
            return []
        except requests.exceptions.RequestException as e:
            print(f"❌ Error calling Serper API: {e}")
            return []
        except Exception as e:
            print(f"❌ Error searching web: {e}")
            return []
    
    def _is_valid_url(self, url: str) -> bool:
        """
        Kiểm tra URL có hợp lệ không (chỉ check domain, không check HTTP)
        
        Args:
            url: URL cần kiểm tra
        
        Returns:
            True nếu URL hợp lệ
        """
        if not url or not url.startswith('http'):
            return False
        
        # Check domain có trong danh sách ưu tiên hoặc liên quan đến toán học
        domain = self._extract_domain(url)
        
        # Ưu tiên các domain giáo dục Việt Nam
        valid_keywords = [
            'vietjack', 'hoidap', 'toanmath', 'vndoc', 'hoc247',
            'violet', 'olm', 'loigiaihay', 'tailieu', 'thuvien',
            'edu', 'toan', 'hoc', 'bai', 'giai'
        ]
        
        # Chấp nhận nếu domain chứa keyword hợp lệ
        return any(keyword in domain.lower() for keyword in valid_keywords)
    
    def _extract_domain(self, url: str) -> str:
        """Trích xuất domain từ URL"""
        try:
            from urllib.parse import urlparse
            parsed = urlparse(url)
            return parsed.netloc
        except:
            return ""
    
    def _sort_by_priority(self, results: List[Dict]) -> List[Dict]:
        """
        Sắp xếp kết quả theo priority domains
        
        Args:
            results: List kết quả search
        
        Returns:
            List đã sắp xếp, priority domains lên đầu
        """
        def get_priority(result):
            domain = result.get('domain', '')
            for i, priority_domain in enumerate(self.priority_domains):
                if priority_domain in domain:
                    return i
            return 999  # Không có trong priority list
        
        return sorted(results, key=get_priority)
    
    def search_with_site_filter(self, keywords: str, site: str) -> List[Dict]:
        """
        Tìm kiếm chỉ trong 1 site cụ thể
        
        Args:
            keywords: Keywords
            site: Domain (ví dụ: khoahoc.vietjack.com)
        
        Returns:
            List kết quả từ site đó
        """
        query = f"site:{site} {keywords}"
        
        try:
            headers = {
                'X-API-KEY': self.api_key,
                'Content-Type': 'application/json'
            }
            
            payload = {
                'q': query,
                'num': 5,
                'gl': 'vn',
                'hl': 'vi'
            }
            
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=10
            )
            
            if response.status_code != 200:
                return []
            
            data = response.json()
            organic_results = data.get('organic', [])
            
            return [{
                'url': r.get('link', ''),
                'title': r.get('title', ''),
                'snippet': r.get('snippet', ''),
                'domain': site
            } for r in organic_results]
            
        except Exception as e:
            print(f"❌ Error searching site {site}: {e}")
            return []
