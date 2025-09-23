"""
Amenity information extractor from HTML
"""

import re
from typing import Dict, Any
from ..models import AmenityKeywords


class AmenityExtractor:
    """Extract amenity information including parking status"""
    
    def __init__(self):
        self.amenity_keywords = AmenityKeywords.AMENITY_KEYWORDS
    
    def extract_amenities(self, html: str, data: Dict[str, Any]) -> Dict[str, Any]:
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
    
    def _get_context_around_keyword(self, text: str, keyword: str, context_length: int = 50) -> str:
        """Get context around a keyword for better analysis"""
        index = text.find(keyword)
        if index == -1:
            return ""
        
        start = max(0, index - context_length)
        end = min(len(text), index + len(keyword) + context_length)
        return text[start:end]