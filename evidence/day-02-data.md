# Day 2 환경 및 데이터 확인 증거

## T09 — 클러스터 노드 확인

### GET /_cat/nodes?v&h=name,ip,node.role,master,version

```
name ip         node.role   master version
es01 172.18.0.3 cdfhilmrstw -      9.5.0
es02 172.18.0.4 cdfhilmrstw *      9.5.0
es03 172.18.0.5 cdfhilmrstw -      9.5.0
```

- 노드 수: 3개 확인
- 버전: 9.5.0 확인
- master 노드: es02 (`*`)

### GET /_cat/indices?v

```
health status index                                           uuid                   pri rep docs.count docs.deleted store.size pri.store.size dataset.size
green  open   .internal.alerts-security.alerts-default-000001 5QdRtKSJRcOBDf9GYD3nUA   1   1          0            0       498b           249b         249b
green  open   .ds-.workflows-events-2026.08.31-000001         5RbCBjrUSuapKVHYCu5Z3Q   1   1          0            0       498b           249b         249b
green  open   .ds-.kibana_change_history-2026.08.31-000001    0CbT1fu0RwKAZjJKYTSC_g   1   1          0            0       498b           249b         249b
green  open   my-index                                        HhfulZQHRfG2WeM08KM26w   1   1          0            0       498b           249b         249b
```

- products index 존재 여부: 없음 (아직 생성 전 — 정상)

### GET /_cat/shards/beauty-products?v
```
index           shard prirep state   docs   store dataset ip         node
beauty-products 0     p      STARTED 1000 365.6kb 365.6kb 172.18.0.5 es03
beauty-products 0     r      STARTED 1000 354.6kb 354.6kb 172.18.0.4 es02
```
- primary: es03 / replica: es02 / 둘 다 STARTED ✅

## T12 — index 생성 및 mapping 확인

### PUT /beauty-products 결과
```json
{
  "acknowledged": true,
  "shards_acknowledged": true,
  "index": "beauty-products"
}
```

### GET /beauty-products/_mapping 결과
```json
{
  "beauty-products": {
    "mappings": {
      "dynamic": "strict",
      "properties": {
        "brand":          { "type": "keyword" },
        "category":       { "type": "keyword" },
        "personal_color": { "type": "keyword" },
        "price":          { "type": "integer" },
        "product_id":     { "type": "keyword" },
        "product_name":   { "type": "text", "fields": { "keyword": { "type": "keyword", "ignore_above": 256 } }, "analyzer": "korean_search" },
        "rating":         { "type": "float" },
        "release_date":   { "type": "date" },
        "review_count":   { "type": "integer" },
        "skin_type":      { "type": "keyword" },
        "tags":           { "type": "text", "analyzer": "korean_search" }
      }
    }
  }
}
```

- dynamic: strict 확인 ✅
- 전체 11개 field 확인 ✅
- product_name: text + keyword 멀티필드 확인 ✅

## T13 — _analyze 토큰 확인

### POST /_analyze (standard 직접 지정)
- 입력: "촉촉한 봄웜 립틴트"
- 예상 token: 촉촉한, 봄웜, 립틴트
- 실제 token: 촉촉한(0), 봄웜(1), 립틴트(2)
- 차이: 없음

### 검색어 3개 × 2방식 결과

| 검색어 | standard 결과 | field 결과 | 차이 |
|---|---|---|---|
| 촉촉한 봄웜 립틴트 | 촉촉한, 봄웜, 립틴트 | 촉촉한, 봄웜, 립틴트 | 없음 |
| 지속력 좋은 코랄 블러셔 | 지속력, 좋은, 코랄, 블러셔 | 지속력, 좋은, 코랄, 블러셔 | 없음 |
| 2만원 이하 평점 좋은 아이섀도우 | 2만원(ALPHANUM), 이하, 평점, 좋은, 아이섀도우 | 동일 | 없음 |

- "2만원"은 숫자+한글 혼합이라 ALPHANUM 타입으로 인식됨 (검색 시 주의)
- 전체적으로 korean_search(standard)는 공백 기준 token 분리, 두 방식 결과 동일

## T14 — CRUD

| 동작 | 요청 | 결과 |
|---|---|---|
| Create | PUT /beauty-products/_doc/P-00001?op_type=create | result: created, version: 1 |
| Read | GET /beauty-products/_doc/P-00001 | found: true, price: 13000 확인 |
| Update | POST /beauty-products/_update/P-00001 (price→12000) | result: updated, version: 2 |
| Delete | DELETE /beauty-products/_doc/P-00001 | result: deleted, version: 3 |
| 삭제 확인 | GET /beauty-products/_doc/P-00001 | found: false ✅ |

## T15 — 데이터 생성 및 적재

- 생성 방식: Python 스크립트 (generate-beauty.py), seed=20260901
- 생성 건수: 1,000건
- 파일: data/pbl-data-template/generated/beauty-products-1000.ndjson
- Bulk 적재 결과: errors: false, items: 1000
- count 검증: GET /beauty-products/_count → count: 1000 ✅

## T16 — 분포 검증

### 카테고리별 건수
| 카테고리 | 건수 |
|---|---|
| 블러셔 | 187 |
| 립틴트 | 177 |
| 아이섀도우 | 174 |
| 파운데이션 | 173 |
| 쿠션 | 149 |
| 립스틱 | 140 |

### 퍼스널컬러별 건수
| 퍼스널컬러 | 건수 |
|---|---|
| 갈웜 | 267 |
| 여쿨 | 261 |
| 봄웜 | 247 |
| 겨쿨 | 225 |

### 가격 통계
- 최솟값: 5,228원 / 최댓값: 44,935원 / 평균: 24,913원 (설정 범위 5,000~45,000 내 ✅)

### 평점 통계
- 최솟값: 2.0 / 최댓값: 5.0 / 평균: 3.5 (설정 범위 2.0~5.0 내 ✅)
