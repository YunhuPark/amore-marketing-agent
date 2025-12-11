"""
고품질 RAG 테스트용 더미 데이터 생성 스크립트
아모레퍼시픽 브랜드의 제품, 고객 페르소나, 브랜드 톤 데이터를 생성합니다.
"""

import csv
import os
from pathlib import Path
import random

# 데이터 저장 경로
DATA_DIR = Path(__file__).parent.parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

# 브랜드별 특성 정의
BRAND_CHARACTERISTICS = {
    "설화수": {
        "categories": ["스킨케어", "메이크업", "클렌징"],
        "price_range": (50000, 350000),
        "tone": "우아하고 고급스러운",
        "keywords": ["한방", "자음생", "윤조에센스", "궁중", "동백꽃", "인삼", "영양", "탄력", "윤기"],
        "description_style": "한국의 전통 미를 담은 럭셔리 한방 화장품으로, 귀한 한방 성분과 현대 과학의 만남을 통해 피부 본연의 아름다움을 되찾아드립니다."
    },
    "헤라": {
        "categories": ["메이크업", "스킨케어", "쿠션"],
        "price_range": (30000, 120000),
        "tone": "세련되고 프로페셔널한",
        "keywords": ["센슈얼", "글로우", "쿠션", "립스틱", "파운데이션", "커버력", "지속력", "럭셔리"],
        "description_style": "아시아 여성의 아름다움을 재정의하는 프리미엄 메이크업 브랜드로, 트렌디하면서도 세련된 컬러와 완벽한 피부 표현력을 선사합니다."
    },
    "에스트라": {
        "categories": ["스킨케어", "안티에이징", "세럼"],
        "price_range": (40000, 200000),
        "tone": "전문적이고 신뢰감 있는",
        "keywords": ["더마", "약산성", "저자극", "진정", "아토베리어", "세라마이드", "민감성", "피부장벽"],
        "description_style": "피부과학에 기반한 더마 코스메틱 브랜드로, 민감하고 예민한 피부를 위한 저자극 고기능 솔루션을 제공합니다."
    },
    "에뛰드": {
        "categories": ["메이크업", "스킨케어", "색조"],
        "price_range": (8000, 35000),
        "tone": "발랄하고 친근한",
        "keywords": ["플레이", "컬러풀", "틴트", "쥬시", "귀여운", "트렌디", "가성비", "MZ세대"],
        "description_style": "메이크업을 더욱 즐겁고 재미있게! 트렌디한 컬러와 귀여운 패키징으로 일상에 생기를 더하는 플레이풀 뷰티 브랜드입니다."
    },
    "라네즈": {
        "categories": ["스킨케어", "수분케어", "마스크"],
        "price_range": (15000, 80000),
        "tone": "편안하고 신뢰감 있는",
        "keywords": ["수분", "워터뱅크", "슬리핑마스크", "히알루론산", "보습", "촉촉함", "글로우", "베스트셀러"],
        "description_style": "수분 전문 브랜드로, 피부 본연의 물광을 찾아주는 워터사이언스 기술로 건강한 피부 루틴을 완성합니다."
    }
}

# 제품 이름 템플릿
PRODUCT_TEMPLATES = {
    "스킨케어": [
        "{keyword} 에센스", "{keyword} 크림", "{keyword} 세럼",
        "{keyword} 토너", "{keyword} 로션", "{keyword} 앰플",
        "{keyword} 아이크림", "{keyword} 나이트크림"
    ],
    "메이크업": [
        "{keyword} 쿠션", "{keyword} 파운데이션", "{keyword} 립스틱",
        "{keyword} 틴트", "{keyword} 아이섀도우 팔레트", "{keyword} 블러셔",
        "{keyword} 컨실러", "{keyword} 립글로스"
    ],
    "클렌징": [
        "{keyword} 클렌징폼", "{keyword} 클렌징오일", "{keyword} 클렌징워터",
        "{keyword} 필링젤", "{keyword} 스크럽"
    ],
    "수분케어": [
        "{keyword} 수분크림", "{keyword} 젤크림", "{keyword} 하이드레이팅 세럼",
        "{keyword} 워터에센스"
    ],
    "안티에이징": [
        "{keyword} 리프팅 세럼", "{keyword} 링클 크림", "{keyword} 탄력 앰플",
        "{keyword} 아이 세럼"
    ],
    "마스크": [
        "{keyword} 슬리핑마스크", "{keyword} 시트마스크", "{keyword} 워시오프마스크"
    ],
    "색조": [
        "{keyword} 립밤", "{keyword} 마스카라", "{keyword} 아이라이너",
        "{keyword} 브로우", "{keyword} 하이라이터"
    ],
    "쿠션": [
        "{keyword} 롱래스팅 쿠션", "{keyword} 글로우 쿠션", "{keyword} 커버 쿠션"
    ]
}

def generate_product_description(brand, product_name, category, keywords):
    """브랜드 톤앤매너를 반영한 상세 제품 설명 생성"""
    brand_info = BRAND_CHARACTERISTICS[brand]

    descriptions = {
        "설화수": [
            f"{product_name}는 귀한 {random.choice(keywords)}을(를) 함유하여 피부 깊숙이 영양을 전달하는 프리미엄 한방 화장품입니다. "
            f"궁중 미용 비방에서 영감을 받은 독자적인 기술로 추출한 한방 성분이 피부 본연의 생명력을 일깨워, "
            f"세월이 흘러도 변치 않는 아름다움을 지키실 수 있도록 정성을 다해 만들었습니다. "
            f"오랜 시간 숙성된 한방 원료의 깊은 향과 함께 풍부한 영양감이 피부에 스며들어 "
            f"탄력 있고 윤기 나는 피부로 가꾸어 드립니다. 아침저녁으로 정성스럽게 사용하시면 "
            f"피부가 한층 더 촉촉하고 생기 있게 변화하는 것을 느끼실 수 있습니다.",

            f"한국의 전통 미를 현대적으로 재해석한 {product_name}는 {random.choice(keywords)} 성분의 탁월한 효능으로 "
            f"피부 고민을 근본부터 케어합니다. 장인 정신으로 정제한 순수 한방 원료가 피부 깊숙한 곳까지 침투하여 "
            f"내면의 건강함을 끌어올리고, 겉으로 드러나는 피부 결과 윤기를 개선합니다. "
            f"특히 {category} 제품으로서 일상적인 관리는 물론, 특별한 날을 위한 집중 케어에도 완벽합니다. "
            f"고급스러운 텍스처와 은은한 한방 향이 사용할 때마다 품격 있는 뷰티 루틴을 선사하며, "
            f"지속적으로 사용하실수록 피부가 건강해지고 빛나는 변화를 경험하실 수 있습니다."
        ],

        "헤라": [
            f"{product_name}는 아시아 여성의 피부톤과 특성을 완벽하게 분석하여 개발된 프로페셔널 {category} 제품입니다. "
            f"{random.choice(keywords)}의 혁신적인 포뮬러가 피부에 밀착되어 오랜 시간 흐트러짐 없이 완벽한 메이크업을 유지해줍니다. "
            f"프로 메이크업 아티스트들의 노하우가 담긴 이 제품은 섬세한 컬러 표현력과 뛰어난 지속력으로 "
            f"아침부터 저녁까지 갓 바른 듯한 생생한 메이크업을 선사합니다. "
            f"특히 {random.choice(keywords)} 기술이 적용되어 자연스러우면서도 트렌디한 룩을 완성할 수 있으며, "
            f"피부 자극을 최소화한 처방으로 민감한 피부도 안심하고 사용할 수 있습니다.",

            f"럭셔리 메이크업의 새로운 기준을 제시하는 {product_name}는 세련된 발색과 실크처럼 부드러운 텍스처로 "
            f"메이크업의 즐거움을 선사합니다. {random.choice(keywords)} 성분이 함유되어 메이크업과 스킨케어를 동시에 제공하며, "
            f"한국, 중국, 일본 등 아시아 주요 시장의 트렌드를 반영한 컬러 라인업이 다양한 룩 연출을 가능하게 합니다. "
            f"고밀착 포뮬러가 피부 결을 매끄럽게 정돈하고, 오일 컨트롤 파우더가 피지와 땀에도 무너지지 않는 "
            f"완벽한 마무리를 제공합니다. 세련된 패키징과 프리미엄 품질로 특별한 순간을 더욱 빛나게 만들어 드립니다."
        ],

        "에스트라": [
            f"{product_name}는 피부과학 연구를 통해 개발된 더마 코스메틱 제품으로, {random.choice(keywords)} 성분이 "
            f"민감하고 예민한 피부를 진정시키고 건강한 피부 장벽을 구축합니다. 엄격한 저자극 테스트를 거쳐 완성된 이 제품은 "
            f"약산성 pH를 유지하여 피부 본연의 균형을 지키며, 외부 자극으로부터 피부를 보호합니다. "
            f"특히 {category} 제품으로서 즉각적인 진정 효과와 함께 장기적인 피부 개선 효과를 제공하여 "
            f"아토피, 여드름, 홍조 등 다양한 피부 고민을 과학적으로 해결합니다. "
            f"무향료, 무파라벤, 무인공색소로 민감성 피부도 안심하고 매일 사용할 수 있습니다.",

            f"피부 전문가들이 추천하는 {product_name}는 {random.choice(keywords)} 테크놀로지를 적용하여 "
            f"손상된 피부 장벽을 집중적으로 회복시키고 건강한 피부로 가꾸어 줍니다. 더마 성분의 최적 배합으로 "
            f"자극은 최소화하고 효과는 극대화한 이 제품은 피부과 시술 후 관리나 계절 변화로 인한 피부 트러블에도 "
            f"탁월한 효능을 발휘합니다. 임상 테스트를 통해 입증된 진정 효과와 보습 지속력으로 "
            f"하루 종일 편안하고 촉촉한 피부 상태를 유지하며, 지속적인 사용으로 피부 자생력을 강화하여 "
            f"건강한 피부 본연의 아름다움을 되찾을 수 있도록 도와드립니다."
        ],

        "에뛰드": [
            f"안녕하세요! 플레이풀 뷰티의 대명사 {product_name}를 소개할게요 💕 {random.choice(keywords)}의 매력이 가득한 이 제품은 "
            f"트렌디한 컬러와 재미있는 사용감으로 메이크업을 즐겁게 만들어줘요! 가볍고 촉촉한 텍스처가 피부에 쏙쏙 스며들면서 "
            f"자연스러운 발색을 선사하고, 귀여운 패키징은 화장대를 보는 것만으로도 기분을 좋게 만들어준답니다 ✨ "
            f"{category} 아이템으로 데일리 메이크업부터 특별한 데이트 룩까지 다양하게 연출할 수 있어요. "
            f"가격 대비 훌륭한 품질로 MZ세대 사이에서 입소문이 난 이 제품, 여러분도 꼭 한번 경험해보세요! "
            f"친구들과 함께 나눠 쓰기에도 좋고, 선물용으로도 완전 최고랍니다 🎁",

            f"매일매일 새로운 나를 발견하고 싶다면 {product_name}와 함께해요! {random.choice(keywords)} 컬러가 넘치는 이 제품은 "
            f"기분에 따라, TPO에 따라 자유롭게 스타일을 바꿀 수 있는 플레이풀한 아이템이에요 🌈 "
            f"부담 없는 가격에 퀄리티는 프리미엄급이라 뷰티 유튜버들도 강력 추천하는 제품이죠! "
            f"특히 {random.choice(keywords)} 성분이 들어있어서 메이크업하면서 피부 케어도 함께 할 수 있어요. "
            f"발림성이 정말 좋아서 초보자도 쉽게 사용할 수 있고, 지속력도 뛰어나서 오랜 시간 예쁜 메이크업을 유지할 수 있답니다. "
            f"SNS에서 핫한 이 제품으로 여러분의 뷰티 라이프를 더욱 즐겁게 만들어보세요 💄"
        ],

        "라네즈": [
            f"{product_name}는 라네즈의 독자적인 워터 사이언스 기술로 개발된 수분 전문 {category} 제품입니다. "
            f"{random.choice(keywords)} 성분이 피부 깊숙이 침투하여 피부 속부터 촉촉함을 채우고, "
            f"피부 표면의 수분 장벽을 강화하여 오랜 시간 보습력을 유지합니다. 특히 건조한 환경이나 계절 변화로 인한 "
            f"피부 당김, 각질, 칙칙함 등의 고민을 효과적으로 해결하며, 사용 직후부터 촉촉하고 투명한 물광 피부를 경험하실 수 있습니다. "
            f"가볍고 산뜻한 텍스처가 피부에 빠르게 흡수되어 끈적임 없이 보송보송한 마무리감을 제공하며, "
            f"아침저녁 꾸준히 사용하면 피부 수분 밸런스가 개선되어 건강하고 탄력 있는 피부로 가꿀 수 있습니다.",

            f"전 세계적으로 사랑받는 베스트셀러 {product_name}는 {random.choice(keywords)} 테크놀로지로 "
            f"수분 공급과 보습 지속력을 모두 잡은 스테디셀러 제품입니다. 히말라야 빙하수에서 추출한 미네랄 워터가 "
            f"피부에 생기를 더하고, 이온 미네랄 워터™가 피부 각질층까지 깊이 침투하여 속부터 차오르는 수분감을 선사합니다. "
            f"특히 {category} 제품으로서 바쁜 일상 속에서도 간편하게 사용할 수 있으며, "
            f"민감성 피부도 자극 없이 편안하게 사용할 수 있도록 저자극 테스트를 완료했습니다. "
            f"매일 밤 꾸준히 사용하면 다음날 아침 물광 피부로 깨어나는 기쁨을 느끼실 수 있으며, "
            f"계속된 사용으로 피부 결이 매끄러워지고 투명도가 높아지는 것을 확인하실 수 있습니다."
        ]
    }

    return random.choice(descriptions[brand])

def generate_tags(brand, keywords):
    """제품 태그 생성"""
    common_tags = ["#데일리케어", "#K뷰티", "#추천템", "#베스트셀러"]
    brand_tags = [f"#{keyword}" for keyword in random.sample(keywords, min(3, len(keywords)))]
    seasonal_tags = random.choice([["#겨울케어", "#보습"], ["#여름케어", "#산뜻함"], ["#환절기케어"], []])

    return " ".join(common_tags + brand_tags + seasonal_tags)

def generate_products():
    """제품 데이터 생성"""
    products = []
    product_id = 1

    for brand, info in BRAND_CHARACTERISTICS.items():
        # 브랜드당 10개 제품 생성
        for _ in range(10):
            category = random.choice(info["categories"])
            keyword = random.choice(info["keywords"])

            # 카테고리에 맞는 제품명 템플릿 선택
            if category in PRODUCT_TEMPLATES:
                template = random.choice(PRODUCT_TEMPLATES[category])
            else:
                template = random.choice(PRODUCT_TEMPLATES["스킨케어"])

            product_name = template.format(keyword=keyword)
            price = random.randint(info["price_range"][0], info["price_range"][1])

            # 가격을 천원 단위로 반올림
            price = round(price / 1000) * 1000

            description = generate_product_description(brand, product_name, category, info["keywords"])
            tags = generate_tags(brand, info["keywords"])
            url = f"https://www.amorepacific.com/{brand.lower()}/products/{product_id}"

            products.append({
                "brand": brand,
                "product_name": product_name,
                "category": category,
                "price": price,
                "description": description,
                "tags": tags,
                "url": url
            })

            product_id += 1

    return products

def generate_personas():
    """고객 페르소나 데이터 생성"""
    personas = [
        {
            "customer_id": "C001",
            "age_group": "30대",
            "skin_type": "건성",
            "skin_concern": "탄력저하, 미세주름",
            "preferred_brand": "설화수",
            "lifestyle_keyword": "워킹맘, 바쁜 아침 간편한 케어 중시, 프리미엄 선호",
            "purchase_history": "설화수 윤조에센스, 자음생크림, 에스트라 세럼 구매 이력 다수"
        },
        {
            "customer_id": "C002",
            "age_group": "20대 후반",
            "skin_type": "복합성",
            "skin_concern": "모공, 피지, 메이크업 지속력",
            "preferred_brand": "헤라",
            "lifestyle_keyword": "직장인, 완벽한 메이크업 중시, 트렌드 세터",
            "purchase_history": "헤라 블랙쿠션, 센슈얼 립스틱 5종 이상 보유, 정기 구매자"
        },
        {
            "customer_id": "C003",
            "age_group": "20대 초반",
            "skin_type": "민감성",
            "skin_concern": "트러블, 홍조, 자극 반응",
            "preferred_brand": "에스트라",
            "lifestyle_keyword": "대학생, 가성비 중시하지만 피부 고민으로 더마 제품 필요",
            "purchase_history": "에스트라 아토베리어 라인 풀 구매, 진정 제품 위주"
        },
        {
            "customer_id": "C004",
            "age_group": "10대 후반",
            "skin_type": "지성",
            "skin_concern": "피지, 여드름, 트렌디한 메이크업",
            "preferred_brand": "에뛰드",
            "lifestyle_keyword": "고등학생, SNS 활동 활발, 틴트와 립밤 수집광",
            "purchase_history": "에뛰드 플레이 컬러 아이즈, 디어달링 틴트 다수 보유"
        },
        {
            "customer_id": "C005",
            "age_group": "20대 중반",
            "skin_type": "건성",
            "skin_concern": "수분부족, 각질, 칙칙함",
            "preferred_brand": "라네즈",
            "lifestyle_keyword": "직장인, 야근 잦음, 수면 부족으로 피부 건조",
            "purchase_history": "라네즈 워터뱅크 라인, 슬리핑마스크 애용자, 리필 구매 다수"
        },
        {
            "customer_id": "C006",
            "age_group": "40대",
            "skin_type": "건성",
            "skin_concern": "주름, 탄력, 피부톤",
            "preferred_brand": "설화수",
            "lifestyle_keyword": "전업주부, 안티에이징 집중 관리, 백화점 VIP 고객",
            "purchase_history": "설화수 자음생 라인 정기 구매, 시즌 한정 제품 수집"
        },
        {
            "customer_id": "C007",
            "age_group": "30대 초반",
            "skin_type": "복합성",
            "skin_concern": "T존 피지, 볼 건조, 잡티",
            "preferred_brand": "헤라",
            "lifestyle_keyword": "프리랜서, 홈뷰티 루틴 중시, 온라인 쇼핑 선호",
            "purchase_history": "헤라 쿠션 2종 교차 사용, 스킨케어는 에스트라 혼용"
        },
        {
            "customer_id": "C008",
            "age_group": "20대 중반",
            "skin_type": "민감복합성",
            "skin_concern": "생리 주기별 트러블, 붉은기",
            "preferred_brand": "에스트라, 라네즈",
            "lifestyle_keyword": "직장인, 스트레스성 피부 고민, 저자극 제품 선호",
            "purchase_history": "에스트라 진정라인과 라네즈 크림 스킨 함께 구매"
        },
        {
            "customer_id": "C009",
            "age_group": "10대 후반",
            "skin_type": "복합성",
            "skin_concern": "피지, 메이크업 서툼, 색조 궁금증 많음",
            "preferred_brand": "에뛰드",
            "lifestyle_keyword": "고등학생, 용돈으로 구매, 유튜브 메이크업 튜토리얼 시청",
            "purchase_history": "에뛰드 입문 제품 위주, 립 제품과 치크 소량 구매"
        },
        {
            "customer_id": "C010",
            "age_group": "30대 후반",
            "skin_type": "복합성",
            "skin_concern": "처짐, 모공, 피부결",
            "preferred_brand": "설화수, 헤라",
            "lifestyle_keyword": "워킹맘, 효율적인 케어 중시, 스킨케어와 메이크업 모두 중요",
            "purchase_history": "설화수 에센스와 헤라 쿠션 정기 구매, 시즌 신상 체크"
        }
    ]

    return personas

def generate_brand_tones():
    """브랜드 톤 데이터 생성"""
    brand_tones = [
        {
            "brand": "설화수",
            "tone_description": "우아하고 격조 있는 하십시오체, 한방 관련 단어 적극 활용, 전통과 현대의 조화 강조, 프리미엄 럭셔리 톤",
            "example_sentence": "귀한 궁중 비방에서 영감을 받은 자음생 에센스로 피부 본연의 아름다움을 되찾으시길 바랍니다. 세월이 흘러도 변치 않는 윤기와 탄력을 경험하십시오."
        },
        {
            "brand": "헤라",
            "tone_description": "세련되고 프로페셔널한 해요체, 메이크업 전문 용어 사용, 아시아 뷰티 트렌드 강조, 자신감 있는 톤",
            "example_sentence": "프로 메이크업 아티스트의 노하우를 담은 헤라 블랙쿠션으로 완벽한 피부 표현을 완성해보세요. 아시아 여성의 피부톤에 최적화된 컬러로 자연스러운 글로우 피부를 연출합니다."
        },
        {
            "brand": "에스트라",
            "tone_description": "전문적이고 신뢰감 있는 합니다체, 피부과학 용어 사용, 임상 데이터 강조, 안심 메시지 전달",
            "example_sentence": "피부과학 연구를 통해 개발된 에스트라 아토베리어 크림은 손상된 피부 장벽을 회복시키고 민감한 피부를 진정시킵니다. 저자극 테스트 완료로 안심하고 사용하실 수 있습니다."
        },
        {
            "brand": "에뛰드",
            "tone_description": "발랄하고 친근한 해요체, 이모지 적극 사용, 줄임말과 신조어 활용, 공감과 재미 요소 강조",
            "example_sentence": "오늘의 무드는? 💕 에뛰드 플레이 컬러 아이즈로 매일매일 다른 나를 발견해보세요! 트렌디한 컬러와 쫀쫀한 밀착력으로 완전 찰떡 메이크업 완성 ✨ 가성비 갑 인정?"
        },
        {
            "brand": "라네즈",
            "tone_description": "편안하고 친근한 합니다/해요체 혼용, 수분과 보습 관련 표현 강조, 데일리 루틴 중시, 신뢰감 있는 톤",
            "example_sentence": "매일 밤 라네즈 워터 슬리핑 마스크로 수분을 가득 채워보세요. 히말라야 빙하수에서 추출한 미네랄 워터가 피부 속 깊이 침투하여 다음날 아침 물광 피부로 깨어날 수 있습니다."
        }
    ]

    return brand_tones

def save_to_csv(data, filename, fieldnames):
    """데이터를 CSV 파일로 저장"""
    filepath = DATA_DIR / filename
    with open(filepath, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    print(f"[OK] {filename} 생성 완료: {len(data)}개 레코드")

def main():
    """메인 실행 함수"""
    print("RAG 테스트용 더미 데이터 생성 시작...\n")

    # 1. 제품 데이터 생성
    print("[1/3] 제품 데이터 생성 중...")
    products = generate_products()
    save_to_csv(
        products,
        "products.csv",
        ["brand", "product_name", "category", "price", "description", "tags", "url"]
    )

    # 2. 페르소나 데이터 생성
    print("\n[2/3] 고객 페르소나 데이터 생성 중...")
    personas = generate_personas()
    save_to_csv(
        personas,
        "personas.csv",
        ["customer_id", "age_group", "skin_type", "skin_concern", "preferred_brand", "lifestyle_keyword", "purchase_history"]
    )

    # 3. 브랜드 톤 데이터 생성
    print("\n[3/3] 브랜드 톤 데이터 생성 중...")
    brand_tones = generate_brand_tones()
    save_to_csv(
        brand_tones,
        "brand_tones.csv",
        ["brand", "tone_description", "example_sentence"]
    )

    print("\n" + "="*50)
    print("*** 모든 더미 데이터 생성 완료! ***")
    print(f"저장 위치: {DATA_DIR.absolute()}")
    print("="*50)

    # 생성된 데이터 요약
    print("\n생성된 데이터 요약:")
    print(f"  - 제품 데이터: {len(products)}개")
    print(f"  - 고객 페르소나: {len(personas)}개")
    print(f"  - 브랜드 톤: {len(brand_tones)}개")

    print("\n브랜드별 제품 수:")
    brand_counts = {}
    for product in products:
        brand = product["brand"]
        brand_counts[brand] = brand_counts.get(brand, 0) + 1

    for brand, count in brand_counts.items():
        print(f"  - {brand}: {count}개")

if __name__ == "__main__":
    main()
