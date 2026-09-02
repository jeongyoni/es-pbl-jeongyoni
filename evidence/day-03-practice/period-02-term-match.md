# 2교시 실습 — term과 match

## (공통) 문제 1 — 제공 코드로 정확 조건 확인

```http
GET /products/_search
{
  "size": 5,
  "query": { "term": { "category": "전자기기" } }
}
```

### 결과 입력

- `hits.total.value`: 1250
- 상위 3개 문서 ID: P-00009, P-00025, P-00081
- 상위 3개 문서의 category: 전자기기, 전자기기, 전자기기
- 모든 확인 문서가 정확 조건을 만족하는가: 예, 3개 모두 category가 "전자기기"로 정확히 일치
- `term`을 선택한 mapping 근거: category가 keyword 타입이므로 분석 없이 원값 그대로 비교하는 term이 적합

## (공통) 문제 2 — text 전문 검색 직접 구현

`products` index에서 상품명 `name`에 `무선`이라는 검색 의도가 있는 문서를 찾으세요. text 전문 검색에 적합한 query를 선택해 최대 5건을 반환하세요.

### API 전체 입력

```http
GET /products/_search
{
  "size": 5,
  "query": { "match": { "name": "무선" } }
}
```

### 결과 입력

- 선택한 query와 이유: match — name이 text 타입으로 분석된 token 기반 검색에 적합
- `hits.total.value`: 505
- 상위 3개 ID·name: P-00025(MobiCore 컴팩트 무선 이어폰), P-00042(CleanMate 실속형 무선 청소기), P-00129(Auralis 스마트 무선 이어폰)

## (공통) 문제 3 — 부적절한 조합 비교

같은 `name` field와 `무선` 검색어에 `term` query를 사용한 API를 직접 작성하세요. 문제 2와 결과를 비교하고, 차이를 mapping 또는 분석된 token 관점에서 설명하세요.

### API 전체 입력

```http
GET /products/_search
{
  "size": 5,
  "query": { "term": { "name": "무선" } }
}
```

### 비교 결과

- 문제 2 total / 문제 3 total: 505 / 505
- 공통으로 나온 문서 ID: 동일 문서 반환
- 달라진 이유: "무선"은 standard analyzer로 분석해도 동일한 단일 token이라 term과 match 결과가 같음. 하지만 "무선 이어폰"처럼 다중 단어 검색 시 term은 0건, match는 결과가 나와 text field에 term은 부적합
- `term`은 text에서 항상 0건인가? 실제 근거: 아니오. 검색어가 분석 후 token과 정확히 같은 단일 단어라면 결과가 나올 수 있음. 그러나 multi-word나 대소문자 차이가 있으면 0건이 되므로 text field에는 match 사용이 원칙

## (개인) 문제 4 — 자기 정확 조건 검색

자기 mapping에서 값 전체가 정확히 일치해야 하는 `keyword` 또는 `boolean` field 하나를 선택해 정확 조건 검색을 구현하세요.

### 역할·검증 기준

- 실제 존재하는 field와 값을 사용합니다.
- 반환 문서의 `_source`에서 조건을 직접 확인합니다.
- 왜 전문 검색이 아니라 정확 비교인지 설명합니다.

### API와 결과 입력

```http
GET /beauty-products/_search
{
  "size": 5,
  "query": { "term": { "personal_color": "봄웜" } }
}
```

- field / type / 값: personal_color / keyword / 봄웜
- 사용자 질문: 퍼스널컬러가 봄웜인 상품 찾기
- 상위 3개 ID와 실제 값: P-00240(봄웜), P-00244(봄웜), P-00257(봄웜)
- 통과/실패와 근거: 통과. personal_color는 keyword 타입으로 분석 없이 원값 비교하므로 term이 정확. 총 247건 반환

## (개인) 문제 5 — 자기 전문 검색

자기 mapping의 `text` field 하나와 사용자가 입력할 검색어를 정해 전문 검색 API를 구현하세요.

### 역할·검증 기준

- field가 실제 `text`인지 mapping으로 확인합니다.
- 상위 3개 결과를 관련/보류/무관으로 판정합니다.
- 정확 조건 문제와 query 선택 이유가 달라야 합니다.

### API와 결과 입력

```http
GET /beauty-products/_search
{
  "size": 5,
  "query": { "match": { "tags": "촉촉함" } }
}
```

- field / type / 검색어: tags / text / 촉촉함
- 상위 3개 ID: P-00230, P-00235, P-00238
- 관련/보류/무관과 이유: 3개 모두 관련 — tags에 "촉촉함" 포함 확인. text field라 token 기반 검색이므로 match 사용
- 완료 판정: 완료
