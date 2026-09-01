# Day 2 실제 실행 증거

공통과 개인을 구분한다. 실행하지 않은 결과는 미실행으로 적는다. 비밀번호/인증 헤더를 기록하지 않는다.

## V1-T09-C/P 환경

- 실제 node 이름/버전/master: es01(172.18.0.3)·es02(172.18.0.4, master*)·es03(172.18.0.5) / 모두 9.5.0
- products 존재 여부 / 실제 CAT 값: 없음 — beauty-products(1000 docs, green), my-index(0 docs, green)
- 개인 index 이름: beauty-products

## V1-T12-C/P 생성/조회

- 공통/개인 구분, 대상 index: P(개인) / beauty-products
- 신규 생성 또는 기존 확인: 신규 생성
- 요청과 실제 응답(settings/mapping/shards):

PUT /beauty-products → `{"acknowledged":true,"shards_acknowledged":true,"index":"beauty-products"}`

GET /beauty-products/_mapping:
```json
{"beauty-products":{"mappings":{"dynamic":"strict","properties":{
  "brand":{"type":"keyword"},"category":{"type":"keyword"},
  "personal_color":{"type":"keyword"},"price":{"type":"integer"},
  "product_id":{"type":"keyword"},
  "product_name":{"type":"text","analyzer":"korean_search","fields":{"keyword":{"type":"keyword","ignore_above":256}}},
  "rating":{"type":"float"},"release_date":{"type":"date"},
  "review_count":{"type":"integer"},"skin_type":{"type":"keyword"},
  "tags":{"type":"text","analyzer":"korean_search"}
}}}}
```

GET /_cat/shards/beauty-products?v:
```
index           shard prirep state   docs   store ip         node
beauty-products 0     p      STARTED 1000 365.6kb 172.18.0.5 es03
beauty-products 0     r      STARTED 1000 354.6kb 172.18.0.4 es02
```

- 기대/실제 비교: dynamic:strict·11 field·1 primary/1 replica — 모두 기대와 일치 ✅

## V1-T13-C/P 분석

| 입력 | 방식(standard/field) | 예상 token | 실제 token/position | 차이 이유 |
|---|---|---|---|---|
| 촉촉한 봄웜 립틴트 | standard | 촉촉한, 봄웜, 립틴트 | 촉촉한(0), 봄웜(1), 립틴트(2) | 없음 |
| 촉촉한 봄웜 립틴트 | field(product_name) | 촉촉한, 봄웜, 립틴트 | 촉촉한(0), 봄웜(1), 립틴트(2) | 없음 |
| 지속력 좋은 코랄 블러셔 | standard | 지속력, 좋은, 코랄, 블러셔 | 지속력(0), 좋은(1), 코랄(2), 블러셔(3) | 없음 |
| 지속력 좋은 코랄 블러셔 | field(product_name) | 지속력, 좋은, 코랄, 블러셔 | 동일 | 없음 |
| 2만원 이하 평점 좋은 아이섀도우 | standard | 2만원, 이하, 평점, 좋은, 아이섀도우 | 2만원(ALPHANUM,0), 이하(1), 평점(2), 좋은(3), 아이섀도우(4) | 없음 |
| 2만원 이하 평점 좋은 아이섀도우 | field(product_name) | 동일 | 동일 | 없음 |

개인 검색어3개를 두 방식으로 각각 기록한다. 요청은 루트 requests.http에 보존한다.

## V1-T14-C/P CRUD

- 대상 index / 임시 ID / 출발 count: beauty-products / P-00001 / 0 (mapping 생성 직후)

| 단계 | 예상 result | 실제 result | 실제 source/변경·유지 field |
|---|---|---|---|
| 생성 | created | created, version:1 | 전체 11 field 저장, price:13000 |
| 조회 | found:true | found:true | price:13000 확인 |
| 수정/재조회 | updated | updated, version:2 | price:12000(변경), 나머지 field 유지 |
| 삭제/재조회 | deleted / found:false | deleted, version:3 / found:false | — |

- 삭제 뒤 found/count: found:false / count:0
- 선택 noop/not_found 관찰: 미실행

## V1-T15-C/P 생성·적재

- 생성 설정/명령/건수/seed: Python(generate-beauty.py) / python3 generator/generate-beauty.py → docker cp + docker exec 내부 curl Bulk API / 1000건 / seed=20260901
- 로컬 검사 결과: beauty-products-sample-30.ndjson 30건·generation-summary.json 생성 확인
- 표본 ID/field/조건 사례 확인: P-00001~P-00030 / 11 field 정상 / personal_color·category·tags 분포 포함
- 실제 Bulk 결과 / 현재 단계 / S67에서 이어 할 작업: errors:false, 1000건 / 완료 / 없음(pipeline 미구현)

## V1-T16-C simulate

| 입력 사례 | 예상 변화/오류 | 실제 변화/오류 | 저장 여부 |
|---|---|---|---|
| Samsung | brand_name→brand 변환, temp·raw_price 제거, in_stock:true 추가 | brand:"Samsung", in_stock:true, temp·raw_price 제거 | 저장 안 됨 |
| Apple | 동일 패턴, category 유지 | brand:"Apple", category:"전자기기" 유지, in_stock:true, temp·raw_price 제거 | 저장 안 됨 |
| in_stock=false | override:false이므로 기존 false 유지 | in_stock:false 유지 | 저장 안 됨 |
| temp 누락 | remove processor 오류 | IllegalArgumentException: field [temp] not present as part of path [temp] | 저장 안 됨 |

## V1-T16-P 필수 개인 완료

- 개인 index / 생성 건수 / 실제 ES count: beauty-products / 1000 / 1000 ✅
- 분류 terms / 숫자 stats / 필요한 날짜 범위: 카테고리(블러셔 187·립틴트 177·아이섀도우 174·파운데이션 173·쿠션 149·립스틱 140), 퍼스널컬러(갈웜 267·여쿨 261·봄웜 247·겨쿨 225) / 가격 min 5228·max 44935·avg 24913, 평점 min 2.0·max 5.0·avg 3.5 / release_date 2024-01-01~2026-08-01
- 계획과 실제 분포 차이 이유: seed=20260901 균등 분포, 카테고리·퍼스널컬러 편차는 정상 통계 분산 범위 내
- 선택 pipeline 실제 단건/GET/정리 결과(미구현이면 해당 없음): 해당 없음

## 오류·재검증

| 요청/파일 | 오류 | 수정 | 실제 재실행 결과 | 다음 조치 |
|---|---|---|---|---|
| Bulk API curl | Mac 환경 SSL cert 경로 오류 | docker cp로 ndjson 복사 후 docker exec 내부 curl 실행 | errors:false, 1000건 적재 완료 | 완료 |

## 제출

- commit hash / 현재 branch: 4eef83e / main
- GitHub에서 확인한 동일 commit / push 실패라면 원인: 확인 완료
- 미완료와 다음 요청: T14-C·T15-C 공통 products index 미실행(개인 환경에서 미생성)
