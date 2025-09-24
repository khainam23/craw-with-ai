"""
Module xử lý extract hình ảnh từ HTML
"""

import re
from bs4 import BeautifulSoup
from typing import List, Dict
from .config import CrawlerConfig


class ImageExtractor:
    """Class xử lý extract hình ảnh từ HTML content"""
    
    def __init__(self):
        self.config = CrawlerConfig()
    
    def extract_images_from_html(self, html: str) -> List[Dict[str, str]]:
        """
        Extract images từ HTML content
        """
        if not html:
            return []
        
        soup = BeautifulSoup(html, "lxml")
        images = []
        
        for img in soup.find_all("img"):
            src = (
                img.get("src")
                or img.get("data-src")
                or img.get("data-original")
                or img.get("data-lazy")
            )
            alt = img.get("alt", "")

            if self._is_valid_image(src):
                images.append({
                    "url": src,
                    "category": self._categorize_image(alt, len(images))
                })

            if len(images) >= self.config.MAX_IMAGES:
                break

        return images
    
    def _parse_image_match(self, match, pattern: str) -> tuple:
        """Parse image match từ regex"""
        if isinstance(match, tuple):
            if len(match) == 2:
                # Pattern with both src and alt
                if 'src=' in pattern and pattern.index('src=') < pattern.index('alt='):
                    src, alt = match
                else:
                    alt, src = match
            else:
                src = match[0]
                alt = ""
        else:
            src = match
            alt = ""
        
        return src, alt
    
    def _is_valid_image(self, src: str) -> bool:
        """Kiểm tra xem image có hợp lệ không"""
        if not src:
            return False
        
        # Filter out small icons and invalid URLs
        if any(skip in src.lower() for skip in self.config.IMAGE_SKIP_PATTERNS):
            return False
        
        # Check if starts with http or /
        if not (src.startswith('http') or src.startswith('/')):
            return False
        
        # Check valid extensions
        if not any(ext in src.lower() for ext in self.config.VALID_IMAGE_EXTENSIONS):
            return False
        
        return True
    
    def _categorize_image(self, alt_text: str, index: int) -> str:
        """
        Categorize image dựa trên alt text hoặc index
        """
        alt_lower = alt_text.lower() if alt_text else ""
        
        # Japanese keywords for categorization
        if any(keyword in alt_lower for keyword in ['外観', 'exterior', 'building']):
            return 'exterior'
        elif any(keyword in alt_lower for keyword in ['内装', 'interior', 'room', '室内']):
            return 'interior'
        elif any(keyword in alt_lower for keyword in ['キッチン', 'kitchen']):
            return 'kitchen'
        elif any(keyword in alt_lower for keyword in ['バス', 'bath', '浴室', 'bathroom']):
            return 'bathroom'
        elif any(keyword in alt_lower for keyword in ['バルコニー', 'balcony', 'ベランダ']):
            return 'balcony'
        elif any(keyword in alt_lower for keyword in ['間取り', 'floor plan', 'layout']):
            return 'floor_plan'
        elif any(keyword in alt_lower for keyword in ['周辺', 'area', 'location']):
            return 'area'
        else:
            # Default categorization based on index
            if index == 0:
                return 'main'
            elif index < 3:
                return 'exterior'
            elif index < 8:
                return 'interior'
            else:
                return 'other'