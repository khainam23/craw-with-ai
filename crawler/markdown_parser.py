"""
Module xử lý parse Markdown content
"""

import re
from typing import Dict, Any
from .config import CrawlerConfig


class MarkdownParser:
    """Class xử lý parse markdown content và extract dữ liệu"""
    
    def __init__(self):
        self.config = CrawlerConfig()
    
    def extract_from_markdown(self, markdown: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract additional data từ markdown content
        """
        if not markdown:
            return data
        
        lines = markdown.split('\n')
        station_count = 1
        
        for line in lines:
            line = line.strip()
            
            # Extract address components
            data = self._extract_address_info(line, data)
            
            # Extract station information
            station_count = self._extract_station_info(line, data, station_count)
            
            # Extract building type
            data = self._extract_building_type(line, data)
            
            # Extract available date
            data = self._extract_available_date(line, data)
            
            # Extract postcode
            data = self._extract_postcode(line, data)
            
            # Extract unit number
            data = self._extract_unit_number(line, data)
        
        return data
    
    def _extract_address_info(self, line: str, data: Dict[str, Any]) -> Dict[str, Any]:
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
                break
        
        return data
    
    def _extract_station_info(self, line: str, data: Dict[str, Any], station_count: int) -> int:
        """Extract station information từ line"""
        if '駅' in line and station_count <= self.config.MAX_STATIONS:
            # Flexible station name extraction patterns
            station_patterns = [
                # Station with walking time patterns
                r'([ぁ-ゟ一-龯ァ-ヾa-zA-Z]{2,}駅).*?(\d+)\s*分',
                r'([ぁ-ゟ一-龯ァ-ヾa-zA-Z]{2,}駅).*?徒歩(\d+)分',
                
                # General station patterns
                r'([ぁ-ゟ一-龯ァ-ヾ]{2,}駅)',  # Japanese characters (at least 2) + 駅
                r'([a-zA-Z]{2,}駅)',  # English (at least 2) + 駅
            ]
            
            for pattern in station_patterns:
                station_matches = re.findall(pattern, line)
                for match in station_matches:
                    if isinstance(match, tuple):
                        station_name, walk_time = match[0], match[1] if len(match) > 1 else None
                    else:
                        station_name, walk_time = match, None
                    
                    # Validate station name
                    if self._is_valid_station_name(station_name):
                        station_field = f'station_name_{station_count}'
                        if not data[station_field]:
                            data[station_field] = station_name
                            
                            # Set walk time if found
                            if walk_time:
                                walk_field = f'walk_{station_count}'
                                if not data[walk_field]:
                                    data[walk_field] = walk_time
                            
                            # Extract train line
                            self._extract_train_line(line, data, station_count)
                            
                            # Extract transportation times (if not already set)
                            if not walk_time:
                                self._extract_transportation_times(line, data, station_count)
                            
                            station_count += 1
                            if station_count > self.config.MAX_STATIONS:
                                break
        
        return station_count
    
    def _extract_train_line(self, line: str, data: Dict[str, Any], station_count: int):
        """Extract train line information"""
        line_patterns = [
            r'([^線\s]+線)',
            r'JR([^駅\s]+)',
            r'(東急[^駅\s]+)',
            r'(京急[^駅\s]+)',
            r'(小田急[^駅\s]+)'
        ]
        
        for pattern in line_patterns:
            line_match = re.search(pattern, line)
            if line_match:
                train_line_field = f'train_line_name_{station_count}'
                if not data[train_line_field]:
                    data[train_line_field] = line_match.group(1)
                break
    
    def _extract_transportation_times(self, line: str, data: Dict[str, Any], station_count: int):
        """Extract transportation times"""
        # Extract walking time
        walk_match = re.search(r'徒歩(\d+)分', line)
        if walk_match:
            walk_field = f'walk_{station_count}'
            if not data[walk_field]:
                data[walk_field] = walk_match.group(1)
        
        # Extract bus time
        bus_match = re.search(r'バス(\d+)分', line)
        if bus_match:
            bus_field = f'bus_{station_count}'
            if not data[bus_field]:
                data[bus_field] = bus_match.group(1)
        
        # Extract car time
        car_match = re.search(r'車(\d+)分', line)
        if car_match:
            car_field = f'car_{station_count}'
            if not data[car_field]:
                data[car_field] = car_match.group(1)
    
    def _extract_building_type(self, line: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract building type từ line"""
        if not data['building_type']:
            building_types = ['マンション', 'アパート', '一戸建て', 'テラスハウス', 'タウンハウス']
            for building_type in building_types:
                if building_type in line:
                    data['building_type'] = building_type
                    break
        
        return data
    
    def _extract_available_date(self, line: str, data: Dict[str, Any]) -> Dict[str, Any]:
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
    
    def _extract_postcode(self, line: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract postcode từ line"""
        if not data['postcode']:
            postcode_match = re.search(r'〒(\d{3}-\d{4})', line)
            if postcode_match:
                data['postcode'] = postcode_match.group(1)
        
        return data
    
    def _extract_unit_number(self, line: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract unit number từ line"""
        if not data['unit_no']:
            unit_patterns = [
                r'(\d+号室)',
                r'部屋番号[：:]\s*(\d+)',
                r'Unit\s*(\d+)'
            ]
            
            for pattern in unit_patterns:
                unit_match = re.search(pattern, line, re.IGNORECASE)
                if unit_match:
                    data['unit_no'] = unit_match.group(1)
                    break
        
        return data
    
    def _is_valid_station_name(self, station_name: str) -> bool:
        """Validate if station name is reasonable and not a false positive"""
        if not station_name or len(station_name) < 3:
            return False
            
        # Invalid patterns that commonly appear in false positives
        invalid_patterns = [
            '建物', '出入口', '起点', '掲載', '徒歩分数', '分数', '建物の',
            'minutes', 'foot', 'walk', 'station', '駅駅', '・駅', '、駅',
            '[駅', '駅', '建物の出入口を起点とし駅', '起点とし駅', 
            '出入口を起点とし駅', '掲載の徒歩分数は、建物の出入口を起点とし駅'
        ]
        
        # Check if station name contains any invalid patterns
        for invalid in invalid_patterns:
            if invalid in station_name:
                return False
        
        # Additional validation: station name should not be too long
        if len(station_name) > 15:
            return False
            
        # Should contain at least one Japanese character or be a known English station
        has_japanese = any('\u3040' <= char <= '\u309F' or '\u30A0' <= char <= '\u30FF' or '\u4E00' <= char <= '\u9FAF' for char in station_name)
        has_english = any('a' <= char.lower() <= 'z' for char in station_name)
        
        return has_japanese or has_english