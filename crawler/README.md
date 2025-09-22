# Property Crawler Package

Đây là package được tách từ file `enhanced_crawler.py` gốc để tạo cấu trúc module rõ ràng, dễ đọc, dễ bảo trì và có thể mở rộng.

## Cấu trúc Package

```
crawler/
├── __init__.py              # Export các class chính
├── config.py                # Cấu hình crawler
├── data_schema.py           # Schema và cấu trúc dữ liệu
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
- Chứa tất cả cấu hình cho crawler
- Browser config, run config, limits, patterns

### 2. `data_schema.py`
- Định nghĩa schema dữ liệu property
- Keywords cho amenities detection
- Cấu trúc dữ liệu chuẩn

### 3. `image_extractor.py`
- Extract và categorize hình ảnh từ HTML
- Filter invalid images
- Limit số lượng images

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
- Module chính orchestrate việc extract
- Sử dụng tất cả parsers khác
- Tạo comprehensive property data

### 7. `property_crawler.py`
- Class chính EnhancedPropertyCrawler
- Crawl single/multiple properties
- Save results to JSON/CSV

### 8. `utils.py`
- Utility functions cho property processing
- File operations
- Validation và model creation

## Cách sử dụng

### Import package
```python
from crawler import EnhancedPropertyCrawler, crawl_single_property
```

### Crawl single property
```python
import asyncio
from crawler import crawl_single_property

async def main():
    url = "https://example.com/property/123"
    result = await crawl_single_property(url)
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
    crawler.save_results_to_json(results)
    crawler.save_results_to_csv(results)

asyncio.run(main())
```