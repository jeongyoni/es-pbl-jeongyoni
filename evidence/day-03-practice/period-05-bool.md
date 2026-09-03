# 5교시 실습 — bool 검색

## (공통) 문제 1 — 제공 코드로 must·filter 확인

```http
GET /products/_search
{
  "size": 10,
  "query": {
    "bool": {
      "must": [{ "match": { "name": "무선" } }],
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

- `hits.total.value`: 74
- 상위 3개 ID·name:
  - P-00025 / MobiCore 컴팩트 무선 이어폰
  - P-00129 / Auralis 스마트 무선 이어폰
  - P-00369 / SoundLab 데일리 무선 이어폰
- 세 filter의 실제 값:
  - category: 전자기기 ✓ / in_stock: true ✓ / price: 59,400 (50,000~200,000 이내) ✓
- must와 filter의 역할 차이: must는 점수(relevance)에 영향을 주며 일치 여부를 따짐. filter는 점수 계산 없이 조건 충족 여부만 판단하므로 캐싱 가능하고 성능상 유리함

## (공통) 문제 2 — 조건 제거 실험 직접 구현

문제 1의 요청에서 `in_stock` filter만 제거한 API를 작성하세요. 다른 조건은 바꾸지 마세요.

### API 전체 입력

```http
GET /products/_search
{
  "size": 10,
  "query": {
    "bool": {
      "must": [{ "match": { "name": "무선" } }],
      "filter": [
        { "term": { "category": "전자기기" } },
        { "range": { "price": { "gte": 50000, "lte": 200000 } } }
      ]
    }
  }
}
```

### 비교 결과

- 변경 전 total / 변경 후 total: 74 / 83
- 새로 포함된 문서 ID·in_stock: P-00457 (in_stock: false), P-00521 (in_stock: false)
- 변화가 없다면 데이터 근거: —
- 제거한 조건의 역할: in_stock=true인 문서만 통과시키는 정확 조건 필터. 제거 시 품절 상품이 결과에 포함됨

## (공통) 문제 3 — should 조건 직접 구현

category가 `전자기기`인 문서 중 `name`에 `무선`이 있거나 `in_stock=true`인 조건을 최소 하나 만족하도록 bool API를 작성하세요. `minimum_should_match`를 명시하세요.

### API 전체 입력

```http
GET /products/_search
{
  "size": 10,
  "query": {
    "bool": {
      "filter": [{ "term": { "category": "전자기기" } }],
      "should": [
        { "match": { "name": "무선" } },
        { "term": { "in_stock": true } }
      ],
      "minimum_should_match": 1
    }
  }
}
```

### 결과 입력

- `hits.total.value`: 1,097
- 무선이지만 품절인 문서 존재 여부: 있음 — P-00457 (MobiCore 데일리 무선 이어폰, in_stock: false)
- 무선이 아니지만 재고가 있는 문서 존재 여부: 있음 — P-00009 (NeoTech 데일리 기계식 키보드, in_stock: true)
- should 조건 판정: 두 조건 중 하나만 만족해도 포함됨. minimum_should_match=1이므로 OR 논리 동작 확인 ✓

## (개인) 문제 4 — 자기 bool 검색

자기 사용자 질문 하나를 검색 의도와 정확 조건으로 분해해 bool 요청을 구현하세요.

### 역할·검증 기준

- must 0~1개, filter 2개 이상을 사용합니다.
- 각 field와 query 선택 이유를 mapping type으로 설명합니다.
- 반환 문서 3개 이상을 실제 값으로 검증합니다.

### API와 결과 입력

```http
GET /beauty-products/_search
{
  "size": 10,
  "_source": ["product_id", "product_name", "brand", "personal_color", "skin_type", "category"],
  "query": {
    "bool": {
      "must": [{ "match": { "product_name": "립틴트" } }],
      "filter": [
        { "term": { "personal_color": "봄웜" } },
        { "term": { "skin_type": "건성" } }
      ]
    }
  }
}
```

- 사용자 질문: "봄웜이고 건성인 피부에 맞는 립틴트 추천해줘"
- must와 이유: `product_name` match "립틴트" — text 타입이므로 분석기를 거친 full-text 검색, 점수에 반영해 관련성 높은 문서를 상위 노출
- filter 2개와 이유:
  - `personal_color` = "봄웜" (keyword) — 정확히 일치해야 하는 분류값이므로 term filter 적합
  - `skin_type` = "건성" (keyword) — 동일하게 정확 분류값이므로 term filter 적합
- 실제 검증 결과: total 18건. 상위 3건(P-00286 3CE 립틴트 / P-00372 맥 립틴트 / P-00414 클리오 립틴트) 모두 봄웜·건성 확인 ✓

## (개인) 문제 5 — 조건 역할 검증

개인 문제 4에서 filter 하나를 제거하고 전후 결과를 비교하세요. 추가로 원래 조건에서 제외되어야 하는 문서 1개를 독립 요청으로 확인하세요.

### 역할·검증 기준

- 한 번에 filter 하나만 제거합니다.
- 새로 포함된 문서의 실제 값을 확인합니다.
- 제외 문서는 원래 bool 결과에 포함되지 않아야 합니다.

### API와 결과 입력

```http
# skin_type filter 제거
GET /beauty-products/_search
{
  "size": 10,
  "_source": ["product_id", "product_name", "personal_color", "skin_type"],
  "query": {
    "bool": {
      "must": [{ "match": { "product_name": "립틴트" } }],
      "filter": [
        { "term": { "personal_color": "봄웜" } }
      ]
    }
  }
}
```

- 제거한 filter: `skin_type` = "건성"
- 전/후 total: 18 / 45
- 새로 포함된 ID와 값: P-00302 (봄웜, skin_type: 지성), P-00309 (봄웜, skin_type: 지성) 등 건성이 아닌 봄웜 립틴트 포함됨
- 제외 확인 ID와 근거: P-00255 (롬앤 립틴트 255, personal_color: 갈웜) — 원래 결과에 없으며, 독립 요청으로 갈웜 조건 검색 시 등장 확인 ✓
