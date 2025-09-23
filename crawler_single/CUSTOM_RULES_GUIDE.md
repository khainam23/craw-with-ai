# 🛠️ Custom Rules System - Hướng dẫn sử dụng

## 📋 Tổng quan

Custom Rules System cho phép bạn tự viết logic extraction mà không cần sửa code core. Hệ thống bao gồm:

- **Rules**: Logic để extract dữ liệu từ HTML
- **Hooks**: Xử lý trước và sau khi extract
- **Priority**: Thứ tự ưu tiên của rules

## 🚀 Cách sử dụng

### 1. File chính để chỉnh sửa

```
crawler_single/custom_config.py
```

Tất cả custom logic của bạn sẽ được viết trong file này.

### 2. Cấu trúc cơ bản

```python
def setup_custom_extractor() -> CustomExtractor:
    extractor = CustomExtractor()
    
    # Thêm rules
    extractor.add_rule(your_rule)
    
    # Thêm hooks
    extractor.add_pre_hook(your_pre_hook)
    extractor.add_post_hook(your_post_hook)
    
    return extractor
```

## 📝 Các loại Rules

### 1. CSS Selector Rule

```python
# Extract bằng CSS selector
extractor.add_rule(RuleBuilder.css_selector_rule(
    name="rent_price",           # Tên rule
    field="monthly_rent",        # Field trong data model
    selector=".price-value",     # CSS selector
    attribute="text",            # "text" hoặc attribute name
    priority=10                  # Số cao = chạy trước
))
```

### 2. Regex Rule

```python
# Extract bằng regex
extractor.add_rule(RuleBuilder.regex_rule(
    name="rent_regex",
    field="monthly_rent", 
    pattern=r'(\d+(?:,\d+)?)万円',  # Regex pattern với group
    group=1,                        # Group number để lấy
    priority=5
))
```

### 3. URL Condition Rule

```python
# Rule chỉ áp dụng cho URL cụ thể
def extract_special_data(html: str, data: Dict[str, Any]) -> str:
    # Logic extract của bạn
    return "extracted_value"

extractor.add_rule(RuleBuilder.url_condition_rule(
    name="special_site",
    field="special_field",
    url_pattern=r'special-site\.com',  # Regex cho URL
    extract_func=extract_special_data,
    priority=15
))
```

### 4. Custom Rule (Linh hoạt nhất)

```python
def my_condition(html: str, data: Dict[str, Any]) -> bool:
    # Return True nếu rule có thể áp dụng
    return "keyword" in html

def my_action(html: str, data: Dict[str, Any]) -> str:
    # Logic extract của bạn
    soup = BeautifulSoup(html, 'html.parser')
    element = soup.find('div', class_='my-class')
    return element.text if element else None

rule = ExtractionRule(
    name="my_custom_rule",
    field="my_field", 
    condition=my_condition,
    action=my_action,
    priority=8
)
extractor.add_rule(rule)
```

## 🔧 Hooks

### Pre-hook (Chạy trước extraction)

```python
def my_pre_hook(html: str, data: Dict[str, Any]) -> tuple:
    # Modify HTML hoặc data trước khi extract
    print("🔄 Pre-processing...")
    
    # Có thể clean HTML, thêm data, etc.
    cleaned_html = html.replace('unwanted', '')
    data['preprocessing_done'] = True
    
    return cleaned_html, data

extractor.add_pre_hook(my_pre_hook)
```

### Post-hook (Chạy sau extraction)

```python
def my_post_hook(data: Dict[str, Any]) -> Dict[str, Any]:
    # Transform data sau khi extract
    print("🔧 Post-processing...")
    
    # Tính toán thêm
    if 'monthly_rent' in data and data['monthly_rent']:
        rent = float(str(data['monthly_rent']).replace(',', ''))
        data['yearly_rent'] = str(int(rent * 12))
        data['total_cost'] = str(int(rent * 1.1))  # +10% phí
    
    return data

extractor.add_post_hook(my_post_hook)
```

## 🗺️ Ví dụ thực tế: Coordinate Conversion

Hệ thống hiện tại đã có sẵn tính năng convert tọa độ X,Y sang lat/lng:

```python
def convert_coordinates(data: Dict[str, Any]) -> Dict[str, Any]:
    html = data.get('_html', '')
    
    # Extract MAP_X và MAP_Y từ hidden inputs
    x_match = re.search(r'name="[^"]*MAP_X"[^>]*value="([^"]*)"', html, re.IGNORECASE)
    y_match = re.search(r'name="[^"]*MAP_Y"[^>]*value="([^"]*)"', html, re.IGNORECASE)
    
    if x_match and y_match:
        try:
            from utils.convert_gis import xy_to_latlon_tokyo
            
            x = float(x_match.group(1))
            y = float(y_match.group(1))
            
            # Convert tọa độ
            lat, lon = xy_to_latlon_tokyo(x, y, zone=9)
            
            data['map_lat'] = str(lat)
            data['map_lng'] = str(lon)
            
            print(f"🗺️ Converted: X={x}, Y={y} → Lat={lat:.6f}, Lng={lon:.6f}")
            
        except Exception as e:
            print(f"❌ Coordinate conversion error: {e}")
    
    return data
```

## 🎯 Ví dụ hoàn chỉnh

```python
def setup_custom_extractor() -> CustomExtractor:
    extractor = CustomExtractor()
    
    # 1. Extract giá thuê bằng CSS (ưu tiên cao)
    extractor.add_rule(RuleBuilder.css_selector_rule(
        name="rent_css",
        field="monthly_rent",
        selector=".price-display, .rent-value",
        priority=10
    ))
    
    # 2. Fallback regex nếu CSS không tìm thấy
    extractor.add_rule(RuleBuilder.regex_rule(
        name="rent_regex", 
        field="monthly_rent",
        pattern=r'(\d+(?:,\d+)?)万円',
        group=1,
        priority=5
    ))
    
    # 3. Extract diện tích cho site đặc biệt
    def extract_area_special(html: str, data: Dict[str, Any]) -> str:
        match = re.search(r'面積：(\d+\.?\d*)㎡', html)
        return match.group(1) if match else None
    
    extractor.add_rule(RuleBuilder.url_condition_rule(
        name="area_special_site",
        field="size",
        url_pattern=r'special-site\.com',
        extract_func=extract_area_special,
        priority=8
    ))
    
    # 4. Pre-hook để clean HTML
    def clean_html(html: str, data: Dict[str, Any]) -> tuple:
        # Remove ads, scripts, etc.
        cleaned = re.sub(r'<script.*?</script>', '', html, flags=re.DOTALL)
        cleaned = re.sub(r'<style.*?</style>', '', cleaned, flags=re.DOTALL)
        return cleaned, data
    
    # 5. Post-hook để tính toán thêm
    def calculate_extras(data: Dict[str, Any]) -> Dict[str, Any]:
        # Tính chi phí hàng năm
        if 'monthly_rent' in data and data['monthly_rent']:
            try:
                rent = float(str(data['monthly_rent']).replace(',', ''))
                data['yearly_rent'] = str(int(rent * 12))
                data['total_cost_with_fees'] = str(int(rent * 1.15))  # +15% phí
            except:
                pass
        
        # Format lại số điện thoại
        if 'contact_phone' in data and data['contact_phone']:
            phone = re.sub(r'[^\d]', '', data['contact_phone'])
            if len(phone) >= 10:
                data['contact_phone'] = f"{phone[:3]}-{phone[3:7]}-{phone[7:]}"
        
        return data
    
    extractor.add_pre_hook(clean_html)
    extractor.add_post_hook(calculate_extras)
    
    return extractor
```

## 🔍 Debug và Test

### 1. Xem log khi chạy

```bash
cd d:\Learn\craw-data-by-ai
python -m crawler_single.main
```

Bạn sẽ thấy:
```
✅ Applied rule 'rent_css' for field 'monthly_rent': 125000
🗺️ Converted: X=502813.183, Y=128669.157 → Lat=35.737000, Lng=139.654000
🔧 Post-processing...
```

### 2. Test rule riêng lẻ

```python
# Trong custom_config.py, thêm debug
def debug_rule(html: str, data: Dict[str, Any]) -> Dict[str, Any]:
    print(f"🐛 Current data: {list(data.keys())}")
    print(f"🐛 HTML length: {len(html)}")
    return data

extractor.add_post_hook(debug_rule)
```

## ⚠️ Lưu ý quan trọng

### 1. Priority Rules
- **Số cao = chạy trước**: Priority 10 chạy trước Priority 5
- **First match wins**: Rule đầu tiên thành công sẽ dừng, không thử rule khác cho cùng field

### 2. Error Handling
- Rules tự động catch exception, không crash hệ thống
- Nếu rule fail, sẽ thử rule tiếp theo (priority thấp hơn)

### 3. Performance
- Đừng viết regex quá phức tạp
- Sử dụng CSS selector khi có thể (nhanh hơn regex)
- Pre-hook có thể clean HTML để tăng tốc

### 4. Data Fields
- Sử dụng đúng tên field theo PropertyModel
- Có thể tạo field mới, nhưng cần update model nếu muốn lưu DB

## 🎨 Tips và Tricks

### 1. Multi-step Extraction

```python
def extract_complex_data(html: str, data: Dict[str, Any]) -> str:
    soup = BeautifulSoup(html, 'html.parser')
    
    # Step 1: Find container
    container = soup.find('div', class_='property-info')
    if not container:
        return None
    
    # Step 2: Extract from container
    price_elem = container.find('span', class_='price')
    return price_elem.text.strip() if price_elem else None
```

### 2. Conditional Logic

```python
def smart_extraction(html: str, data: Dict[str, Any]) -> str:
    # Thử nhiều cách khác nhau
    methods = [
        lambda: re.search(r'method1_pattern', html),
        lambda: re.search(r'method2_pattern', html),
        lambda: BeautifulSoup(html, 'html.parser').find('div', class_='fallback')
    ]
    
    for method in methods:
        try:
            result = method()
            if result:
                return result.group(1) if hasattr(result, 'group') else result.text
        except:
            continue
    
    return None
```

### 3. Data Validation

```python
def validate_and_clean(data: Dict[str, Any]) -> Dict[str, Any]:
    # Validate giá thuê
    if 'monthly_rent' in data:
        try:
            rent = float(str(data['monthly_rent']).replace(',', ''))
            if rent < 10000 or rent > 1000000:  # Reasonable range
                print(f"⚠️ Suspicious rent value: {rent}")
                del data['monthly_rent']
        except:
            del data['monthly_rent']
    
    # Clean phone number
    if 'contact_phone' in data:
        phone = re.sub(r'[^\d-]', '', data['contact_phone'])
        data['contact_phone'] = phone if len(phone) >= 10 else None
    
    return data

extractor.add_post_hook(validate_and_clean)
```

---

## 🚀 Bắt đầu ngay

1. Mở file `crawler_single/custom_config.py`
2. Uncomment và modify các example rules
3. Chạy crawler để test
4. Xem log và adjust theo nhu cầu

Happy crawling! 🕷️✨