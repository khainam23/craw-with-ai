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
        seen_urls = set()  # Track URLs to avoid duplicates
        
        for img in soup.find_all("img"):
            src = (
                img.get("data-src")
                or img.get("data-original")
                or img.get("data-lazy")
                or img.get("src")
            )
            
            if self._is_valid_image(src) and src not in seen_urls:
                seen_urls.add(src)  # Mark this URL as seen
                images.append({
                    "url": src,
                    "category": self._categorize_image(len(images))
                })

            if len(images) >= self.config.MAX_IMAGES:
                break

        return images
    
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
    
    def _categorize_image(self, position: int) -> str:
        if position > 1:
            return 'interior'
        else:
            return 'others'
        