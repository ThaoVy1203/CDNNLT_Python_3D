"""
Script để kiểm tra các model Gemini có sẵn
"""
import os
from dotenv import load_dotenv

load_dotenv()

try:
    from google import genai
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: GEMINI_API_KEY not found in .env")
        exit(1)
    
    client = genai.Client(api_key=api_key)
    
    print("=" * 60)
    print("DANH SÁCH CÁC MODEL GEMINI CÓ SẴN:")
    print("=" * 60)
    
    # Các model phổ biến để thử
    models_to_test = [
        'gemini-2.0-flash-exp',
        'gemini-2.5-flash',
        'gemini-2.5-flash-lite',
        'gemini-1.5-flash',
        'gemini-1.5-flash-8b',
        'gemini-1.5-pro',
    ]
    
    for model_name in models_to_test:
        try:
            # Thử gọi model với prompt đơn giản
            response = client.models.generate_content(
                model=model_name,
                contents="Hello, respond with 'OK' if you're working"
            )
            status = "✅ HOẠT ĐỘNG"
            print(f"{status:20} | {model_name}")
        except Exception as e:
            error_msg = str(e)
            if "503" in error_msg or "UNAVAILABLE" in error_msg:
                status = "❌ QUÁ TẢI (503)"
            elif "429" in error_msg:
                status = "⚠️ GIỚI HẠN (429)"
            elif "404" in error_msg or "not found" in error_msg.lower():
                status = "❓ KHÔNG TỒN TẠI"
            else:
                status = f"❌ LỖI: {error_msg[:30]}"
            print(f"{status:20} | {model_name}")
    
    print("=" * 60)
    print("\nGỢI Ý:")
    print("- Nếu model hiện tại bị quá tải, hãy đổi sang model khác")
    print("- Model nhanh nhất: gemini-2.5-flash-lite, gemini-1.5-flash-8b")
    print("- Model cân bằng: gemini-2.5-flash, gemini-1.5-flash")
    print("- Model mạnh nhất: gemini-1.5-pro")
    
except ImportError:
    print("ERROR: google-genai not installed")
    print("Run: pip install google-genai")
except Exception as e:
    print(f"ERROR: {e}")
