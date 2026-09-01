# 데이터 모델 초안

## 0. index 기본 정보 (T09-P)

- index 이름: beauty-products
- 문서 한 건의 의미: 화장품 상품 1개
- 업무 ID field: product_id
- 예시 ID: P-0001

## 1. 문서 단위

- 검색 결과 한 건은 무엇인가: 화장품 상품 1개
- 이 문서 한 건이 사용자에게 보여 주는 정보는 무엇인가: 제품명, 브랜드, 카테고리, 퍼스널컬러, 피부타입, 가격, 평점, 리뷰 수, 태그, 출시일

## 2. 대표 문서 예시

```json
{
  "product_name": "롬앤 쥬시래스팅 틴트",
  "brand": "롬앤",
  "category": "립틴트",
  "personal_color": "봄웜",
  "skin_type": "건성",
  "price": 13000,
  "rating": 4.7,
  "review_count": 3251,
  "tags": ["촉촉함", "발색", "지속력"],
  "release_date": "2026-03-01"
}
```

## 3. 핵심 field와 역할

Day 1에는 field의 검색 역할과 ES type 후보를 초안으로 적습니다. Day 2에 mapping과 함께 확정합니다.

| field | 예시 값 | 검색에서 맡는 역할 | ES type 후보 | 선택 이유 |
|---|---|---|---|---|
| product_name | "롬앤 쥬시래스팅 틴트" | 전문 검색 | text (+ keyword) | 제품명을 token 단위로 검색하되 정렬·집계용 keyword도 필요 |
| brand | "롬앤" | 정확 조건 / 집계 | keyword | 브랜드명 전체 일치 필터 및 집계 |
| category | "립틴트" | 정확 조건 / 집계 | keyword | 카테고리 필터 및 Dashboard 집계 |
| personal_color | "봄웜" | 정확 조건 / 집계 | keyword | 퍼스널컬러 필터 및 Dashboard 집계 |
| skin_type | "건성" | 정확 조건 | keyword | 피부타입 필터 |
| price | 13000 | 범위 / 정렬 / 집계 | integer | 가격 범위 필터, 낮은 순 정렬, 가격대 분포 집계 |
| rating | 4.7 | 범위 / 정렬 / 집계 | float | 평점 필터, 높은 순 정렬, 평균 집계 |
| review_count | 3251 | 정렬 / 집계 | integer | 리뷰 많은 순 정렬 |
| tags | ["촉촉함", "발색"] | 전문 검색 | text | 사용자 입력 키워드와 태그 token 매칭 |
| release_date | "2026-03-01" | 범위 / 정렬 | date | 신상품 정렬, 출시일 범위 필터 |

## 4. 검색 질문과 field 연결

| 검색 질문 | 사용할 field | 확인할 역할 |
|---|---|---|
| 촉촉한 봄웜 립틴트 | tags(전문 검색), personal_color(정확 조건), category(정확 조건) | "촉촉함" token 포함 + personal_color=봄웜 + category=립틴트 |
| 지속력 좋은 코랄 블러셔 | tags(전문 검색), category(정확 조건) | "지속력" token 포함 + category=블러셔 |
| 2만원 이하 평점 좋은 아이섀도우 | price(범위), category(정확 조건), rating(정렬) | price≤20000 + category=아이섀도우, rating 내림차순 |

## 5. 제외할 데이터

- 수집하거나 저장하지 않을 개인정보: 실제 소비자 구매 이력, 회원 정보, 리뷰 작성자 정보
- 제외 이유: 과제 범위 외이며 개인정보보호 원칙에 따라 합성 데이터만 사용
