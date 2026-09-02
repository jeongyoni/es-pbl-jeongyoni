# 3교시 실습 — 전문 검색 확장

## (공통) 문제 1 — 제공 코드로 여러 field 검색

```http
GET /products/_search
{
  "size": 5,
  "query": {
    "multi_match": {
      "query": "무선 이어폰",
      "fields": ["name", "description"]
    }
  }
}
```

### 결과 입력

- `hits.total.value`: 505
- 상위 3개 ID·name: P-00241(SoundLab 프리미엄 무선 이어폰), P-00305(Auralis 실속형 무선 이어폰), P-00529(NeoTech 스마트 무선 이어폰)
- 각 문서가 name·description 중 어디에서 의도와 연결되는가: 3개 모두 name에 "무선"·"이어폰" 두 token이 포함되어 name에서 연결
- 상위 3개 관련/보류/무관 판정: 3개 모두 관련 — name에 무선 이어폰 명시

## (공통) 문제 2 — field boost 직접 구현

문제 1과 같은 조건을 유지하되 `name` 일치를 `description`보다 3배 중요하게 보는 Search API를 작성하세요.

### API 전체 입력

```http
GET /products/_search
{
  "size": 5,
  "query": {
    "multi_match": {
      "query": "무선 이어폰",
      "fields": ["name^3", "description"]
    }
  }
}
```

### 비교 결과

- 변경 전 상위 3개 ID: P-00241, P-00305, P-00529
- 변경 후 상위 3개 ID: P-00241, P-00305, P-00529
- 순위가 달라진 문서와 이유: 변화 없음 — 상위 문서들이 이미 name에 두 token을 모두 포함하고 있어 boost 전후 상위권 순위 동일
- boost가 사용자 의도에 유리했는가: 예. name 일치에 가중치를 주면 description에만 일치하는 관련성 낮은 문서보다 name에 정확히 일치하는 문서가 상위에 오름

## (공통) 문제 3 — 구문 검색 직접 구현

`products` index의 `name`에서 `무선 이어폰`이라는 단어 순서와 인접성을 중요하게 검색하세요. `slop`은 0, 최대 5건으로 구현하세요.

### API 전체 입력

```http
GET /products/_search
{
  "size": 5,
  "query": {
    "match_phrase": {
      "name": {
        "query": "무선 이어폰",
        "slop": 0
      }
    }
  }
}
```

### 결과 입력

- `hits.total.value`: 249
- 상위 문서 ID·name: P-00241(SoundLab 프리미엄 무선 이어폰), P-00305(Auralis 실속형 무선 이어폰), P-00529(NeoTech 스마트 무선 이어폰)
- 문제 1보다 결과가 줄어든 이유: match_phrase는 "무선"과 "이어폰"이 이 순서로 인접해야 하므로 "무선 청소기" 같이 다른 단어가 뒤에 오는 문서는 제외됨. match는 두 token 중 하나라도 있으면 포함
- 구문 의도에 맞지 않는 문서가 있는가: 없음. 상위 문서 모두 name에 "무선 이어폰"이 연속으로 포함

## (개인) 문제 4 — 여러 text field 검색

자기 프로젝트에서 같은 사용자 검색어가 적용될 수 있는 text field 2개 이상을 선택해 전문 검색을 구현하세요.

### 역할·검증 기준

- 각 field의 서비스 역할을 설명합니다.
- 상위 3개 문서를 사람이 평가합니다.
- 한 field만 필요한 도메인이라면 `match`를 선택하고 그 이유를 적어도 됩니다.

### API와 결과 입력

```http
GET /beauty-products/_search
{
  "size": 5,
  "query": {
    "multi_match": {
      "query": "립틴트 촉촉함",
      "fields": ["product_name", "tags"]
    }
  }
}
```

- 사용자 질문·검색어: 촉촉한 립틴트 찾기 / "립틴트 촉촉함"
- 선택 field와 역할: product_name(상품명 전문 검색), tags(특성 키워드 검색)
- 상위 3개 판정: P-00033(롬앤 아이섀도우, tags 촉촉함) → 보류(카테고리 불일치) / P-00085(토니모리 립틴트, tags 촉촉함) → 관련 / P-00087(미샤 아이섀도우, tags 촉촉함) → 보류(카테고리 불일치)
- query 선택 근거: product_name·tags 모두 text 타입이므로 multi_match로 두 field를 동시에 검색

## (개인) 문제 5 — boost 또는 phrase 가설 검증

자기 검색에서 field boost 또는 phrase 중 하나를 선택해 기본 요청과 비교하세요.

### 역할·검증 기준

- 같은 index·데이터·검색어·size를 유지합니다.
- 한 요소만 변경합니다.
- 결과가 바뀌지 않아도 실제 결과대로 기록합니다.

### API와 결과 입력

```http
GET /beauty-products/_search
{
  "size": 5,
  "query": {
    "multi_match": {
      "query": "립틴트 촉촉함",
      "fields": ["product_name^3", "tags"]
    }
  }
}
```

- 선택한 가설: product_name에 boost^3 적용 시 카테고리가 립틴트인 상품이 상위로 올라올 것
- 변경 전 상위 3개: P-00033(롬앤 아이섀도우, tags 촉촉함), P-00085(토니모리 립틴트, tags 촉촉함), P-00087(미샤 아이섀도우, tags 촉촉함)
- 변경 후 상위 3개: P-00229(에뛰드 립틴트 229), P-00230(맥 립틴트 230), P-00243(클리오 립틴트 243)
- 개선/보류/악화 판정: 개선
- 판정 근거: boost 후 product_name에 "립틴트"가 포함된 문서가 상위로 올라와 tags만 일치하는 아이섀도우가 밀려남. 사용자 의도에 더 부합
