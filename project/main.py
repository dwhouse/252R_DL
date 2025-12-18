# 라이브러리 로드 및 환경 변수 설정
import os
import json
import time
import argparse
from pathlib import Path

from dotenv import load_dotenv
load_dotenv(dotenv_path="../.env", override=True)  # .env 파일 키를 우선 적용

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


# PDF 경로(모든 파일 data 폴더 내에 위치)
PDF_FILES = [
    "data/2-1-1 고려대학교 학칙.pdf",
    "data/2-1-2 학사운영 규정.pdf",
    "data/졸업요건_경제통계학부.pdf",
    "data/졸업요건_글로벌경영전공.pdf",
    "data/졸업요건_데이터계산과학전공.pdf",
    "data/졸업요건_빅데이터사이언스학부.pdf",
    "data/졸업요건_컴퓨터융합소프트웨어학과.pdf"
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

    # 1. PDF 파일 로드
    print("[1] PDF 파일을 로드하는 중...")
    print(f"  - 로드할 PDF 파일: {len(PDF_FILES)}개")
    for pdf in PDF_FILES:
        print(f"    • {pdf}")
    reader = SimpleDirectoryReader(input_files=PDF_FILES)
    documents = reader.load_data()
    print(f"  - 총 {len(documents)} 페이지가 로드되었습니다.")

    # 2. 문서를 노드로 분할 (SentenceSplitter 사용)
    print("\n[2] 문서를 청크로 분할하는 중...")
    splitter = SentenceSplitter(
        chunk_size = 1024,
        chunk_overlap = 200
    )
    nodes = splitter.get_nodes_from_documents(documents)
    print(f"총 {len(nodes)} 개의 노드로 분할되었습니다.")

    # 3. ChromaDB 클라이언트 및 컬렉션 생성
    print("\n[3] ChromaDB를 초기화하는 중...")
    chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)

    # 기존 컬렉션이 있으면 삭제 후 재생성
    try:
        chroma_client.delete_collection(COLLECTION_NAME)
        print(f"기존 컬렉션 '{COLLECTION_NAME}'을 삭제했습니다.")
    except Exception:
        pass

    chroma_collection = chroma_client.get_or_create_collection(COLLECTION_NAME)
    print(f"컬렉션 '{COLLECTION_NAME}'을 생성했습니다.")

    # 4. ChromaVectorStore 생성
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # 5. VectorStoreIndex 생성 (임베딩 생성 및 저장)
    print("\n[4] 벡터 인덱스를 생성하고 ChromaDB에 저장하는 중...")
    index = VectorStoreIndex(
        nodes=nodes,
        storage_context=storage_context,
    )

    print(f"ChromaDB 저장 완료.\n - 경로: {CHROMA_PATH}")


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

    _init_llamaindex_settings()  # LlamaIndex 설정 고정

    # 1. 쿼리 JSON 파일 로드
    print(f"[1] 쿼리 파일 로드 중: {queries_json}")
    with open(queries_json, "r", encoding="utf-8") as f:
        queries = json.load(f)
    print(f" - 총 {len(queries)} 개의 쿼리가 로드되었습니다.")

    # 2. ChromaDB 불러오기
    print(f"\n[2] ChromaDB 로드 중: {CHROMA_PATH}")
    chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
    chroma_collection = chroma_client.get_collection(COLLECTION_NAME)

    # 3. VectorStoreIndex 로드
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    index = VectorStoreIndex.from_vector_store(vector_store=vector_store)

    # 4. Query Engine 생성
    query_engine = index.as_query_engine(similarity_top_k=7)

    # 4-2. Prompt Template Define
    qa_prompt_tmpl_str = """
    당신은 고려대학교 학칙 및 졸업요건에 대한 엄격한 행정 전문가입니다.
    아래에 제공된 [문맥 정보] 만을 사용하여 질문에 답해야 합니다.
    사전 지식을 사용하지 말고, 문맥에 없는 내용은 답하지 마십시오.
    
    [문맥 정보]
    --------------------
    {context_str}
    --------------------
    
    [질문] : {query_str}
    
    [필수 추론단계]
    ### 1) 조항 탐색
    - 질문 키워드로 관련 조항을 **모두** 찾기(본문 + 주석/별표/부칙 포함)

    ### 2) 적용 범위 확정
    - 질문 시점을 고정: **신청 요건**인지 **졸업/이수 요건**인지 구분
    - 예외/단서 확인: “단, 다만, ~제외, ~할 수 있다” 문구 우선 체크
    - 우선순위 적용: **특별 규정(학과/학번/과정/전형별)** > 일반 규정

    ### 3) 정답 검증
    - 숫자/조건이 질문 조건과 **정확히 일치**하는지 재확인(시점·대상·학번·재수강 등)
    - 보기 A, B, C, D 중 결론과 **가장 일치**하는 것 선택
    
    [답변 형식]
    설명 없이 오직 알파벳 한 글자(A, B, C, D)만 출력하세요.
    """
    from llama_index.core.prompts import PromptTemplate
    qa_prompt = PromptTemplate(qa_prompt_tmpl_str)
    query_engine.update_prompts({"response_synthesizer:text_qa_template": qa_prompt})
    
    # 5. 각 쿼리에 대해 RAG 질의 수행
    print(f"\n[3] RAG 질의 수행 중...")
    results = []
    print(f"총 {len(queries)} 개의 쿼리 처리를 시작합니다.")
    for i, query_item in enumerate(queries):
        query_id = query_item["id"]
        question = query_item["question"]
        options = query_item["options"]
        
        # 질문 구성
        full_query = f"""
        {question}
        
        보기:
        A: {options['A']}
        B: {options['B']}
        C: {options['C']}
        D: {options['D']}
        """

        # 시간 측정 시작
        start_time = time.time()

        # RAG 질의 수행
        response = query_engine.query(full_query)
        answer_text = str(response).strip().upper().replace(".", "")

        # 시간 측정 종료
        elapsed_sec = round(time.time() - start_time, 2)

        # 응답에서 A, B, C, D 추출 (첫 번째로 등장하는 유효한 답 추출)
        answer = None
        for char in answer_text:
            if char in ["A", "B", "C", "D"]:
                answer = char
                break

        # 유효한 답이 없으면 기본값 설정
        if answer is None:
            answer = "A"
            print(f"  [경고] {query_id}: 유효한 답을 추출할 수 없어 기본값 'A'로 설정")

        citations = []
        for node in response.source_nodes:
            # 메타데이터에서 파일명과 페이지 정보 추출 (LlamaIndex 기본 메타데이터 활용)
            # file_name이 없으면 page_label 등 다른 키를 확인
            file_name = node.metadata.get("file_name", "Unknown File")
            page_label = node.metadata.get("page_label", "N/A")
            
            # 텍스트 일부 추출 (너무 길면 줄임)
            content_preview = node.node.get_text()[:100].replace("\n", " ")
            
            citations.append({
                "file": file_name,
                "page": page_label,
                "span": content_preview + "..."
            })
            
        # 결과 저장
        result = {
            "id": query_id,
            "question": question,
            "answer": answer,
            "elapsed_sec": elapsed_sec,
            "citations": citations
        }
        results.append(result)

        print(f"[{i+1}/{len(queries)}] {query_id}: 답={answer}, 시간={elapsed_sec}초 (근거 {len(citations)}개)")
        
    # 6. 결과를 JSON 파일로 저장
    print(f"\n결과 저장 중: {output_json}")
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"추론 완료! 총 {len(results)}개 쿼리 처리됨.")
    print(f" - 결과 파일: {output_json}")


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
