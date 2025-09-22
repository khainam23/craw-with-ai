# Craw Data By AI

Hệ thống AI-powered crawler chuyên nghiệp để crawl và phân tích dữ liệu bất động sản Nhật Bản với cấu trúc dữ liệu chuẩn hóa và khả năng mở rộng cao.

## 🚀 Tính năng chính

- **AI-Powered Extraction**: Sử dụng AI của crawl4ai để extract dữ liệu thông minh
- **Structured Data**: Output JSON/CSV với 200+ fields theo PropertyModel chuẩn
- **Multi-language Support**: Hỗ trợ tiếng Nhật, Anh, Việt, Trung (CN/TW)
- **Smart Image Classification**: Tự động phân loại hình ảnh (exterior, interior, kitchen, etc.)
- **Transportation Info**: Extract thông tin 5 ga tàu gần nhất với đầy đủ phương tiện
- **Comprehensive Amenities**: Detect 50+ tiện nghi và đặc điểm căn hộ
- **Modular Architecture**: Cấu trúc package rõ ràng, dễ bảo trì và mở rộng
- **Batch Processing**: Crawl nhiều properties cùng lúc với hiệu suất cao
- **Statistics & Reports**: Tạo báo cáo thống kê tự động

## 📁 Cấu trúc dự án

```
├── crawler/                    # Package crawler chính
│   ├── __init__.py            # Export các class chính
│   ├── config.py              # Cấu hình crawler
│   ├── data_schema.py         # Schema và cấu trúc dữ liệu
│   ├── html_parser.py         # Parse HTML và extract dữ liệu
│   ├── markdown_parser.py     # Parse markdown content
│   ├── image_extractor.py     # Xử lý extract hình ảnh
│   ├── property_extractor.py  # Logic chính extract dữ liệu property
│   ├── property_crawler.py    # Crawler chính
│   ├── utils.py               # Các utility functions
│   └── README.md              # Tài liệu package
├── index.py                   # File demo đơn giản
├── models.py                  # Pydantic models (200+ fields)
├── requirements.txt           # Dependencies
├── structure.json             # Mô tả chi tiết 200+ fields
├── FIELD_MANAGEMENT_GUIDE.md  # Hướng dẫn thêm/xóa trường
└── README.md                  # Hướng dẫn này
```

## 🛠️ Cài đặt

### 1. Tạo môi trường Python 3.10
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# hoặc
source venv/bin/activate  # Linux/Mac
```

### 2. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### 3. Thiết lập crawl4ai
```bash
crawl4ai-setup
```

### 4. Kiểm tra thiết lập
```bash
crawl4ai-doctor
```

## 🎯 Cách sử dụng

### 1. Demo nhanh (file đơn giản)
```bash
python index.py
```

### 2. Sử dụng package crawler (khuyến nghị)

#### Crawl
```python
import asyncio
from crawler import EnhancedPropertyCrawler

async def main():
    urls = [
        "https://example.com/property/123",
        "https://example.com/property/456",
        "https://example.com/property/789"
    ]
    
    crawler = EnhancedPropertyCrawler()
    results = await crawler.crawl_multiple_properties(urls)
    
    # Lưu kết quả
    json_file = crawler.save_results_to_json(results)
    csv_file = crawler.save_results_to_csv(results)
    
    print(f"Đã lưu JSON: {json_file}")
    print(f"Đã lưu CSV: {csv_file}")

asyncio.run(main())
```

### 3. Import trực tiếp các module
```python
from crawler import EnhancedPropertyCrawler, PropertyExtractor
from crawler.config import CrawlerConfig
from crawler.utils import create_property_model
```

## 🏗️ PropertyModel Structure (200+ Fields)

Hệ thống sử dụng cấu trúc dữ liệu chuẩn hóa với 200+ trường dữ liệu được phân nhóm rõ ràng:

### 📍 Thông tin địa chỉ
- `postcode`: Mã bưu điện
- `prefecture`: Tỉnh (東京都, 大阪府, etc.)
- `city`: Thành phố
- `district`: Quận/phường
- `chome_banchi`: Số khối và lô (hệ thống địa chỉ Nhật)

### 🏢 Thông tin tòa nhà
- `building_name_ja/en/zh_CN/zh_TW`: Tên tòa nhà đa ngôn ngữ
- `building_type`: Loại tòa nhà (chung cư, nhà riêng)
- `building_description_*`: Mô tả tòa nhà đa ngôn ngữ
- `year`: Năm xây dựng
- `floors`: Số tầng
- `num_units`: Số căn hộ trong tòa nhà
- `structure`: Loại cấu trúc (thép, gỗ, khác)

### 🏠 Thông tin căn hộ
- `room_type`: Loại phòng (1K, 1DK, 2LDK, etc.)
- `size`: Diện tích (m²)
- `floor_no`: Số tầng của căn hộ
- `unit_no`: Số căn hộ
- `balcony_size`: Diện tích ban công

### 💰 Thông tin tài chính
- `monthly_rent`: Tiền thuê hàng tháng
- `monthly_maintenance`: Phí bảo trì hàng tháng
- `months_deposit/numeric_deposit`: Tiền đặt cọc
- `months_key/numeric_key`: Tiền chìa khóa
- `fire_insurance`: Phí bảo hiểm cháy nổ
- `other_initial_fees`: Các phí ban đầu khác

### 🚇 Giao thông (5 ga gần nhất)
- `station_name_1/2/3/4/5`: Tên ga tàu
- `train_line_name_1/2/3/4/5`: Tên tuyến tàu
- `walk_1/2/3/4/5`: Thời gian đi bộ (phút)
- `bus_1/2/3/4/5`: Thời gian đi xe buýt (phút)
- `car_1/2/3/4/5`: Thời gian đi ô tô (phút)
- `cycle_1/2/3/4/5`: Thời gian đi xe đạp (phút)

### 🏢 Tiện ích tòa nhà
- `autolock`: Khóa tự động (Y/N)
- `elevator`: Thang máy (Y/N)
- `parking`: Chỗ đậu xe (Y/N)
- `bicycle_parking`: Chỗ đậu xe đạp (Y/N)
- `delivery_box`: Hộp giao hàng (Y/N)
- `concierge`: Dịch vụ lễ tân (Y/N)
- `gym`: Phòng tập thể dục (Y/N)
- `swimming_pool`: Hồ bơi (Y/N)

### 🏠 Tiện nghi căn hộ (50+ items)
- `aircon`: Điều hòa không khí (Y/N)
- `internet_wifi`: WiFi (Y/N)
- `system_kitchen`: Bếp hệ thống (Y/N)
- `washer_dryer`: Máy giặt/sấy (Y/N)
- `bath`: Bồn tắm (Y/N)
- `separate_toilet`: Toilet riêng biệt (Y/N)
- `balcony`: Ban công (Y/N)
- `storage`: Kho chứa (Y/N)
- ... và 40+ tiện nghi khác

### 🧭 Hướng căn hộ
- `facing_north/south/east/west`: Hướng bắc/nam/đông/tây (Y/N)
- `facing_northeast/southeast/southwest/northwest`: Hướng chéo (Y/N)

### 📸 Hình ảnh (16 slots)
- `image_category_1-16`: Danh mục hình ảnh
- `image_url_1-16`: URL hình ảnh

### 📍 Tọa độ & Links
- `map_lat`: Vĩ độ
- `map_lng`: Kinh độ
- `youtube`: Link video YouTube
- `vr_link`: Link tour thực tế ảo

> **Chi tiết đầy đủ**: Xem file `structure.json` để biết mô tả chi tiết tất cả 200+ trường dữ liệu

## 📊 Sample Output

```json
{
  "success": true,
  "url": "https://example.com/property/123",
  "property_data": {
    "property_csv_id": "PROP_123",
    "building_name_ja": "サンプルマンション",
    "building_type": "Apartment",
    "prefecture": "東京都",
    "city": "渋谷区",
    "room_type": "1K",
    "size": 25.5,
    "monthly_rent": 120000,
    "station_name_1": "渋谷駅",
    "train_line_name_1": "JR山手線",
    "walk_1": 5,
    "aircon": "Y",
    "elevator": "Y",
    "images": [
      {
        "category": "exterior",
        "url": "https://example.com/image1.jpg"
      }
    ],
    "map_lat": 35.6762,
    "map_lng": 139.6503
  }
}
```

## 🤖 AI Configuration

Hệ thống sử dụng AI để extract dữ liệu thông minh với các tính năng:

- **Schema-based**: Extract theo cấu trúc PropertyModel chuẩn
- **Smart Conversion**: Tự động chuyển đổi 万円 → yen, 坪 → m²
- **Context-aware**: Hiểu ngữ cảnh tiếng Nhật và đa ngôn ngữ
- **Modular Processing**: Tách biệt HTML parser và Markdown parser

### Cấu hình AI Provider

Trong `crawler/config.py`:

```python
# Cấu hình mặc định (Ollama local)
CRAWLER_CONFIG = {
    "ai_provider": "ollama/llama3.2",
    "api_token": None,  # Không cần token cho Ollama
    # ...
}

# Sử dụng OpenAI
CRAWLER_CONFIG = {
    "ai_provider": "openai/gpt-4",
    "api_token": "your-openai-api-key",
    # ...
}

# Sử dụng Claude
CRAWLER_CONFIG = {
    "ai_provider": "anthropic/claude-3",
    "api_token": "your-anthropic-api-key",
    # ...
}
```

## 📈 Statistics & Reports

Tự động tạo báo cáo thống kê:

```json
{
  "summary": {
    "total_properties": 100,
    "successful_crawls": 95,
    "success_rate": "95.0%"
  },
  "statistics": {
    "building_types": {"Apartment": 80, "House": 15},
    "prefectures": {"東京都": 60, "大阪府": 25},
    "price_ranges": {"50k_100k": 40, "100k_200k": 35},
    "amenities": {"aircon": 90, "elevator": 75}
  }
}
```

## 🔧 Troubleshooting

### Lỗi thường gặp:

1. **"Failed to extract content"**
   - Kiểm tra crawl4ai-setup: `crawl4ai-setup`
   - Kiểm tra internet connection
   - Thử URL khác

2. **"AI provider error"**
   - Kiểm tra Ollama đã chạy: `ollama serve`
   - Hoặc thay đổi provider trong `crawler/config.py`

3. **"Timeout error"**
   - Tăng page_timeout trong `crawler/config.py`
   - Kiểm tra tốc độ mạng

4. **"Import error"**
   - Kiểm tra package đã cài đúng: `pip install -r requirements.txt`
   - Kiểm tra Python path

### Debug mode:

```python
# Thêm vào script của bạn
import logging
logging.basicConfig(level=logging.DEBUG)

# Hoặc sử dụng config debug
from crawler.config import CrawlerConfig
config = CrawlerConfig()
config.debug = True
```

### Kiểm tra cấu trúc package:

```bash
# Test syntax
python -c "from models import PropertyModel; print('✅ Models OK')"
python -c "from crawler import EnhancedPropertyCrawler; print('✅ Crawler OK')"

# Test data structure  
python -c "from crawler.data_schema import PropertyDataSchema; data = PropertyDataSchema.get_empty_property_data('test'); print(f'✅ {len(data)} fields')"
```

## 🚨 Lưu ý quan trọng

1. **Rate Limiting**: Thêm delay giữa requests
2. **Legal Compliance**: Tuân thủ robots.txt và ToS
3. **Resource Usage**: AI extraction tốn tài nguyên
4. **Data Accuracy**: Luôn verify dữ liệu quan trọng

## 🎯 Roadmap

- [x] ✅ Cấu trúc package modular
- [x] ✅ Hỗ trợ 200+ fields chuẩn hóa
- [x] ✅ Export JSON/CSV
- [x] ✅ Multi-language support (4 ngôn ngữ)
- [x] ✅ Comprehensive field management guide
- [ ] 🔄 Dashboard web interface
- [ ] 🔄 Real-time monitoring
- [ ] 🔄 Multi-threading optimization
- [ ] 🔄 Hỗ trợ thêm website bất động sản
- [ ] 🔄 API REST endpoints
- [ ] 🔄 Docker containerization

## 📚 Tài liệu bổ sung

- **[FIELD_MANAGEMENT_GUIDE.md](FIELD_MANAGEMENT_GUIDE.md)**: Hướng dẫn thêm/xóa trường dữ liệu
- **[crawler/README.md](crawler/README.md)**: Tài liệu chi tiết về package crawler
- **[structure.json](structure.json)**: Mô tả đầy đủ 200+ fields
- **[models.py](models.py)**: Pydantic models definition

---