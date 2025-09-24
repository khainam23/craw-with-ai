# Property Crawler Package

## Cấu trúc Package

```
crawler/
├── __init__.py              # Export các class chính
├── config.py                # Cấu hình crawler
├── models.py                # Pydantic models và schema dữ liệu
├── image_extractor.py       # Xử lý extract hình ảnh
├── html_parser.py           # Parse HTML và extract dữ liệu
├── markdown_parser.py       # Parse markdown content
├── property_extractor.py    # Logic chính extract dữ liệu property
├── property_crawler.py      # Crawler chính
├── utils.py                 # Các utility functions
└── README.md               # Tài liệu này
```

## Các Module

### 1. `config.py`
- Chứa class `CrawlerConfig` với tất cả cấu hình cho crawler
- Browser config, run config, limits, patterns
- Cấu hình cho crawl4ai BrowserConfig và CrawlerRunConfig

### 2. `models.py`
- Định nghĩa Pydantic models: `PropertyModel`, `PropertyImage`
- Schema dữ liệu property với validation
- Cấu trúc dữ liệu chuẩn cho bất động sản

### 3. `image_extractor.py`
- Extract và categorize hình ảnh từ HTML
- Filter invalid images theo patterns và extensions
- Limit số lượng images theo config

### 4. `html_parser.py`
- Parse HTML content
- Extract rent, size, floor, year patterns
- Extract amenities và pricing info
- Extract building info và coordinates

### 5. `markdown_parser.py`
- Parse markdown content
- Extract address, station info
- Extract building type, dates, unit numbers

### 6. `property_extractor.py`
- Module chính `PropertyExtractor` orchestrate việc extract
- Sử dụng tất cả parsers khác
- Tạo comprehensive property data

### 7. `property_crawler.py`
- Class chính `EnhancedPropertyCrawler`
- Crawl single/multiple properties
- Save results to JSON/CSV

### 8. `utils.py`
- Class `PropertyUtils` và `FileUtils`
- Utility functions cho property processing
- File operations, validation và model creation

### 9. `custom_config.py` & `custom_rules.py`
- Custom extraction rules và hooks system
- **Tab Click Feature**: Tự động click tab selector để load thêm ảnh
- Coordinate conversion và custom data processing
- Xem `TAB_CLICK_GUIDE.md` để biết chi tiết về tính năng click tab

## Cách sử dụng

### Import package
```python
from crawler import EnhancedPropertyCrawler, PropertyExtractor, CrawlerConfig
from crawler import PropertyUtils, FileUtils
```

### Crawl single property
```python
import asyncio
from crawler import EnhancedPropertyCrawler

async def main():
    url = "https://example.com/property/123"
    crawler = EnhancedPropertyCrawler()
    result = await crawler.crawl_single_property(url)
    print(result)

asyncio.run(main())
```

### Crawl multiple properties
```python
import asyncio
from crawler import EnhancedPropertyCrawler

async def main():
    urls = ["url1", "url2", "url3"]
    crawler = EnhancedPropertyCrawler()
    results = await crawler.crawl_multiple_properties(urls)
    
    # Save results
    await crawler.save_results_to_json(results)
    await crawler.save_results_to_csv(results)

asyncio.run(main())
```

### Sử dụng PropertyExtractor riêng lẻ
```python
from crawler import PropertyExtractor
from crawler.models import PropertyModel

# Tạo extractor
extractor = PropertyExtractor()

# Extract từ HTML và markdown content
html_content = "<html>...</html>"
markdown_content = "# Property details..."
url = "https://example.com/property/123"

property_data = extractor.extract_property_data(html_content, markdown_content, url)
property_model = PropertyModel(**property_data)
```

### Sử dụng Utils
```python
from crawler import PropertyUtils, FileUtils

# Property utilities
property_utils = PropertyUtils()
validated_data = property_utils.validate_property_data(raw_data)

# File utilities  
file_utils = FileUtils()
file_utils.save_to_json(data, "output.json")
file_utils.save_to_csv(data, "output.csv")
```

## Tính năng Tab Click

### Mô tả
Tính năng Tab Click cho phép crawler tự động click vào tab selector trên website để load thêm ảnh và nội dung. Đặc biệt hữu ích cho các website có ảnh được load động qua JavaScript.

### Cách hoạt động
1. **Detection**: Tự động phát hiện tab selector `data-js-buildroom-slide-tab="exterior"`
2. **Click**: Thực thi JavaScript để click tab và chờ content load
3. **Extract**: Thu thập thêm ảnh từ content được load động

### Cấu hình
- **Tab selector**: `[data-js-buildroom-slide-tab="exterior"]`
- **Delay**: 3 giây sau click + 2 giây cho lazy images
- **Image category**: `exterior_tab`

### Test
```bash
python test/test_tab_click.py
```

### Chi tiết
Xem file `TAB_CLICK_GUIDE.md` để biết hướng dẫn chi tiết và customization.