# 252R 딥러닝응용 (LlamaIndex · RAG)

이 레포는 **252R 딥러닝응용 수업 실습**(Chapter 1~10)과, **2025-2학기 딥러닝응용 프로젝트**(RAG 기반 학칙/학사운영 규정 Q&A)를 함께 관리합니다.

- `practice/`: Chapter별 실습 노트북/코드
- `theory/`: 이론 자료(PDF) 및 노트북
- `project/`: 학칙 PDF 기반 RAG 질의응답 프로젝트(ChromaDB + LlamaIndex)
- `dla/`: `uv` 기반 파이썬 환경(의존성 묶음)

## Chapter 별 실습 내용

| Chapter | 주제 | 주요 파일/폴더 | 간단 요약 |
|---:|---|---|---|
| 1 | LlamaIndex 입문 | `practice/ch01/starter.ipynb` | 기본 개념/설치/첫 실행 |
| 2 | RAG 파이프라인 | `practice/ch02/ch02_practice.ipynb` | 로딩→청킹→인덱싱→질의 흐름 |
| 3 | 벡터DB/저장소 | `practice/ch03/01_chroma_example.ipynb` | Chroma/Pinecone/Qdrant 비교 실습 |
| 4 | 문서 RAG(PDF 등) | `practice/ch04/ch04_practice.ipynb` | PDF 기반 RAG 기본기 |
| 5 | 멀티모달 RAG | `practice/ch05/multimodal_rag.ipynb` | 텍스트+이미지 검색/질의 |
| 6 | Agentic RAG | `practice/ch06/ch06_agentic_rag.ipynb` | 에이전트 구성 및 도구 활용 |
| 7 | Advanced RAG | `practice/ch07/ch07_advanced_rag.ipynb` | Reranking/HyDE 등 고급 기법 |
| 8 | Function Calling | `practice/ch08/ch08_practice.ipynb` | 외부 도구 호출 기반 에이전트 |
| 9 | Text-to-SQL | `practice/ch09/ch09_text_to_sql.ipynb` | 자연어→SQL 질의 에이전트 |
| 10 | MCP | `practice/ch10/server.py` | MCP 서버/클라이언트 및 예제 |

요약: 1~4장은 “문서→벡터→검색→답변” RAG 기본기를 다지고, 5~10장은 멀티모달/에이전트/고급 검색/툴링(MCP)까지 확장합니다.

## 레포 구조

```text
.
├── practice/              # Chapter별 실습(노트북/스크립트/샘플 데이터)
├── theory/                # Transformer/LLM 등 이론 자료
├── project/               # 2025-2 프로젝트: 학칙 PDF RAG Q&A
│   ├── data/              # 제공 PDF(7개) — 이 폴더의 PDF만 사용
│   ├── main.py            # 제출 파일(단일 파일)
│   ├── test/              # 예시 queries/outputs
│   └── chroma_db_test/    # (--save) 실행 시 생성/갱신
└── dla/                   # uv 환경(의존성)
```

## 실행/개발 환경

- Python 3.10+ 권장
- 의존성 설치(권장: `uv`): `dla/`는 LlamaIndex/Chroma/Jupyter 등을 포함한 실습용 환경입니다.

```bash
cd dla
uv sync
source .venv/bin/activate
```

## 환경 변수(.env)

프로젝트/실습에서 API 키는 루트의 `.env`를 사용합니다.

```bash
OPENAI_API_KEY=...

# (선택) 실습/확장에 따라 필요
GOOGLE_API_KEY=...
PINECONE_API_KEY=...
OPENWEATHER_API_KEY=...
```

## 2025-2학기 딥러닝응용 프로젝트

고려대학교 **학칙 및 학사운영 규정 PDF**를 기반으로, 규정 관련 질문에 자동 응답하는 **RAG 기반 질의응답 시스템(챗봇)** 구현이 목표입니다.

### 개요(파이프라인)

1. `--save`: PDF 로드 → 문단/청크 분할 → 임베딩 생성(OpenAI) → ChromaDB 저장  
2. `--infer`: `queries.json` 입력 → ChromaDB 검색(근거 문단) → LLM 답변 생성 → `outputs.json` 저장

`outputs.json`에는 `id`, `question`, `answer`(A/B/C/D), `elapsed_sec`, `citations`(참고근거) 를 포함합니다.

### 실행 방법

`project/` 폴더에서 실행해야 경로가 맞습니다.

```bash
cd project

# 1) ChromaDB 생성/갱신
python main.py --save

# 2) 질의응답 수행
python main.py --infer test/queries.json test/outputs.json
```

### 제출/평가 메모

- 마감: 2025년 12월 19일(금) 23:59
- 제출: `project/main.py` (단일 파일)
- 실행: `--save`, `--infer` 모두 오류 없이 동작해야 함
- 평가: 테스트 쿼리 → `outputs.json`의 `"answer"`(A/B/C/D) 정답률 비교
- 구현 제한: 과제 안내에 따라 `save_to_chroma()`, `infer()` 외 수정 금지(자세한 주석 참고)

## License

MIT License
