"""
아모레퍼시픽 CRM 마케팅 메시지 생성 대시보드
Streamlit 기반 UI
"""

import html
import sys
from pathlib import Path
import streamlit as st
import pandas as pd


def esc(value) -> str:
    """unsafe_allow_html 로 넣는 모든 값(AI 출력·CSV 값)은 이스케이프한다."""
    return html.escape(str(value), quote=True)

# 프로젝트 루트를 sys.path에 추가
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.agent.message_generator import CRMMessageGenerator

# 페이지 설정
st.set_page_config(
    page_title="아모레퍼시픽 CRM 마케팅 Agent",
    page_icon="💄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 아모레퍼시픽 브랜드 컬러 스타일
st.markdown("""
<style>
    /* 메인 컬러: 진한 네이비 */
    .main-header {
        background: linear-gradient(135deg, #1a237e 0%, #283593 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }

    .main-header h1 {
        color: white;
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
    }

    .main-header p {
        color: #e3f2fd;
        margin-top: 0.5rem;
        font-size: 1.1rem;
    }

    /* 카드 스타일 */
    .info-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #1a237e;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }

    .product-card {
        background: #f5f5f5;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        margin-bottom: 1rem;
    }

    .message-box {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        padding: 2rem;
        border-radius: 10px;
        border: 2px solid #1a237e;
        margin-top: 2rem;
    }

    .brand-tone-box {
        background: #fff3e0;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #ff6f00;
        margin-top: 1rem;
    }

    /* 버튼 스타일 */
    .stButton>button {
        background: linear-gradient(135deg, #1a237e 0%, #283593 100%);
        color: white;
        font-weight: 600;
        border: none;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        border-radius: 8px;
        width: 100%;
        transition: all 0.3s;
    }

    .stButton>button:hover {
        background: linear-gradient(135deg, #0d1b5e 0%, #1a237e 100%);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }

    /* 사이드바 스타일 */
    .sidebar .sidebar-content {
        background: #f8f9fa;
    }

    /* 태그 스타일 */
    .tag {
        display: inline-block;
        background: #1a237e;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        margin: 0.2rem;
    }
</style>
""", unsafe_allow_html=True)

# 세션 상태 초기화
if 'generator' not in st.session_state:
    with st.spinner('AI 엔진을 초기화하고 있습니다...'):
        st.session_state.generator = CRMMessageGenerator()

if 'generated_message' not in st.session_state:
    st.session_state.generated_message = None


def main():
    """메인 UI"""

    # 헤더
    st.markdown("""
    <div class="main-header">
        <h1>💄 아모레퍼시픽 CRM 마케팅 Agent</h1>
        <p>AI 기반 개인화 마케팅 메시지 생성 시스템</p>
    </div>
    """, unsafe_allow_html=True)

    # 사이드바 설정
    with st.sidebar:
        st.image("https://www.apgroup.com/assets/images/logo.png", width=200)
        st.markdown("---")

        st.markdown("### 🎯 메시지 생성 설정")

        # 고객 선택
        personas = st.session_state.generator.personas
        customer_options = {
            f"{cid} ({data['age_group']}, {data['skin_type']}피부)": cid
            for cid, data in personas.items()
        }

        selected_customer_label = st.selectbox(
            "고객 선택",
            options=list(customer_options.keys()),
            help="메시지를 생성할 타겟 고객을 선택하세요"
        )
        selected_customer_id = customer_options[selected_customer_label]

        # 메시지 목적 선택
        message_purpose = st.selectbox(
            "메시지 목적",
            options=["신제품_소개", "시즌_프로모션", "재구매_유도", "특별_이벤트"],
            help="생성할 메시지의 목적을 선택하세요"
        )

        # 추천 제품 수
        num_products = st.slider(
            "추천 제품 수",
            min_value=1,
            max_value=5,
            value=3,
            help="고객에게 추천할 제품 개수"
        )

        st.markdown("---")

        # 생성 버튼
        generate_button = st.button("🚀 AI 메시지 생성", use_container_width=True)

        st.markdown("---")
        st.markdown("### ℹ️ 시스템 정보")
        st.info(f"""
        - LLM: Google Gemini Pro
        - 임베딩: text-embedding-004
        - 벡터 DB: ChromaDB
        - 페르소나: {len(personas)}명
        - 제품: 50개
        """)

    # 메인 영역
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("### 👤 고객 정보")

        # 선택된 고객 정보 표시
        persona = personas[selected_customer_id]

        st.markdown(f"""
        <div class="info-card">
            <h4>🆔 {esc(selected_customer_id)}</h4>
            <p><strong>연령대:</strong> {esc(persona['age_group'])}</p>
            <p><strong>피부 타입:</strong> {esc(persona['skin_type'])}</p>
            <p><strong>피부 고민:</strong> {esc(persona['skin_concern'])}</p>
            <p><strong>선호 브랜드:</strong> {esc(persona['preferred_brand'])}</p>
            <p><strong>라이프스타일:</strong> {esc(persona['lifestyle_keyword'])}</p>
            <p><strong>구매 이력:</strong> {esc(persona['purchase_history'])}</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("### 🎨 브랜드 톤")

        # 선호 브랜드의 톤 정보
        preferred_brand = persona['preferred_brand'].split(',')[0].strip()
        if preferred_brand in st.session_state.generator.brand_tones:
            brand_tone = st.session_state.generator.brand_tones[preferred_brand]
            st.markdown(f"""
            <div class="brand-tone-box">
                <h4>📣 {esc(brand_tone['brand'])}</h4>
                <p><strong>톤 설명:</strong><br>{esc(brand_tone['tone_description'])}</p>
                <p><strong>예시:</strong><br>"{esc(brand_tone['example_sentence'])}"</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("선호 브랜드의 톤 정보를 찾을 수 없습니다.")

    # 메시지 생성 처리
    if generate_button:
        with st.spinner('🤖 AI가 고객 맞춤 메시지를 생성하고 있습니다...'):
            try:
                result = st.session_state.generator.generate_crm_message(
                    customer_id=selected_customer_id,
                    purpose=message_purpose,
                    num_products=num_products
                )
                st.session_state.generated_message = result
                st.success("✅ 메시지 생성이 완료되었습니다!")
            except Exception as e:
                st.error(f"❌ 메시지 생성 중 오류가 발생했습니다: {e}")
                st.session_state.generated_message = None

    # 생성된 메시지 표시
    if st.session_state.generated_message:
        st.markdown("---")

        result = st.session_state.generated_message

        # 생성된 메시지
        st.markdown("### 💌 생성된 마케팅 메시지")

        st.markdown(f"""
        <div class="message-box">
            <h3 style="color: #1a237e; margin-top: 0;">📧 {esc(result['title'])}</h3>
            <p style="font-size: 1.1rem; line-height: 1.8; color: #333;">
                {esc(result['body'])}
            </p>
            <hr style="border: none; border-top: 1px solid #1a237e; margin: 1.5rem 0;">
            <p style="color: #666; font-size: 0.9rem; margin: 0;">
                <strong>목적:</strong> {esc(result['purpose'])} |
                <strong>브랜드:</strong> {esc(result['brand'])}
            </p>
        </div>
        """, unsafe_allow_html=True)

        # 추천 제품
        st.markdown("### 🛍️ 추천 제품")

        products_cols = st.columns(min(num_products, 3))

        for idx, product in enumerate(result['recommended_products']):
            col_idx = idx % 3
            with products_cols[col_idx]:
                st.markdown(f"""
                <div class="product-card">
                    <h4 style="color: #1a237e; margin-top: 0;">{esc(product['brand'])}</h4>
                    <h5 style="margin: 0.5rem 0;">{esc(product['product_name'])}</h5>
                    <p style="color: #666; font-size: 0.9rem;">
                        <strong>카테고리:</strong> {esc(product['category'])}<br>
                        <strong>가격:</strong> {int(product['price']):,}원
                    </p>
                    <div>
                        {' '.join([f'<span class="tag">{esc(tag)}</span>' for tag in str(product['tags']).split()[:3]])}
                    </div>
                </div>
                """, unsafe_allow_html=True)

        # 원본 메시지 (디버깅용)
        with st.expander("🔍 원본 AI 응답 보기"):
            st.code(result['raw_message'], language="markdown")

    else:
        st.info("👈 왼쪽 사이드바에서 고객과 메시지 목적을 선택한 후 '🚀 AI 메시지 생성' 버튼을 클릭하세요.")


if __name__ == "__main__":
    main()
