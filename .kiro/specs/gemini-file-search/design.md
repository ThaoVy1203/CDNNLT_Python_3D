# Design Document - Gemini File Search Integration

## Overview

Tích hợp Gemini File Search API để sử dụng tài liệu hình học không gian làm context khi giải toán. Hệ thống sẽ tự động upload PDF files từ `Documents/`, tạo index, và search nội dung liên quan khi cần giải toán.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Gemini File Search Flow                   │
└─────────────────────────────────────────────────────────────┘

1. STARTUP PHASE:
   Documents/*.pdf → FileSearchService.initialize()
                  → Upload to Gemini File Search
                  → Create/Update Index

2. SOLVE PROBLEM PHASE:
   Problem Text → FileSearchService.search(query)
               → Gemini File Search API
               → Relevant Documents Context
               → Enhanced Prompt → Gemini AI
               → Solution with References

3. RESPONSE:
   {
     "solution": {...},
     "references": [
       {"file": "Tom_tat_ly_thuyet.pdf", "excerpt": "..."}
     ]
   }
```

## Components and Interfaces

### 1. FileSearchService (`be/app/services/file_search_service.py`)

Service chính quản lý Gemini File Search.

```python
class FileSearchService:
    def __init__(self):
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.index_name = "geometry-documents-index"
        self.documents_path = Path("Documents")
        self.index_id = None
        
    async def initialize(self) -> bool:
        """Khởi tạo index và upload files"""
        
    async def upload_documents(self) -> List[str]:
        """Upload tất cả PDF files từ Documents/"""
        
    async def search(self, query: str, max_results: int = 3) -> List[dict]:
        """Search tài liệu liên quan"""
        
    async def get_index_status(self) -> dict:
        """Lấy trạng thái index"""
        
    async def refresh_index(self) -> bool:
        """Refresh toàn bộ index"""
```

### 2. Enhanced GeminiService (`be/app/services/gemini_service.py`)

Mở rộng GeminiService để tích hợp File Search.

```python
class GeminiService:
    def __init__(self):
        self.file_search = FileSearchService()
        
    async def solve_problem_with_context(
        self, 
        problem_text: str
    ) -> dict:
        """
        Giải toán với context từ tài liệu
        
        Returns:
            {
                "steps": [...],
                "result": "...",
                "formulas_used": [...],
                "references": [
                    {
                        "file": "Tom_tat_ly_thuyet.pdf",
                        "excerpt": "...",
                        "relevance_score": 0.95
                    }
                ]
            }
        """
```

### 3. Configuration (`be/app/core/config.py`)

Thêm cấu hình cho File Search.

```python
class Settings(BaseSettings):
    # Existing settings...
    
    # File Search Settings
    USE_FILE_SEARCH: bool = True
    DOCUMENTS_PATH: str = "Documents"
    MAX_SEARCH_RESULTS: int = 3
    FILE_SEARCH_INDEX_NAME: str = "geometry-documents-index"
```

### 4. API Endpoint Updates (`be/app/api/routes/geometry.py`)

Cập nhật endpoint giải toán để sử dụng File Search.

```python
@router.post("/solve-problem/{ma_bai_toan}")
async def solve_problem_with_ai(ma_bai_toan: int):
    """
    Giải toán với context từ tài liệu (nếu bật USE_FILE_SEARCH)
    """
    # Existing code...
    
    # NEW: Use File Search if enabled
    if settings.USE_FILE_SEARCH:
        solution = await gemini_service.solve_problem_with_context(problem_text)
    else:
        solution = await gemini_service.solve_problem(problem_text)
    
    # Return solution with references
    return {
        "success": True,
        "data": {
            "solution": solution,
            "references": solution.get("references", []),
            "usedFileSearch": settings.USE_FILE_SEARCH
        }
    }
```

## Data Models

### FileSearchIndex

```python
{
    "index_id": "abc123",
    "index_name": "geometry-documents-index",
    "files": [
        {
            "file_id": "file_xyz",
            "filename": "Tom_tat_ly_thuyet_Hinh_khong_gian.pdf",
            "size_bytes": 1024000,
            "upload_date": "2024-01-15T10:30:00Z",
            "status": "active"
        }
    ],
    "total_files": 2,
    "total_size_mb": 5.2,
    "last_updated": "2024-01-15T10:30:00Z"
}
```

### SearchResult

```python
{
    "query": "Tính thể tích hình chóp",
    "results": [
        {
            "file": "Tom_tat_ly_thuyet_Hinh_khong_gian.pdf",
            "excerpt": "Công thức thể tích hình chóp: V = (1/3) × S_đáy × h",
            "relevance_score": 0.95,
            "page": 12
        }
    ],
    "search_time_ms": 150
}
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Index initialization idempotence
*For any* system startup, calling initialize() multiple times should result in the same index state without duplicating files
**Validates: Requirements 2.1**

### Property 2: File upload uniqueness
*For any* PDF file in Documents/, uploading it multiple times should only create one entry in the index
**Validates: Requirements 2.1**

### Property 3: Search relevance ordering
*For any* search query, results should be ordered by relevance score from highest to lowest
**Validates: Requirements 1.3**

### Property 4: Context injection consistency
*For any* problem text, if File Search is enabled and finds results, the enhanced prompt should include context from those results
**Validates: Requirements 1.4**

### Property 5: Fallback behavior
*For any* File Search API error or quota exceeded, the system should fallback to solving without context and log the error
**Validates: Requirements 4.4**

### Property 6: Reference tracking
*For any* solution generated with File Search, the response should include references to all documents used as context
**Validates: Requirements 3.1, 3.2**

## Error Handling

### 1. File Upload Errors

```python
try:
    file_id = await upload_file(pdf_path)
except FileNotFoundError:
    logger.error(f"File not found: {pdf_path}")
    continue  # Skip this file
except FileSizeExceeded:
    logger.warning(f"File too large: {pdf_path}")
    continue
except APIQuotaExceeded:
    logger.error("Gemini API quota exceeded")
    return False  # Stop uploading
```

### 2. Search Errors

```python
try:
    results = await file_search.search(query)
except APIError as e:
    logger.error(f"File Search API error: {e}")
    results = []  # Fallback to empty results
except Timeout:
    logger.warning("File Search timeout")
    results = []
```

### 3. Index Errors

```python
try:
    await file_search.initialize()
except IndexCreationError:
    logger.error("Failed to create index")
    settings.USE_FILE_SEARCH = False  # Disable File Search
```

## Testing Strategy

### Unit Tests

1. **test_file_search_service.py**
   - Test upload_documents() với mock files
   - Test search() với mock query
   - Test initialize() idempotence
   - Test error handling

2. **test_gemini_service_with_context.py**
   - Test solve_problem_with_context() với mock search results
   - Test prompt enhancement với context
   - Test fallback khi không có results

### Integration Tests

1. **test_file_search_integration.py**
   - Test upload thật với PDF files
   - Test search thật với Gemini API
   - Test end-to-end flow: upload → search → solve

### Property-Based Tests

1. **test_file_search_properties.py**
   - Property 1: Index initialization idempotence
   - Property 2: File upload uniqueness
   - Property 3: Search relevance ordering
   - Property 5: Fallback behavior
   - Property 6: Reference tracking

## Performance Considerations

### 1. Caching

- Cache search results trong 1 giờ để tránh query lại
- Cache index status trong 5 phút

### 2. Batch Upload

- Upload files theo batch (5 files/batch) để tránh timeout
- Retry failed uploads với exponential backoff

### 3. Async Operations

- Tất cả operations đều async để không block
- Use asyncio.gather() cho parallel uploads

## Security Considerations

### 1. API Key Protection

- GEMINI_API_KEY phải được lưu trong .env
- Không log API key trong logs

### 2. File Validation

- Chỉ accept PDF files
- Kiểm tra file size < 10MB
- Scan for malicious content (optional)

### 3. Rate Limiting

- Giới hạn số lượng search queries/minute
- Implement exponential backoff khi hit rate limit

## Deployment Notes

### 1. Environment Variables

```env
# File Search Configuration
USE_FILE_SEARCH=true
DOCUMENTS_PATH=Documents
MAX_SEARCH_RESULTS=3
FILE_SEARCH_INDEX_NAME=geometry-documents-index
```

### 2. Startup Sequence

1. Load configuration
2. Initialize FileSearchService
3. Upload documents (async, không block startup)
4. Start API server

### 3. Monitoring

- Log số lượng files uploaded
- Log search queries và results
- Alert khi API quota gần hết
