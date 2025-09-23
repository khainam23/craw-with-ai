"""
Date and station information extractor from HTML
"""

import re
from typing import Dict, Any


class DateStationExtractor:
    """Extract available dates and station information from HTML"""
    
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
    
    def extract_station_from_html(self, html: str, data: Dict[str, Any]) -> Dict[str, Any]:
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
    
    def _get_context_around_keyword(self, text: str, keyword: str, context_length: int = 50) -> str:
        """Get context around a keyword for better analysis"""
        index = text.find(keyword)
        if index == -1:
            return ""
        
        start = max(0, index - context_length)
        end = min(len(text), index + len(keyword) + context_length)
        return text[start:end]