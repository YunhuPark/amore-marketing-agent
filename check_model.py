"""
Google Generative AI 모델 목록 확인 스크립트
"""
import google.generativeai as genai
from dotenv import load_dotenv
import os

# .env 파일에서 API 키 로드 (config/.env 경로)
from pathlib import Path
env_path = Path("config") / ".env"
load_dotenv(env_path)
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("ERROR: GOOGLE_API_KEY를 찾을 수 없습니다.")
    print("config/.env 파일을 확인하세요.")
    exit(1)

# API 키 설정
genai.configure(api_key=api_key)

print("=" * 70)
print("Google Generative AI - generateContent 지원 모델 목록")
print("=" * 70)

# 모든 모델 리스트 확인
models = genai.list_models()

gemini_models = []
for model in models:
    # generateContent 메서드를 지원하는 모델만 필터링
    if 'generateContent' in model.supported_generation_methods:
        print(f"\n모델명: {model.name}")
        print(f"  - Display Name: {model.display_name}")
        print(f"  - Description: {model.description}")
        print(f"  - Supported Methods: {model.supported_generation_methods}")

        # gemini가 포함된 모델만 별도 저장
        if 'gemini' in model.name.lower():
            gemini_models.append(model.name)

print("\n" + "=" * 70)
print("Gemini 모델 목록 (generateContent 지원):")
print("=" * 70)
for model_name in gemini_models:
    print(f"  - {model_name}")

print("\n" + "=" * 70)
print(f"총 {len(gemini_models)}개의 Gemini 모델을 찾았습니다.")
print("=" * 70)
