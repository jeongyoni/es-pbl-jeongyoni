# Beauty Finder - 사용자 조건 기반 화장품 검색 및 분석

## 1. 프로젝트 소개

- **주제**: 자신의 퍼스널컬러·피부타입·예산에 맞는 화장품을 찾기 어려운 소비자를 위해, 조건 기반 검색과 데이터 시각화를 제공한다.
- **검색 대상 문서 1건**: 화장품 상품 1건 — 제품명, 브랜드, 카테고리, 퍼스널컬러, 피부타입, 가격, 평점, 리뷰수, 태그, 출시일을 담은 JSON 문서
- **주제 선택 이유**: 전문 검색(태그·제품명 text), 정확 조건 필터(keyword), 범위 필터(integer/float), 정렬, 집계(Dashboard) 등 Elasticsearch 핵심 기능을 자연스럽게 모두 실습할 수 있다. personal_color·skin_type처럼 화장품에 특화된 field를 통해 단순 쇼핑몰 예제와 차별화된 검색 시나리오를 만든다.

## 2. 실행 순서

1. Docker 환경 시작: `es-5days-pbl-course/day-01/docker/` 에서 `docker compose up -d` 실행
2. Index와 mapping 생성: `elasticsearch/index-create.json` 기반으로 Dev Tools Console에서 PUT 요청
3. 데이터 Bulk 적재: `data/pbl-data-template/generated/beauty-products-1000.ndjson` 을 Bulk API로 색인
4. 검색 요청 실행: `elasticsearch/requests.http` 의 검색 질문 확인
5. 검색 앱 실행: `search-app-template/` 에서 `docker compose up -d` → http://localhost:3000
6. Kibana Dashboard 확인: http://localhost:5601 → Dashboards → D4 개인 미션 - Beauty Finder - 정연

## 3. 데이터와 mapping

- **문서 수**: 1,000건 (올리브영 실제 판매 브랜드·상품 기반 합성 데이터)
- **데이터 생성**: Python 생성기, `seed=9502026` 고정으로 재현 가능
- **개인정보 미사용**: 실제 소비자 정보 없음. 제품명·브랜드·태그 모두 실제 올리브영 판매 상품 기반 합성값
- **출시일 범위**: 2023-01-04 ~ 2026-08-xx (`release_date` field, 판매 추세가 아닌 상품 등록 시점)

| field | type | 선택 이유 |
|---|---|---|
| product_id | keyword | 고유 식별자 |
| product_name | text + keyword | 전문 검색(text) + 정렬(keyword) |
| brand | keyword | 정확 필터, 집계 |
| category | keyword | 정확 필터, 집계 |
| personal_color | keyword | 정확 필터, Dashboard Control |
| skin_type | keyword | 정확 필터 |
| price | integer | 범위 필터·정렬·평균 집계 |
| rating | float | 정렬·평균 집계 |
| review_count | integer | 정렬 |
| tags | text | 전문 검색 (촉촉함, 지속력 등 특성 태그) |
| release_date | date | 범위 필터 (판매 추세로 해석 불가 — 출시일) |

## 4. 검색·품질 테스트

| 검색 질문 | 사용 query | 기대 결과 | 실제 결과 | 판정 |
|---|---|---|---|---|
| 촉촉한 봄웜 립틴트 | multi_match(tags) + filter(personal_color, category) | tags에 "촉촉함" 포함, personal_color=봄웜, category=립틴트 상위 노출 | total 53건, 3CE 립틴트·맥 립틴트 상위 | 관련 |
| 지속력 좋은 코랄 블러셔 | multi_match(tags) + filter(category=블러셔) | tags에 "지속력" 포함, 블러셔 카테고리 | total 63건, 페리페라·릴리바이레드 블러셔 상위 | 관련 |
| 2만원 이하 평점 좋은 아이섀도우 | filter(price≤20000, category) + sort(rating desc) | 가격 조건 내 평점 높은 순 | 해당 조건 내 정렬 정상 동작 | 관련 |

## 5. Day 4 개인 Dashboard

### 5-1. 대시보드 개요

- **Dashboard 이름**: D4 개인 미션 - Beauty Finder - 정연
- **Data View**: `beauty-products` (1,000건, time field: `release_date`)
- **시간 범위**: 2023-01-01 ~ 2026-09-03 (전체 데이터 포함)
- **패널 수**: 5개 + Control 1개

### 5-2. 패널 구성

| 패널 | 분석 질문 | 차트 타입 | 필드 | 주요 값 |
|---|---|---|---|---|
| 전체 상품 수 | 검색 대상 상품은 몇 개인가? | Metric | Count of records | **1,000** |
| 카테고리별 상품 수 | 어떤 카테고리에 상품이 가장 많은가? | Bar (Lens) | category | 블러셔 187 최다 |
| 브랜드별 상품 수·평균가격·평균평점 | 브랜드별 상품 구색과 가격대·평점은? | Table (Lens) | brand, price, rating | 롬엔 111건 최다 |
| 퍼스널컬러별 상품 비율 | 퍼스널컬러 유형별 제품 구성은? | Donut (Lens) | personal_color | 겨울 26.3% |
| 카테고리×퍼스널컬러 상품 수 | 퍼스널컬러별로 어떤 카테고리가 강한가? | Heatmap (Lens) | category × personal_color, price | 색상=평균가격 범위 |

### 5-3. Control

- **타입**: Options list (단일 선택)
- **필드**: `personal_color`
- **목적**: 퍼스널컬러(겨울/봄웜/여름/강원) 선택 시 5개 패널이 동시에 필터링되어 해당 퍼스널컬러 소비자에게 맞는 카테고리·브랜드를 즉시 확인 가능

### 5-4. filter/control 전후 검증

| 항목 | 적용 전 (Any) | 겨울 필터 적용 후 | 정상 여부 |
|---|---:|---:|---|
| 전체 상품 수 | 1,000 | **263** | 정상 |
| 카테고리 최다 | 블러셔 187 | 립틴트·파운데이션 50 | 정상 |
| 퍼스널컬러 Donut | 4분할 | 겨울 100% | 정상 |
| 브랜드 상위 | 롬엔 111 | 롬엔 23 | 정상 |

### 5-5. 핵심값 교차 검증

| Dashboard 표시값 | Elasticsearch 집계 결과 | 일치 여부 |
|---|---:|---|
| 전체 상품 수 1,000 | `GET beauty-products/_count` → 1,000 | 일치 |
| 블러셔 187 | `terms` 집계 → 187 | 일치 |
| 겨울 263 | `terms` 집계 → 263 | 일치 |

### 5-6. 결과 해석

1. 전체 1,000건 중 카테고리는 블러셔(187)·립틴트(177)·아이섀도우(174) 순으로 고르게 분포하고 립스틱(140)이 가장 적다. 카테고리 편차가 크지 않아 소비자에게 다양한 카테고리 선택지를 제공할 수 있으며, 립스틱 라인 보강을 검토할 여지가 있다.
2. 퍼스널컬러를 겨울(263건)로 좁히면 최다 카테고리가 블러셔 → 립틴트·파운데이션(각 50)으로 순위가 바뀐다. "겨울 타입 소비자에게는 블러셔보다 립틴트·파운데이션을 먼저 추천"하는 데이터 기반 판단이 가능하다.

### 5-7. 데이터 한계

- `release_date`(출시일)만 있고 `sales_count`(판매량)·`sold_at`(구매 시점)·`stock`(재고) field가 없어 실제 인기 상품이나 판매 추세는 파악 불가
- `rating`은 평균값만 있고 리뷰 수 신뢰도를 함께 고려해야 정확한 품질 판단 가능
- 합성 데이터 특성상 퍼스널컬러 분포가 23~26%로 균일하여 실제 편중 패턴(예: 봄웜 제품이 더 많은 시장)을 반영하지 못함

### 5-8. 캡처 파일

| 파일 | 설명 |
|---|---|
| `evidence/captures/personal-dashboard.png` | 전체 1,000건, 필터 없음 (Any) |
| `evidence/captures/personal-dashboard-filtered.png` | 퍼스널컬러=겨울 필터 적용, 263건 |

## 6. AI Search 확장 판단

- 적용 여부와 근거: Day 5에 판단 예정
- 후보 기능: semantic search (product_name · tags에 dense_vector), kNN 유사 상품 추천
