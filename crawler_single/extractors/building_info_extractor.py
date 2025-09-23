"""
Building information extractor from HTML
"""

import re
from typing import Dict, Any


class BuildingInfoExtractor:
    """Extract building information like structure, floors, building type"""
    
    def extract_building_info(self, html: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract building information từ HTML"""
        # Extract building structure with flexible patterns
        data = self._extract_building_structure(html, data)
        
        # Extract building floors with more patterns
        data = self._extract_building_floors(html, data)
        
        # Extract building type with more detail
        data = self._extract_building_type(html, data)
        
        return data
    
    def _extract_building_structure(self, html: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract building structure with flexible patterns"""
        if data.get('structure'):
            return data
            
        # Comprehensive structure patterns
        structure_patterns = [
            # Specific detailed patterns
            r'鉄筋コンクリート造[^<\n]*地上\d+階建[^<\n]*',
            r'RC造[^<\n]*地上\d+階建[^<\n]*',
            r'SRC造[^<\n]*地上\d+階建[^<\n]*',
            
            # General structure patterns
            r'構造[：:\s]*([^<\n]+)',
            r'(鉄筋コンクリート造[^<\n]*)',
            r'(RC造[^<\n]*)',
            r'(SRC造[^<\n]*)',
            r'(鉄骨造[^<\n]*)',
            r'(木造[^<\n]*)',
            r'(軽量鉄骨造[^<\n]*)',
            r'structure[：:\s]*([^<\n]+)',
            
            # Simple structure types
            r'(RC|SRC|木造|鉄骨|軽量鉄骨)(?![a-zA-Z])'
        ]
        
        for pattern in structure_patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            if matches:
                structure_text = matches[0].strip()
                # Clean up the structure text
                structure_text = re.sub(r'<[^>]+>', '', structure_text)
                structure_text = re.sub(r'&nbsp;', ' ', structure_text)
                structure_text = re.sub(r'\s+', ' ', structure_text).strip()
                
                if len(structure_text) > 1:  # Avoid single characters
                    data['structure'] = structure_text
                    break
        
        return data
    
    def _extract_building_floors(self, html: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract building floors with more patterns"""
        building_floor_patterns = [
            r'地上(\d+)階建?',
            r'(\d+)階建て?',
            r'(\d+)階建',
            r'building.*?(\d+)\s*floors?'
        ]
        
        for pattern in building_floor_patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            if matches:
                data['floors'] = matches[0]
                break
        
        return data
    
    def _extract_building_type(self, html: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract building type with more detail"""
        if not data.get('building_type'):
            building_type_patterns = [
                r'(鉄筋コンクリート造\s*地上\d+階建)',
                r'(マンション)',
                r'(アパート)',
                r'(一戸建て)',
                r'(テラスハウス)',
                r'(タウンハウス)'
            ]
            
            for pattern in building_type_patterns:
                matches = re.findall(pattern, html)
                if matches:
                    data['building_type'] = matches[0]
                    break
        
        return data