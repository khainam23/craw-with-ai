# Craw Data By AI

Dùng AI crawl dữ liệu từ trang web bất động sản của Nhật Bản bất kỳ và phân tích theo cấu trúc định nghĩa.

## 🚀 Tính năng chính

- **AI-Powered Extraction**: Sử dụng AI của crawl4ai để extract dữ liệu thông minh
- **Structured Data**: Output JSON với 200+ fields theo PropertyModel
- **Multi-language Support**: Hỗ trợ tiếng Nhật, Anh, Việt
- **Smart Image Classification**: Tự động phân loại hình ảnh (exterior, interior, kitchen, etc.)
- **Transportation Info**: Extract thông tin 3 ga tàu gần nhất
- **Comprehensive Amenities**: Detect 50+ tiện nghi khác nhau
- **Batch Processing**: Crawl nhiều properties cùng lúc
- **Statistics & Reports**: Tạo báo cáo thống kê tự động

## 📁 Files

```
├── index.py              # File gốc đơn giản
├── models.py            # Pydantic models (200+ fields)
├── enhanced_crawler.py  # AI-powered crawler chính
├── demo.py             # Demo script với UI đẹp
├── requirements.txt    # Dependencies
└── README.md          # Hướng dẫn này
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

### 1. Demo nhanh
```bash
python demo.py
```

### 2. Sử dụng file gốc (đơn giản)
```bash
python index.py
```

### 3. Sử dụng enhanced crawler (AI)
```bash
python enhanced_crawler.py
```

### 4. Sử dụng trong code

```python
from enhanced_crawler import EnhancedPropertyCrawler
import asyncio

async def crawl_property():
    crawler = EnhancedPropertyCrawler()
    
    # Crawl một property
    result = await crawler.crawl_property('https://example.com/property/123')
    
    if result['success']:
        data = result['property_data']
        print(f"Tên tòa nhà: {data.get('building_name_ja')}")
        print(f"Tiền thuê: {data.get('monthly_rent')} yen")
        print(f"Diện tích: {data.get('size')} m²")
    
    # Lưu vào file JSON
    filename = crawler.save_results_to_file([result])
    print(f"Đã lưu: {filename}")

asyncio.run(crawl_property())
```

## 🏗️ PropertyModel Structure

PropertyModel bao gồm 200+ fields:

### Thông tin cơ bản
- `property_csv_id`: Mã định danh
- `link`: URL gốc  
- `building_name_ja/en/vi`: Tên tòa nhà đa ngôn ngữ
- `building_type`: Loại tòa nhà

### Địa chỉ
- `prefecture`: Tỉnh (東京都, 大阪府, etc.)
- `city`: Thành phố
- `district`: Quận/phường
- `chome_banchi`: Số nhà theo hệ thống Nhật

### Thông tin phòng
- `room_type`: Loại phòng (1K, 1DK, 2LDK, etc.)
- `size`: Diện tích (m²)
- `floor_no`: Số tầng
- `monthly_rent`: Tiền thuê/tháng
- `monthly_maintenance`: Phí quản lý

### Giao thông (3 ga gần nhất)
- `station_name_1/2/3`: Tên ga
- `train_line_name_1/2/3`: Tên tuyến
- `walk_1/2/3`: Thời gian đi bộ (phút)

### Tiện nghi (50+ items)
- `aircon`: Điều hòa (Y/N)
- `elevator`: Thang máy (Y/N)
- `autolock`: Khóa tự động (Y/N)
- `parking`: Chỗ đậu xe (Y/N)
- `internet_wifi`: WiFi (Y/N)
- ... và nhiều tiện nghi khác

### Hình ảnh
- `images`: Array với category và URL

### Tọa độ
- `map_lat`: Vĩ độ
- `map_lng`: Kinh độ

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

Crawler sử dụng AI để extract dữ liệu thông minh:

- **Provider**: Ollama/llama3.2 (local) hoặc OpenAI/Claude
- **Schema-based**: Extract theo cấu trúc PropertyModel
- **Smart Conversion**: Tự động chuyển đổi 万円 → yen, 坪 → m²
- **Context-aware**: Hiểu ngữ cảnh tiếng Nhật

### Thay đổi AI Provider

Trong `enhanced_crawler.py`:

```python
# Sử dụng OpenAI
extraction_strategy = LLMExtractionStrategy(
    provider="openai/gpt-4",
    api_token="your-api-key",
    # ...
)

# Sử dụng Claude
extraction_strategy = LLMExtractionStrategy(
    provider="anthropic/claude-3",
    api_token="your-api-key", 
    # ...
)
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
   - Kiểm tra crawl4ai-setup
   - Kiểm tra internet connection
   - Thử URL khác

2. **"AI provider error"**
   - Kiểm tra Ollama đã chạy: `ollama serve`
   - Hoặc thay đổi provider trong code

3. **"Timeout error"**
   - Tăng page_timeout trong config
   - Kiểm tra tốc độ mạng

### Debug mode:

```python
# Thêm vào enhanced_crawler.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🚨 Lưu ý quan trọng

1. **Rate Limiting**: Thêm delay giữa requests
2. **Legal Compliance**: Tuân thủ robots.txt và ToS
3. **Resource Usage**: AI extraction tốn tài nguyên
4. **Data Accuracy**: Luôn verify dữ liệu quan trọng

## 🎯 Roadmap

- [ ] Hỗ trợ thêm website bất động sản
- [ ] Cải thiện accuracy của AI extraction  
- [ ] Thêm export CSV/Excel
- [ ] Dashboard web interface
- [ ] Real-time monitoring
- [ ] Multi-threading optimization

## 🤝 Contributing

1. Fork repository
2. Create feature branch
3. Test thoroughly
4. Submit pull request

---

**Happy Crawling with AI! 🤖🏠**