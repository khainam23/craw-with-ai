"""
Address information parser from Markdown content
"""

import re
from typing import Dict, Any


class AddressParser:
    """Parse address information from markdown content"""
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