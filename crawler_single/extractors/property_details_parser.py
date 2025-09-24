"""
Property details parser from Markdown content
"""

import re
from typing import Dict, Any


class PropertyDetailsParser:
    """Parse property details like building type, available date, postcode, unit number"""
    
    def extract_building_type(self, line: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract building type từ line"""
        if not data['building_type']:
            building_types = ['マンション', 'アパート', '一戸建て', 'テラスハウス', 'タウンハウス']
            for building_type in building_types:
                if building_type in line:
                    data['building_type'] = building_type
                    break
        
        return data
    
    def extract_available_date(self, line: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract available date từ line"""
        if not data['available_from']:
            date_patterns = [
                r'入居可能日[：:]\s*([^\n]+)',
                r'(\d{4}年\d{1,2}月\d{1,2}日)',
                r'(\d{1,2}月\d{1,2}日)',  # Month and day only
                r'(\d{1,2}月上旬)',       # Early month
                r'(\d{1,2}月中旬)',       # Mid month  
                r'(\d{1,2}月下旬)',       # Late month
                r'(\d{1,2}月末)',         # End of month
                r'即入居可',
                r'相談',
                r'要相談'
            ]
            
            for pattern in date_patterns:
                date_match = re.search(pattern, line)
                if date_match:
                    if pattern in [r'即入居可']:
                        data['available_from'] = '即入居可'
                    elif pattern in [r'相談', r'要相談']:
                        data['available_from'] = '相談'
                    else:
                        data['available_from'] = date_match.group(1).strip()
                    break
        
        return data