"""
Custom Configuration - Optimized version with better performance and structure
"""
import re
import requests
from typing import Dict, Any, Optional, Tuple
from functools import lru_cache
from ..custom_rules import CustomExtractor
from pyproj import CRS, Transformer

# ============================================================================
# CONSTANTS AND CONFIGURATIONS
# ============================================================================

# Coordinate conversion constants
COORDINATE_OFFSET_LAT = -1.291213
COORDINATE_OFFSET_LON = -5.82497
DEFAULT_ZONE = 9
MAX_IMAGES = 16
GALLERY_TIMEOUT = 5

# Default amenities configuration
DEFAULT_AMENITIES = {
    'credit_card': 'Y',
    'no_guarantor': 'Y', 
    'aircon': 'Y',
    'aircon_heater': 'Y',
    'bs': 'Y',
    'cable': 'Y',
    'internet_broadband': 'Y',
    'internet_wifi': 'Y',
    'phoneline': 'Y',
    'flooring': 'Y',
    'system_kitchen': 'Y',
    'bath': 'Y',
    'shower': 'Y',
    'unit_bath': 'Y',
    'western_toilet': 'Y',
    'fire_insurance': 20000,
}

# Direction mapping
DIRECTION_MAPPING = {
    '北': 'facing_north',
    '北東': 'facing_northeast', 
    '東': 'facing_east',
    '東南': 'facing_southeast',
    '南': 'facing_south',
    '南西': 'facing_southwest',
    '西': 'facing_west',
    '西北': 'facing_northwest',
    '北西': 'facing_northwest'
}

# Amenities mapping
AMENITIES_MAPPING = {
    'フロント': 'concierge',
    '宅配ロッカー': 'delivery_box',
    'オートロック': 'autolock',
    'バイク置場': 'motorcycle_parking',
    '敷地内ごみ置場': 'cleaning_service',
    'エレベータ': 'elevator',
    '24時間管理': 'cleaning_service',
    '防犯カメラ': 'autolock',
    'セキュリティシステム': 'autolock',
    'バルコニー': 'balcony',
    'バストイレ': 'unit_bath',
    '洗面所独立': 'separate_toilet',
    '室内洗濯機置場': 'washing_machine',
    'バス有': 'bath',
    '浴室乾燥機': 'bath_water_heater',
    '給湯追い焚き有': 'auto_fill_bath',
    'キッチン有': 'system_kitchen',
    'コンロ有': 'range',
    'グリル': 'oven',
    'オープン': 'counter_kitchen',
    'インターネット': 'internet_broadband',
    'BS': 'bs',
    'CS': 'cable',
    'ピアノ可': 'furnished',
    'ウォークインクロゼット': 'storage',
    'ペット可': 'pets',
    'エアコン': 'aircon',
    'フローリング': 'flooring',
    'システムキッチン': 'system_kitchen',
    'シャワー': 'shower',
    'ガス': 'gas',
    'WiFi': 'internet_wifi',
    'Wi-Fi': 'internet_wifi',
    'インターホン': 'autolock',
    'TVモニター付インターホン': 'autolock',
    '宅配BOX': 'delivery_box',
    'ゴミ置場': 'cleaning_service',
    '温水洗浄便座': 'washlet',
    '床暖房': 'underfloor_heating',
    '食器洗い乾燥機': 'dishwasher',
    'IHクッキングヒーター': 'induction_cooker',
    '追い焚き機能': 'auto_fill_bath',
    '宅配ボックス': 'delivery_box',
    'オール電化': 'all_electric',
    'カウンターキッチン': 'counter_kitchen',
    'ロフト': 'loft',
    'ルーフバルコニー': 'roof_balcony',
    'ベランダ': 'veranda',
    '庭': 'yard',
    'SOHO可': 'soho',
    '女性限定': 'female_only',
    '学生可': 'student_friendly',
}

# ============================================================================
# CACHED UTILITIES
# ============================================================================

@lru_cache(maxsize=32)
def get_coordinate_transformer(zone: int = DEFAULT_ZONE) -> Transformer:
    """Get cached coordinate transformer for better performance"""
    epsg_code = 30160 + zone
    crs_xy = CRS.from_epsg(epsg_code)
    crs_wgs84 = CRS.from_epsg(4326)
    return Transformer.from_crs(crs_xy, crs_wgs84, always_xy=True)

@lru_cache(maxsize=128)
def compile_regex(pattern: str, flags: int = re.DOTALL | re.IGNORECASE) -> re.Pattern:
    """Cache compiled regex patterns for better performance"""
    return re.compile(pattern, flags)

# ============================================================================
# CORE UTILITIES
# ============================================================================

class RequestsSession:
    """Singleton requests session for connection pooling"""
    _instance = None
    _session = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._session = requests.Session()
            cls._session.headers.update({'User-Agent': 'Mozilla/5.0 (compatible; crawler)'})
        return cls._instance
    
    def get(self, url: str, **kwargs) -> requests.Response:
        return self._session.get(url, **kwargs)

# Global session instance
session = RequestsSession()

# ============================================================================
# COORDINATE CONVERSION
# ============================================================================

def xy_to_latlon_tokyo(x: float, y: float, zone: int = DEFAULT_ZONE) -> Tuple[float, float]:
    """
    Optimized coordinate conversion with cached transformer
    """
    transformer = get_coordinate_transformer(zone)
    lon, lat = transformer.transform(x, y)
    return lat + COORDINATE_OFFSET_LAT, lon + COORDINATE_OFFSET_LON

def parse_japanese_address(address: str) -> dict:
    """Parse Japanese address to extract chome_banchi"""
    if not address:
        return {"chome_banchi": None}
    
    # Use cached regex
    pattern = compile_regex(r'^(?:.*?[都道府県])?(?:.*?[市区町村])?(.*)$')
    match = pattern.match(address)
    
    return {
        "chome_banchi": match.group(1).strip() if match else None
    }

# ============================================================================
# HTML UTILITIES
# ============================================================================

def find(pattern: str, html: str) -> Optional[str]:
    """Find pattern in HTML with cached regex"""
    regex = compile_regex(pattern)
    match = regex.search(html)
    return match.group(1).strip() if match else None

def clean_html(text: str) -> str:
    """Remove HTML tags and clean text"""
    if not text:
        return ""
    # Use cached regex for HTML tag removal
    html_tag_regex = compile_regex(r'<[^>]+>')
    cleaned = html_tag_regex.sub('', text).strip()
    # Clean HTML entities
    cleaned = cleaned.replace('&nbsp;', ' ').replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
    return cleaned

def setup_custom_extractor() -> CustomExtractor:
    """
    Setup optimized custom extractor with better performance and structure
    """
    extractor = CustomExtractor()
    
    # Wrapper for error handling
    def safe_wrapper(callback):
        """Wrapper for safe processing with error handling"""
        def wrapper_func(data: Dict[str, Any]) -> Dict[str, Any]:
            html = data.get('_html', '')
            if not html:
                return data
            
            try:
                return callback(data, html)
            except Exception as e:
                print(f"❌ Error in {callback.__name__}: {e}")
                return data
        
        return wrapper_func
    
    # Chuyển đổi tọa độ X, Y
    def convert_coordinates(data: Dict[str, Any], html: str) -> Dict[str, Any]:
        """Convert coordinates from XY to lat/lon"""
        x_value = find(r'name="[^"]*MAP_X"[^>]*value="([^"]*)"', html)
        y_value = find(r'name="[^"]*MAP_Y"[^>]*value="([^"]*)"', html)
        
        if x_value and y_value:
            try:
                x, y = float(x_value), float(y_value)
                lat, lon = xy_to_latlon_tokyo(x, y)
                
                data.update({
                    'map_lat': str(lat),
                    'map_lng': str(lon)
                })
                
                print(f"🗺️ Converted: X={x}, Y={y} → Lat={lat:.6f}, Lng={lon:.6f}")
                
            except (ValueError, Exception) as e:
                print(f"❌ Coordinate conversion error: {e}")
        
        return data
    
    # Xử lý trước khi dùng
    def pass_html(html: str, data: Dict[str, Any]) -> tuple:
        """Clean HTML before processing with cached regex"""
        # Remove related sections
        related_pattern = compile_regex(r'<section[^>]*class="[^"]*--related[^"]*"[^>]*>.*?</section>')
        html = related_pattern.sub('', html)
        
        # Remove Japanese related properties text
        japanese_pattern = compile_regex(r'この部屋をチェックした人は、こんな部屋もチェックしています。.*?(?=<footer|$)')
        html = japanese_pattern.sub('', html)
        
        data['_html'] = html
        return html, data
    
    # Xử lý cho hình ảnh
    def get_gallery_images(html: str) -> Tuple[list, list, list]:
        """Extract gallery images with optimized request handling"""
        floorplan_images = []
        exterior_images = []
        interior_images = []
        
        # 1. Floor plan
        firstfloor_url = find(r'RF_firstfloorplan_photo\s*=\s*["\']([^"\']+)["\']', html)
        if firstfloor_url and firstfloor_url != "null":
            floorplan_images.append(firstfloor_url)

        # 2. Gallery
        gallery_url = find(r'RF_gallery_url\s*=\s*["\']([^"\']+)["\']', html)
        if not gallery_url or gallery_url == "null":
            return exterior_images, floorplan_images, interior_images
        
        try:
            print(f"🖼️ Fetching gallery: {gallery_url}")
            response = session.get(gallery_url, timeout=GALLERY_TIMEOUT)
            
            if response.status_code != 200:
                print(f"❌ Gallery fetch failed: HTTP {response.status_code}")
                return exterior_images, floorplan_images, interior_images
            
            gallery_data = response.json()
            for item in gallery_data:
                filename = item.get("filename", "")
                if not filename:
                    continue
                    
                room_no = item.get("ROOM_NO", 0)
                if room_no == 99999 and not exterior_images:
                    exterior_images.append(filename)
                else:
                    interior_images.append(filename)
                    
        except requests.exceptions.Timeout:
            print("⏰ Gallery request timeout")
        except Exception as e:
            print(f"❌ Gallery request error: {e}")
        
        return exterior_images, floorplan_images, interior_images
    
    def extract_image(data: Dict[str, Any], html: str) -> Dict[str, Any]:
        images_list = []
        used_urls = set()
        used_names = set()

        def add_image(img_url: str, category: str) -> bool:
            """Add image if not duplicate and under limit"""
            if (len(images_list) >= MAX_IMAGES or 
                img_url in used_urls or 
                img_url.split('/')[-1] in used_names):
                return False

            images_list.append({'url': img_url, 'category': category})
            used_urls.add(img_url)
            used_names.add(img_url.split('/')[-1])
            return True

        try:
            exterior_images, floorplan_images, interior_images = get_gallery_images(html)

            # Exterior → lấy đúng 1 ảnh
            if exterior_images:
                add_image(exterior_images[0], "exterior")

            # Floorplan → lấy đúng 1 ảnh
            if floorplan_images:
                add_image(floorplan_images[0], "floorplan")

            # Interior → lấy nhiều cho đến khi đủ MAX_IMAGES
            for img_url in interior_images:
                print("print", img_url)
                add_image(img_url, "interior")

        except Exception as e:
            print(f"❌ Image extraction error: {e}")

        if images_list:
            data['images'] = images_list
            print(f"🎯 Total images: {len(images_list)}")

        return data

    
    # Các thông số mặc định
    def set_default_amenities(data: Dict[str, Any], html: str) -> Dict[str, Any]:
        """Set default amenities using global constants"""
        data.update(DEFAULT_AMENITIES)
        return data
    
    # Xử lý tiền
    def process_pricing(data: Dict[str, Any], html: str) -> Dict[str, Any]:
        """Process pricing calculations with validation"""
        if not all(key in data for key in ['monthly_rent', 'monthly_maintenance']):
            return data

        try:
            monthly_rent = data['monthly_rent']
            monthly_maintenance = data['monthly_maintenance']
            total_monthly = monthly_rent + monthly_maintenance

            if total_monthly > 0:
                data.update({
                    "total_monthly": total_monthly,
                    "numeric_guarantor": total_monthly * 50 // 100,
                    "numeric_guarantor_max": total_monthly * 80 // 100,
                })
                
                print(f"💰 Calculated pricing: total={total_monthly}円")
            else:
                print(f"⚠️ Invalid total monthly amount: {total_monthly}")

        except Exception as e:
            print(f"❌ Error processing pricing: {e}")

        return data
    
    # Làm sạch các biến temp
    def cleanup_temp_fields(data: Dict[str, Any], html: str) -> Dict[str, Any]:
        """Remove temporary fields that shouldn't be in final JSON"""
        if '_html' in data:
            del data['_html']
            print("🧹 Cleaned up temporary _html field")
        return data
    
    # Xử lý nội dung tĩnh - Optimized with modular approach
    def extract_header_info(data: Dict[str, Any], html: str):
        """Extract building name, floor, and room number"""
        try:
            h1_content = find(r'<h1[^>]*>(.*?)</h1>', html)
            if not h1_content:
                print("⚠️ No h1 tag found")
                return
            
            h1_text = clean_html(h1_content)
            pattern = compile_regex(r'^(.+?)\s+(\d+)階(\d+)$')
            match = pattern.match(h1_text)
            
            if match:
                data.update({
                    'building_name_ja': match.group(1).strip(),
                    'floor_no': int(match.group(2)),
                    'room_no': int(match.group(3))
                })
            else:
               data.update({
                    'building_name_ja': h1_text,
                })
                
        except Exception as e:
            print(f"❌ Error extracting header info: {e}")
            
    def extract_available_from(data: Dict[str, Any], html: str):
        '''
        Tìm 入居可能日 và nội dung thẻ dd sau nó lưu vào available_from
        '''
        try:
            # Tìm thẻ dt chứa "入居可能日" và thẻ dd ngay sau nó
            available_from_content = find(r'<dt[^>]*>入居可能日</dt>\s*<dd[^>]*>(.*?)</dd>', html)
            if not available_from_content:
                print("⚠️ No available_from section found")
                return
            
            # Làm sạch HTML và lấy text
            available_from_text = clean_html(available_from_content)
            if available_from_text:
                data['available_from'] = available_from_text
                print(f"📅 Set available_from: {available_from_text}")
            else:
                print("⚠️ Available_from content is empty after cleaning")
                
        except Exception as e:
            print(f"❌ Error extracting available_from: {e}")
    
    def extract_address_info(data: Dict[str, Any], html: str):
        """Extract address information"""
        try:
            address_section = find(r'<dt[^>]*>所在地</dt>(.*?)(?=<dt|</dl>|$)', html)
            if not address_section:
                print("⚠️ No address section found")
                return
            
            dd_pattern = compile_regex(r'<dd[^>]*>(.*?)</dd>')
            dd_matches = dd_pattern.findall(address_section)
            
            if len(dd_matches) >= 2:
                address_text = clean_html(dd_matches[1])
                address_parts = parse_japanese_address(address_text)
                
                data['address'] = address_text
                if address_parts['chome_banchi']:
                    data['chome_banchi'] = address_parts['chome_banchi']
                
                print(f"🏠 Set address: {address_text}")
            else:
                print(f"⚠️ Found {len(dd_matches)} dd tags, expected at least 2")
                
        except Exception as e:
            print(f"❌ Error extracting address info: {e}")
    
    def extract_rent_info(data: Dict[str, Any], html: str):
        """Extract rent information"""
        try:
            rent_pattern = compile_regex(r'class="[^"]*__rent[^"]*"[^>]*>(.*?)</[^>]+>')
            rent_match = rent_pattern.search(html)
            
            if not rent_match:
                print("⚠️ No rent class found")
                return
            
            rent_text = clean_html(rent_match.group(1))
            print(f"🏠 Found rent text: {rent_text}")
            
            # Extract rent and maintenance fees
            price_pattern = compile_regex(r'([\d,]+)円(?:\s*/\s*([\d,]+)円)?')
            price_match = price_pattern.search(rent_text)
            
            if price_match:
                monthly_rent = int(price_match.group(1).replace(',', ''))
                monthly_maintenance = int(price_match.group(2).replace(',', '')) if price_match.group(2) else 0
                
                data.update({
                    'monthly_rent': monthly_rent,
                    'monthly_maintenance': monthly_maintenance
                })
                
                print(f"💰 Extracted rent: {monthly_rent}円, maintenance: {monthly_maintenance}円")
            else:
                print(f"⚠️ Rent format not matched: {rent_text}")
                
        except Exception as e:
            print(f"❌ Error extracting rent info: {e}")
    
    def extract_deposit_key_info(data: Dict[str, Any], html: str):
        """Extract deposit and key money information"""
        try:
            deposit_key_content = find(r'<dt[^>]*>敷金／礼金</dt>\s*<dd[^>]*>(.*?)</dd>', html)
            if not deposit_key_content:
                print("⚠️ No deposit/key section found")
                return
            
            deposit_key_text = clean_html(deposit_key_content)
            print(f"💰 Found deposit/key info: {deposit_key_text}")
            
            pattern = compile_regex(r'([\d.]+)ヶ月\s*/\s*([\d.]+)ヶ月')
            match = pattern.search(deposit_key_text)
            
            if match:
                data.update({
                    'numeric_deposit': float(match.group(1)),
                    'numeric_key': float(match.group(2))
                })
                
        except Exception as e:
            print(f"❌ Error extracting deposit/key info: {e}")
    
    def extract_room_info(data: Dict[str, Any], html: str):
        """Extract room type and size"""
        try:
            room_info_content = find(r'<dt[^>]*>間取り・面積</dt>\s*<dd[^>]*>(.*?)</dd>', html)
            if not room_info_content:
                print("⚠️ No room info section found")
                return
            
            room_info_text = clean_html(room_info_content)
            pattern = compile_regex(r'^([^/]+?)\s*/\s*([\d.]+)㎡')
            match = pattern.search(room_info_text)
            
            if match:
                room_type = re.sub(r'[^\w]', '', match.group(1).strip())
                size = float(match.group(2))
                
                data.update({
                    'room_type': room_type,
                    'size': size
                })
                
        except Exception as e:
            print(f"❌ Error extracting room info: {e}")
    
    def extract_construction_date(data: Dict[str, Any], html: str):
        """Extract construction date"""
        try:
            construction_content = find(r'<dt[^>]*>竣工日</dt>\s*<dd[^>]*>(.*?)</dd>', html)
            if not construction_content:
                print("⚠️ No construction date section found")
                return
            
            construction_text = clean_html(construction_content)
            year_pattern = compile_regex(r'(\d{4})年')
            year_match = year_pattern.search(construction_text)
            
            if year_match:
                data['year'] = int(year_match.group(1))
            else:
                print(f"⚠️ Could not extract year from: {construction_text}")
                
        except Exception as e:
            print(f"❌ Error extracting construction date: {e}")
    
    def extract_structure_info(data: Dict[str, Any], html: str):
        """Extract building structure information"""
        try:
            structure_content = find(r'<dt[^>]*>規模構造</dt>\s*<dd[^>]*>(.*?)</dd>', html)
            if not structure_content:
                print("⚠️ No structure section found")
                return
            
            structure_text = clean_html(structure_content)
            print(f"🏗️ Structure text: '{structure_text}'")
            
            pattern = compile_regex(r'^(.*?造)\s*地上(\d+)階(?:地下(\d+)階建?)?')
            match = pattern.search(structure_text)
            
            if match:
                data.update({
                    'structure': match.group(1).strip(),
                    'floors': int(match.group(2))
                })
                
                if match.group(3):
                    data['basement_floors'] = int(match.group(3))
                    
                print(f"🏗️ Extracted structure info successfully")
            else:
                print(f"⚠️ Structure pattern did not match: '{structure_text}'")
                
        except Exception as e:
            print(f"❌ Error extracting structure info: {e}")
    
    def extract_renewal_fee(data: Dict[str, Any], html: str):
        """Extract renewal fee information"""
        try:
            renewal_content = find(r'<dt[^>]*>更新料</dt>\s*<dd[^>]*>(.*?)</dd>', html)
            if not renewal_content:
                print("⚠️ No renewal fee section found")
                return
            
            renewal_text = clean_html(renewal_content)
            pattern = compile_regex(r'新賃料の(\d+)ヶ月分')
            match = pattern.search(renewal_text)
            
            if match:
                months = int(match.group(1))
                data.update({
                    'renewal_new_rent': 'Y',
                    'months_renewal': 12 if months == 1 else months
                })
                
        except Exception as e:
            print(f"❌ Error extracting renewal fee: {e}")
    
    def extract_direction_info(data: Dict[str, Any], html: str):
        """Extract apartment facing direction"""
        try:
            direction_content = find(r'<dt[^>]*>方位</dt>\s*<dd[^>]*>(.*?)</dd>', html)
            if not direction_content:
                print("⚠️ No direction section found")
                return
            
            direction_text = clean_html(direction_content)
            
            for jp_direction, field_name in DIRECTION_MAPPING.items():
                if jp_direction in direction_text:
                    data[field_name] = 'Y'
                    break
            else:
                print(f"⚠️ No recognizable directions found in: {direction_text}")
                
        except Exception as e:
            print(f"❌ Error extracting direction info: {e}")
    
    def extract_lock_exchange(data: Dict[str, Any], html: str):
        """Extract lock exchange fee"""
        try:
            other_fees_content = find(r'<dt[^>]*>その他費用</dt>\s*<dd[^>]*>(.*?)</dd>', html)
            if not other_fees_content:
                print("⚠️ No other fees section found")
                return
            
            other_fees_text = clean_html(other_fees_content)
            pattern = compile_regex(r'玄関錠交換代[^\d]*([\d,]+)円')
            match = pattern.search(other_fees_text)
            
            if match:
                data['lock_exchange'] = int(match.group(1).replace(',', ''))
                
        except Exception as e:
            print(f"❌ Error extracting lock exchange: {e}")
    
    def extract_amenities(data: Dict[str, Any], html: str):
        """Extract amenities information"""
        try:
            amenities_pattern = compile_regex(r'<dt[^>]*>専有部・共用部設備</dt>\s*<dd[^>]*>(.*?)</dd>')
            amenities_match = amenities_pattern.search(html)
            
            if not amenities_match:
                print("⚠️ No amenities section found")
                return
            
            amenities_text = clean_html(amenities_match.group(1))
            print(f"🏢 Found amenities info: {amenities_text}")
            
            found_amenities = []
            for jp_amenity, field_name in AMENITIES_MAPPING.items():
                if jp_amenity in amenities_text:
                    data[field_name] = 'Y'
                    found_amenities.append(f"{jp_amenity} → {field_name}")
            
            if found_amenities:
                print(f"🏢 Set amenities to Y:")
                for amenity in found_amenities:
                    print(f"   {amenity}")
            else:
                print(f"⚠️ No recognizable amenities found")
                
        except Exception as e:
            print(f"❌ Error extracting amenities: {e}")
    
    def extract_building_description(data: Dict[str, Any], html: str):
        """Extract building description"""
        try:
            description_pattern = compile_regex(r'<dt[^>]*>備考</dt>\s*<dd[^>]*>(.*?)</dd>')
            description_match = description_pattern.search(html)
            
            if description_match:
                description_text = clean_html(description_match.group(1))
                if description_text:
                    data['building_description_ja'] = description_text
                    
        except Exception as e:
            print(f"❌ Error extracting building description: {e}")
    
    def get_static_info(data: Dict[str, Any], html: str) -> Dict[str, Any]:
        """Process static information extraction using modular approach"""
        # Process each section using dedicated functions
        extract_header_info(data, html)
        extract_available_from(data, html)
        extract_address_info(data, html)
        extract_rent_info(data, html)
        extract_deposit_key_info(data, html)
        extract_room_info(data, html)
        extract_construction_date(data, html)
        extract_structure_info(data, html)
        extract_renewal_fee(data, html)
        extract_direction_info(data, html)
        extract_lock_exchange(data, html)
        extract_amenities(data, html)
        extract_building_description(data, html)
        
        return data
    
    # Setup hooks
    extractor.add_pre_hook(pass_html)
    
    # Add processors in order
    processors = [
        extract_image,
        get_static_info,
        convert_coordinates, 
        set_default_amenities,
        process_pricing,
        cleanup_temp_fields,
    ]
    
    for processor in processors:
        extractor.add_post_hook(safe_wrapper(processor))
    
    return extractor