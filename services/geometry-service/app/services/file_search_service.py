"""
File Search Service - Quản lý Gemini File Search API
Upload tài liệu PDF và search nội dung liên quan
"""
import os
import json
import hashlib
from pathlib import Path
from typing import List, Dict, Optional
import google.generativeai as genai
from app.core.config import settings


class FileSearchService:
    """Service quản lý Gemini File Search"""
    
    def __init__(self):
        """Khởi tạo File Search Service"""
        # Documents path relative to the geometry-service root.
        project_root = Path(__file__).resolve().parents[2]
        self.documents_path = project_root / settings.DOCUMENTS_PATH
        self.index_name = settings.FILE_SEARCH_INDEX_NAME
        self.max_results = settings.MAX_SEARCH_RESULTS
        self.uploaded_files = {}  # Cache: {filename: file_id}
        
        # Cache file path
        self.cache_file = project_root / ".file_search_cache.json"
        
        # Configure Gemini
        genai.configure(api_key=settings.GEMINI_API_KEY)
        
        print(f"📚 FileSearchService initialized")
        print(f"   - Documents path: {self.documents_path}")
        print(f"   - Index name: {self.index_name}")
        print(f"   - Cache file: {self.cache_file}")
    
    def _load_cache(self) -> Dict[str, Dict]:
        """
        Load cache từ file
        
        Returns:
            {
                "filename.pdf": {
                    "file_id": "files/xxx",
                    "checksum": "abc123..."
                }
            }
        """
        try:
            if self.cache_file.exists():
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"⚠️  Failed to load cache: {e}")
        return {}
    
    def _save_cache(self, cache: Dict[str, Dict]):
        """Save cache to file"""
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️  Failed to save cache: {e}")
    
    def _get_file_checksum(self, file_path: Path) -> str:
        """Tính checksum của file để detect thay đổi"""
        try:
            with open(file_path, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except Exception as e:
            print(f"⚠️  Failed to compute checksum for {file_path.name}: {e}")
            return ""
    
    async def initialize(self) -> bool:
        """
        Khởi tạo: Upload tất cả PDF files từ Documents/
        Sử dụng cache để tránh upload lại files đã có
        
        Returns:
            True nếu thành công, False nếu có lỗi
        """
        try:
            print(f"\n📤 Initializing File Search...")
            
            # Check if documents folder exists
            if not self.documents_path.exists():
                print(f"⚠️  Documents folder not found: {self.documents_path}")
                return False
            
            # Get all PDF files
            pdf_files = list(self.documents_path.glob("*.pdf"))
            if not pdf_files:
                print(f"⚠️  No PDF files found in {self.documents_path}")
                return False
            
            print(f"📄 Found {len(pdf_files)} PDF files")
            
            # Load cache
            cache = self._load_cache()
            print(f"💾 Loaded cache with {len(cache)} entries")
            
            # Process each file
            uploaded_count = 0
            reused_count = 0
            new_cache = {}
            
            for pdf_path in pdf_files:
                try:
                    filename = pdf_path.name
                    checksum = self._get_file_checksum(pdf_path)
                    
                    # Check if file exists in cache with same checksum
                    if filename in cache and cache[filename].get("checksum") == checksum:
                        # Verify file_id is still accessible (not expired or wrong key)
                        file_id = cache[filename]["file_id"]
                        if await self._verify_file_id(file_id):
                            self.uploaded_files[filename] = file_id
                            new_cache[filename] = cache[filename]
                            reused_count += 1
                            print(f"   ♻️  {filename} → {file_id} (cached, verified)")
                        else:
                            # file_id expired or inaccessible → re-upload
                            print(f"   ⚠️  {filename} → {file_id} (expired, re-uploading...)")
                            file_id = await self._upload_file(pdf_path)
                            if file_id:
                                self.uploaded_files[filename] = file_id
                                new_cache[filename] = {
                                    "file_id": file_id,
                                    "checksum": checksum
                                }
                                uploaded_count += 1
                                print(f"   ✅ {filename} → {file_id} (re-uploaded)")
                    else:
                        # Upload new/changed file
                        file_id = await self._upload_file(pdf_path)
                        if file_id:
                            self.uploaded_files[filename] = file_id
                            new_cache[filename] = {
                                "file_id": file_id,
                                "checksum": checksum
                            }
                            uploaded_count += 1
                            print(f"   ✅ {filename} → {file_id} (uploaded)")
                        
                except Exception as e:
                    print(f"   ❌ {pdf_path.name}: {e}")
                    continue
            
            # Save updated cache
            self._save_cache(new_cache)
            
            print(f"\n✅ Ready: {reused_count} cached + {uploaded_count} uploaded = {len(self.uploaded_files)} total files")
            return len(self.uploaded_files) > 0
            
        except Exception as e:
            print(f"❌ File Search initialization error: {e}")
            return False
    
    async def _verify_file_id(self, file_id: str) -> bool:
        """
        Kiểm tra file_id còn truy cập được không.
        Trả về True nếu OK, False nếu expired/403/404.
        """
        try:
            genai.get_file(file_id)
            return True
        except Exception as e:
            error_msg = str(e)
            if "403" in error_msg or "404" in error_msg or "not found" in error_msg.lower():
                return False
            # Lỗi khác (network, timeout) → coi như OK để tránh upload thừa
            print(f"   ⚠️  Verify file_id {file_id} got unexpected error: {e}")
            return True

    async def _upload_file(self, file_path: Path) -> Optional[str]:
        """
        Upload một file lên Gemini
        
        Args:
            file_path: Đường dẫn đến file
            
        Returns:
            file_id nếu thành công, None nếu lỗi
        """
        try:
            # Check file size (max 10MB)
            file_size = file_path.stat().st_size
            if file_size > 10 * 1024 * 1024:
                print(f"⚠️  File too large: {file_path.name} ({file_size / 1024 / 1024:.1f}MB)")
                return None
            
            # Upload file
            uploaded_file = genai.upload_file(
                path=str(file_path),
                display_name=file_path.name
            )
            
            return uploaded_file.name
            
        except Exception as e:
            print(f"❌ Upload error for {file_path.name}: {e}")
            return None
    
    async def search(self, query: str) -> List[Dict]:
        """
        Search tài liệu liên quan với query
        
        Args:
            query: Câu hỏi hoặc đề bài cần search
            
        Returns:
            List of relevant documents with excerpts
            [
                {
                    "file": "Tom_tat_ly_thuyet.pdf",
                    "excerpt": "Công thức thể tích...",
                    "relevance_score": 0.95
                }
            ]
        """
        try:
            if not self.uploaded_files:
                print("⚠️  No files uploaded yet")
                return []
            
            print(f"\n🔍 Searching for: {query[:100]}...")
            
            # Create a model with file search
            model = genai.GenerativeModel(
                model_name=settings.GEMINI_MODEL,
            )
            
            # Build search prompt
            search_prompt = f"""Tìm kiếm thông tin liên quan đến bài toán sau trong tài liệu:

BÀI TOÁN:
{query}

Hãy trích xuất:
1. Công thức liên quan
2. Định lý cần dùng
3. Phương pháp giải
4. Ví dụ tương tự (nếu có)

Trả về JSON format:
{{
  "relevant_content": "Nội dung liên quan...",
  "formulas": ["Công thức 1", "Công thức 2"],
  "theorems": ["Định lý 1", "Định lý 2"],
  "methods": ["Phương pháp 1", "Phương pháp 2"]
}}
"""
            
            # Generate content with files as context
            file_refs = [genai.get_file(file_id) for file_id in self.uploaded_files.values()]
            
            response = model.generate_content([search_prompt] + file_refs)
            
            # Parse response
            response_text = response.text.strip()
            
            # Extract JSON from response
            if "```json" in response_text:
                json_str = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                json_str = response_text.split("```")[1].split("```")[0].strip()
            else:
                json_str = response_text
            
            try:
                search_result = json.loads(json_str)
            except json.JSONDecodeError:
                # Fallback: use raw text
                search_result = {
                    "relevant_content": response_text,
                    "formulas": [],
                    "theorems": [],
                    "methods": []
                }
            
            # Format results
            results = []
            for filename in self.uploaded_files.keys():
                results.append({
                    "file": filename,
                    "excerpt": search_result.get("relevant_content", "")[:500],
                    "formulas": search_result.get("formulas", []),
                    "theorems": search_result.get("theorems", []),
                    "methods": search_result.get("methods", []),
                    "relevance_score": 0.9  # Placeholder
                })
            
            print(f"✅ Found {len(results)} relevant documents")
            return results[:self.max_results]
            
        except Exception as e:
            print(f"❌ Search error: {e}")
            return []
    
    def get_status(self) -> Dict:
        """
        Lấy trạng thái hiện tại của File Search
        
        Returns:
            {
                "enabled": True/False,
                "total_files": 2,
                "files": ["file1.pdf", "file2.pdf"]
            }
        """
        return {
            "enabled": settings.USE_FILE_SEARCH,
            "total_files": len(self.uploaded_files),
            "files": list(self.uploaded_files.keys()),
            "documents_path": str(self.documents_path),
            "max_results": self.max_results
        }


# Global instance
file_search_service = FileSearchService()
