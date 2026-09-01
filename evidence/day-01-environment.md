# Day 1 환경 확인 증거

## preflight 체크 결과

- Docker CLI: PASS
- Docker Engine: PASS (29.6.1)
- Docker Compose: PASS
- 포트 9200: 사용 가능
- 포트 5601: 사용 가능
- 디스크 여유: 670GB

## ES 클러스터 실행 결과

- 실행일: 2026-08-31
- docker compose up -d 결과: 컨테이너 3개 (es01, es02, es03) 정상 기동
- status 확인: green ✅

## GET / 응답

```json
{
  "name" : "es01",
  "cluster_name" : "es-5days-pbl",
  "cluster_uuid" : "xUPzKy_nT0SYJgx8shgemQ",
  "version" : {
    "number" : "9.5.0",
    "build_flavor" : "default",
    "build_type" : "docker",
    "build_hash" : "8d4246a64bc255212407b1b313fe402391299c88",
    "build_date" : "2026-07-29T23:38:48.847847767Z",
    "build_snapshot" : false,
    "lucene_version" : "10.5.0",
    "minimum_wire_compatibility_version" : "8.19.0",
    "minimum_index_compatibility_version" : "8.0.0"
  },
  "tagline" : "You Know, for Search"
}
```

## GET /_cluster/health 응답

```json
{
  "cluster_name" : "es-5days-pbl",
  "status" : "green",
  "timed_out" : false,
  "number_of_nodes" : 3,
  "number_of_data_nodes" : 3,
  "active_primary_shards" : 54,
  "active_shards" : 108,
  "relocating_shards" : 0,
  "initializing_shards" : 0,
  "unassigned_shards" : 0,
  "unassigned_primary_shards" : 0,
  "delayed_unassigned_shards" : 0,
  "number_of_pending_tasks" : 0,
  "number_of_in_flight_fetch" : 0,
  "task_max_waiting_in_queue_millis" : 0,
  "active_shards_percent_as_number" : 100.0
}
```

- status: green ✅
- number_of_nodes: 3 ✅
- 판정: 클러스터 정상 — 3노드 green 확인

## Kibana 접속 확인

- URL: http://localhost:5601
- 접속 결과: 로그인 화면 정상 표시, elastic 계정으로 로그인 성공
- Dev Tools Console 진입: Management → Dev Tools 경로로 진입 확인
