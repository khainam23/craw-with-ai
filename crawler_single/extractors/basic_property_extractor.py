"""
Basic property information extractor from HTML
"""

import re
from typing import Dict, Any


class BasicPropertyExtractor:
    """Extract basic property information like rent, size, floor, year"""
    
    def extract_rent_patterns(self, html: str, data: Dict[str, Any]) -> Dict[str, Any]:
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
    
    def extract_size_patterns(self, html: str, data: Dict[str, Any]) -> Dict[str, Any]:
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
    
    def extract_floor_patterns(self, html: str, data: Dict[str, Any]) -> Dict[str, Any]:
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
    
    def extract_year_patterns(self, html: str, data: Dict[str, Any]) -> Dict[str, Any]:
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