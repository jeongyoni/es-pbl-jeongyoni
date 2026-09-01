# 메모장에서 '=' 오른쪽 값과 field 규칙만 자신의 주제에 맞게 바꿉니다.
# 이 파일은 생성기가 읽는 PowerShell 변수 설정입니다. 제공된 형식을 유지하고 값과 규칙만 수정합니다.

$IndexName = 'beauty-products'
$DocumentCount = 1000
$Seed = 20260901
$IdPrefix = 'P'
$IdField = 'product_id'
$SampleCount = 30

# choice와 tags 규칙이 참조하는 도메인별 후보 목록입니다.
$Vocabularies = [ordered]@{
  categories     = @('립틴트', '블러셔', '아이섀도우', '파운데이션', '쿠션', '립스틱')
  brands         = @('롬앤', '클리오', '에뛰드', '3CE', '맥', '라네즈', '토니모리', '미샤')
  personal_colors = @('봄웜', '여쿨', '갈웜', '겨쿨')
  skin_types     = @('건성', '지성', '복합성', '민감성')
  tags           = @('촉촉함', '발색', '지속력', '은은한발색', '매트', '글로시', '가성비', '데일리', '커버력', '선크림')
}

# 문서는 위에서 아래 순서로 만들어집니다.
$FieldRules = @(
  @{ Name = 'product_id';    Kind = 'id';              Digits = 5 }
  @{ Name = 'category';      Kind = 'choice';           Source = 'categories' }
  @{ Name = 'brand';         Kind = 'choice';           Source = 'brands' }
  @{ Name = 'personal_color'; Kind = 'choice';          Source = 'personal_colors' }
  @{ Name = 'skin_type';     Kind = 'choice';           Source = 'skin_types' }
  @{ Name = 'price';         Kind = 'integer';          Min = 5000;  Max = 45000 }
  @{ Name = 'rating';        Kind = 'decimal';          Min = 2.0;   Max = 5.0; Digits = 1 }
  @{ Name = 'review_count';  Kind = 'integer';          Min = 0;     Max = 10000 }
  @{ Name = 'product_name';  Kind = 'template';         Template = '{{brand}} {{category}} {{sequence}}' }
  @{ Name = 'tags';          Kind = 'tags';             Source = 'tags'; MinItems = 1; MaxItems = 4 }
  @{ Name = 'release_date';  Kind = 'date';             Start = '2024-01-01T00:00:00Z'; End = '2026-08-01T00:00:00Z' }
)
