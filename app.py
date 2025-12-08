# app.py
import streamlit as st
import sys
import os

# 1. src 폴더를 경로에 추가 (agent 모듈을 찾기 위함)
# 현재 파일(app.py)의 위치를 기준으로 'src' 폴더를 찾아서 파이썬 라이브러리 경로에 추가합니다.
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, 'src')
sys.path.append(src_path)

# 2. agent 패키지에서 함수 불러오기
# src/agent/__init__.py 에 작성한 함수를 가져옵니다.
try:
    from agent import get_marketing_message
except ImportError:
    st.error("❌ 'src/agent' 폴더를 찾을 수 없거나 코드가 비어있습니다. 경로를 확인해주세요.")
    st.stop()

# ---------------------------------------------------------
# Streamlit UI 설정
# ---------------------------------------------------------
st.set_page_config(
    page_title="Amore Marketing Agent (Gemini)",
    page_icon="💄",
    layout="wide"
)

# 헤더 영역
col1, col2 = st.columns([1, 5])
with col1:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Google_Gemini_logo.svg/2560px-Google_Gemini_logo.svg.png", width=80)
with col2:
    st.title("Amorepacific Marketing Agent")
    st.caption("Powered by Google Gemini (Latest) 🚀")

st.markdown("---")

# 사이드바 (설정)
with st.sidebar:
    st.header("⚙️ 설정 (Settings)")
    st.info("현재 **무료 Gemini 모드**로 실행 중입니다.")
    
    target_customer = st.selectbox(
        "타겟 고객층", 
        ["20대 대학생", "30대 직장인 여성", "40대 주부", "MZ세대 남성", "50대 액티브 시니어"]
    )
    product_line = st.text_input("제품명/라인업", value="설화수 자음생크림")
    tone = st.radio("문구 톤앤매너", ["감성적인", "논리적인", "유머러스한", "간결한"])

# 메인 입력 영역
st.subheader("📝 마케팅 포인트 입력")
user_intent = st.text_area(
    "강조하고 싶은 핵심 키워드를 입력하세요", 
    value="탄력, 안티에이징, 부모님 선물용, 고급스러운 패키지",
    height=100
)

# 실행 버튼
if st.button("마케팅 메시지 생성하기 ✨", use_container_width=True):
    if not user_intent:
        st.warning("⚠️ 강조할 포인트를 입력해주세요.")
    else:
        with st.spinner("Gemini가 창의적인 카피를 고민하고 있습니다... 🤖"):
            try:
                # 프롬프트 조합
                full_topic = f"""
                - 타겟 고객: {target_customer}
                - 제품: {product_line}
                - 원하는 톤: {tone}
                - 강조 포인트: {user_intent}
                """
                
                # AI 에이전트 호출 (agent/__init__.py 의 함수 실행)
                result = get_marketing_message(full_topic)
                
                # 결과 출력
                st.success("생성 완료!")
                st.markdown("### 💌 생성된 메시지")
                st.info(result)
                
            except Exception as e:
                st.error(f"에러가 발생했습니다: {e}")
                st.markdown("Tip: `.env` 파일에 `GOOGLE_API_KEY`가 올바르게 들어있는지 확인해보세요.")