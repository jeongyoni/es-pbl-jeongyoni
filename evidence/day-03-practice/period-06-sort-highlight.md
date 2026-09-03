# 6교시 실습 — 정렬·highlight

## (공통) 문제 1 — 제공 코드로 1·2차 정렬 확인

```http
GET /products/_search
{
  "size": 10,
  "_source": ["product_id", "name", "price", "rating", "in_stock"],
  "query": { "match": { "name": "무선" } },
  "sort": [
    { "rating": "desc" },
    { "price": "asc" }
  ]
}
```

### 결과 입력

- 상위 5개 ID / rating / price:
  - P-03842 / 5.0 / 13,900
  - P-10193 / 5.0 / 72,500
  - P-08761 / 5.0 / 107,200
  - P-07634 / 5.0 / 132,300
  - P-05962 / 5.0 / 138,300
- 1차 정렬이 올바른가: 올바름 — 상위 5개 모두 rating 5.0으로 내림차순 정렬 ✓
- rating 동률에서 2차 정렬이 적용된 사례: rating 5.0 동률 구간에서 price 오름차순 적용됨 (13,900 → 72,500 → 107,200 순)
- 동률이 없다면 2차 정렬을 확인할 수 있는 방법: —

## (공통) 문제 2 — 정렬 우선순위 교환

문제 1과 같은 검색 결과를 가격이 낮은 순서로 먼저 정렬하고, 가격이 같으면 평점이 높은 순서로 정렬하세요.

### API 전체 입력

```http
GET /products/_search
{
  "size": 10,
  "_source": ["product_id", "name", "price", "rating"],
  "query": { "match": { "name": "무선" } },
  "sort": [
    { "price": "asc" },
    { "rating": "desc" }
  ]
}
```

### 비교 결과

- 변경 후 상위 5개 ID / price / rating:
  - P-19794 / 9,200 / 4.3
  - P-16954 / 9,900 / 2.5
  - P-11130 / 10,100 / 3.9
  - P-01490 / 10,900 / 2.9
  - P-15722 / 11,300 / 3.0
- 순서가 달라진 문서: 전체 순서 변경 — 문제 1은 rating 최고값 우선, 문제 2는 price 최저값 우선
- 검색 hit 집합도 달라졌는가: 달라지지 않음 — 동일한 996건, 정렬 순서만 변경됨

## (공통) 문제 3 — highlight와 표시 field 구현

`name`, `description`에서 `무선 이어폰`을 검색하되 `name`에 3배 boost를 적용하세요. 최대 5건을 반환하고 결과 카드용 field만 `_source`에 포함하며 `name`, `description`에 highlight를 적용하세요.

### API 전체 입력

```http
GET /products/_search
{
  "size": 5,
  "_source": ["product_id", "name", "category", "price", "rating"],
  "query": {
    "multi_match": {
      "query": "무선 이어폰",
      "fields": ["name^3", "description"]
    }
  },
  "highlight": {
    "pre_tags": ["<em>"],
    "post_tags": ["</em>"],
    "fields": { "name": {}, "description": {} }
  }
}
```

### 결과 입력

- `_source` field 목록: product_id, name, category, price, rating
- highlight가 생성된 문서 ID와 field:
  - P-00025: name → `MobiCore 컴팩트 <em>무선</em> <em>이어폰</em>`
  - P-00129: name → `Auralis 스마트 <em>무선</em> <em>이어폰</em>`
  - P-00153: name → `SoundLab 실속형 <em>무선</em> <em>이어폰</em>`
  - P-00209: name → `NeoTech 프리미엄 <em>무선</em> <em>이어폰</em>`
  - P-00369: name → `SoundLab 데일리 <em>무선</em> <em>이어폰</em>`
- `_source`와 highlight의 차이: `_source`는 원본 전체 텍스트, highlight는 검색어 위치에 태그를 삽입한 조각
- highlight가 없는 hit가 있다면 이유 추정: 전체 5건 모두 name에 highlight 생성됨. description에 매칭됐으나 name boost로 name 우선 노출

## (개인) 문제 4 — 자기 결과 정렬·카드 설계

자기 서비스에서 중요한 1차·2차 정렬 기준과 결과 카드 field 3~5개를 선택해 Search API를 구현하세요.

### 역할·검증 기준

- 정렬 가능한 mapping type을 사용합니다.
- 1차·2차 정렬의 업무적 이유를 설명합니다.
- 실제 상위 5개 값으로 순서를 검증합니다.

### API와 결과 입력

```http
GET /beauty-products/_search
{
  "size": 10,
  "_source": ["product_id", "product_name", "brand", "category", "price", "rating"],
  "query": { "match_all": {} },
  "sort": [
    { "rating": "desc" },
    { "price": "asc" }
  ]
}
```

- 정렬 field·방향·이유:
  - 1차: `rating` 내림차순 — 사용자가 만족도 높은 상품을 먼저 보기 위함
  - 2차: `price` 오름차순 — 동일 평점이면 저렴한 상품을 우선 노출
- 카드 field와 이유: product_name(상품명), brand(브랜드), category(카테고리), price(가격), rating(평점)
- 상위 5개 정렬 검증:
  - P-00891 페리페라 잉크 무드 글로이 틴트 05 피치 / rating 5.0 / price 11,500
  - P-00086 에스쁘아 꾸뛰르 립스틱 리부스트 05 버건디 / rating 5.0 / price 12,300
  - P-00162 맥 아이섀도우 팔레트 #10 퍼플 / rating 5.0 / price 12,500
  - P-00565 얼터너티브스테레오 립 포션 카라멜 글레이즈 / rating 5.0 / price 15,100
  - P-00826 티르티르 마스크 핏 레드 파운데이션 W21 쿨베이지 / rating 5.0 / price 19,300

## (개인) 문제 5 — 자기 highlight 또는 표시 최적화

자기 text 검색에 highlight를 적용하세요. text 검색이 없는 프로젝트라면 `_source` 최소화 전후를 비교하세요.

### 역할·검증 기준

- 검색 field와 highlight field의 관계가 타당해야 합니다.
- 원본 데이터와 강조 조각을 구분합니다.
- 사용자 판단에 실제로 도움이 되는지 평가합니다.

### API와 결과 입력

```http
GET /beauty-products/_search
{
  "size": 5,
  "_source": ["product_id", "product_name", "brand", "category", "price", "rating"],
  "query": {
    "multi_match": {
      "query": "틴트",
      "fields": ["product_name^3", "tags"]
    }
  },
  "highlight": {
    "pre_tags": ["<em>"],
    "post_tags": ["</em>"],
    "fields": { "product_name": {}, "tags": {} }
  }
}
```

- 선택한 방식과 이유: `product_name`과 `tags` 모두 text 타입이므로 검색어 위치에 highlight 적용 가능
- 실제 결과: total 163건. 상위 5건 모두 product_name에 `<em>틴트</em>` highlight 생성됨
  - P-00265 삐아 글로우 <em>틴트</em> 01 핑크베이지
  - P-00276 삐아 글로우 <em>틴트</em> 12 빈티지레드
- 사용자에게 유용한가: 유용함 — 검색어 위치를 즉시 확인할 수 있어 상품명 중 어느 부분이 매칭됐는지 파악 가능
- 개선할 점: `tags` field highlight도 추가하면 태그 기반 매칭 여부도 사용자에게 표시할 수 있음
