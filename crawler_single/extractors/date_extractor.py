"""
Date information extractor from HTML
"""

import re
from typing import Dict, Any


class DateExtractor:
    """Extract available dates from HTML"""
    
    def extract_available_date_from_html(self, html: str, data: Dict[str, Any]) -> Dict[str, Any]:
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