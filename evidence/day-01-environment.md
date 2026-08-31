# Day 1 환경 확인 증거

## preflight 체크 결과

- Docker CLI: PASS
- Docker Engine: PASS (29.6.1)
- Docker Compose: PASS
- 포트 9200: 사용 가능
- 포트 5601: 사용 가능
- 디스크 여유: 670GB

## ES 클러스터 실행 결과

- 실행일:
- start.ps1 / docker compose up 결과:
- status 확인:

## GET / 응답

```json

```

## GET /_cluster/health 응답

```json

```

- status: (green 확인)
- number_of_nodes: (3 확인)
- 판정:

## Kibana 접속 확인

- URL: http://localhost:5601
- 접속 결과:
- Dev Tools Console 진입:
