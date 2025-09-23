"""
Address information parser from Markdown content
"""

import re
from typing import Dict, Any


class AddressParser:
    """Parse address information from markdown content"""
    
    def extract_address_info(self, line: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract address information từ line"""
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
                
                # Improved chome-banchi extraction with more patterns
                data = self._extract_chome_banchi(remaining, data)
                break
        
        return data
    
    def _extract_chome_banchi(self, remaining: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract chome-banchi information"""
        chome_patterns = [
            r'(\d+丁目\d+番\d+号)',  # Full format: 三丁目２０番３号
            r'(\d+丁目\d+番)',       # Partial: 三丁目２０番
            r'(\d+丁目)',            # Just chome: 三丁目
            r'([一二三四五六七八九十]+丁目[一二三四五六七八九十〇]+番[一二三四五六七八九十〇]+号)', # Kanji numbers
            r'([一二三四五六七八九十]+丁目[一二三四五六七八九十〇]+番)', # Kanji partial
            r'([一二三四五六七八九十]+丁目)'  # Kanji chome only
        ]
        
        for pattern in chome_patterns:
            chome_match = re.search(pattern, remaining)
            if chome_match and not data['chome_banchi']:
                data['chome_banchi'] = chome_match.group(1)
                break
        
        return data