# Beauty Finder - 사용자 조건 기반 화장품 검색 및 분석

## 1. 프로젝트 소개

- 문제와 사용자: 자신의 퍼스널컬러·피부타입·예산에 맞는 화장품을 찾기 어려운 소비자를 위해, 조건 기반 검색과 분석을 제공한다.
- ES로 검색할 문서 1건: 화장품 상품 정보 1건 — 제품명, 브랜드, 카테고리, 퍼스널컬러, 피부타입, 가격, 평점, 리뷰수, 태그, 출시일을 담은 JSON 문서
- 이 주제를 선택한 이유: 전문 검색(태그·제품명), 정확 조건 필터(퍼스널컬러·카테고리), 범위 필터(가격), 정렬(평점·리뷰수), 집계(Dashboard)까지 ES의 핵심 기능을 자연스럽게 모두 실습할 수 있다.

## 2. 실행 순서

1. Docker 환경 시작: `es-5days-pbl-course/day-01/docker/` 에서 `start.ps1` 실행
2. index와 mapping 생성: `elasticsearch/index-create.json` 기반으로 Dev Tools Console에서 PUT 요청
3. 데이터 생성·Bulk 적재: `data/pbl-data-template/` 의 생성기로 5,000건 합성 후 Bulk 색인
4. 검색 요청 실행: `elasticsearch/requests.http` 의 검색 질문 3개 확인
5. Kibana Dashboard 확인: `evidence/dashboard.png` 캡처 저장

## 3. 데이터와 mapping

- 문서 수: 5,000건 (합성 데이터)
- 데이터 생성 규칙과 seed: Day 2에 확정 예정 — Python 생성기, seed 고정으로 재현 가능
- 개인정보 미사용 확인: 실제 소비자 정보 없음. 제품명·브랜드·태그 모두 합성값
- 핵심 필드와 타입 선택 이유: Day 2 mapping 확정 후 기록 예정

## 4. 검색·품질 테스트

| 검색 질문 | 기대 결과 | 실제 결과 | 판정 |
|---|---|---|---|
| 촉촉한 봄웜 립틴트 | tags에 "촉촉함" 포함, personal_color=봄웜, category=립틴트 상품 | Day 3 기록 | - |
| 지속력 좋은 코랄 블러셔 | tags에 "지속력" 포함, category=블러셔 상품 | Day 3 기록 | - |
| 2만원 이하 평점 좋은 아이섀도우 | price≤20000, category=아이섀도우, rating 높은 순 정렬 | Day 3 기록 | - |

## 5. Dashboard

- Dashboard 사용자: 화장품 구매를 고려 중인 소비자 또는 상품 기획 담당자
- 차트 1이 답하는 질문: 카테고리별 평균 평점은?
- 차트 2가 답하는 질문: 퍼스널컬러별 제품 수 분포는?
- control/filter 목적: 카테고리·퍼스널컬러를 선택해 원하는 조건의 제품만 집계 확인

## 6. AI Search 확장 판단

- 적용 여부와 근거: Day 5에 판단 예정
