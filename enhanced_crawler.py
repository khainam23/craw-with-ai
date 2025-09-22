"""
Enhanced Property Crawler sử dụng crawl4ai (không cần LLM)
Tận dụng sức mạnh của crawl4ai để crawl dữ liệu bất động sản
"""

import asyncio
import json
import re
from datetime import datetime
from typing import Dict, List, Optional, Any
from crawl4ai import AsyncWebCrawler
from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig
from models import PropertyModel, PropertyImage
import time as t


class PropertyExtractor:
    """
    Sử dụng crawl4ai để extract dữ liệu bất động sản (không cần LLM)
    """
    
    def __init__(self):
        self.browser_config = BrowserConfig(
            headless=True,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        )
    
    async def extract_property_data(self, url: str) -> Dict[str, Any]:
        """
        Extract dữ liệu bất động sản từ URL với đầy đủ thông tin theo PropertyModel
        """
        # Cấu hình crawler để lấy đầy đủ thông tin
        run_config = CrawlerRunConfig(
            wait_for_images=True,
            delay_before_return_html=3.0,
            page_timeout=45000,
            remove_overlay_elements=True,
            screenshot=True
        )
        
        try:
            async with AsyncWebCrawler(config=self.browser_config) as crawler:
                result = await crawler.arun(
                    url=url,
                    config=run_config
                )
                
                if result.success:
                    # Extract comprehensive property data
                    extracted_data = self._extract_comprehensive_data(url, result)
                    
                    print(f"✅ Successfully crawled: {url}")
                    print(f"🔍 Title: {extracted_data.get('building_name_ja', 'N/A')}")
                    print(f"🔍 Extracted {len([k for k, v in extracted_data.items() if v is not None])} fields with data")
                    
                    return {
                        'success': True,
                        'url': url,
                        'property_data': extracted_data,
                        'crawl_timestamp': datetime.now().isoformat(),
                        'raw_html_length': len(result.html) if result.html else 0,
                        'metadata': {
                            'title': result.metadata.get('title', ''),
                            'description': result.metadata.get('description', ''),
                            'keywords': result.metadata.get('keywords', '')
                        }
                    }
                else:
                    return {
                        'success': False,
                        'url': url,
                        'error': result.error_message or 'Failed to extract content',
                        'crawl_timestamp': datetime.now().isoformat()
                    }
                    
        except Exception as e:
            return {
                'success': False,
                'url': url,
                'error': str(e),
                'crawl_timestamp': datetime.now().isoformat()
            }
    
    def _extract_comprehensive_data(self, url: str, result) -> Dict[str, Any]:
        """
        Extract comprehensive property data từ crawl result
        """
        # Khởi tạo data structure với tất cả fields từ PropertyModel
        extracted_data = {
            # Thông tin cơ bản
            'link': url,
            'property_csv_id': self._generate_property_id(url),
            'create_date': datetime.now().isoformat(),
            
            # Địa chỉ
            'postcode': None,
            'prefecture': None,
            'city': None,
            'district': None,
            'chome_banchi': None,
            
            # Thông tin tòa nhà
            'building_type': None,
            'year': None,
            
            # Tên tòa nhà đa ngôn ngữ
            'building_name_en': None,
            'building_name_ja': None,
            'building_name_vi': None,
            
            # Mô tả tòa nhà đa ngôn ngữ
            'building_description_en': None,
            'building_description_ja': None,
            'building_description_vi': None,
            
            # Địa danh gần đó đa ngôn ngữ
            'building_landmarks_en': None,
            'building_landmarks_ja': None,
            'building_landmarks_vi': None,
            
            # Thông tin ga tàu (5 ga)
            'station_name_1': None, 'train_line_name_1': None, 'walk_1': None, 'bus_1': None, 'car_1': None, 'cycle_1': None,
            'station_name_2': None, 'train_line_name_2': None, 'walk_2': None, 'bus_2': None, 'car_2': None, 'cycle_2': None,
            'station_name_3': None, 'train_line_name_3': None, 'walk_3': None, 'bus_3': None, 'car_3': None, 'cycle_3': None,
            'station_name_4': None, 'train_line_name_4': None, 'walk_4': None, 'bus_4': None, 'car_4': None, 'cycle_4': None,
            'station_name_5': None, 'train_line_name_5': None, 'walk_5': None, 'bus_5': None, 'car_5': None, 'cycle_5': None,
            
            # Tọa độ địa lý
            'map_lat': None,
            'map_lng': None,
            
            # Thông tin cấu trúc tòa nhà
            'num_units': None,
            'floors': None,
            'basement_floors': None,
            
            # Thông tin đậu xe
            'parking': None,
            'parking_cost': None,
            'bicycle_parking': None,
            'motorcycle_parking': None,
            
            # Thông tin cấu trúc và phong cách
            'structure': None,
            'building_notes': None,
            'building_style': None,
            
            # Tiện ích tòa nhà
            'autolock': None, 'credit_card': None, 'concierge': None, 'delivery_box': None,
            'elevator': None, 'gym': None, 'newly_built': None, 'pets': None,
            'swimming_pool': None, 'ur': None,
            
            # Thông tin căn hộ
            'room_type': None,
            'size': None,
            'unit_no': None,
            'ad_type': None,
            'available_from': None,
            
            # Mô tả bất động sản đa ngôn ngữ
            'property_description_en': None,
            'property_description_ja': None,
            'property_description_vi': None,
            
            # Chi phí khác đa ngôn ngữ
            'property_other_expenses_en': None,
            'property_other_expenses_ja': None,
            'property_other_expenses_vi': None,
            
            # Loại nổi bật
            'featured_a': None, 'featured_b': None, 'featured_c': None,
            
            # Thông tin tầng và giá thuê
            'floor_no': None,
            'monthly_rent': None,
            'monthly_maintenance': None,
            
            # Các khoản phí
            'months_deposit': None, 'numeric_deposit': None,
            'months_key': None, 'numeric_key': None,
            'months_guarantor': None, 'numeric_guarantor': None,
            'months_agency': None, 'numeric_agency': None,
            'months_renewal': None, 'numeric_renewal': None,
            'months_deposit_amortization': None, 'numeric_deposit_amortization': None,
            'months_security_deposit': None, 'numeric_security_deposit': None,
            
            # Các phí khác
            'lock_exchange': None,
            'fire_insurance': None,
            'other_initial_fees': None,
            'other_subscription_fees': None,
            
            # Thông tin bảo lãnh
            'no_guarantor': None,
            'guarantor_agency': None,
            'guarantor_agency_name': None,
            'numeric_guarantor_max': None,
            
            # Thông tin thuê
            'rent_negotiable': None,
            'renewal_new_rent': None,
            'lease_date': None,
            'lease_months': None,
            'lease_type': None,
            'short_term_ok': None,
            
            # Thông tin ban công và ghi chú
            'balcony_size': None,
            'property_notes': None,
            'discount': None,
            
            # Hướng căn hộ
            'facing_north': None, 'facing_northeast': None, 'facing_east': None, 'facing_southeast': None,
            'facing_south': None, 'facing_southwest': None, 'facing_west': None, 'facing_northwest': None,
            
            # Tiện nghi căn hộ (rất nhiều)
            'aircon': None, 'aircon_heater': None, 'all_electric': None, 'auto_fill_bath': None,
            'balcony': None, 'bath': None, 'bath_water_heater': None, 'blinds': None,
            'bs': None, 'cable': None, 'carpet': None, 'cleaning_service': None,
            'counter_kitchen': None, 'dishwasher': None, 'drapes': None, 'female_only': None,
            'fireplace': None, 'flooring': None, 'full_kitchen': None, 'furnished': None,
            'gas': None, 'induction_cooker': None, 'internet_broadband': None, 'internet_wifi': None,
            'japanese_toilet': None, 'linen': None, 'loft': None, 'microwave': None,
            'oven': None, 'phoneline': None, 'range': None, 'refrigerator': None,
            'refrigerator_freezer': None, 'roof_balcony': None, 'separate_toilet': None, 'shower': None,
            'soho': None, 'storage': None, 'student_friendly': None, 'system_kitchen': None,
            'tatami': None, 'underfloor_heating': None, 'unit_bath': None, 'utensils_cutlery': None,
            'veranda': None, 'washer_dryer': None, 'washing_machine': None, 'washlet': None,
            'western_toilet': None, 'yard': None,
            
            # Media links
            'youtube': None,
            'vr_link': None,
            
            # Hình ảnh
            'images': []
        }
        
        # Extract data từ HTML content
        html_content = result.html if result.html else ""
        markdown_content = result.markdown if result.markdown else ""
        
        # Extract basic info từ metadata
        metadata = result.metadata or {}
        title = metadata.get('title', '')
        description = metadata.get('description', '')
        
        # Set building name từ title
        if title:
            extracted_data['building_name_ja'] = title
            extracted_data['building_name_en'] = title  # Có thể translate sau
        
        # Set description
        if description:
            extracted_data['property_description_ja'] = description
            extracted_data['property_description_en'] = description  # Có thể translate sau
        
        # Extract images từ HTML content
        images = self._extract_images_from_html(html_content)
        extracted_data['images'] = images
        
        # Extract structured data từ HTML patterns
        extracted_data = self._extract_from_html_patterns(html_content, extracted_data)
        
        # Extract từ markdown content
        extracted_data = self._extract_from_markdown(markdown_content, extracted_data)
        
        return extracted_data
    
    def _extract_images_from_html(self, html: str) -> List[Dict[str, str]]:
        """
        Extract images từ HTML content
        """
        if not html:
            return []
        
        images = []
        
        # Extract img tags with src attributes
        img_patterns = [
            r'<img[^>]+src=["\']([^"\']+)["\'][^>]*alt=["\']([^"\']*)["\'][^>]*>',
            r'<img[^>]+alt=["\']([^"\']*)["\'][^>]*src=["\']([^"\']+)["\'][^>]*>',
            r'<img[^>]+src=["\']([^"\']+)["\'][^>]*>'
        ]
        
        for pattern in img_patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    if len(match) == 2:
                        # Pattern with both src and alt
                        if 'src=' in pattern and pattern.index('src=') < pattern.index('alt='):
                            src, alt = match
                        else:
                            alt, src = match
                    else:
                        src = match[0]
                        alt = ""
                else:
                    src = match
                    alt = ""
                
                # Filter out small icons and invalid URLs
                if (src and 
                    not any(skip in src.lower() for skip in ['icon', 'logo', 'button', 'arrow']) and
                    (src.startswith('http') or src.startswith('/')) and
                    any(ext in src.lower() for ext in ['.jpg', '.jpeg', '.png', '.webp', '.gif'])):
                    
                    # Make relative URLs absolute
                    if src.startswith('/'):
                        # Extract domain from the current URL if needed
                        src = src  # Keep as is for now, can be enhanced later
                    
                    image_data = {
                        'url': src,
                        'category': self._categorize_image(alt, len(images))
                    }
                    images.append(image_data)
                    
                    # Limit to 20 images
                    if len(images) >= 20:
                        break
            
            if len(images) >= 20:
                break
        
        return images
    
    def _categorize_image(self, alt_text: str, index: int) -> str:
        """
        Categorize image dựa trên alt text hoặc index
        """
        alt_lower = alt_text.lower() if alt_text else ""
        
        # Japanese keywords for categorization
        if any(word in alt_lower for word in ['exterior', 'outside', 'building', 'facade', '外観', '建物']):
            return 'exterior'
        elif any(word in alt_lower for word in ['interior', 'room', 'living', 'bedroom', '室内', '部屋', 'リビング']):
            return 'interior'
        elif any(word in alt_lower for word in ['kitchen', 'dining', 'キッチン', '台所']):
            return 'kitchen'
        elif any(word in alt_lower for word in ['bathroom', 'bath', 'toilet', 'バス', 'トイレ', '浴室']):
            return 'bathroom'
        elif any(word in alt_lower for word in ['balcony', 'terrace', 'veranda', 'バルコニー', 'ベランダ']):
            return 'balcony'
        else:
            # Default categorization based on index
            categories = ['exterior', 'interior', 'kitchen', 'bathroom', 'balcony', 'other']
            return categories[index % len(categories)]
    
    def _extract_from_html_patterns(self, html: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract data từ HTML patterns (regex-based)
        """
        if not html:
            return data
        
        # Extract rent price patterns
        rent_patterns = [
            r'¥([\d,]+)',
            r'(\d+)万円',
            r'(\d+),(\d+)円'
        ]
        
        for pattern in rent_patterns:
            matches = re.findall(pattern, html)
            if matches:
                try:
                    if isinstance(matches[0], tuple):
                        # Handle comma-separated numbers
                        rent_value = ''.join(matches[0])
                    else:
                        rent_value = matches[0].replace(',', '')
                    data['monthly_rent'] = rent_value
                    break
                except:
                    continue
        
        # Extract room type patterns
        room_patterns = [
            r'(\d+[LDKS]+)',
            r'(\d+K)',
            r'(\d+DK)',
            r'(\d+LDK)'
        ]
        
        for pattern in room_patterns:
            matches = re.findall(pattern, html)
            if matches:
                data['room_type'] = matches[0]
                break
        
        # Extract size patterns
        size_patterns = [
            r'(\d+\.?\d*)㎡',
            r'(\d+\.?\d*)m²',
            r'(\d+\.?\d*)\s*平米'
        ]
        
        for pattern in size_patterns:
            matches = re.findall(pattern, html)
            if matches:
                data['size'] = matches[0]
                break
        
        # Extract floor patterns
        floor_patterns = [
            r'(\d+)階',
            r'(\d+)F'
        ]
        
        for pattern in floor_patterns:
            matches = re.findall(pattern, html)
            if matches:
                data['floor_no'] = matches[0]
                break
        
        # Extract year patterns
        year_patterns = [
            r'築(\d{4})年',
            r'(\d{4})年築',
            r'建築年.*?(\d{4})'
        ]
        
        for pattern in year_patterns:
            matches = re.findall(pattern, html)
            if matches:
                data['year'] = matches[0]
                break
        
        # Extract boolean amenities (Y/N fields) - comprehensive list
        amenity_keywords = {
            # Building amenities
            'elevator': ['エレベーター', 'elevator', 'EV'],
            'autolock': ['オートロック', 'auto lock', 'autoloc'],
            'delivery_box': ['宅配ボックス', 'delivery box', '宅配BOX'],
            'concierge': ['コンシェルジュ', 'concierge', 'フロント'],
            'gym': ['ジム', 'gym', 'フィットネス'],
            'swimming_pool': ['プール', 'pool', 'swimming'],
            
            # Parking
            'parking': ['駐車場', 'parking', '駐車'],
            'bicycle_parking': ['駐輪場', 'bicycle parking', '自転車'],
            'motorcycle_parking': ['バイク置場', 'motorcycle', 'バイク'],
            
            # Unit amenities
            'aircon': ['エアコン', 'air conditioning', 'aircon', 'AC'],
            'aircon_heater': ['エアコン暖房', 'air conditioning heater'],
            'internet_wifi': ['WiFi', 'インターネット', 'internet', 'ネット'],
            'cable': ['ケーブルTV', 'cable', 'CATV'],
            'bs': ['BS', 'BS放送', 'satellite'],
            
            # Kitchen
            'system_kitchen': ['システムキッチン', 'system kitchen'],
            'counter_kitchen': ['カウンターキッチン', 'counter kitchen'],
            'full_kitchen': ['フルキッチン', 'full kitchen'],
            'induction_cooker': ['IHクッキング', 'induction', 'IH'],
            'gas': ['ガス', 'gas'],
            'microwave': ['電子レンジ', 'microwave'],
            'oven': ['オーブン', 'oven'],
            'dishwasher': ['食洗機', 'dishwasher', '食器洗い'],
            'refrigerator': ['冷蔵庫', 'refrigerator', '冷蔵'],
            'refrigerator_freezer': ['冷凍冷蔵庫', 'freezer'],
            
            # Bathroom
            'bath': ['バス', 'bath', '浴室'],
            'separate_toilet': ['独立洗面台', 'separate toilet', '独立'],
            'unit_bath': ['ユニットバス', 'unit bath'],
            'auto_fill_bath': ['自動給湯', 'auto fill'],
            'shower': ['シャワー', 'shower'],
            'japanese_toilet': ['和式トイレ', 'japanese toilet'],
            'western_toilet': ['洋式トイレ', 'western toilet'],
            'washlet': ['ウォシュレット', 'washlet'],
            
            # Flooring & Interior
            'flooring': ['フローリング', 'flooring', 'フロア'],
            'tatami': ['畳', 'tatami'],
            'carpet': ['カーペット', 'carpet'],
            'underfloor_heating': ['床暖房', 'underfloor heating'],
            
            # Storage & Space
            'storage': ['収納', 'storage', 'クローゼット'],
            'loft': ['ロフト', 'loft'],
            'balcony': ['バルコニー', 'balcony'],
            'veranda': ['ベランダ', 'veranda'],
            'roof_balcony': ['ルーフバルコニー', 'roof balcony'],
            'yard': ['庭', 'yard', 'ガーデン'],
            
            # Appliances
            'washing_machine': ['洗濯機', 'washing machine'],
            'washer_dryer': ['洗濯乾燥機', 'washer dryer'],
            'furnished': ['家具付き', 'furnished', '家具'],
            'all_electric': ['オール電化', 'all electric'],
            
            # Special features
            'pets': ['ペット', 'pet', 'ペット可'],
            'female_only': ['女性限定', 'female only', '女性専用'],
            'student_friendly': ['学生可', 'student', '学生'],
            'soho': ['SOHO', 'soho', '事務所可'],
            'newly_built': ['新築', 'newly built', '新築物件']
        }
        
        for field, keywords in amenity_keywords.items():
            for keyword in keywords:
                if keyword in html:
                    data[field] = 'Y'
                    break
            if data[field] != 'Y':
                data[field] = None  # Keep as None if not found
        
        # Extract additional pricing information
        deposit_patterns = [
            r'敷金[：:]\s*(\d+)万円',
            r'敷金[：:]\s*(\d+)ヶ?月',
            r'deposit[：:]\s*¥([\d,]+)'
        ]
        
        for pattern in deposit_patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            if matches:
                data['numeric_deposit'] = matches[0].replace(',', '')
                break
        
        # Extract key money patterns
        key_patterns = [
            r'礼金[：:]\s*(\d+)万円',
            r'礼金[：:]\s*(\d+)ヶ?月',
            r'key money[：:]\s*¥([\d,]+)'
        ]
        
        for pattern in key_patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            if matches:
                data['numeric_key'] = matches[0].replace(',', '')
                break
        
        # Extract maintenance fee patterns
        maintenance_patterns = [
            r'管理費[：:]\s*(\d+)円',
            r'共益費[：:]\s*(\d+)円',
            r'maintenance[：:]\s*¥([\d,]+)'
        ]
        
        for pattern in maintenance_patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            if matches:
                data['monthly_maintenance'] = matches[0].replace(',', '')
                break
        
        # Extract building structure
        structure_patterns = [
            r'構造[：:]\s*([^<\n]+)',
            r'(RC|SRC|木造|鉄骨|軽量鉄骨)',
            r'structure[：:]\s*([^<\n]+)'
        ]
        
        for pattern in structure_patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            if matches:
                data['structure'] = matches[0].strip()
                break
        
        # Extract building floors
        building_floor_patterns = [
            r'地上(\d+)階',
            r'(\d+)階建',
            r'building.*?(\d+)\s*floors?'
        ]
        
        for pattern in building_floor_patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            if matches:
                data['floors'] = matches[0]
                break
        
        # Extract coordinates from maps or scripts
        lat_patterns = [
            r'lat["\']?\s*[:=]\s*([0-9.-]+)',
            r'latitude["\']?\s*[:=]\s*([0-9.-]+)',
            r'緯度[：:]\s*([0-9.-]+)'
        ]
        
        lng_patterns = [
            r'lng["\']?\s*[:=]\s*([0-9.-]+)',
            r'longitude["\']?\s*[:=]\s*([0-9.-]+)',
            r'経度[：:]\s*([0-9.-]+)'
        ]
        
        for pattern in lat_patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            if matches:
                data['map_lat'] = matches[0]
                break
        
        for pattern in lng_patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            if matches:
                data['map_lng'] = matches[0]
                break
        
        return data
    
    def _extract_from_markdown(self, markdown: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract additional data từ markdown content
        """
        if not markdown:
            return data
        
        # Extract address components từ markdown
        lines = markdown.split('\n')
        station_count = 1
        
        for line in lines:
            line = line.strip()
            
            # Look for address patterns (more comprehensive)
            prefecture_patterns = [
                '東京都', '大阪府', '神奈川県', '愛知県', '兵庫県', '福岡県', 
                '埼玉県', '千葉県', '北海道', '京都府', '広島県', '宮城県'
            ]
            
            for prefecture in prefecture_patterns:
                if prefecture in line and not data['prefecture']:
                    data['prefecture'] = prefecture
                    # Extract city and district from the same line
                    remaining = line.split(prefecture)[1] if prefecture in line else line
                    
                    # Extract city (市)
                    city_match = re.search(r'([^市]+市)', remaining)
                    if city_match and not data['city']:
                        data['city'] = city_match.group(1)
                    
                    # Extract district (区)
                    district_match = re.search(r'([^区]+区)', remaining)
                    if district_match and not data['district']:
                        data['district'] = district_match.group(1)
                    
                    # Extract chome-banchi
                    chome_match = re.search(r'(\d+丁目\d+番\d+号?)', remaining)
                    if chome_match and not data['chome_banchi']:
                        data['chome_banchi'] = chome_match.group(1)
                    break
            
            # Extract multiple station information
            if '駅' in line and station_count <= 5:
                # Extract station name
                station_match = re.search(r'([^駅\s]+駅)', line)
                if station_match:
                    station_field = f'station_name_{station_count}'
                    if not data[station_field]:
                        data[station_field] = station_match.group(1)
                        
                        # Extract train line
                        line_patterns = [
                            r'([^線\s]+線)',
                            r'JR([^駅\s]+)',
                            r'(東急[^駅\s]+)',
                            r'(京急[^駅\s]+)',
                            r'(小田急[^駅\s]+)'
                        ]
                        
                        for pattern in line_patterns:
                            line_match = re.search(pattern, line)
                            if line_match:
                                train_line_field = f'train_line_name_{station_count}'
                                if not data[train_line_field]:
                                    data[train_line_field] = line_match.group(1)
                                break
                        
                        # Extract walking time
                        walk_match = re.search(r'徒歩(\d+)分', line)
                        if walk_match:
                            walk_field = f'walk_{station_count}'
                            if not data[walk_field]:
                                data[walk_field] = walk_match.group(1)
                        
                        # Extract bus time
                        bus_match = re.search(r'バス(\d+)分', line)
                        if bus_match:
                            bus_field = f'bus_{station_count}'
                            if not data[bus_field]:
                                data[bus_field] = bus_match.group(1)
                        
                        # Extract car time
                        car_match = re.search(r'車(\d+)分', line)
                        if car_match:
                            car_field = f'car_{station_count}'
                            if not data[car_field]:
                                data[car_field] = car_match.group(1)
                        
                        station_count += 1
            
            # Extract building type
            if not data['building_type']:
                building_types = ['マンション', 'アパート', '一戸建て', 'テラスハウス', 'タウンハウス']
                for building_type in building_types:
                    if building_type in line:
                        data['building_type'] = building_type
                        break
            
            # Extract available date
            if not data['available_from']:
                date_patterns = [
                    r'入居可能日[：:]\s*([^\n]+)',
                    r'(\d{4}年\d{1,2}月\d{1,2}日)',
                    r'即入居可',
                    r'相談'
                ]
                
                for pattern in date_patterns:
                    date_match = re.search(pattern, line)
                    if date_match:
                        if pattern == r'即入居可':
                            data['available_from'] = '即入居可'
                        elif pattern == r'相談':
                            data['available_from'] = '相談'
                        else:
                            data['available_from'] = date_match.group(1).strip()
                        break
            
            # Extract postcode
            if not data['postcode']:
                postcode_match = re.search(r'〒(\d{3}-\d{4})', line)
                if postcode_match:
                    data['postcode'] = postcode_match.group(1)
            
            # Extract unit number
            if not data['unit_no']:
                unit_patterns = [
                    r'(\d+号室)',
                    r'部屋番号[：:]\s*(\d+)',
                    r'Unit\s*(\d+)'
                ]
                
                for pattern in unit_patterns:
                    unit_match = re.search(pattern, line, re.IGNORECASE)
                    if unit_match:
                        data['unit_no'] = unit_match.group(1)
                        break
        
        return data
    
    def _generate_property_id(self, url: str) -> str:
        """Tạo property ID từ URL"""
        # Extract ID từ URL
        match = re.search(r'/(\d+)/?$', url)
        if match:
            return f"PROP_{match.group(1)}"
        
        # Extract từ path
        path_match = re.search(r'/([^/]+)/?$', url)
        if path_match:
            return f"PROP_{path_match.group(1)}"
        
        # Fallback: timestamp
        return f"PROP_{int(datetime.now().timestamp())}"
    
    def validate_and_create_property_model(self, data: Dict[str, Any]) -> PropertyModel:
        """
        Validate và tạo PropertyModel từ extracted data
        """
        try:
            print(f"🔍 Creating PropertyModel with data type: {type(data)}")
            print(f"🔍 Data keys: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}")
            
            # Xử lý images nếu có
            if 'images' in data and isinstance(data['images'], list):
                print(f"🔍 Processing {len(data['images'])} images")
                processed_images = []
                for i, img in enumerate(data['images']):
                    print(f"🔍 Image {i}: {type(img)} - {img}")
                    if isinstance(img, dict) and 'url' in img:
                        processed_images.append(PropertyImage(**img))
                    else:
                        print(f"⚠️ Skipping invalid image data: {img}")
                data['images'] = processed_images
            
            # Tạo PropertyModel
            property_model = PropertyModel(**data)
            return property_model
            
        except Exception as e:
            print(f"❌ Error creating PropertyModel: {e}")
            print(f"🔍 Data causing error: {data}")
            import traceback
            traceback.print_exc()
            
            # Tạo model với dữ liệu cơ bản
            basic_data = {
                'link': data.get('link'),
                'property_csv_id': data.get('property_csv_id'),
                'create_date': data.get('create_date')
            }
            return PropertyModel(**basic_data)


class EnhancedPropertyCrawler:
    """
    Enhanced Property Crawler sử dụng crawl4ai (không cần LLM)
    """
    
    def __init__(self):
        self.extractor = PropertyExtractor()
    
    async def crawl_property(self, url: str) -> Dict[str, Any]:
        """
        Crawl một property và trả về dữ liệu JSON hoàn chỉnh
        """
        print(f"🚀 Crawling: {url}")
        
        # Extract dữ liệu bằng crawl4ai
        result = await self.extractor.extract_property_data(url)
        
        if result['success']:
            # Validate và tạo PropertyModel
            property_model = self.extractor.validate_and_create_property_model(
                result['property_data']
            )
            
            # Convert về dict để serialize JSON
            result['property_data'] = property_model.dict(exclude_none=True)
            
            print(f"✅ Success: Extracted {len(result['property_data'])} fields")
        else:
            print(f"❌ Failed: {result.get('error', 'Unknown error')}")
        
        return result
    
    async def crawl_multiple_properties(self, urls: List[str]) -> List[Dict[str, Any]]:
        """
        Crawl nhiều properties cùng lúc
        """
        print(f"🏘️ Crawling {len(urls)} properties...")
        
        # Tạo tasks cho tất cả URLs
        tasks = [self.crawl_property(url) for url in urls]
        
        # Chạy parallel với error handling
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Xử lý exceptions
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                print(f"❌ Error crawling {urls[i]}: {result}")
                processed_results.append({
                    'success': False,
                    'url': urls[i],
                    'error': str(result),
                    'crawl_timestamp': datetime.now().isoformat()
                })
            else:
                processed_results.append(result)
        
        # Thống kê
        success_count = sum(1 for r in processed_results if r.get('success', False))
        print(f"📊 Results: {success_count}/{len(urls)} successful")
        
        return processed_results
    
    def save_results_to_json(self, results: List[Dict[str, Any]], filename: str = None):
        """
        Lưu kết quả crawl vào file JSON
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"crawl_results_{timestamp}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            print(f"💾 Saved results to: {filename}")
            return filename
        except Exception as e:
            print(f"❌ Error saving to JSON: {e}")
            return None
    
    def save_results_to_csv(self, results: List[Dict[str, Any]], filename: str = None):
        """
        Lưu kết quả crawl vào file CSV
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"crawl_results_{timestamp}.csv"
        
        try:
            import pandas as pd
            
            # Flatten dữ liệu cho CSV
            flattened_data = []
            for result in results:
                if result.get('success') and 'property_data' in result:
                    flat_data = result['property_data'].copy()
                    flat_data['crawl_success'] = True
                    flat_data['crawl_timestamp'] = result.get('crawl_timestamp')
                    flat_data['crawl_url'] = result.get('url')
                    flattened_data.append(flat_data)
                else:
                    # Thêm failed records
                    flattened_data.append({
                        'crawl_success': False,
                        'crawl_timestamp': result.get('crawl_timestamp'),
                        'crawl_url': result.get('url'),
                        'crawl_error': result.get('error')
                    })
            
            df = pd.DataFrame(flattened_data)
            df.to_csv(filename, index=False, encoding='utf-8')
            print(f"💾 Saved results to CSV: {filename}")
            return filename
            
        except ImportError:
            print("❌ pandas not installed. Cannot save to CSV.")
            return None
        except Exception as e:
            print(f"❌ Error saving to CSV: {e}")
            return None


# Utility functions
async def crawl_single_property(url: str) -> Dict[str, Any]:
    """
    Convenience function để crawl một property
    """
    crawler = EnhancedPropertyCrawler()
    return await crawler.crawl_property(url)


async def crawl_property_list(urls: List[str]) -> List[Dict[str, Any]]:
    """
    Convenience function để crawl nhiều properties
    """
    crawler = EnhancedPropertyCrawler()
    return await crawler.crawl_multiple_properties(urls)


# Example usage
async def main():
    """
    Example usage của Enhanced Property Crawler
    """
    time_start = datetime.now().strftime("%Y%m%d_%H%M%S")
    # Test URLs (thay bằng URLs thực tế)
    test_urls = [
        "https://rent.tokyu-housing-lease.co.jp/rent/8034884/117024"
    ]
    
    # Tạo crawler
    crawler = EnhancedPropertyCrawler()
    
    # Crawl single property
    print("=== Testing Single Property Crawl ===")
    if test_urls:
        single_result = await crawler.crawl_property(test_urls[0])
        print(f"Single result: {json.dumps(single_result, indent=2, ensure_ascii=False)}")
    
    # Crawl multiple properties
    print("\n=== Testing Multiple Properties Crawl ===")
    results = await crawler.crawl_multiple_properties(test_urls)
    
    # Save results
    json_file = crawler.save_results_to_json(results)    
    print(f"\n=== Summary ===")
    print(f"Total URLs: {len(test_urls)}")
    print(f"Successful: {sum(1 for r in results if r.get('success'))}")
    print(f"Failed: {sum(1 for r in results if not r.get('success'))}")
    if json_file:
        print(f"JSON saved: {json_file}")
        
    time_end = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    duration = datetime.strptime(time_end, "%Y%m%d_%H%M%S") - datetime.strptime(time_start, "%Y%m%d_%H%M%S")

    print(
        f"Start time: {time_start}, End time: {time_end} 🕒 Duration: {duration}"
    )
    
    # trung bình 16s - 1 ngày 24 tiếng crawl được 5400 data


if __name__ == "__main__":
    asyncio.run(main())