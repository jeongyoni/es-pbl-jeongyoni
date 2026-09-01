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

## T11 — index/mapping 생성

(Day 2 진행 중 기록 예정)

## T15 — 데이터 적재 및 검증

(Day 2 진행 중 기록 예정)
