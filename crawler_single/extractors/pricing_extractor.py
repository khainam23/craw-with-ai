"""
Pricing information extractor from HTML
"""

import re
from typing import Dict, Any


class PricingExtractor:
    """Extract pricing information like deposit, key money, maintenance fees"""
    
    def extract_pricing_info(self, html: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract pricing information từ HTML"""
        # Extract deposit patterns
        data = self._extract_deposit_patterns(html, data)
        
        # Extract key money patterns
        data = self._extract_key_money_patterns(html, data)
        
        # Extract maintenance fee patterns
        data = self._extract_maintenance_patterns(html, data)
        
        return data
    
    def _extract_deposit_patterns(self, html: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract deposit patterns"""
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
        
        return data
    
    def _extract_key_money_patterns(self, html: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract key money patterns"""
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
        
        return data
    
    def _extract_maintenance_patterns(self, html: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract maintenance fee patterns"""
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