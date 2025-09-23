"""
Location information extractor from HTML
"""

import re
from typing import Dict, Any


class LocationExtractor:
    """Extract location information like coordinates and address"""
    
    def extract_coordinates(self, html: str, data: Dict[str, Any]) -> Dict[str, Any]:
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
    
    def extract_address_from_html(self, html: str, data: Dict[str, Any]) -> Dict[str, Any]:
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