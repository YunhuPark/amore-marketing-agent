"""
RAG 벡터 스토어 모듈
ChromaDB를 사용한 제품 정보 임베딩 및 검색 엔진
"""

import os
import csv
from pathlib import Path
from typing import List, Dict, Any
import logging
from dotenv import load_dotenv

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 경로 설정
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
CHROMA_DIR = PROJECT_ROOT / "chroma_db"

# .env 파일 로드
env_path = PROJECT_ROOT / "config" / ".env"
load_dotenv(env_path)

# 임베딩 모델 설정
EMBEDDING_MODEL = "models/text-embedding-004"


class ProductVectorStore:
    """제품 정보를 위한 벡터 스토어 클래스"""

    def __init__(self, collection_name: str = "amore_products"):
        """
        벡터 스토어 초기화

        Args:
            collection_name: ChromaDB 컬렉션 이름
        """
        self.collection_name = collection_name
        self.embeddings = None
        self.vectorstore = None
        self._initialize_embeddings()

    def _initialize_embeddings(self):
        """Google Generative AI 임베딩 모델 초기화"""
        try:
            api_key = os.getenv("GOOGLE_API_KEY")
            if not api_key:
                raise ValueError(
                    "GOOGLE_API_KEY가 설정되지 않았습니다. .env 파일을 확인하세요."
                )

            self.embeddings = GoogleGenerativeAIEmbeddings(
                model=EMBEDDING_MODEL,
                google_api_key=api_key
            )
            logger.info(f"임베딩 모델 '{EMBEDDING_MODEL}' 초기화 완료")
        except Exception as e:
            logger.error(f"임베딩 모델 초기화 실패: {e}")
            raise

    def load_products_from_csv(self, csv_path: Path = None) -> List[Dict[str, Any]]:
        """
        CSV 파일에서 제품 데이터 로드

        Args:
            csv_path: CSV 파일 경로 (기본값: data/products.csv)

        Returns:
            제품 데이터 리스트
        """
        if csv_path is None:
            csv_path = DATA_DIR / "products.csv"

        if not csv_path.exists():
            raise FileNotFoundError(f"제품 데이터 파일을 찾을 수 없습니다: {csv_path}")

        products = []
        with open(csv_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            products = list(reader)

        logger.info(f"{len(products)}개의 제품 데이터를 로드했습니다.")
        return products

    def create_documents(self, products: List[Dict[str, Any]]) -> List[Document]:
        """
        제품 데이터를 LangChain Document 객체로 변환

        Args:
            products: 제품 데이터 리스트

        Returns:
            Document 객체 리스트
        """
        documents = []

        for product in products:
            # description, brand, tags를 합쳐서 검색 텍스트 생성
            combined_text = f"""
브랜드: {product['brand']}
제품명: {product['product_name']}
카테고리: {product['category']}

{product['description']}

{product['tags']}
            """.strip()

            # 메타데이터 구성
            metadata = {
                "brand": product['brand'],
                "product_name": product['product_name'],
                "category": product['category'],
                "price": product['price'],
                "tags": product['tags'],
                "url": product['url']
            }

            doc = Document(
                page_content=combined_text,
                metadata=metadata
            )
            documents.append(doc)

        logger.info(f"{len(documents)}개의 Document를 생성했습니다.")
        return documents

    def build_vectorstore(self, force_rebuild: bool = False) -> Chroma:
        """
        벡터 스토어 구축 또는 로드

        Args:
            force_rebuild: True면 기존 DB를 삭제하고 재구축

        Returns:
            Chroma 벡터 스토어 객체
        """
        # 기존 DB 삭제 (재구축 모드)
        if force_rebuild and CHROMA_DIR.exists():
            import shutil
            logger.info("기존 벡터 DB를 삭제합니다...")
            shutil.rmtree(CHROMA_DIR)

        # 기존 DB가 있으면 로드
        if CHROMA_DIR.exists() and not force_rebuild:
            logger.info("기존 벡터 DB를 로드합니다...")
            self.vectorstore = Chroma(
                collection_name=self.collection_name,
                embedding_function=self.embeddings,
                persist_directory=str(CHROMA_DIR)
            )
            logger.info(f"벡터 DB 로드 완료 (저장 위치: {CHROMA_DIR})")
            return self.vectorstore

        # 새로운 DB 구축
        logger.info("새로운 벡터 DB를 구축합니다...")

        # 제품 데이터 로드
        products = self.load_products_from_csv()

        # Document 생성
        documents = self.create_documents(products)

        # ChromaDB 생성
        CHROMA_DIR.mkdir(parents=True, exist_ok=True)

        self.vectorstore = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            collection_name=self.collection_name,
            persist_directory=str(CHROMA_DIR)
        )

        logger.info(f"벡터 DB 구축 완료 (저장 위치: {CHROMA_DIR})")
        logger.info(f"총 {len(documents)}개의 제품이 임베딩되었습니다.")

        return self.vectorstore

    def search_products(
        self,
        query: str,
        k: int = 5,
        filter_dict: Dict[str, Any] = None
    ) -> List[Dict[str, Any]]:
        """
        제품 검색

        Args:
            query: 검색 쿼리
            k: 반환할 결과 개수
            filter_dict: 메타데이터 필터 (예: {"brand": "설화수"})

        Returns:
            검색 결과 리스트 (각 결과는 content와 metadata 포함)
        """
        if self.vectorstore is None:
            logger.info("벡터 스토어가 없습니다. 먼저 구축합니다...")
            self.build_vectorstore()

        logger.info(f"검색 쿼리: '{query}' (최대 {k}개 결과)")

        # 유사도 검색 (score 포함)
        if filter_dict:
            results = self.vectorstore.similarity_search_with_score(
                query=query,
                k=k,
                filter=filter_dict
            )
        else:
            results = self.vectorstore.similarity_search_with_score(
                query=query,
                k=k
            )

        # 결과 포맷팅
        formatted_results = []
        for doc, score in results:
            result = {
                "content": doc.page_content,
                "metadata": doc.metadata,
                "similarity_score": float(score)
            }
            formatted_results.append(result)

        logger.info(f"{len(formatted_results)}개의 결과를 찾았습니다.")
        return formatted_results

    def get_retriever(self, k: int = 5):
        """
        LangChain Retriever 객체 반환 (체인 구성용)

        Args:
            k: 반환할 결과 개수

        Returns:
            Retriever 객체
        """
        if self.vectorstore is None:
            self.build_vectorstore()

        return self.vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": k}
        )


def main():
    """테스트 및 초기 DB 구축"""
    print("="*60)
    print("RAG 벡터 스토어 구축 시작")
    print("="*60)

    # 벡터 스토어 생성
    vector_store = ProductVectorStore()

    # 벡터 DB 구축 (force_rebuild=True로 새로 생성)
    print("\n[1/2] 벡터 DB 구축 중...")
    vector_store.build_vectorstore(force_rebuild=True)

    # 테스트 검색
    print("\n[2/2] 검색 테스트 실행 중...")
    print("\n" + "-"*60)

    test_queries = [
        "건조한 피부를 위한 수분 크림 추천해줘",
        "30대 여성을 위한 안티에이징 제품",
        "에뛰드 틴트 제품",
        "한방 성분이 들어간 프리미엄 제품"
    ]

    for i, query in enumerate(test_queries, 1):
        print(f"\n테스트 {i}: {query}")
        print("-"*60)

        results = vector_store.search_products(query, k=3)

        for j, result in enumerate(results, 1):
            print(f"\n[결과 {j}] (유사도: {result['similarity_score']:.4f})")
            print(f"브랜드: {result['metadata']['brand']}")
            print(f"제품명: {result['metadata']['product_name']}")
            print(f"가격: {result['metadata']['price']}원")
            print(f"태그: {result['metadata']['tags']}")

    print("\n" + "="*60)
    print("벡터 스토어 구축 및 테스트 완료!")
    print(f"DB 저장 위치: {CHROMA_DIR.absolute()}")
    print("="*60)


if __name__ == "__main__":
    main()
