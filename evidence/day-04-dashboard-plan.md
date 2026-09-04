# Day 4 개인 Dashboard 설계

## 1. 사용자와 목적

- 내 주제: 올리브영 화장품 검색·추천 "Beauty Finder — 사용자 조건 기반 화장품 검색 및 분석"
- 이 Dashboard를 볼 사람: 자신의 퍼스널컬러(예: 겨쿨)와 피부타입을 아는 20대 화장품 소비자
- Dashboard를 보고 결정하거나 행동할 것: 내 퍼스널컬러·피부타입·예산에 맞는 카테고리와 브랜드를 좁혀 무엇을 살지 고른다
- 사용할 index / Data View: `beauty-products` (개인 index, 1,000건, time field `release_date`)

## 2. 데이터 준비 경로

- [x] A: 개인 데이터로 제작
- [ ] B: 공통 products로 제작하며 개인 데이터 보강 규칙 작성
- [ ] C: 공통 Dashboard를 완성하고 개인 청사진에 집중

선택 이유: 개인 index `beauty-products`가 이미 1,000건(브랜드·카테고리·퍼스널컬러·피부타입·가격·평점 field 포함)으로 존재해 네 가지 질문을 실제 값으로 바로 만들 수 있음. 공통 products에는 personal_color·rating 같은 뷰티 조건 field가 없어 주제에 맞지 않음.

## 3. 질문-데이터-차트 청사진

| 번호 | 분석 질문 | 필요한 field | 현재 존재? | mapping type | 계산·그룹 방식 | 차트 | filter/control | 확인 기준 |
|---|---|---|---|---|---|---|---|---|
| Q1 전체 규모 | 검색 대상 상품은 모두 몇 개인가 | (Records) | 예 | - | Count of records | Metric | personal_color Control | 1,000 |
| Q2 그룹 비교 | 어떤 카테고리에 상품이 가장 많은가 | category | 예 | keyword | Top values(8) + Count | Bar(가로) | personal_color Control | 블러셔 최다 |
| Q3 분포/정확한 값 | 브랜드별 상품 수·평균 가격·평균 평점은 | brand, price, rating | 예 | keyword, integer, float | Top values + Count + Avg price + Avg rating | Table | personal_color Control | 롬앤 상품 수 최다 |
| Q4 상태/시간 | 퍼스널컬러별 상품 구성 비율은 | personal_color | 예 | keyword | Top values + Count | Donut | personal_color Control | 겨쿨 비중 최대 |

## 4. 데이터 부족 분석

- 현재 데이터로 답할 수 없는 질문: "실제로 어떤 상품이 많이 팔렸는가", "월별 판매 추세는 어떤가"
- 부족한 field: `sales_count`(판매량), `stock`(재고 수량), `review_sentiment`(리뷰 긍/부정)
- 필요한 mapping type: sales_count·stock → integer, review_sentiment → keyword
- 필요한 값의 범위·범주·비율: sales_count 0~50,000(대표 상품 편중), stock 0~500, review_sentiment 긍정/중립/부정 ≈ 6:2:2
- 날짜가 필요하다면 기간과 단위: 판매 추세는 `sold_at`(구매 시점) 필드가 별도로 필요, 월 단위. `release_date`는 출시일이라 판매 추세로 쓸 수 없음
- 한 문서가 의미할 사건 또는 대상: 현재는 "화장품 상품 1건". 판매 분석을 하려면 "구매 이벤트 1건" 문서가 별도로 필요
- 생성 또는 수집 방법: Python 합성 생성. 브랜드·카테고리별 대표 상품에 판매량을 편중시켜 분포가 드러나게 함
- 데이터 수가 충분하다고 판단할 기준: 각 category·personal_color 조합이 최소 20건 이상이어서 필터 후에도 막대/조각이 사라지지 않을 때

## 5. 제작 순서

1. 공통 products로 6패널(Metric·Bar·Table·가격구간·재고 Donut·월별 Line)과 category Control 실습 후 저장
2. 개인 `beauty-products`로 전환, 시간 범위를 2023-01-01~2026-09-03으로 넓혀 1,000건 전부 표시
3. Q1~Q4 패널(전체 상품 수 Metric, 카테고리 Bar, 브랜드 Table, 퍼스널컬러 Donut) 제작·제목 부여
4. personal_color Options list Control 추가 → 겨쿨 선택 전후 검증 → 개인본으로 저장

## 6. 완료 예상 화면

- Dashboard 제목: `D4 개인 미션 - Beauty Finder - 정연`
- 필수 패널 수: 4 (Metric, 카테고리 Bar, 브랜드 Table, 퍼스널컬러 Donut) + Control 1
- 사용할 control/filter: personal_color Options list Control
- 저장할 캡처 파일명: `captures/p-p07-dashboard.png`, `captures/p-p08-final.png`
