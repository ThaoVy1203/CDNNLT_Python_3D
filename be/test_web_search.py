"""
Test web search service với Serper.dev (Google Search API)
"""
from app.services.web_search_service import WebSearchService

def test_search():
    print("=" * 60)
    print("TEST WEB SEARCH SERVICE (SERPER.DEV)")
    print("=" * 60)
    
    service = WebSearchService()
    
    if not service.api_key:
        print("❌ SERPER_API_KEY not found in .env")
        print("Please add: SERPER_API_KEY=your_key")
        return
    
    # Test 1: Search với keywords hình chóp
    print("\n📝 Test 1: Tìm bài toán hình chóp")
    print("-" * 60)
    keywords = "hình chóp góc vuông góc"
    results = service.search(keywords, max_results=10)
    
    print(f"\n✅ Tìm thấy {len(results)} kết quả:")
    for i, result in enumerate(results[:5], 1):
        print(f"\n{i}. {result['title']}")
        print(f"   Domain: {result['domain']}")
        print(f"   URL: {result['url']}")
        print(f"   Snippet: {result['snippet'][:100]}...")
    
    # Test 2: Search với site filter
    print("\n\n📝 Test 2: Tìm chỉ trong khoahoc.vietjack.com")
    print("-" * 60)
    results2 = service.search_with_site_filter(
        "hình chóp thể tích",
        "khoahoc.vietjack.com"
    )
    
    print(f"\n✅ Tìm thấy {len(results2)} kết quả từ vietjack:")
    for i, result in enumerate(results2, 1):
        print(f"\n{i}. {result['title']}")
        print(f"   URL: {result['url']}")
    
    print("\n" + "=" * 60)
    print("HOÀN THÀNH!")
    print("=" * 60)

if __name__ == "__main__":
    test_search()
