# test_model.py
import os
from dotenv import load_dotenv
import google.generativeai as genai

# .env 로드
load_dotenv("config/.env")
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("❌ 키가 없습니다. .env를 확인하세요.")
else:
    genai.configure(api_key=api_key)
    print(f"✅ 키 확인됨: {api_key[:5]}...")
    
    print("\n🔍 사용 가능한 모델 목록:")
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f" - {m.name}")
    except Exception as e:
        print(f"❌ 에러 발생: {e}")