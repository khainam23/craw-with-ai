# Hướng Dẫn Thêm/Xóa Trường Trong Dự Án Crawl Bất Động Sản

## Tổng Quan

Dự án này sử dụng Pydantic để định nghĩa cấu trúc dữ liệu bất động sản. Khi cần thêm hoặc xóa trường, bạn cần cập nhật ở 2 file chính:
- `models.py`: Định nghĩa cấu trúc dữ liệu
- `enhanced_crawler.py`: Logic crawl và extract dữ liệu

## 📋 Cấu Trúc Dự Án

```
d:\Learn\craw-data-by-ai\
├── models.py              # Định nghĩa PropertyModel và PropertyImage
├── enhanced_crawler.py    # Logic crawl và extract dữ liệu
├── requirements.txt       # Dependencies
└── FIELD_MANAGEMENT_GUIDE.md  # File này
```

## ➕ Cách Thêm Trường Mới

### Bước 1: Thêm Trường Vào PropertyModel

Mở file `models.py` và thêm trường mới vào class `PropertyModel`:

```python
# Ví dụ: Thêm trường thông tin về an ninh
security_system: Optional[Literal['Y', 'N']] = Field(None, description="Có hệ thống an ninh không? ('Y' hoặc 'N')")
security_camera: Optional[Literal['Y', 'N']] = Field(None, description="Có camera an ninh không? ('Y' hoặc 'N')")
security_guard: Optional[str] = Field(None, description="Thông tin về bảo vệ")

# Ví dụ: Thêm trường thông tin về môi trường
noise_level: Optional[str] = Field(None, description="Mức độ tiếng ồn (thấp/trung bình/cao)")
air_quality: Optional[str] = Field(None, description="Chất lượng không khí")
green_space_nearby: Optional[Literal['Y', 'N']] = Field(None, description="Có không gian xanh gần đó không? ('Y' hoặc 'N')")
```

### Bước 2: Cập Nhật Logic Extract Trong enhanced_crawler.py

Mở file `enhanced_crawler.py` và tìm method `_extract_comprehensive_data()`:

1. **Thêm trường vào extracted_data dictionary** (khoảng dòng 89-237):

```python
# Thêm vào phần khởi tạo extracted_data
extracted_data = {
    # ... các trường hiện tại ...
    
    # Thông tin an ninh (thêm mới)
    'security_system': None,
    'security_camera': None,
    'security_guard': None,
    
    # Thông tin môi trường (thêm mới)
    'noise_level': None,
    'air_quality': None,
    'green_space_nearby': None,
    
    # ... tiếp tục với các trường khác ...
}
```

2. **Thêm logic extract cho trường mới** trong các method extract:

```python
def _extract_from_html_patterns(self, html: str, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract dữ liệu từ HTML patterns
    """
    if not html:
        return extracted_data
    
    # ... logic hiện tại ...
    
    # Extract thông tin an ninh
    if re.search(r'セキュリティ|security|防犯', html, re.IGNORECASE):
        extracted_data['security_system'] = 'Y'
    
    if re.search(r'監視カメラ|security camera|防犯カメラ', html, re.IGNORECASE):
        extracted_data['security_camera'] = 'Y'
    
    # Extract thông tin môi trường
    noise_match = re.search(r'騒音レベル|noise level|静か|うるさい', html, re.IGNORECASE)
    if noise_match:
        # Logic để xác định mức độ tiếng ồn
        extracted_data['noise_level'] = 'low'  # hoặc logic phức tạp hơn
    
    return extracted_data
```

### Bước 3: Cập Nhật Schema Example (Tùy Chọn)

Trong `models.py`, cập nhật `schema_extra` example:

```python
schema_extra = {
    "example": {
        # ... các trường hiện tại ...
        "security_system": "Y",
        "security_camera": "Y",
        "noise_level": "low",
        "green_space_nearby": "Y"
    }
}
```

## ➖ Cách Xóa Trường

### Bước 1: Xóa Trường Khỏi PropertyModel

Mở file `models.py` và xóa/comment trường không cần thiết:

```python
# Ví dụ: Xóa trường không cần thiết
# bs: Optional[Literal['Y', 'N']] = Field(None, description="Có BS (vệ tinh phát sóng) không? ('Y' hoặc 'N')")
```

### Bước 2: Xóa Khỏi enhanced_crawler.py

1. **Xóa khỏi extracted_data dictionary**:

```python
extracted_data = {
    # ... các trường khác ...
    # 'bs': None,  # Xóa dòng này
}
```

2. **Xóa logic extract liên quan**:

```python
# Xóa hoặc comment các đoạn code extract cho trường đã xóa
# if re.search(r'BS|satellite', html, re.IGNORECASE):
#     extracted_data['bs'] = 'Y'
```

### Bước 3: Cập Nhật Schema Example

Xóa trường khỏi example trong `schema_extra`.

## 🔧 Các Loại Trường Thường Gặp

### 1. Trường Boolean (Y/N)
```python
field_name: Optional[Literal['Y', 'N']] = Field(None, description="Mô tả trường")
```

### 2. Trường Text
```python
field_name: Optional[str] = Field(None, description="Mô tả trường")
```

### 3. Trường Số
```python
field_name: Optional[str] = Field(None, description="Mô tả trường (lưu dưới dạng string)")
```

### 4. Trường Enum
```python
field_name: Optional[Literal['option1', 'option2', 'option3']] = Field(None, description="Mô tả trường")
```

## 🎯 Các Vị Trí Thêm Trường Theo Nhóm

### 1. Thông Tin Địa Chỉ (dòng 95-100)
```python
# Địa chỉ
'postcode': None,
'prefecture': None,
# Thêm trường mới ở đây
```

### 2. Thông Tin Tòa Nhà (dòng 102-116)
```python
# Thông tin tòa nhà
'building_type': None,
'year': None,
# Thêm trường mới ở đây
```

### 3. Tiện Ích Tòa Nhà (dòng 148-151)
```python
# Tiện ích tòa nhà
'autolock': None,
'credit_card': None,
# Thêm trường mới ở đây
```

### 4. Tiện Nghi Căn Hộ (dòng 216-229)
```python
# Tiện nghi căn hộ
'aircon': None,
'aircon_heater': None,
# Thêm trường mới ở đây
```

## 🧪 Testing Sau Khi Thay Đổi

### 1. Kiểm Tra Syntax
```bash
python -c "from models import PropertyModel; print('Models OK')"
```

### 2. Kiểm Tra Import
```bash
python -c "from enhanced_crawler import PropertyExtractor; print('Crawler OK')"
```

### 3. Test Với Dữ Liệu Mẫu
```python
from models import PropertyModel

# Test tạo model với trường mới
test_data = {
    'property_csv_id': 'TEST001',
    'security_system': 'Y',  # Trường mới
    'noise_level': 'low'     # Trường mới
}

try:
    property_obj = PropertyModel(**test_data)
    print("✅ Model validation passed")
    print(f"Security System: {property_obj.security_system}")
    print(f"Noise Level: {property_obj.noise_level}")
except Exception as e:
    print(f"❌ Model validation failed: {e}")
```

## 📝 Quy Tắc Đặt Tên Trường

### 1. Sử dụng snake_case
```python
# ✅ Đúng
security_system: Optional[str] = Field(...)

# ❌ Sai
securitySystem: Optional[str] = Field(...)
SecuritySystem: Optional[str] = Field(...)
```

### 2. Tên Trường Có Ý Nghĩa
```python
# ✅ Đúng
monthly_maintenance_fee: Optional[str] = Field(...)

# ❌ Sai
fee1: Optional[str] = Field(...)
```

### 3. Nhóm Trường Liên Quan
```python
# ✅ Đúng - nhóm theo chủ đề
security_system: Optional[str] = Field(...)
security_camera: Optional[str] = Field(...)
security_guard: Optional[str] = Field(...)
```

## 🚨 Lưu Ý Quan Trọng

### 1. Backup Trước Khi Thay Đổi
```bash
# Backup files quan trọng
copy models.py models.py.backup
copy enhanced_crawler.py enhanced_crawler.py.backup
```

### 2. Kiểm Tra Tương Thích Ngược
- Khi xóa trường, đảm bảo không có code nào khác đang sử dụng
- Khi thêm trường, đặt default value là `None`

### 3. Cập Nhật Documentation
- Cập nhật mô tả trong Field()
- Cập nhật example trong schema_extra
- Cập nhật README.md nếu cần

### 4. Performance Considerations
- Quá nhiều trường có thể làm chậm quá trình crawl
- Chỉ thêm trường thực sự cần thiết
- Xóa trường không sử dụng để tối ưu performance

## 🔍 Debugging

### 1. Kiểm Tra Trường Nào Được Extract
```python
# Thêm vào enhanced_crawler.py để debug
extracted_fields = [k for k, v in extracted_data.items() if v is not None]
print(f"🔍 Extracted {len(extracted_fields)} fields: {extracted_fields}")
```

### 2. Kiểm Tra Giá Trị Trường Cụ Thể
```python
# Debug trường cụ thể
if extracted_data.get('security_system'):
    print(f"🔒 Security System: {extracted_data['security_system']}")
```

## 📚 Ví Dụ Hoàn Chỉnh

### Thêm Nhóm Trường "Thông Tin Học Đường"

**1. Thêm vào models.py:**
```python
# Thông tin học đường
school_elementary_nearby: Optional[Literal['Y', 'N']] = Field(None, description="Có trường tiểu học gần đó không? ('Y' hoặc 'N')")
school_middle_nearby: Optional[Literal['Y', 'N']] = Field(None, description="Có trường trung học cơ sở gần đó không? ('Y' hoặc 'N')")
school_high_nearby: Optional[Literal['Y', 'N']] = Field(None, description="Có trường trung học phổ thông gần đó không? ('Y' hoặc 'N')")
school_university_nearby: Optional[Literal['Y', 'N']] = Field(None, description="Có trường đại học gần đó không? ('Y' hoặc 'N')")
school_distance_elementary: Optional[str] = Field(None, description="Khoảng cách đến trường tiểu học gần nhất (mét)")
```

**2. Thêm vào enhanced_crawler.py:**
```python
# Trong _extract_comprehensive_data()
extracted_data = {
    # ... các trường hiện tại ...
    
    # Thông tin học đường
    'school_elementary_nearby': None,
    'school_middle_nearby': None,
    'school_high_nearby': None,
    'school_university_nearby': None,
    'school_distance_elementary': None,
    
    # ... tiếp tục ...
}

# Trong _extract_from_html_patterns()
# Extract thông tin học đường
if re.search(r'小学校|elementary school|tiểu học', html, re.IGNORECASE):
    extracted_data['school_elementary_nearby'] = 'Y'

if re.search(r'中学校|middle school|trung học cơ sở', html, re.IGNORECASE):
    extracted_data['school_middle_nearby'] = 'Y'

# Extract khoảng cách
distance_match = re.search(r'小学校まで(\d+)m|elementary school (\d+)m', html, re.IGNORECASE)
if distance_match:
    distance = distance_match.group(1) or distance_match.group(2)
    extracted_data['school_distance_elementary'] = distance
```

**3. Cập nhật example:**
```python
schema_extra = {
    "example": {
        # ... các trường hiện tại ...
        "school_elementary_nearby": "Y",
        "school_distance_elementary": "300"
    }
}
```

---

## 🎉 Kết Luận

Việc thêm/xóa trường trong dự án này khá đơn giản nhưng cần thực hiện đồng bộ ở cả 2 file chính. Luôn nhớ:

1. ✅ Cập nhật `models.py` trước
2. ✅ Cập nhật `enhanced_crawler.py` sau
3. ✅ Test kỹ lưỡng trước khi deploy
4. ✅ Backup trước khi thay đổi
5. ✅ Đặt tên trường có ý nghĩa và nhất quán

Chúc bạn thành công trong việc mở rộng dự án! 🚀