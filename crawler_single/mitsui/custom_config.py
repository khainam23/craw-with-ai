"""
Custom Configuration - Setup your custom rules and hooks here
"""
import re
import requests
from typing import Dict, Any
from ..custom_rules import CustomExtractor
from pyproj import CRS, Transformer

# Xử lý chuyển đổi tọa độ phẳng
def xy_to_latlon_tokyo(x, y, zone=9):
    """
    Chuyển đổi từ tọa độ phẳng XY (Japan Plane Rectangular CS dựa trên Tokyo Datum) về lat/lon (WGS84).
    :param x: X coordinate (m)
    :param y: Y coordinate (m)
    :param zone: Zone number (1-19)
    :return: (lat, lon) in degrees
    """
    # Định nghĩa hệ tọa độ phẳng Nhật Bản dựa trên Tokyo Datum
    epsg_code = 30160 + zone  # Zone 9 -> EPSG:30169 (Tokyo / Japan Plane Rectangular CS IX)
    crs_xy = CRS.from_epsg(epsg_code)
    
    # Hệ tọa độ chuẩn WGS84
    crs_wgs84 = CRS.from_epsg(4326)
    
    # Tạo transformer
    transformer = Transformer.from_crs(crs_xy, crs_wgs84, always_xy=True)
    
    # Chuyển đổi
    lon, lat = transformer.transform(x, y)
    return lat - 1.291213 , lon - 5.82497 # Sai số trên lệch, tính dựa vào thống kê trung bình nhiều điểm

# Xử lý cho địa chỉ
PREFECTURES = [
    "北海道", "青森県", "岩手県", "宮城県", "秋田県", "山形県", "福島県",
    "茨城県", "栃木県", "群馬県", "埼玉県", "千葉県", "東京都", "神奈川県",
    "新潟県", "富山県", "石川県", "福井県", "山梨県", "長野県",
    "岐阜県", "静岡県", "愛知県", "三重県",
    "滋賀県", "京都府", "大阪府", "兵庫県", "奈良県", "和歌山県",
    "鳥取県", "島根県", "岡山県", "広島県", "山口県",
    "徳島県", "香川県", "愛媛県", "高知県",
    "福岡県", "佐賀県", "長崎県", "熊本県", "大分県", "宮崎県", "鹿児島県", "沖縄県"
]

def parse_japanese_address(address: str) -> dict:
    result = {
        "postcode": None,
        "prefecture": None,
        "city": None,
        "district": None,
        "chome_banchi": None
    }

    # Prefecture
    for pref in PREFECTURES:
        if address.startswith(pref):
            result["prefecture"] = pref
            address = address[len(pref):]
            break

    # City/District (市, 区, 町, 村)
    m = re.match(r'^(.*?[市区町村])', address)
    if m:
        val = m.group(1)
        # 区 thì để vào district
        if val.endswith("区"):
            result["district"] = val
        else:
            result["city"] = val
        address = address[len(val):]

    # Phần còn lại là 丁目 番地 号
    if address:
        result["chome_banchi"] = address

    return result

def setup_custom_extractor() -> CustomExtractor:
    """
    Setup custom extractor - Add your rules and hooks here
    """
    extractor = CustomExtractor()
    
    # Hàm giúp tìm thông tin nhanh
    def find(pattern: str, html: str):
        match = re.search(pattern, html, re.DOTALL | re.IGNORECASE)
        return match.group(1).strip() if match else None
    
    # Hàm bọc lại cho gọn code
    def wrapper(data: Dict[str, Any], callback) -> Dict[str, Any]:
        html = data.get('_html', '')
        if not html:
            return data
        
        try:
            return callback(data, html)
        except Exception as e:
            print(f"❌ Error in custom callback: {e}")
            return data
    
    # Chuyển đổi tọa độ X, Y
    def convert_coordinates(data: Dict[str, Any], html: str) -> Dict[str, Any]:
        # Extract MAP_X
        x_value = find(r'name="[^"]*MAP_X"[^>]*value="([^"]*)"', html)
        # Extract MAP_Y  
        y_value = find(r'name="[^"]*MAP_Y"[^>]*value="([^"]*)"', html)
        
        if x_value and y_value:
            try:
                x = float(x_value)
                y = float(y_value)
                
                lat, lon = xy_to_latlon_tokyo(x, y, zone=9)
                
                data['map_lat'] = str(lat)
                data['map_lng'] = str(lon)
                
                print(f"🗺️ Converted: X={x}, Y={y} → Lat={lat:.6f}, Lng={lon:.6f}")
                
            except Exception as e:
                print(f"❌ Coordinate conversion error: {e}")
        
        # Keep _html for image extraction from cleaned HTML, will be cleaned up after processing
        return data
    
    # Xử lý trước khi dùng
    def pass_html(html: str, data: Dict[str, Any]) -> tuple:
        # Remove section tags with class containing "--related"
        html = re.sub(r'<section[^>]*class="[^"]*--related[^"]*"[^>]*>.*?</section>', '', html, flags=re.DOTALL | re.IGNORECASE)
        
        # Remove the specific Japanese text section about related properties
        html = re.sub(r'この部屋をチェックした人は、こんな部屋もチェックしています。.*?(?=<footer|$)', '', html, flags=re.DOTALL | re.IGNORECASE)
        
        data['_html'] = html
        return html, data
    
    # Xử lý cho hình ảnh
    def extract_image(data: Dict[str, Any], html: str) -> Dict[str, Any]:
        used_urls = set()
        used_name = set()
        images_list = []

        def add_image(img_url: str, category: str):
            """Thêm ảnh vào images list"""
            if img_url not in used_urls and img_url.split('/')[-1] not in used_name and len(images_list) < 16:
                image_data = {
                    'url': img_url,
                    'category': category
                }
                images_list.append(image_data)
                used_urls.add(img_url)
                used_name.add(img_url.split('/')[-1])

        try:
            # 1. Floor plan
            firstfloor_url = find(r'RF_firstfloorplan_photo\s*=\s*["\']([^"\']+)["\']', html)
            if firstfloor_url and firstfloor_url != "null":
                add_image(firstfloor_url, "floorplan")

            # 2. Gallery - Optimized with faster timeout
            gallery_url = find(r'RF_gallery_url\s*=\s*["\']([^"\']+)["\']', html)
            if gallery_url and gallery_url != "null":
                print(f"🖼️ Fetching gallery from: {gallery_url}")
                try:
                    response = requests.get(gallery_url, timeout=3)  # Reduced timeout to 3s
                    if response.status_code == 200:
                        gallery_data = response.json()
                        for item in gallery_data:
                            room_no = item.get("ROOM_NO", 0)
                            filename = item.get("filename", "")
                            if room_no != 99999 and filename:
                                add_image(filename, "interior")
                    else:
                        print(f"❌ Failed to fetch gallery: HTTP {response.status_code}")
                except requests.exceptions.Timeout:
                    print(f"⏰ Gallery request timeout - skipping images")
                except Exception as e:
                    print(f"❌ Gallery request error: {e}")

        except Exception as e:
            print(f"❌ Extraction error: {e}")

        # Gán images list vào data
        if images_list:
            data['images'] = images_list
            print(f"🎯 Total images extracted: {len(images_list)}")
        
        return data
    
    # Các thông số mặc định
    def set_default_amenities(data: Dict[str, Any], html: str) -> Dict[str, Any]:
        """
        Set specific amenities to Y by default
        """
        default_amenities = {
            'credit_card': 'Y',         # Credit Card Accepted
            'no_guarantor': 'Y',        # No Guarantor
            'aircon': 'Y',              # Aircon
            'aircon_heater': 'Y',       # Aircon Heater
            'bs': 'Y',                  # Broadcast Satellite TV
            'cable': 'Y',               # Cable
            'internet_broadband': 'Y',  # Broadband
            'internet_wifi': 'Y',       # Internet WiFi
            'phoneline': 'Y',           # Phoneline
            'flooring': 'Y',            # Flooring
            'system_kitchen': 'Y',      # System Kitchen
            'bath': 'Y',                # Bath
            'shower': 'Y',              # Shower
            'unit_bath': 'Y',           # Unit Bath
            'western_toilet': 'Y',      # Western Toilet
            'fire_insurance': 20000,    # Insurance Fee
        }
    
        
        # Set all default amenities to Y
        for field_name, value in default_amenities.items():
            data[field_name] = value
        
        return data
    
    # Xử lý tiền
    def process_pricing(data: Dict[str, Any], html: str) -> Dict[str, Any]:
        """
        Extract めやす賃料 from HTML using regex and calculate monthly_rent and monthly_maintenance.
        """
        def extract_price_from_html(field_name: str) -> str:
            """
            Tìm giá trị trong <dd> ngay sau <dt>field_name</dt>.
            """
            return find(rf"<dt[^>]*>{field_name}</dt>\s*<dd[^>]*>(.*?)</dd>", html) or ""

        try:
            total_monthly_raw = extract_price_from_html("めやす賃料")

            if total_monthly_raw:
                numeric_value = find(r"([\d,]+)", total_monthly_raw)
                if numeric_value:
                    total_monthly = int(numeric_value.replace(",", ""))

                    # Tính toán
                    numeric_guarantor = total_monthly * 50 // 100
                    numeric_guarantor_max = total_monthly * 80 // 100

                    # Ghi vào data
                    data.update({
                        "total_monthly": total_monthly,
                        "numeric_guarantor": numeric_guarantor,
                        "numeric_guarantor_max": numeric_guarantor_max,
                    })

                    print(f"💰 Processed pricing:")
                    print(f"   total_monthly = {total_monthly:,}円")
                    print(f"   numeric_guarantor = {numeric_guarantor:,}円 (50%)")
                    print(f"   numeric_guarantor_max = {numeric_guarantor_max:,}円 (80%)")
                else:
                    print(f"⚠️ Could not extract numeric value from: {total_monthly_raw}")

        except Exception as e:
            print(f"❌ Error processing pricing: {e}")

        return data
    
    # Làm sạch các biến temp
    def cleanup_temp_fields(data: Dict[str, Any], html: str) -> Dict[str, Any]:
        """
        Remove temporary fields that shouldn't be in final JSON
        """
        # Remove _html field used for processing
        if '_html' in data:
            del data['_html']
            print("🧹 Cleaned up temporary _html field")
        
        return data
    
    # Xử lý nội dung tĩnh
    def get_static_info(data: Dict[str, Any], html: str) -> Dict[str, Any]:
        # Lấy thông tin của header
        try:
            # Tìm nội dung thẻ h1
            h1_content = find(r'<h1[^>]*>(.*?)</h1>', html)
            
            if h1_content:
                # Loại bỏ các thẻ HTML còn lại và làm sạch
                h1_text = re.sub(r'<[^>]+>', '', h1_content).strip()
                
                pattern = r'^(.+?)\s+(\d+)階(\d+)$'
                match = re.match(pattern, h1_text)
                
                if match:
                    building_name_ja = match.group(1).strip()
                    floor_no = int(match.group(2))
                    room_no = int(match.group(3))
                    
                    data['building_name_ja'] = building_name_ja
                    data['floor_no'] = floor_no
                    data['room_no'] = room_no
                else:
                    print(f"⚠️ Could not parse h1 format: {h1_text}")
            else:
                print("⚠️ No h1 tag found in HTML")       
        except Exception as e:
            print(f"❌ Error extracting static info: {e}")
        
        # Lấy thông tin địa chỉ
        try:
            # Tìm section chứa 所在地
            address_section = find(r'<dt[^>]*>所在地</dt>(.*?)(?=<dt|</dl>|$)', html)
            
            if address_section:
                # Tìm tất cả thẻ dd trong section này
                dd_matches = re.findall(r'<dd[^>]*>(.*?)</dd>', address_section, re.DOTALL | re.IGNORECASE)
                
                if len(dd_matches) >= 2:
                    # Lấy thẻ dd thứ 2 (index 1)
                    address_raw = dd_matches[1]
                    # Loại bỏ thẻ HTML và làm sạch
                    address_text = re.sub(r'<[^>]+>', '', address_raw).strip()
                    
                    print(f"🏠 Found address: {address_text}")
                    
                    # Sử dụng hàm parse_japanese_address để phân tích
                    address_parts = parse_japanese_address(address_text)
                    
                    # Gán các phần địa chỉ vào data
                    if address_parts['prefecture']:
                        data['prefecture'] = address_parts['prefecture']
                    if address_parts['city']:
                        data['city'] = address_parts['city']
                    if address_parts['district']:
                        data['district'] = address_parts['district']
                    if address_parts['chome_banchi']:
                        data['chome_banchi'] = address_parts['chome_banchi']
                    
                    print(f"🏠 Parsed address:")
                    print(f"   prefecture = {address_parts['prefecture']}")
                    print(f"   city = {address_parts['city']}")
                    print(f"   district = {address_parts['district']}")
                    print(f"   chome_banchi = {address_parts['chome_banchi']}")
                    
                else:
                    print(f"⚠️ Found {len(dd_matches)} dd tags, expected at least 2")
            else:
                print("⚠️ No 所在地 section found in HTML") 
        except Exception as e:
            print(f"❌ Error extracting address info: {e}")
        
        # Lấy tiền thuê
        try:
            # Tìm thẻ có class "__rent"
            rent_content = find(r'class="[^"]*__rent[^"]*"[^>]*>(.*?)</[^>]+>', html)
            
            if rent_content:
                # Loại bỏ thẻ HTML và làm sạch
                rent_text = re.sub(r'<[^>]+>', '', rent_content).strip()
                
                # Pattern để tách "505,000円 / 0円"
                rent_pattern = r'([\d,]+)円\s*/\s*([\d,]+)円'
                rent_match = re.search(rent_pattern, rent_text)
                
                if rent_match:
                    monthly_rent = int(rent_match.group(1).replace(',', ''))
                    monthly_maintenance = int(rent_match.group(2).replace(',', ''))
                    
                    data['monthly_rent'] = monthly_rent
                    data['monthly_maintenance'] = monthly_maintenance
            else:
                print("⚠️ No __rent class found in HTML")
        except Exception as e:
            print(f"❌ Error extracting rent info: {e}")
        
        # Lấy depot và key money - sẽ làm sau
        
        # Lấy room type và size 
        try:
            # Tìm section chứa 間取り・面積
            room_info_content = find(r'<dt[^>]*>間取り・面積</dt>\s*<dd[^>]*>(.*?)</dd>', html)
            
            if room_info_content:
                # Loại bỏ thẻ HTML và làm sạch
                room_info_text = re.sub(r'<[^>]+>', '', room_info_content).strip()
                
                # Pattern để tách "1LD･K / 69.26㎡"
                room_pattern = r'^([^/]+?)\s*/\s*([\d.]+)㎡'
                room_match = re.search(room_pattern, room_info_text)
                
                if room_match:
                    room_type = room_match.group(1).strip()
                    size = float(room_match.group(2))
                    
                    data['room_type'] = room_type
                    data['size'] = size
            else:
                print("⚠️ No 間取り・面積 section found in HTML")    
        except Exception as e:
            print(f"❌ Error extracting room info: {e}")
        
        # Lấy thời gian xây dựng 
        try:
            # Tìm section chứa 竣工日
            construction_content = find(r'<dt[^>]*>竣工日</dt>\s*<dd[^>]*>(.*?)</dd>', html)
            
            if construction_content:
                # Loại bỏ thẻ HTML và làm sạch
                construction_text = re.sub(r'<[^>]+>', '', construction_content).strip()
                
                # Pattern để tách năm từ định dạng "1994年08月31日"
                year_pattern = r'(\d{4})年'
                year_match = re.search(year_pattern, construction_text)
                
                if year_match:
                    year = int(year_match.group(1))
                    data['year'] = year                    
                else:
                    print(f"⚠️ Could not extract year from: {construction_text}")
            else:
                print("⚠️ No 竣工日 section found in HTML")
        except Exception as e:
            print(f"❌ Error extracting construction date: {e}")

        # Lấy thời gian khả dụng khi chuyển vào - sẽ làm sau
        
        # Lấy structure và no floor và tầng hầm
        try:
            # Tìm section chứa 規模構造
            structure_content = find(r'<dt[^>]*>規模構造</dt>\s*<dd[^>]*>(.*?)</dd>', html)
            
            if structure_content:
                # Loại bỏ thẻ HTML và làm sạch
                structure_text = re.sub(r'<[^>]+>', '', structure_content).strip()

                structure_pattern = r'^(.*?造)\s*地上(\d+)階(?:地下(\d+)階建?)?'
                structure_match = re.search(structure_pattern, structure_text)
                
                if structure_match:
                    # Trích xuất cấu trúc
                    structure = structure_match.group(1).strip()
                    data['structure'] = structure
                    
                    # Trích xuất số tầng trên mặt đất
                    floors = int(structure_match.group(2))
                    data['floors'] = floors
                    
                    # Trích xuất số tầng hầm (có thể không có)
                    basement_floors_str = structure_match.group(3)
                    if basement_floors_str:
                        basement_floors = int(basement_floors_str)
                        data['basement_floors'] = basement_floors
            else:
                print("⚠️ No 規模構造 section found in HTML")
        except Exception as e:
            print(f"❌ Error extracting structure info: {e}")
            
        # Lấy renewal fee
        try:
            # Tìm thẻ dt chứa "更新料" và thẻ dd ngay sau nó
            renewal_content = find(r'<dt[^>]*>更新料</dt>\s*<dd[^>]*>(.*?)</dd>', html)
            
            if renewal_content:
                # Loại bỏ thẻ HTML và làm sạch
                renewal_text = re.sub(r'<[^>]+>', '', renewal_content).strip()

                months_pattern = r'新賃料の(\d+)ヶ月分'
                months_match = re.search(months_pattern, renewal_text)
                
                if months_match:
                    months_renewal = int(months_match.group(1))
                    data['renewal_new_rent'] = 'Y'
                    data['months_renewal'] = months_renewal                    
            else:
                print("⚠️ No 更新料 section found in HTML")
        except Exception as e:
            print(f"❌ Error extracting renewal fee info: {e}")
        
        # Checkbox Parking - sẽ làm sau
        
        # Lấy hướng căn hộ
        try:
            # Tìm thẻ dt chứa "方位" và thẻ dd ngay sau nó
            direction_content = find(r'<dt[^>]*>方位</dt>\s*<dd[^>]*>(.*?)</dd>', html)
            
            if direction_content:
                # Loại bỏ thẻ HTML và làm sạch
                direction_text = re.sub(r'<[^>]+>', '', direction_content).strip()
                
                # Mapping từ tiếng Nhật sang field name
                direction_mapping = {
                    '北': 'facing_north',
                    '北東': 'facing_northeast', 
                    '東': 'facing_east',
                    '東南': 'facing_southeast',
                    '南': 'facing_south',
                    '南西': 'facing_southwest',
                    '西': 'facing_west',
                    '西北': 'facing_northwest',
                    '北西': 'facing_northwest'  # Alternative notation
                }
                
                # Tìm các hướng có trong text và set Y
                for jp_direction, field_name in direction_mapping.items():
                    if jp_direction in direction_text:
                        data[field_name] = 'Y'
                        break
                else:
                    print(f"⚠️ No recognizable directions found in: {direction_text}")
                    
            else:
                print("⚠️ No 方位 section found in HTML")
        except Exception as e:
            print(f"❌ Error extracting direction info: {e}")
        
        # Lấy other fee khác - sẽ làm sau
        
        # Extract amenities from 専有部・共用部設備 section
        try:
            # Tìm section 専有部・共用部設備 và lấy nội dung dd
            amenities_pattern = r'<dt[^>]*>専有部・共用部設備</dt>\s*<dd[^>]*>(.*?)</dd>'
            amenities_match = re.search(amenities_pattern, html, re.DOTALL | re.IGNORECASE)
            
            if amenities_match:
                amenities_text = amenities_match.group(1)
                # Loại bỏ HTML tags và làm sạch
                amenities_clean = re.sub(r'<[^>]+>', '', amenities_text).strip()
                
                print(f"🏢 Found amenities info: {amenities_clean}")
                
                # Mapping từ tiếng Nhật sang field names trong structure.json
                amenities_mapping = {
                    # Building amenities
                    'フロント': 'concierge',                    # Front desk/Concierge
                    '宅配ロッカー': 'delivery_box',             # Delivery box
                    'オートロック': 'autolock',                 # Auto lock
                    'バイク置場': 'motorcycle_parking',         # Motorcycle parking
                    '敷地内ごみ置場': 'cleaning_service',       # On-site garbage area
                    'エレベータ': 'elevator',                   # Elevator
                    '24時間管理': 'cleaning_service',           # 24-hour management
                    '防犯カメラ': 'autolock',                   # Security camera (maps to autolock as security feature)
                    'セキュリティシステム': 'autolock',          # Security system
                    
                    # Room amenities
                    'バルコニー': 'balcony',                    # Balcony
                    'バストイレ': 'unit_bath',                 # Unit bath (bath + toilet)
                    '洗面所独立': 'separate_toilet',           # Separate washroom
                    '室内洗濯機置場': 'washing_machine',        # Indoor washing machine space
                    'バス有': 'bath',                          # Bath available
                    '浴室乾燥機': 'bath_water_heater',         # Bathroom dryer
                    '給湯追い焚き有': 'auto_fill_bath',         # Hot water reheating
                    
                    # Kitchen & Appliances
                    'キッチン有': 'system_kitchen',            # Kitchen available
                    'コンロ有': 'range',                       # Stove/Range available
                    'グリル': 'oven',                          # Grill
                    'オープン': 'counter_kitchen',             # Open kitchen
                    
                    # Internet & Media
                    'インターネット': 'internet_broadband',     # Internet
                    'BS': 'bs',                               # BS satellite
                    'CS': 'cable',                            # CS satellite
                    
                    # Special features
                    'ピアノ可': 'furnished',                   # Piano allowed (maps to furnished)
                    'ウォークインクロゼット': 'storage',        # Walk-in closet
                    
                    # Additional mappings - có thể thêm dễ dàng
                    'ペット可': 'pets',                        # Pets allowed
                    'エアコン': 'aircon',                      # Air conditioning
                    'フローリング': 'flooring',                # Flooring
                    'システムキッチン': 'system_kitchen',       # System kitchen
                    'シャワー': 'shower',                      # Shower
                    'ガス': 'gas',                            # Gas
                    'WiFi': 'internet_wifi',                  # WiFi
                    'Wi-Fi': 'internet_wifi',                 # WiFi (alternative)
                    'インターホン': 'autolock',                # Intercom
                    'TVモニター付インターホン': 'autolock',      # TV monitor intercom
                    '宅配BOX': 'delivery_box',                # Delivery box (alternative)
                    'ゴミ置場': 'cleaning_service',           # Garbage area
                    '温水洗浄便座': 'washlet',                 # Washlet toilet
                    '床暖房': 'underfloor_heating',           # Underfloor heating
                    '食器洗い乾燥機': 'dishwasher',           # Dishwasher
                    'IHクッキングヒーター': 'induction_cooker', # Induction cooker
                    '追い焚き機能': 'auto_fill_bath',         # Bath reheating function
                    '宅配ボックス': 'delivery_box',           # Delivery box (alternative spelling)
                    'オール電化': 'all_electric',             # All electric
                    'カウンターキッチン': 'counter_kitchen',   # Counter kitchen
                    'ロフト': 'loft',                         # Loft
                    'ルーフバルコニー': 'roof_balcony',        # Roof balcony
                    'ベランダ': 'veranda',                    # Veranda
                    '庭': 'yard',                             # Yard
                    'SOHO可': 'soho',                         # SOHO allowed
                    '女性限定': 'female_only',                # Female only
                    '学生可': 'student_friendly',             # Student friendly
                }
                
                # Tìm và set các amenities
                found_amenities = []
                for jp_amenity, field_name in amenities_mapping.items():
                    if jp_amenity in amenities_clean:
                        data[field_name] = 'Y'
                        found_amenities.append(f"{jp_amenity} → {field_name}")
                
                if found_amenities:
                    print(f"🏢 Set amenities to Y:")
                    for amenity in found_amenities:
                        print(f"   {amenity}")
                else:
                    print(f"⚠️ No recognizable amenities found in: {amenities_clean}")
                    
            else:
                print("⚠️ No 専有部・共用部設備 section found")       
        except Exception as e:
            print(f"❌ Error extracting amenities info: {e}")
        
        # Extract building description from 備考 section
        try:
            # Tìm section 備考 và lấy nội dung dd
            description_pattern = r'<dt[^>]*>備考</dt>\s*<dd[^>]*>(.*?)</dd>'
            description_match = re.search(description_pattern, html, re.DOTALL | re.IGNORECASE)
            
            if description_match:
                description_text = description_match.group(1)
                # Loại bỏ HTML tags và làm sạch
                description_clean = re.sub(r'<[^>]+>', '', description_text).strip()
                
                if description_clean:
                    data['building_notes'] = description_clean  
        except Exception as e:
            print(f"❌ Error extracting building description: {e}")
        return data
    
    # Xử lý trước khi dùng 
    extractor.add_pre_hook(pass_html)
    
    # Xử lý sau khi dùng
    list_funcs = [
        get_static_info,
        convert_coordinates, 
        set_default_amenities,
        process_pricing,
        extract_image,
        cleanup_temp_fields,
    ] 
    
    for func in list_funcs:
        extractor.add_post_hook(lambda d, f=func: wrapper(d, f))
    
    return extractor