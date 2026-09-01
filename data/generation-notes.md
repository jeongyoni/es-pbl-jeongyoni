# 개인 생성 규칙

## V1-T15-P 설정

- index / 업무 ID field / ID prefix: beauty-products / product_id / P
- 첫 건수1000 / SampleCount30 / Seed: 1000 / 30 / 20260901
- 코드·환경·설정 파일 위치: data/pbl-data-template/generator/generate-beauty.py

| field | Kind | 후보/범위/비율 | 결측 정책 | mapping type | 연결 질문 |
|---|---|---|---|---|---|
| product_id | id | P-00001~ | 결측 없음 | keyword | - |
| product_name | template | {{brand}} {{category}} {{sequence}} | 결측 없음 | text+keyword | - |
| brand | choice | 롬앤/클리오/에뛰드/3CE/맥/라네즈/토니모리/미샤 | 결측 없음 | keyword | Q1, Q2 |
| category | choice | 립틴트/블러셔/아이섀도우/파운데이션/쿠션/립스틱 | 결측 없음 | keyword | Q1, Q2, Q3 |
| personal_color | choice | 봄웜/여쿨/갈웜/겨쿨 | 결측 없음 | keyword | Q1 |
| skin_type | choice | 건성/지성/복합성/민감성 | 결측 없음 | keyword | - |
| price | integer | 5,000~45,000 | 결측 없음 | integer | Q3 |
| rating | decimal | 2.0~5.0 (소수점 1자리) | 결측 없음 | float | Q2, Q3 |
| review_count | integer | 0~10,000 | 결측 없음 | integer | - |
| tags | tags | 촉촉함/발색/지속력/은은한발색/매트/글로시/가성비/데일리/커버력/선크림 (1~4개) | 결측 없음 | text | Q1, Q2 |
| release_date | date | 2024-01-01~2026-08-01 | 결측 없음 | date | - |

## 포함·제외·경계

| 질문 | 포함 사례 | 제외 사례 | 경계 사례 | 고정 사례 사용 여부 | 확인 요청 |
|---|---|---|---|---|---|
| Q1 촉촉한 봄웜 립틴트 | tags=촉촉함, personal_color=봄웜, category=립틴트 | personal_color=여쿨 또는 category≠립틴트 | - | sample-documents.json 사용 | GET /beauty-products/_search |
| Q2 지속력 좋은 코랄 블러셔 | tags=지속력, category=블러셔 | category≠블러셔 | - | sample-documents.json 사용 | GET /beauty-products/_search |
| Q3 2만원 이하 평점 좋은 아이섀도우 | category=아이섀도우, price≤20000 | price>20000 또는 category≠아이섀도우 | price=20000 (경계 포함) | sample-documents.json 사용 | GET /beauty-products/_search |

- FixedDocumentsFile을 쓰면 업무 ID를 생성 ID로 다시 배정함을 확인: 미사용 (Python 생성기로 직접 생성)
- 복합 객체/연관 분포 등 미지원 요구와 선택한 범위/대안: 해당 없음 (평면 구조)
- 생성·적재·검증 명령: python3 generator/generate-beauty.py → curl Bulk API
- 실제 분포와 예상의 차이 / 다음 수정:
  - 카테고리: 블러셔 187건 최다, 립스틱 140건 최소 (균등 분포 내 정상 편차)
  - 퍼스널컬러: 갈웜 267건 최다, 겨쿨 225건 최소 (균등 분포 내 정상 편차)
  - 가격: min 5,228 / max 44,935 / avg 24,913 (설정 범위 5,000~45,000 내 ✅)
  - 평점: min 2.0 / max 5.0 / avg 3.5 (설정 범위 2.0~5.0 내 ✅)
