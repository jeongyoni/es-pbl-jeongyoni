# 검색 품질 테스트

## 검색 질문별 기대·제외·판정 기준

### 질문 1: 촉촉한 봄웜 립틴트

- 검색어: 촉촉한 봄웜 립틴트
- 사용할 field: tags (전문 검색), personal_color (정확 조건), category (정확 조건)
- filter: personal_color = 봄웜, category = 립틴트
- 기대 문서: tags에 "촉촉함" 포함 + personal_color = 봄웜 + category = 립틴트인 상품
- 제외 문서: personal_color가 봄웜이 아닌 상품, category가 립틴트가 아닌 상품
- 0건 조건: 봄웜 립틴트 중 tags에 "촉촉함"이 없는 경우 → 의도된 0건
- 판정 기준: 상위 결과 모두 봄웜 립틴트이고 tags에 촉촉함 관련 token 포함
- 실제 결과: (Day 3 기록)
- 판정: (Day 3 기록)

### 질문 2: 지속력 좋은 코랄 블러셔

- 검색어: 지속력 좋은 코랄 블러셔
- 사용할 field: tags (전문 검색), category (정확 조건)
- filter: category = 블러셔
- 기대 문서: tags에 "지속력" 포함 + category = 블러셔인 상품
- 제외 문서: category가 블러셔가 아닌 상품
- 0건 조건: 블러셔 중 tags에 "지속력"이 없는 경우 → 의도된 0건
- 판정 기준: 상위 결과 모두 블러셔이고 tags에 지속력 포함
- 실제 결과: (Day 3 기록)
- 판정: (Day 3 기록)

### 질문 3: 2만원 이하 평점 좋은 아이섀도우

- 검색어: 아이섀도우
- 사용할 field: category (정확 조건), price (범위), rating (정렬)
- filter: category = 아이섀도우, price ≤ 20000
- sort: rating 내림차순
- 기대 문서: category = 아이섀도우 + price ≤ 20000 상품, 평점 높은 순 정렬
- 제외 문서: price > 20000인 아이섀도우, 다른 카테고리 상품
- 0건 조건: 2만원 이하 아이섀도우가 데이터에 없는 경우 → 데이터 분포 확인 필요
- 판정 기준: 결과 전부 price ≤ 20000이고 rating 내림차순 정렬 확인
- 실제 결과: (Day 3 기록)
- 판정: (Day 3 기록)
