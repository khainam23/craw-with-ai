"""
Module xử lý parse HTML và extract dữ liệu
"""

import re
from typing import Dict, Any
from .models import AmenityKeywords


class HTMLParser:
    """Class xử lý parse HTML và extract dữ liệu property"""
    
    def __init__(self):
        self.amenity_keywords = AmenityKeywords.AMENITY_KEYWORDS
    
    def extract_from_html_patterns(self, html: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract structured data từ HTML patterns
        """
        if not html:
            return data
        
        # Extract rent patterns
        data = self._extract_rent_patterns(html, data)
        
        # Extract size patterns
        data = self._extract_size_patterns(html, data)
        
        # Extract floor patterns
        data = self._extract_floor_patterns(html, data)
        
        # Extract year patterns
        data = self._extract_year_patterns(html, data)
        
        # Extract amenities
        data = self._extract_amenities(html, data)
        
        # Extract pricing information
        data = self._extract_pricing_info(html, data)
        
        # Extract building structure
        data = self._extract_building_info(html, data)
        
        # Extract coordinates
        data = self._extract_coordinates(html, data)
        
        # Extract address information from HTML
        data = self._extract_address_from_html(html, data)
        
        # Extract available date from HTML
        data = self._extract_available_date_from_html(html, data)
        
        # Extract station information from HTML
        data = self._extract_station_from_html(html, data)
        
        return data
    
    def _extract_rent_patterns(self, html: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract rent patterns từ HTML"""
        rent_patterns = [
            r'家賃[：:]\s*(\d+(?:,\d+)?)万円',
            r'賃料[：:]\s*(\d+(?:,\d+)?)万円',
            r'rent[：:]\s*¥([\d,]+)',
            r'(\d+(?:,\d+)?)万円/月'
        ]
        
        for pattern in rent_patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            if matches:
                rent_value = matches[0].replace(',', '')
                try:
                    # Convert to monthly rent in yen
                    if '万円' in pattern:
                        data['monthly_rent'] = str(int(float(rent_value) * 10000))
                    else:
                        data['monthly_rent'] = rent_value
                except ValueError:
                    data['monthly_rent'] = rent_value
                break
        
        return data
    
    def _extract_size_patterns(self, html: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract size patterns từ HTML"""
        size_patterns = [
            r'(\d+(?:\.\d+)?)\s*㎡',
            r'(\d+(?:\.\d+)?)\s*m²',
            r'専有面積[：:]\s*(\d+(?:\.\d+)?)',
            r'面積[：:]\s*(\d+(?:\.\d+)?)'
        ]
        
        for pattern in size_patterns:
            matches = re.findall(pattern, html)
            if matches:
                data['size'] = matches[0]
                break
        
        return data
    
    def _extract_floor_patterns(self, html: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract floor patterns từ HTML"""
        floor_patterns = [
            r'(\d+)階',
            r'(\d+)F'
        ]
        
        for pattern in floor_patterns:
            matches = re.findall(pattern, html)
            if matches:
                data['floor_no'] = matches[0]
                break
        
        return data
    
    def _extract_year_patterns(self, html: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract year patterns từ HTML"""
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
        
        return data
    
    def _extract_amenities(self, html: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract amenities từ HTML with improved accuracy"""
        for field, keywords in self.amenity_keywords.items():
            found = False
            for keyword in keywords:
                if keyword in html:
                    # Special handling for parking - check for negative indicators
                    if field == 'parking':
                        parking_value = self._extract_parking_status(html, keyword)
                        if parking_value is not None:
                            data[field] = parking_value
                            found = True
                            break
                    else:
                        data[field] = 'Y'
                        found = True
                        break
            
            if not found:
                data[field] = None  # Keep as None if not found
        
        return data
    
    def _get_context_around_keyword(self, text: str, keyword: str, context_length: int = 50) -> str:
        """Get context around a keyword for better analysis"""
        index = text.find(keyword)
        if index == -1:
            return ""
        
        start = max(0, index - context_length)
        end = min(len(text), index + len(keyword) + context_length)
        return text[start:end]
    
    def _extract_pricing_info(self, html: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract pricing information từ HTML"""
        # Extract deposit patterns
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
        
        return data
    
    def _extract_building_info(self, html: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract building information từ HTML"""
        # Extract building structure with flexible patterns
        data = self._extract_building_structure(html, data)
        
        # Extract building floors with more patterns
        building_floor_patterns = [
            r'地上(\d+)階建?',
            r'(\d+)階建て?',
            r'(\d+)階建',
            r'building.*?(\d+)\s*floors?'
        ]
        
        for pattern in building_floor_patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            if matches:
                data['floors'] = matches[0]
                break
        
        # Extract building type with more detail
        if not data.get('building_type'):
            building_type_patterns = [
                r'(鉄筋コンクリート造\s*地上\d+階建)',
                r'(マンション)',
                r'(アパート)',
                r'(一戸建て)',
                r'(テラスハウス)',
                r'(タウンハウス)'
            ]
            
            for pattern in building_type_patterns:
                matches = re.findall(pattern, html)
                if matches:
                    data['building_type'] = matches[0]
                    break
        
        return data
    
    def _extract_coordinates(self, html: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract coordinates từ HTML"""
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
    
    def _extract_parking_status(self, html: str, keyword: str) -> str:
        """Extract parking status with flexible patterns"""
        # Get context around parking keyword
        parking_context = self._get_context_around_keyword(html, keyword, 200)
        
        # Define patterns for different parking statuses
        no_parking_patterns = [
            r'駐車場[：:\s]*無',
            r'駐車場[：:\s]*なし',
            r'駐車場[：:\s]*－',
            r'駐車場[：:\s]*None',
            r'駐車場[：:\s]*×',
            r'parking[：:\s]*no',
            r'parking[：:\s]*none',
            r'no\s+parking'
        ]
        
        has_parking_patterns = [
            r'駐車場[：:\s]*有',
            r'駐車場[：:\s]*あり',
            r'駐車場[：:\s]*○',
            r'駐車場[：:\s]*◯',
            r'駐車場[：:\s]*\d+台',
            r'parking[：:\s]*yes',
            r'parking[：:\s]*available',
            r'\d+\s*台'
        ]
        
        # Check for explicit no parking patterns
        for pattern in no_parking_patterns:
            if re.search(pattern, parking_context, re.IGNORECASE):
                return 'N'
        
        # Check for explicit has parking patterns
        for pattern in has_parking_patterns:
            if re.search(pattern, parking_context, re.IGNORECASE):
                return 'Y'
        
        # Fallback: count negative vs positive indicators
        negative_indicators = ['無', 'なし', 'ない', '不可', 'No', '×', '－', 'None']
        positive_indicators = ['有', 'あり', '可', 'Yes', '○', '◯', '台']
        
        neg_count = sum(1 for neg in negative_indicators if neg in parking_context)
        pos_count = sum(1 for pos in positive_indicators if pos in parking_context)
        
        if neg_count > pos_count:
            return 'N'
        elif pos_count > 0:
            return 'Y'
        
        return None
    
    def _extract_building_structure(self, html: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract building structure with flexible patterns"""
        if data.get('structure'):
            return data
            
        # Comprehensive structure patterns
        structure_patterns = [
            # Specific detailed patterns
            r'鉄筋コンクリート造[^<\n]*地上\d+階建[^<\n]*',
            r'RC造[^<\n]*地上\d+階建[^<\n]*',
            r'SRC造[^<\n]*地上\d+階建[^<\n]*',
            
            # General structure patterns
            r'構造[：:\s]*([^<\n]+)',
            r'(鉄筋コンクリート造[^<\n]*)',
            r'(RC造[^<\n]*)',
            r'(SRC造[^<\n]*)',
            r'(鉄骨造[^<\n]*)',
            r'(木造[^<\n]*)',
            r'(軽量鉄骨造[^<\n]*)',
            r'structure[：:\s]*([^<\n]+)',
            
            # Simple structure types
            r'(RC|SRC|木造|鉄骨|軽量鉄骨)(?![a-zA-Z])'
        ]
        
        for pattern in structure_patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            if matches:
                structure_text = matches[0].strip()
                # Clean up the structure text
                structure_text = re.sub(r'<[^>]+>', '', structure_text)
                structure_text = re.sub(r'&nbsp;', ' ', structure_text)
                structure_text = re.sub(r'\s+', ' ', structure_text).strip()
                
                if len(structure_text) > 1:  # Avoid single characters
                    data['structure'] = structure_text
                    break
        
        return data
    
    def _extract_address_from_html(self, html: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract complete address information from HTML with flexible patterns"""
        # Look for complete address patterns in HTML
        address_patterns = [
            # Hidden input patterns (most reliable)
            r'BUKKEN_ADDR[^>]*value="([^"]*)"',
            r'value="([^"]*[都道府県][^"]*)"',
            
            # General Japanese address patterns
            r'(東京都[^区市]+[区市][^丁町]+[丁町目][^番]+番[^号]*号?)',
            r'(大阪府[^区市]+[区市][^丁町]+[丁町目][^番]+番[^号]*号?)',
            r'(神奈川県[^区市]+[区市][^丁町]+[丁町目][^番]+番[^号]*号?)',
            r'([都道府県][^区市]+[区市][^丁町]+[丁町目][^番]+番[^号]*号?)',
            
            # Broader patterns
            r'([都道府県][^<\n]{10,50})',
            r'location[^>]*>([^<]*[都道府県][^<]*)',
            r'住所[：:\s]*([^<\n]+)'
        ]
        
        for pattern in address_patterns:
            matches = re.findall(pattern, html)
            if matches:
                full_address = matches[0].strip()
                if len(full_address) > 5:  # Reasonable address length
                    self._parse_japanese_address(full_address, data)
                    break
        
        return data
    
    def _parse_japanese_address(self, address: str, data: Dict[str, Any]):
        """Parse Japanese address into components"""
        # Extract prefecture
        prefecture_patterns = [
            '東京都', '大阪府', '京都府', '北海道',
            '神奈川県', '愛知県', '兵庫県', '福岡県', '埼玉県', '千葉県',
            '茨城県', '栃木県', '群馬県', '静岡県', '三重県', '滋賀県',
            '奈良県', '和歌山県', '鳥取県', '島根県', '岡山県', '広島県',
            '山口県', '徳島県', '香川県', '愛媛県', '高知県', '佐賀県',
            '長崎県', '熊本県', '大分県', '宮崎県', '鹿児島県', '沖縄県',
            '青森県', '岩手県', '宮城県', '秋田県', '山形県', '福島県',
            '新潟県', '富山県', '石川県', '福井県', '山梨県', '長野県',
            '岐阜県'
        ]
        
        for prefecture in prefecture_patterns:
            if prefecture in address and not data.get('prefecture'):
                data['prefecture'] = prefecture
                remaining = address.replace(prefecture, '')
                
                # Extract district/city
                district_match = re.search(r'([^区市]+[区市])', remaining)
                if district_match and not data.get('district'):
                    data['district'] = district_match.group(1)
                    remaining = remaining.replace(district_match.group(1), '')
                
                # Extract chome-banchi
                chome_patterns = [
                    r'([^丁町]+[丁町目][^番]+番[^号]*号?)',
                    r'(\d+丁目\d+番\d+号)',
                    r'([一二三四五六七八九十]+丁目[一二三四五六七八九十〇０-９]+番[一二三四五六七八九十〇０-９]+号)',
                    r'([^丁町]+[丁町目])'
                ]
                
                for pattern in chome_patterns:
                    chome_match = re.search(pattern, remaining)
                    if chome_match and not data.get('chome_banchi'):
                        data['chome_banchi'] = chome_match.group(1)
                        break
                break
    
    def _extract_available_date_from_html(self, html: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract available date from HTML with flexible patterns"""
        if data.get('available_from'):
            return data
            
        # Comprehensive date patterns - prioritize specific patterns first
        date_patterns = [
            # Specific completion date patterns (highest priority)
            r'Completion date[^>]*>([^<]+)',
            r'completion[：:\s]*date[^>]*>([^<]+)',
            r'完成予定[：:\s]*([^<\n]+)',
            
            # Japanese date formats
            r'(\d{4}年\d{1,2}月\d{1,2}日)',
            r'(\d{1,2}月\d{1,2}日)',
            r'(\d{1,2}月中旬)',
            r'(\d{1,2}月上旬)',
            r'(\d{1,2}月下旬)',
            r'(\d{1,2}月末)',
            
            # English date formats
            r'(\w+ \d{1,2}, \d{4})',
            
            # Special cases
            r'(即入居可)',
            r'(相談)',
            r'(要相談)',
            r'(入居中)',
            r'(空室)',
            
            # Context-based patterns
            r'入居可能日[：:\s]*([^<\n]+)',
            r'available[：:\s]*([^<\n]+)',
            
            # Low priority patterns (avoid false positives)
            r'(\d{1,2}/\d{1,2}/\d{4})',
            r'(\d{4}-\d{1,2}-\d{1,2})'
        ]
        
        for pattern in date_patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            if matches:
                date_value = matches[0].strip()
                # Convert and normalize date
                normalized_date = self._normalize_date(date_value)
                if normalized_date:
                    data['available_from'] = normalized_date
                    break
        
        return data
    
    def _normalize_date(self, date_str: str) -> str:
        """Normalize date string to consistent format"""
        date_str = date_str.strip()
        
        # Direct mappings
        direct_mappings = {
            '即入居可': '即入居可',
            '相談': '相談',
            '要相談': '相談',
            '入居中': '入居中',
            '空室': '即入居可'
        }
        
        if date_str in direct_mappings:
            return direct_mappings[date_str]
        
        # Month conversions
        month_mappings = {
            'January': '1月', 'February': '2月', 'March': '3月', 'April': '4月',
            'May': '5月', 'June': '6月', 'July': '7月', 'August': '8月',
            'September': '9月', 'October': '10月', 'November': '11月', 'December': '12月'
        }
        
        for eng_month, jp_month in month_mappings.items():
            if eng_month in date_str:
                # Convert "October 15, 2025" to "10月中旬"
                if '15' in date_str or '中' in date_str:
                    return f"{jp_month}中旬"
                elif any(day in date_str for day in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']):
                    return f"{jp_month}上旬"
                elif any(day in date_str for day in ['20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31']):
                    return f"{jp_month}下旬"
                else:
                    return f"{jp_month}中旬"
        
        return date_str
    
    def _extract_station_from_html(self, html: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract station information from HTML with flexible patterns"""
        # Comprehensive station patterns
        station_patterns = [
            # English patterns
            r'([^<>\s]+)\s+(\d+)\s*minutes?\s*on\s*foot',
            r'([^<>\s]+駅).*?(\d+)\s*minutes?\s*on\s*foot',
            
            # Japanese patterns
            r'([^<>\s]+駅).*?徒歩(\d+)分',
            r'([^<>\s]+駅)[^<\n]*(\d+)分',
            
            # General station patterns
            r'([ぁ-ゟ一-龯ァ-ヾ]{2,}駅)',
            r'([a-zA-Z]{2,}駅)'
        ]
        
        station_count = 1
        found_stations = set()
        
        for pattern in station_patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple) and len(match) >= 2:
                    station_name, walk_time = match[0], match[1]
                elif isinstance(match, tuple):
                    station_name, walk_time = match[0], None
                else:
                    station_name, walk_time = match, None
                
                # Clean station name
                station_name = re.sub(r'<[^>]+>', '', station_name).strip()
                
                # Validate station name
                if (self._is_valid_station_name(station_name) and 
                    station_name not in found_stations and 
                    station_count <= 5):
                    
                    station_field = f'station_name_{station_count}'
                    walk_field = f'walk_{station_count}'
                    
                    if not data.get(station_field):
                        data[station_field] = station_name
                        found_stations.add(station_name)
                        
                        if walk_time and not data.get(walk_field):
                            data[walk_field] = str(walk_time)
                        
                        # Extract train line
                        self._extract_train_line_from_html(html, station_name, data, station_count)
                        
                        station_count += 1
        
        return data
    
    def _is_valid_station_name(self, station_name: str) -> bool:
        """Validate if station name is reasonable"""
        if not station_name or len(station_name) < 3:
            return False
            
        # Invalid patterns
        invalid_patterns = [
            '建物', '出入口', '起点', '掲載', '徒歩分数', '分数', '建物の',
            'minutes', 'foot', 'walk', 'station', '駅駅', '・駅', '、駅'
        ]
        
        return not any(invalid in station_name for invalid in invalid_patterns)
    
    def _extract_train_line_from_html(self, html: str, station_name: str, data: Dict[str, Any], station_count: int):
        """Extract train line information from HTML context around station"""
        # Get context around the station name
        station_context = self._get_context_around_keyword(html, station_name, 300)
        
        # Comprehensive train line patterns
        line_patterns = [
            # Specific line patterns
            r'Seibu Railway\s*Seibu Yurakucho',
            r'JR\s*([^駅\s<]+)',
            r'東急\s*([^駅\s<]+)',
            r'京急\s*([^駅\s<]+)',
            r'小田急\s*([^駅\s<]+)',
            r'西武\s*([^駅\s<]+)',
            r'東京メトロ\s*([^駅\s<]+)',
            r'都営\s*([^駅\s<]+)',
            
            # General line patterns
            r'([^線\s<]{2,}線)',
            r'line[：:\s]*([^<\n]+)'
        ]
        
        train_line_field = f'train_line_name_{station_count}'
        if not data.get(train_line_field):
            for pattern in line_patterns:
                line_match = re.search(pattern, station_context, re.IGNORECASE)
                if line_match:
                    line_name = line_match.group(1) if line_match.groups() else line_match.group(0)
                    
                    # Clean HTML tags and attributes
                    line_name = re.sub(r'<[^>]+>', '', line_name)
                    line_name = re.sub(r'class="[^"]*">', '', line_name)
                    line_name = re.sub(r'["\'>]', '', line_name)
                    line_name = line_name.strip()
                    
                    # Normalize line names
                    line_name = self._normalize_train_line_name(line_name)
                    
                    if line_name and len(line_name) > 1:
                        data[train_line_field] = line_name
                        break
    
    def _normalize_train_line_name(self, line_name: str) -> str:
        """Normalize train line names"""
        if not line_name:
            return line_name
            
        # Remove common HTML artifacts and prefixes
        line_name = re.sub(r'sys-tags\d*', '', line_name)
        line_name = re.sub(r'class=', '', line_name)
        line_name = re.sub(r'^["\'>]+|["\'>]+$', '', line_name)
        line_name = line_name.strip()
        
        # Common normalizations
        normalizations = {
            'Seibu Railway Seibu Yurakucho': '西武有楽町線',
            'Seibu Yurakucho': '西武有楽町線',
            'Yurakucho': '有楽町線',
            'Yamanote': '山手線',
            'Chuo': '中央線',
            'Keihin-Tohoku': '京浜東北線',
            'Ikebukuro': '池袋線'
        }
        
        # Check for English to Japanese conversions
        for eng, jp in normalizations.items():
            if eng.lower() in line_name.lower():
                return jp
        
        # If already in Japanese and reasonable length, return as is
        if any('\u3040' <= char <= '\u309F' or '\u30A0' <= char <= '\u30FF' or '\u4E00' <= char <= '\u9FAF' for char in line_name):
            if len(line_name) <= 10:  # Reasonable line name length
                return line_name
        
        return line_name