"""
Basic property information extractor from HTML
"""

import re
from typing import Dict, Any


class BasicPropertyExtractor:
    """Extract basic property information like rent, size, floor, year"""
    
    def extract_rent_patterns(self, html: str, data: Dict[str, Any]) -> Dict[str, Any]:
        # Pattern 1: "賃料・管理費・共益費" followed by rent/management fee
        # Matches: <dt>賃料・管理費・共益費</dt><dd class="__rent"><em>250,000円</em> / 10,000円</dd>
        rent_management_pattern = r'賃料[・･]管理費[・･]共益費.*?<em>([\d,]+)円</em>\s*/\s*([\d,]+)円'
        match = re.search(rent_management_pattern, html, re.DOTALL)
        if match:
            rent = match.group(1).replace(',', '')
            monthly_maintenance = match.group(2).replace(',', '')
            data['monthly_rent'] = int(rent)
            data['monthly_maintenance'] = int(monthly_maintenance)
            return data
        
        # Pattern 2: More general "賃料・管理費・共益費" pattern without <em> tags
        rent_management_pattern2 = r'賃料[・･]管理費[・･]共益費.*?([\d,]+)円\s*/\s*([\d,]+)円'
        match = re.search(rent_management_pattern2, html, re.DOTALL)
        if match:
            rent = match.group(1).replace(',', '')
            monthly_maintenance = match.group(2).replace(',', '')
            data['monthly_rent'] = int(rent)
            data['monthly_maintenance'] = int(monthly_maintenance)
            return data
        
        # Pattern 3: Simple "250,000円 / 10,000円" format (fallback)
        combined_pattern = r'([\d,]+)円\s*/\s*([\d,]+)円'
        match = re.search(combined_pattern, html)
        if match:
            rent = match.group(1).replace(',', '')
            monthly_maintenance = match.group(2).replace(',', '')
            data['monthly_rent'] = int(rent)
            data['monthly_maintenance'] = int(monthly_maintenance)
            return data
        
        # Pattern 4: "めやす賃料" pattern for fallback
        meyasu_pattern = r'めやす賃料.*?([\d,]+)円'
        match = re.search(meyasu_pattern, html, re.DOTALL)
        if match:
            rent = match.group(1).replace(',', '')
            data['monthly_rent'] = int(rent)
            data['rent_type'] = 'meyasu'  # Mark as estimated rent
            return data
        
        # Fallback patterns (existing patterns)
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
                    if '万円' in pattern:
                        data['monthly_rent'] = int(float(rent_value) * 10000)  # convert "25万円" → 250000円
                    else:
                        data['monthly_rent'] = int(rent_value)
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
        """Extract floor patterns từ HTML and also building name + unit number"""
        
        # First try to extract building name, floor, and unit from combined patterns
        # Examples: "アステリオン松濤 3階３０５", "サンプルマンション 5階501"
        building_floor_unit_patterns = [
            # Pattern: Building name + space + floor + unit (full-width numbers)
            r'([^\s\d<>]+)\s+(\d+)階([０-９]+)',
            # Pattern: Building name + space + floor + unit (half-width numbers)  
            r'([^\s\d<>]+)\s+(\d+)階(\d+)',
            # Pattern: Building name + floor + unit (no space, more restrictive)
            r'([^\d<>]{2,}?)(\d+)階([０-９\d]+)',
        ]
        
        for pattern in building_floor_unit_patterns:
            matches = re.findall(pattern, html)
            if matches:
                for match in matches:
                    building_name = match[0].strip()
                    floor_no = match[1]
                    unit_no = match[2]
                    
                    # Convert full-width numbers to half-width
                    unit_no = self._convert_fullwidth_to_halfwidth(unit_no)
                    
                    # Set building name if not already set and it looks valid
                    if not data.get('building_name_ja') and building_name and len(building_name) > 1:
                        # Filter out common HTML artifacts and invalid building names
                        if not any(x in building_name.lower() for x in ['class', 'div', 'span', 'href', 'http']):
                            data['building_name_ja'] = building_name
                    
                    # Set floor number if not already set
                    if not data.get('floor_no') and floor_no:
                        try:
                            data['floor_no'] = int(floor_no)
                        except ValueError:
                            pass
                    
                    # Set unit number if not already set
                    if not data.get('unit_no') and unit_no:
                        data['unit_no'] = unit_no
                    
                    # If we found a good match, break
                    if data.get('building_name_ja') or data.get('floor_no') or data.get('unit_no'):
                        break
                    
        return data
    
    def _convert_fullwidth_to_halfwidth(self, text: str) -> int:
        """Convert full-width numbers to half-width numbers"""
        fullwidth_to_halfwidth = {
            '０': '0', '１': '1', '２': '2', '３': '3', '４': '4',
            '５': '5', '６': '6', '７': '7', '８': '8', '９': '9'
        }
        
        result = text
        for fw, hw in fullwidth_to_halfwidth.items():
            result = result.replace(fw, hw)
        
        return int(result)
    
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