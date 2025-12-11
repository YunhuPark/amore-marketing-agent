"""
CRM 메시지 생성 엔진
Google Gemini Flash + LangChain을 활용한 개인화 마케팅 메시지 생성
"""

import os
import sys
import csv
from pathlib import Path
from typing import Dict, Any, Optional
import logging
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# 프로젝트 루트를 sys.path에 추가
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.rag.vector_store import ProductVectorStore

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 경로 설정
DATA_DIR = PROJECT_ROOT / "data"

# .env 파일 로드
env_path = PROJECT_ROOT / "config" / ".env"
load_dotenv(env_path)

# LLM 모델 설정
MODEL_NAME = "models/gemini-2.5-flash"  # Google API에서 확인된 실제 모델명
TEMPERATURE = 0.7


class CRMMessageGenerator:
    """CRM 마케팅 메시지 생성기"""

    def __init__(self):
        """초기화"""
        self.llm = None
        self.vector_store = None
        self.personas = {}
        self.brand_tones = {}

        self._initialize_llm()
        self._load_data()

    def _initialize_llm(self):
        """Gemini Flash 모델 초기화"""
        try:
            api_key = os.getenv("GOOGLE_API_KEY")
            if not api_key:
                raise ValueError(
                    "GOOGLE_API_KEY가 설정되지 않았습니다. .env 파일을 확인하세요."
                )

            self.llm = ChatGoogleGenerativeAI(
                model=MODEL_NAME,
                google_api_key=api_key,
                temperature=TEMPERATURE,
                convert_system_message_to_human=True  # Gemini는 system 메시지를 human으로 변환 필요
            )
            logger.info(f"LLM 모델 '{MODEL_NAME}' (temperature={TEMPERATURE}) 초기화 완료")
        except Exception as e:
            logger.error(f"LLM 모델 초기화 실패: {e}")
            raise

    def _load_data(self):
        """페르소나 및 브랜드 톤 데이터 로드"""
        try:
            # 페르소나 데이터 로드
            personas_path = DATA_DIR / "personas.csv"
            with open(personas_path, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.personas[row['customer_id']] = row
            logger.info(f"{len(self.personas)}개의 페르소나 데이터를 로드했습니다.")

            # 브랜드 톤 데이터 로드
            brand_tones_path = DATA_DIR / "brand_tones.csv"
            with open(brand_tones_path, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.brand_tones[row['brand']] = row
            logger.info(f"{len(self.brand_tones)}개의 브랜드 톤 데이터를 로드했습니다.")

            # 벡터 스토어 초기화
            self.vector_store = ProductVectorStore()
            self.vector_store.build_vectorstore()
            logger.info("벡터 스토어 초기화 완료")

        except Exception as e:
            logger.error(f"데이터 로드 실패: {e}")
            raise

    def _create_search_query(self, persona: Dict[str, Any], purpose: str) -> str:
        """페르소나 정보를 기반으로 검색 쿼리 생성"""
        skin_concern = persona.get('skin_concern', '')
        skin_type = persona.get('skin_type', '')
        preferred_brand = persona.get('preferred_brand', '')

        if purpose == "신제품_소개":
            query = f"{preferred_brand} {skin_concern} 해결 제품"
        elif purpose == "시즌_프로모션":
            query = f"{skin_type} 피부 {skin_concern} 케어 제품"
        elif purpose == "재구매_유도":
            query = f"{preferred_brand} 베스트셀러 {skin_concern} 제품"
        else:
            query = f"{skin_concern} {skin_type} 피부 제품"

        return query

    def _build_crm_chain(self):
        """LCEL 스타일로 CRM 메시지 생성 체인 구성"""

        # 시스템 프롬프트 템플릿
        system_template = """너는 아모레퍼시픽의 15년 차 베테랑 마케터 'Agent 10'이야.
고객 한 분 한 분께 진심을 담아 개인화된 마케팅 메시지를 작성하는 것이 너의 임무야.

**핵심 원칙:**
1. 제공된 브랜드 톤을 완벽하게 모사해야 해 (말투, 어조, 특징적 표현 모두 반영)
2. 고객의 피부 고민과 라이프스타일을 정확히 이해하고 공감해야 해
3. 추천 제품은 고객의 니즈와 완벽하게 매칭되어야 해
4. 자연스럽고 진정성 있는 메시지로 고객의 마음을 움직여야 해

**브랜드 톤 정보:**
{brand_tone}

**출력 형식:**
제목: [40자 이내의 임팩트 있는 제목]
본문: [350자 이내의 상세하고 매력적인 본문]

제목과 본문만 출력하고, 다른 설명은 포함하지 마."""

        # 휴먼 프롬프트 템플릿
        human_template = """**고객 정보:**
- 고객 ID: {customer_id}
- 연령대: {age_group}
- 피부 타입: {skin_type}
- 피부 고민: {skin_concern}
- 선호 브랜드: {preferred_brand}
- 라이프스타일: {lifestyle_keyword}
- 구매 이력: {purchase_history}

**메시지 목적:**
{purpose}

**추천 제품 정보:**
{product_info}

위 정보를 바탕으로 고객에게 딱 맞는 CRM 메시지를 작성해줘.
브랜드 톤을 정확히 반영하고, 고객의 니즈에 공감하며, 제품의 가치를 효과적으로 전달해야 해."""

        # ChatPromptTemplate 생성
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_template),
            ("human", human_template)
        ])

        # LCEL 체인 구성
        chain = (
            prompt
            | self.llm
            | StrOutputParser()
        )

        return chain

    def generate_crm_message(
        self,
        customer_id: str,
        purpose: str = "신제품_소개",
        num_products: int = 3
    ) -> Dict[str, Any]:
        """
        CRM 마케팅 메시지 생성

        Args:
            customer_id: 고객 ID (예: "C001")
            purpose: 메시지 목적 (신제품_소개, 시즌_프로모션, 재구매_유도 등)
            num_products: 추천할 제품 개수

        Returns:
            생성된 메시지 정보 (제목, 본문, 메타데이터 포함)
        """
        logger.info(f"CRM 메시지 생성 시작 - 고객: {customer_id}, 목적: {purpose}")

        # 1. 페르소나 정보 가져오기
        if customer_id not in self.personas:
            raise ValueError(f"고객 ID '{customer_id}'를 찾을 수 없습니다.")

        persona = self.personas[customer_id]
        preferred_brand = persona.get('preferred_brand', '').split(',')[0].strip()  # 첫 번째 선호 브랜드

        # 2. 브랜드 톤 정보 가져오기
        if preferred_brand not in self.brand_tones:
            logger.warning(f"브랜드 '{preferred_brand}'의 톤 정보를 찾을 수 없습니다. 기본 톤 사용")
            brand_tone_info = "친근하고 전문적인 톤으로 작성해주세요."
        else:
            brand_tone = self.brand_tones[preferred_brand]
            brand_tone_info = f"""
브랜드: {brand_tone['brand']}
톤 설명: {brand_tone['tone_description']}
예시 문장: {brand_tone['example_sentence']}
            """.strip()

        # 3. 제품 검색
        search_query = self._create_search_query(persona, purpose)
        logger.info(f"제품 검색 쿼리: '{search_query}'")

        search_results = self.vector_store.search_products(
            query=search_query,
            k=num_products
        )

        # 4. 제품 정보 포맷팅
        product_info_parts = []
        for i, result in enumerate(search_results, 1):
            metadata = result['metadata']
            product_info_parts.append(f"""
[제품 {i}]
- 브랜드: {metadata['brand']}
- 제품명: {metadata['product_name']}
- 카테고리: {metadata['category']}
- 가격: {metadata['price']}원
- 태그: {metadata['tags']}
- 설명: {result['content'][:200]}...
            """.strip())

        product_info = "\n\n".join(product_info_parts)

        # 5. 체인 실행
        chain = self._build_crm_chain()

        message = chain.invoke({
            "customer_id": customer_id,
            "age_group": persona['age_group'],
            "skin_type": persona['skin_type'],
            "skin_concern": persona['skin_concern'],
            "preferred_brand": persona['preferred_brand'],
            "lifestyle_keyword": persona['lifestyle_keyword'],
            "purchase_history": persona['purchase_history'],
            "purpose": purpose,
            "product_info": product_info,
            "brand_tone": brand_tone_info
        })

        # 6. 결과 파싱
        lines = message.strip().split('\n')
        title = ""
        body = ""

        for line in lines:
            line = line.strip()
            if line.startswith("제목:"):
                title = line.replace("제목:", "").strip()
            elif line.startswith("본문:"):
                body = line.replace("본문:", "").strip()
            elif title and not body:  # 제목 다음 줄이 본문일 수 있음
                if not line.startswith("제목:") and line:
                    body = line
            elif body:  # 본문이 여러 줄일 수 있음
                if line and not line.startswith("제목:") and not line.startswith("본문:"):
                    body += " " + line

        logger.info("CRM 메시지 생성 완료")

        return {
            "customer_id": customer_id,
            "title": title,
            "body": body,
            "purpose": purpose,
            "brand": preferred_brand,
            "persona": persona,
            "recommended_products": [r['metadata'] for r in search_results],
            "raw_message": message
        }


def main():
    """테스트 실행"""
    print("="*70)
    print("CRM 메시지 생성 테스트")
    print("="*70)

    # 메시지 생성기 초기화
    generator = CRMMessageGenerator()

    # 테스트 시나리오
    test_cases = [
        {"customer_id": "C001", "purpose": "신제품_소개"},
        {"customer_id": "C004", "purpose": "시즌_프로모션"},
        {"customer_id": "C005", "purpose": "재구매_유도"}
    ]

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'='*70}")
        print(f"테스트 케이스 {i}: {test_case['customer_id']} ({test_case['purpose']})")
        print("="*70)

        try:
            result = generator.generate_crm_message(**test_case)

            print(f"\n[고객 정보]")
            print(f"- ID: {result['customer_id']}")
            print(f"- 연령대: {result['persona']['age_group']}")
            print(f"- 피부 타입: {result['persona']['skin_type']}")
            print(f"- 피부 고민: {result['persona']['skin_concern']}")
            print(f"- 선호 브랜드: {result['brand']}")

            print(f"\n[생성된 메시지]")
            print(f"제목: {result['title']}")
            print(f"본문: {result['body']}")

            print(f"\n[추천 제품]")
            for j, product in enumerate(result['recommended_products'], 1):
                print(f"{j}. {product['brand']} - {product['product_name']} ({product['price']}원)")

        except Exception as e:
            logger.error(f"메시지 생성 실패: {e}")
            print(f"오류 발생: {e}")

    print("\n" + "="*70)
    print("테스트 완료")
    print("="*70)


if __name__ == "__main__":
    main()
