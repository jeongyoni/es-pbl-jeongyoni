import json
import random
from datetime import datetime, timedelta

SEED = 20260901
random.seed(SEED)

INDEX_NAME = "beauty-products"
DOC_COUNT = 1000
SAMPLE_COUNT = 30

categories = ['립틴트', '블러셔', '아이섀도우', '파운데이션', '쿠션', '립스틱']
brands = ['롬앤', '클리오', '에뛰드', '3CE', '맥', '라네즈', '토니모리', '미샤']
personal_colors = ['봄웜', '여쿨', '갈웜', '겨쿨']
skin_types = ['건성', '지성', '복합성', '민감성']
tags_pool = ['촉촉함', '발색', '지속력', '은은한발색', '매트', '글로시', '가성비', '데일리', '커버력', '선크림']

def random_date(start, end):
    delta = end - start
    return (start + timedelta(seconds=random.randint(0, int(delta.total_seconds())))).strftime('%Y-%m-%d')

start_date = datetime(2024, 1, 1)
end_date = datetime(2026, 8, 1)

docs = []
for i in range(1, DOC_COUNT + 1):
    product_id = f"P-{i:05d}"
    category = random.choice(categories)
    brand = random.choice(brands)
    doc = {
        "product_id": product_id,
        "product_name": f"{brand} {category} {i}",
        "brand": brand,
        "category": category,
        "personal_color": random.choice(personal_colors),
        "skin_type": random.choice(skin_types),
        "price": random.randint(5000, 45000),
        "rating": round(random.uniform(2.0, 5.0), 1),
        "review_count": random.randint(0, 10000),
        "tags": random.sample(tags_pool, random.randint(1, 4)),
        "release_date": random_date(start_date, end_date)
    }
    docs.append(doc)

# Bulk NDJSON 생성
bulk_path = 'generated/beauty-products-1000.ndjson'
with open(bulk_path, 'w', encoding='utf-8') as f:
    for doc in docs:
        f.write(json.dumps({"index": {"_index": INDEX_NAME, "_id": doc["product_id"]}}) + '\n')
        f.write(json.dumps(doc, ensure_ascii=False) + '\n')

# 샘플 30건
sample_path = 'generated/beauty-products-sample-30.ndjson'
with open(sample_path, 'w', encoding='utf-8') as f:
    for doc in docs[:SAMPLE_COUNT]:
        f.write(json.dumps({"index": {"_index": INDEX_NAME, "_id": doc["product_id"]}}) + '\n')
        f.write(json.dumps(doc, ensure_ascii=False) + '\n')

# 요약
summary = {
    "index": INDEX_NAME,
    "document_count": DOC_COUNT,
    "seed": SEED,
    "sample_count": SAMPLE_COUNT,
    "generated_at": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
}
with open('generated/generation-summary.json', 'w', encoding='utf-8') as f:
    json.dump(summary, f, ensure_ascii=False, indent=2)

print(f"생성 완료: {DOC_COUNT}건 → {bulk_path}")
print(f"샘플: {SAMPLE_COUNT}건 → {sample_path}")
