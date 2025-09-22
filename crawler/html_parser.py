"""
Module xử lý parse HTML và extract dữ liệu
"""

import re
from typing import Dict, Any
from .data_schema import AmenityKeywords


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
        """Extract amenities từ HTML"""
        for field, keywords in self.amenity_keywords.items():
            for keyword in keywords:
                if keyword in html:
                    data[field] = 'Y'
                    break
            if data[field] != 'Y':
                data[field] = None  # Keep as None if not found
        
        return data
    
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