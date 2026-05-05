"""
Kiểm tra API key Gemini còn hoạt động không
Chạy: py check_quota.py
"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).parent / ".env")
api_key = os.getenv("GEMINI_API_KEY", "")

print("=" * 50)
print("KIEM TRA GEMINI API KEY")
print("=" * 50)
print(f"API Key: {api_key[:15]}...")
print()

try:
    from google import genai
    from google.genai import types
    client = genai.Client(api_key=api_key)

    models_to_try = [
        "gemini-2.0-flash-exp",
        "gemini-1.5-flash",
        "gemini-1.5-flash-8b",
        "gemini-2.5-flash",
        "gemini-2.0-flash",
        "gemini-2.0-flash-lite",
        "gemini-1.5-flash-latest",
        "gemini-1.5-pro",
    ]

    working = None
    for model in models_to_try:
        try:
            resp = client.models.generate_content(
                model=model,
                contents="Say OK",
                config=types.GenerateContentConfig(max_output_tokens=5)
            )
            print(f"OK  {model} -> '{resp.text.strip()}'")
            if not working:
                working = model
        except Exception as e:
            err = str(e)[:80]
            print(f"FAIL {model} -> {err}")

    print()
    if working:
        print(f"=> Dung model: '{working}'")
        print(f"   Cap nhat vao gemini_client.py: self.model_name = '{working}'")
    else:
        print("=> Khong co model nao hoat dong!")
        print("   Tao API key moi tai: https://aistudio.google.com/apikey")

except Exception as e:
    print(f"LOI: {e}")
    print()
    print("Nguyen nhan co the:")
    if "403" in str(e):
        print("  - API key bi block -> Tao key moi tu account khac")
        print("  - Vao: https://aistudio.google.com/apikey")
    elif "401" in str(e):
        print("  - API key khong hop le")
    else:
        print("  - Kiem tra ket noi internet")
