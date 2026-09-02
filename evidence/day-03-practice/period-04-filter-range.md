# 4교시 실습 — 정확 조건과 경계

## (공통) 문제 1 — 제공 코드로 세 filter 확인

```http
GET /products/_search
{
  "size": 10,
  "query": {
    "bool": {
      "filter": [
        { "term": { "category": "전자기기" } },
        { "term": { "in_stock": true } },
        { "range": { "price": { "gte": 50000, "lte": 200000 } } }
      ]
    }
  }
}
```

### 결과 입력

- `hits.total.value`: 380
- 확인한 문서 ID 3개: P-00025, P-00129, P-00185
- 각 문서의 category / in_stock / price:
  - P-00025: 전자기기 / true / 59,400
  - P-00129: 전자기기 / true / 53,800
  - P-00185: 전자기기 / true / 161,600
- 조건을 위반한 문서가 있는가: 없음 — 세 filter 모두 통과한 문서만 반환됨

## (공통) 문제 2 — 경계 포함 범위 직접 구현

`products`에서 category가 `전자기기`이고 가격이 50,000원 이상 200,000원 이하인 상품을 검색하세요. 최대 10건을 반환하고 `product_id`, `name`, `category`, `price`만 표시하세요.

### API 전체 입력

```http
GET /products/_search
{
  "size": 10,
  "_source": ["product_id", "name", "category", "price"],
  "query": {
    "bool": {
      "filter": [
        { "term": { "category": "전자기기" } },
        { "range": { "price": { "gte": 50000, "lte": 200000 } } }
      ]
    }
  }
}
```

### 결과 입력

- `hits.total.value`: 440
- 최소·최대 price: 50,700 / 199,500
- 50,000 또는 200,000 경계 문서 존재 여부와 ID: 없음 — 정확히 50,000 또는 200,000인 문서가 데이터에 존재하지 않음

## (공통) 문제 3 — 경계 제외 범위 직접 구현

문제 2에서 다른 조건은 모두 그대로 유지하고 가격 조건만 50,000원 초과 200,000원 미만으로 바꾸세요. 한 요소만 변경해야 합니다.

### API 전체 입력

```http
GET /products/_search
{
  "size": 10,
  "_source": ["product_id", "name", "category", "price"],
  "query": {
    "bool": {
      "filter": [
        { "term": { "category": "전자기기" } },
        { "range": { "price": { "gt": 50000, "lt": 200000 } } }
      ]
    }
  }
}
```

### 비교 결과

- 문제 2 total / 문제 3 total: 440 / 440
- 빠진 경계 문서 ID: 없음
- 경계 문서가 없어 결과가 같다면 확인한 근거: price가 정확히 50,000 또는 200,000인 문서가 데이터에 없어 gte↔gt, lte↔lt 전환 시 결과 변화 없음

## (개인) 문제 4 — 자기 정확 조건 2개

자기 데이터에서 정확 조건으로 사용할 field 2개를 선택해 두 조건을 모두 만족하는 검색을 구현하세요.

### 역할·검증 기준

- keyword·boolean 등 실제 mapping type에 적합해야 합니다.
- 실행 전 포함 예상 문서 1개와 제외 예상 문서 1개를 정합니다.
- 실행 후 `_source`로 판정합니다.

### API와 결과 입력

```http
GET /beauty-products/_search
{
  "size": 10,
  "_source": ["product_id", "product_name", "brand", "personal_color", "skin_type", "category"],
  "query": {
    "bool": {
      "filter": [
        { "term": { "personal_color": "봄웜" } },
        { "term": { "skin_type": "지성" } }
      ]
    }
  }
}
```

- field·type·값 2개:
  - `personal_color` (keyword) = "봄웜"
  - `skin_type` (keyword) = "지성"
- 기대 ID / 제외 ID: P-00240 (봄웜·지성 → 포함 예상) / P-00279 (봄웜·건성 → 제외 예상)
- 실제 결과와 판정: total 53건. P-00240 포함 확인 ✓, P-00279는 결과에 없음 ✓ — 두 keyword filter 모두 정상 작동

## (개인) 문제 5 — 자기 범위와 경계 실험

자기 데이터의 numeric 또는 date field를 선택해 포함 경계와 제외 경계 요청을 각각 구현하세요.

### 역할·검증 기준

- 실제 데이터의 최소·최대 또는 의미 있는 경계값을 먼저 확인합니다.
- `gte/lte`와 `gt/lt` 외 조건은 동일하게 유지합니다.
- 경계 문서가 없으면 fixture 설계 또는 부재 근거를 기록합니다.

### API와 결과 입력

```http
# 포함 경계 (gte)
GET /beauty-products/_search
{
  "size": 3,
  "_source": ["product_id", "price"],
  "query": {
    "bool": {
      "filter": [{ "range": { "price": { "gte": 5228, "lte": 20000 } } }]
    }
  },
  "sort": [{ "price": "asc" }]
}

# 제외 경계 (gt)
GET /beauty-products/_search
{
  "size": 3,
  "_source": ["product_id", "price"],
  "query": {
    "bool": {
      "filter": [{ "range": { "price": { "gt": 5228, "lte": 20000 } } }]
    }
  },
  "sort": [{ "price": "asc" }]
}
```

- field / type / 경계값: `price` / integer / 5,228 (데이터 최솟값)
- 포함 요청 total / 제외 요청 total: 370 / 369
- 달라진 문서 ID: P-00051 (price=5,228) — gte에선 포함, gt에선 제외
- 경계 판정: gte/gt 차이 1건 확인 ✓ — 경계값 포함·제외 동작 정상
