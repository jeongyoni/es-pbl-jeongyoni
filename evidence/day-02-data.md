# Day 2 실제 실행 증거

공통과 개인을 구분한다. 실행하지 않은 결과는 미실행으로 적는다. 비밀번호/인증 헤더를 기록하지 않는다.

## V1-T09-C/P 환경

- 실제 node 이름/버전/master:

```
name ip         node.role   master version
es01 172.18.0.3 cdfhilmrstw -      9.5.0
es02 172.18.0.4 cdfhilmrstw *      9.5.0
es03 172.18.0.5 cdfhilmrstw -      9.5.0
```

- products 존재 여부 / 실제 CAT 값: 공통 products index 없음 (수업 외 개인 환경에서 미생성)
- 개인 index 이름: beauty-products

현재 index 목록:

```
health status index           pri rep docs.count store.size
green  open   beauty-products   1   1       1000    720.3kb
green  open   my-index          1   1          0       498b
```

## V1-T12-C/P 생성/조회

- 공통/개인 구분: P(개인) / 대상 index: beauty-products
- 신규 생성: 생성 완료
- 요청과 실제 응답:

**PUT /beauty-products**
```json
{
  "acknowledged": true,
  "shards_acknowledged": true,
  "index": "beauty-products"
}
```

**GET /beauty-products/_mapping (주요 field)**
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
        "product_name":   { "type": "text", "analyzer": "korean_search",
                            "fields": { "keyword": { "type": "keyword", "ignore_above": 256 } } },
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

**GET /_cat/shards/beauty-products?v**
```
index           shard prirep state   docs   store ip         node
beauty-products 0     p      STARTED 1000 365.6kb 172.18.0.5 es03
beauty-products 0     r      STARTED 1000 354.6kb 172.18.0.4 es02
```

- 기대/실제 비교: dynamic:strict, 11개 field, 1 primary / 1 replica — 모두 기대와 일치 ✅

## V1-T13-C/P 분석

| 입력 | 방식(standard/field) | 예상 token | 실제 token/position | 차이 이유 |
|---|---|---|---|---|
| 촉촉한 봄웜 립틴트 | standard | 촉촉한, 봄웜, 립틴트 | 촉촉한(0), 봄웜(1), 립틴트(2) | 없음 |
| 촉촉한 봄웜 립틴트 | field (product_name) | 촉촉한, 봄웜, 립틴트 | 촉촉한(0), 봄웜(1), 립틴트(2) | 없음 |
| 지속력 좋은 코랄 블러셔 | standard | 지속력, 좋은, 코랄, 블러셔 | 지속력(0), 좋은(1), 코랄(2), 블러셔(3) | 없음 |
| 지속력 좋은 코랄 블러셔 | field (product_name) | 지속력, 좋은, 코랄, 블러셔 | 동일 | 없음 |
| 2만원 이하 평점 좋은 아이섀도우 | standard | 2만원, 이하, 평점, 좋은, 아이섀도우 | 2만원(ALPHANUM,0), 이하(1), 평점(2), 좋은(3), 아이섀도우(4) | 없음 |
| 2만원 이하 평점 좋은 아이섀도우 | field (product_name) | 동일 | 동일 | 없음 |

개인 검색어 3개를 두 방식으로 각각 기록. 요청은 elasticsearch/requests.http에 보존.

관찰: "2만원"은 숫자+한글 혼합으로 ALPHANUM 타입 — 가격 범위 검색 시 text 검색이 아닌 range query 사용 필요.

## V1-T14-C/P CRUD

- C(공통): products index 없음 — 미실행
- P(개인): 대상 index: beauty-products / 임시 ID: P-00001 / 출발 count: 0 (mapping 생성 직후)

| 단계 | 예상 result | 실제 result | 실제 source/변경·유지 field |
|---|---|---|---|
| 생성 | created | created, version: 1 | product_id, product_name, brand, category, personal_color, skin_type, price: 13000, rating: 4.7, review_count: 3251, tags, release_date 전체 저장 |
| 조회 | found: true | found: true | price: 13000 확인 |
| 수정/재조회 | updated | updated, version: 2 | price: 12000 (변경), 나머지 field 유지 |
| 삭제/재조회 | deleted / found: false | deleted, version: 3 / found: false | - |

- 삭제 뒤 found: false ✅ / count: 0 확인
- 선택 noop 관찰: 미실행

## V1-T15-C/P 생성·적재

- C(공통) 10000건: 미실행
- P(개인) 생성 설정: Python 스크립트 (generate-beauty.py), seed=20260901, 1000건, sample 30건
- 명령: `python3 generator/generate-beauty.py` → `docker cp` + `docker exec` 내부 curl Bulk API
- 로컬 검사 결과: beauty-products-sample-30.ndjson 30건 생성 확인, generation-summary.json 생성 확인
- 표본 ID/field/조건 사례 확인: P-00001~P-00030 / 전체 11 field 정상 / personal_color·category·tags 분포 포함
- 실제 Bulk 결과: errors: false, items: 1000
- 현재 단계: 완료 / S67 이어 할 작업: 없음 (pipeline 미구현)

## V1-T16-C simulate

| 입력 사례 | 예상 변화/오류 | 실제 변화/오류 | 저장 여부 |
|---|---|---|---|
| Samsung | brand_name→brand 변환, temp/raw_price 제거, in_stock:true 추가 | brand:"Samsung", in_stock:true, temp/raw_price 제거 완료 | 저장 안 됨 |
| Apple | 동일 패턴, category 유지 | brand:"Apple", category:"전자기기" 유지, in_stock:true 추가, temp/raw_price 제거 | 저장 안 됨 |
| in_stock=false | override:false이므로 false 유지 | in_stock: false (기존값 덮어쓰기 안 함) | 저장 안 됨 |
| temp 누락 | remove processor 오류 예상 | IllegalArgumentException: field [temp] not present as part of path [temp] | 저장 안 됨 |

## V1-T16-P 필수 개인 완료

- 개인 index: beauty-products / 생성 건수: 1000 / 실제 ES count: 1000 ✅

분류 terms:

| 카테고리 | 건수 | 퍼스널컬러 | 건수 |
|---|---|---|---|
| 블러셔 | 187 | 갈웜 | 267 |
| 립틴트 | 177 | 여쿨 | 261 |
| 아이섀도우 | 174 | 봄웜 | 247 |
| 파운데이션 | 173 | 겨쿨 | 225 |
| 쿠션 | 149 | | |
| 립스틱 | 140 | | |

숫자 stats:
- 가격: min 5,228 / max 44,935 / avg 24,913 (설정 범위 5,000~45,000 내 ✅)
- 평점: min 2.0 / max 5.0 / avg 3.5 (설정 범위 2.0~5.0 내 ✅)

날짜 범위: release_date 2024-01-01 ~ 2026-08-01 내 ✅

계획과 실제 분포 차이 이유: seed=20260901 기반 균등 분포이므로 카테고리·퍼스널컬러별 편차는 정상 통계 분산

선택 pipeline: 미구현 — Python 생성 데이터는 색인 전 이미 정제 완료, 변환 불필요

## 오류·재검증

| 요청/파일 | 오류 | 수정 | 실제 재실행 결과 | 다음 조치 |
|---|---|---|---|---|
| Bulk API (curl) | Mac에서 ES SSL 인증서 경로 오류 | docker cp로 ndjson 컨테이너 복사 후 docker exec 내부 curl 실행 | errors: false, 1000건 적재 완료 | 완료 |

## 제출

- commit hash / 현재 branch: d7209e5 / main
- GitHub에서 확인한 동일 commit: 확인 완료
- 미완료와 다음 요청: T14-C·T15-C(공통 products) 미실행 — 개인 환경에서 공통 index 미생성
