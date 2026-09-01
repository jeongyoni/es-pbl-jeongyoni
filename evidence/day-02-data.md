# Day 2 데이터 준비 결과

> 예시 문장을 복사하지 말고 자신의 실제 실행 결과를 작성합니다.
> 실행하지 않은 항목은 완료로 표시하지 않습니다.

## 1. Index와 문서

- Index 이름: beauty-products
- 문서 한 건의 의미: 올리브영 화장품 상품 1개의 정보 (이름, 브랜드, 카테고리, 퍼스널컬러, 가격, 평점 등)
- 실제 색인 건수: 1,000건
- Mapping의 `dynamic` 설정: strict

## 2. 최종 Field

| Field | Type | 검색에서 사용할 목적 |
|---|---|---|
| product_id | keyword | 상품 고유 ID (업무 식별자) |
| product_name | text + keyword | 상품명 전문 검색 / 정확 비교·정렬 |
| brand | keyword | 브랜드별 필터 |
| category | keyword | 카테고리별 필터 (립틴트, 블러셔 등) |
| personal_color | keyword | 퍼스널컬러별 필터 (봄웜, 여쿨 등) |
| skin_type | keyword | 피부 타입별 필터 |
| price | integer | 가격 범위 필터·정렬 |
| rating | float | 평점 범위 필터·정렬 |
| review_count | integer | 리뷰 수 정렬 |
| tags | text | 특성 키워드 검색 (촉촉함, 지속력 등) |
| release_date | date | 출시일 범위 필터 |

필요한 만큼 행을 추가합니다.

## 3. 대량 데이터 생성·색인 결과

- 생성 건수:
- 로컬 검증 결과:
- Bulk 색인 결과:
- ES 실제 `_count`:
- 분류·숫자·boolean 분포 확인 결과:

## 4. Day 3 연결

- 검색 질문 기준: `docs/data-model.md`의 사용자 질문 3개

## 5. 결과 파일 위치

- Mapping:
- 실행 요청:
- 대표 문서:
- 데이터 생성 설정:
- 생성 표본:
- 생성 요약:

## 6. Pipeline 적용 판단

- 적용 / 미적용 / 보류:
- 판단 이유:

## 7. 미완료·오류

- 없음 또는 현재 상태:
- 다음에 할 작업:
