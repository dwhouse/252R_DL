import os
import json
import time
import argparse
from pathlib import Path

import chromadb
from llama_index.core import (
    SimpleDirectoryReader,
    VectorStoreIndex,
    StorageContext,
    Settings,
)
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.vector_stores.chroma import ChromaVectorStore


# 사용자 환경 설정
CHROMA_PATH = "./chroma_db_test"                # ChromaDB 저장 경로
COLLECTION_NAME = "korea_univ_rules_v1"         # ChromaDB 컬렉션 이름

# PDF 경로
PDF_FILES = [
    "data/2-1-1 고려대학교 학칙.pdf",
    "data/2-1-2 학사운영 규정.pdf",
    "졸업요건_경제통계학부.pdf",
    "졸업요건_글로벌경영전공.pdf",
    "졸업요건_데이터계산과학전공.pdf",
    "졸업요건_빅데이터사이언스학부.pdf",
    "졸업요건_컴퓨터융합소프트웨어학과.pdf"
]

# Embedding/LLM 모델
EMBED_MODEL = "text-embedding-3-small"
GEN_MODEL = "gpt-5-nano"


def _ensure_paths():
    # PDF 존재 확인
    for fp in PDF_FILES:
        if not Path(fp).exists():
            raise FileNotFoundError(f"PDF not found: {fp}")


def _init_llamaindex_settings():
    # 전역 Settings 고정 (재현성 : Temperature 0)
    Settings.embed_model = OpenAIEmbedding(model=EMBED_MODEL)
    Settings.llm = OpenAI(model=GEN_MODEL, temperature=0)


def save_to_chroma():
    """
    제공된 PDF 파일을 기반으로 벡터 데이터베이스(Chroma)를 생성 및 저장합니다.
    
    ✔ PDF 존재 여부를 확인하고, 임베딩 및 LLM 설정을 초기화합니다.
    ✔ 이후 PDF → 텍스트 분할 → 임베딩 생성 → ChromaDB 저장 과정을 직접 구현해야 합니다.
    ✔ RAG 기반 질의응답을 위한 준비 단계로, 이 함수는 최초 1회 실행하면 충분합니다.

    [구현 요구사항]
    - SimpleDirectoryReader를 이용해 PDF 파일을 로드한다.
    - SentenceSplitter 등으로 문서를 적절한 크기의 노드로 분할한다.
    - VectorStoreIndex를 생성하여 Chroma 벡터DB에 업서트한다.
    """
    
    _ensure_paths() # PDF 존재 확인
    _init_llamaindex_settings() # LlamaIndex 설정 고정

    # PDF → 텍스트 분할 → 임베딩 생성 → ChromaDB 저장 코드를 구현하세요.


def infer(queries_json: str, output_json: str):
    '''
    쿼리(JSON 파일)를 입력으로 받아, 벡터DB 기반 RAG 질의 결과(4지선다 답)를 생성하고 JSON 파일로 저장합니다.

    > queries_json: 쿼리 목록이 담긴 JSON 파일 경로
      - 형식 예시:
        {
          "id": "Q1",
          "question": "...",
          "options": {"A": "...", "B": "...", "C": "...", "D": "..."}
        }

    > output_json: 질의 응답 결과를 저장할 JSON 파일 경로
      - 형식 예시:
        {
          "id": "Q1",
          "question": "...",
          "answer": "B",          # 반드시 "A"/"B"/"C"/"D" 중 하나
          "elapsed_sec": 1.23     # 응답 소요 시간
        }

    ✔ 저장된 벡터 DB를 불러와 RAG 질의를 수행하고, 쿼리당 처리 시간을 출력합니다.
    ✔ LLM 프롬프트에는 question과 options 4개를 모두 포함시키고,
       LLM이 최종적으로 선택한 보기를 한 글자("A"~"D")로만 반환하도록 설계해야 합니다.
    '''

    # 여기에 쿼리 로드 → RAG 질의 수행 → 결과 저장 → 처리 시간 출력 코드를 구현하세요.


def main():
    parser = argparse.ArgumentParser(description="LlamaIndex + Chroma RAG utility")
    parser.add_argument("--save", action="store_true",
                        help="3개의 PDF를 ChromaDB에 저장(컬렉션 리셋 후 재구축)")
    parser.add_argument("--infer", nargs=2, metavar=("queries.json", "output.json"),
                        help="쿼리를 읽어 추론 후 결과를 저장")
    args = parser.parse_args()

    if args.save:
        save_to_chroma()
    elif args.infer:
        qpath, opath = args.infer
        infer(qpath, opath)
    else:
        parser.print_help()


if __name__ == "__main__":

    if not os.environ.get("OPENAI_API_KEY"):
        raise EnvironmentError("OPENAI_API_KEY not set in environment.")
    main()
