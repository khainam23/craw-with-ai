# Hướng Dẫn Thêm/Xóa Trường - Property Crawler

## 📋 Cấu Trúc Files Cần Sửa

```
models.py                    # Pydantic models
crawler/data_schema.py       # Data structure & keywords  
crawler/html_parser.py       # HTML extraction logic
crawler/markdown_parser.py   # Markdown extraction logic
crawler/property_extractor.py # Main extraction orchestrator
```

## ➕ Thêm Trường Mới

### Bước 1: models.py
```python
# Thêm field vào PropertyModel
security_system: Optional[Literal['Y', 'N']] = Field(None, description="Có hệ thống an ninh không?")
```

### Bước 2: crawler/data_schema.py
```python
# Thêm vào get_empty_property_data()
return {
    # ... existing fields ...
    'security_system': None,
}

# Nếu là amenity, thêm keywords
AMENITY_KEYWORDS = {
    # ... existing keywords ...
    'security_system': ['セキュリティ', 'security', '防犯システム'],
}
```

### Bước 3: crawler/html_parser.py
```python
# Thêm method extract hoặc cập nhật existing method
def extract_security_from_html(self, html: str, property_data: Dict[str, Any]) -> Dict[str, Any]:
    if re.search(r'セキュリティ|security|防犯', html, re.IGNORECASE):
        property_data['security_system'] = 'Y'
    return property_data
```

### Bước 4: crawler/property_extractor.py
```python
# Gọi method extract mới
def extract_comprehensive_data(self, url: str, html_content: str, markdown_content: str) -> Dict[str, Any]:
    # ... existing code ...
    property_data = self.html_parser.extract_security_from_html(html_content, property_data)
    return property_data
```

## ➖ Xóa Trường

### Bước 1: models.py
```python
# Comment hoặc xóa field
# bs: Optional[Literal['Y', 'N']] = Field(None, description="...")
```

### Bước 2: crawler/data_schema.py
```python
# Xóa khỏi get_empty_property_data()
return {
    # 'bs': None,  # Xóa dòng này
}

# Xóa keywords (nếu có)
AMENITY_KEYWORDS = {
    # 'bs': ['BS', 'BS放送'],  # Xóa dòng này
}
```

### Bước 3: crawler/html_parser.py
```python
# Xóa logic extract
# if re.search(r'BS|satellite', html, re.IGNORECASE):
#     property_data['bs'] = 'Y'
```

### Bước 4: crawler/property_extractor.py
```python
# Xóa method call (nếu có)
# property_data = self.html_parser.extract_bs_from_html(html_content, property_data)
```

## 🧪 Test Nhanh

```bash
# Test syntax
python -c "from models import PropertyModel; print('✅ Models OK')"
python -c "from crawler import EnhancedPropertyCrawler; print('✅ Crawler OK')"

# Test data structure
python -c "from crawler.data_schema import PropertyDataSchema; data = PropertyDataSchema.get_empty_property_data('test'); print(f'✅ {len(data)} fields')"
```

## 🔧 Các Loại Trường Thường Dùng

```python
# Boolean Y/N
field_name: Optional[Literal['Y', 'N']] = Field(None, description="...")

# Text
field_name: Optional[str] = Field(None, description="...")

# Enum
field_name: Optional[Literal['option1', 'option2']] = Field(None, description="...")
```

## 🚨 Lưu Ý

- **Backup trước khi sửa**: `copy models.py models.py.backup`
- **Đặt tên**: Dùng `snake_case`, tên có ý nghĩa
- **Default value**: Luôn để `None`
- **Test kỹ**: Chạy test sau mỗi thay đổi

## � Vị Trí Thêm Theo Nhóm

**Địa chỉ**: Sau `'chome_banchi': None,`
**Tòa nhà**: Sau `'year': None,`
**Ga tàu**: Sau các station fields
**Tiện ích tòa nhà**: Sau `'ur': None,`
**Tiện nghi căn hộ**: Sau `'yard': None,`

---
*Cập nhật: Cấu trúc package crawler mới*