# Dashboard 계획

## 1. Dashboard 사용자와 목적

- Dashboard를 볼 사용자: 화장품 구매를 고려 중인 소비자 또는 상품 기획 담당자
- 이 사용자가 확인하려는 상황: 카테고리·퍼스널컬러별로 어떤 제품이 많고 평점이 높은지, 가격대 분포가 어떻게 되는지 한눈에 파악
- Dashboard를 본 뒤 할 다음 행동: 특정 카테고리·퍼스널컬러 필터를 걸고 평점 높은 제품을 선별해 구매 후보로 좁힌다

## 2. 분석 질문

1. 카테고리별 평균 평점은 어떻게 되는가?
2. 퍼스널컬러별 제품 수는 어떻게 분포하는가?
3. 가격대(0~1만, 1~2만, 2~3만, 3만+)별 제품 수는?
4. 브랜드별 평균 리뷰 수 상위 10개는?

## 3. 차트 계획

| 번호 | Lens 시각화 | 답할 질문 | 사용할 field | 집계 또는 표시 방식 | 결과를 본 뒤의 판단·행동 |
|---:|---|---|---|---|---|
| 1 | Metric | 전체 상품 수 | — | Records Count | 데이터 색인이 정상인지 확인 |
| 2 | Bar (가로) | 카테고리별 평균 평점 | category, rating | Terms + Average | 평점 낮은 카테고리 개선 필요 여부 판단 |
| 3 | Pie 또는 Bar | 퍼스널컬러별 제품 수 | personal_color | Terms Count | 특정 퍼스널컬러 제품이 부족하면 데이터 보강 |
| 4 | Histogram | 가격대별 제품 분포 | price | Histogram (interval 10000) | 가격대 쏠림 확인, 범위 필터 기준 설정 |

## 4. Control과 시간 설정

- Options list 또는 range control에 사용할 field: category, personal_color (Options list), price (Range slider)
- 이 control로 함께 좁힐 차트: 차트 2, 3, 4 모두
- Data View 이름: beauty-products
- 시간 field: 사용
- 시간 field를 사용한다면 field 이름과 기간: release_date, 전체 기간 기본값

## 5. 제목과 배치 계획

- Dashboard 제목: Beauty Finder — 화장품 검색 분석
- 상단에 둘 차트 또는 control: Metric(전체 상품 수) + category·personal_color Options list control
- 가운데에 둘 차트: 카테고리별 평균 평점 Bar / 퍼스널컬러별 제품 수 Pie
- 하단에 둘 차트: 가격대별 제품 분포 Histogram

## 6. Day 4 완료 기록

- 실제로 만든 차트 수: (Day 4에 기록)
- Dashboard 화면 캡처: `evidence/dashboard.png`
- 선택 export: `kibana/dashboard.ndjson`
- 계획과 다르게 바꾼 점 및 이유: (Day 4에 기록)
