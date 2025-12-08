# src/agent/__init__.py
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser  # <--- 포장지 벗기는 도구 추가!

# 환경변수 로드
load_dotenv(dotenv_path="config/.env")

def get_marketing_message(topic):
    """
    주제(topic)를 받아서 마케팅 메시지를 생성하는 함수
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        return "오류: .env 파일에 GOOGLE_API_KEY가 설정되지 않았습니다."

    # LLM 설정 (최신 모델)
    llm = ChatGoogleGenerativeAI(
        model="gemini-flash-latest", 
        temperature=0.7,
        google_api_key=api_key
    )
    
    # 프롬프트 템플릿
    prompt = ChatPromptTemplate.from_messages([
        ("system", "당신은 아모레퍼시픽의 전문 마케팅 카피라이터입니다. 고객의 니즈에 맞춰 감성적이고 설득력 있는 메시지를 작성하세요. 이모지를 적절히 사용하여 생동감을 더하세요."),
        ("user", "{topic}에 대한 마케팅 메시지를 작성해줘.")
    ])
    
    # 체인 연결 (프롬프트 -> AI -> 포장지 제거)
    chain = prompt | llm | StrOutputParser()
    
    # 실행 (이제 .content를 붙일 필요 없이 바로 글자가 나옵니다)
    response = chain.invoke({"topic": topic})
    
    return response