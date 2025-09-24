"""
Module chính xử lý extract dữ liệu property
"""

from typing import Dict, Any
from crawl4ai import AsyncWebCrawler
from .config import CrawlerConfig
from .models import get_empty_property_data
from .image_extractor import ImageExtractor
from .html_parser import HTMLParser
from .markdown_parser import MarkdownParser
from .utils import PropertyUtils
from .custom_config import setup_custom_extractor

class PropertyExtractor:    
    def __init__(self):
        self.config = CrawlerConfig()
        self.image_extractor = ImageExtractor()
        self.html_parser = HTMLParser()
        self.markdown_parser = MarkdownParser()
        self.utils = PropertyUtils()
        self.custom_extractor = setup_custom_extractor()
    
    async def extract_property_data(self, url: str) -> Dict[str, Any]:
        """
        Extract dữ liệu bất động sản từ URL với đầy đủ thông tin theo PropertyModel
        """
        try:
            async with AsyncWebCrawler(config=self.config.BROWSER_CONFIG) as crawler:
                result = await crawler.arun(
                    url=url,
                    config=self.config.RUN_CONFIG
                )
                
                if result.success:
                    # Extract comprehensive property data
                    extracted_data = self._extract_comprehensive_data(url, result)
                    
                    # Print success message
                    PropertyUtils.print_crawl_success(url, extracted_data)
                    
                    return PropertyUtils.create_crawl_result(
                        property_data=extracted_data,
                    )
                else:
                    error_msg = result.error_message or 'Failed to extract content'
                    PropertyUtils.print_crawl_error(url, error_msg)
                    return PropertyUtils.create_crawl_result(
                        error=error_msg
                    )
                    
        except Exception as e:
            error_msg = str(e)
            PropertyUtils.print_crawl_error(url, error_msg)
            return PropertyUtils.create_crawl_result(
                error=error_msg
            )
    
    def _extract_comprehensive_data(self, url: str, result) -> Dict[str, Any]:
        """
        Extract comprehensive property data từ crawl result
        """
        # Khởi tạo data structure với tất cả fields từ PropertyModel
        extracted_data = get_empty_property_data(url)
        
        # Set property ID
        # extracted_data['property_csv_id'] = PropertyUtils.generate_property_id(url)
        
        # Get content
        html_content = result.html if result.html else ""
        markdown_content = result.markdown if result.markdown else ""
                
        # Apply custom rules (this will clean HTML and store it in _html)
        extracted_data = self.custom_extractor.extract_with_rules(html_content, extracted_data)
        
        # Extract images từ cleaned HTML content (if available) or original HTML
        cleaned_html = extracted_data.get('_html', html_content)
        images = self.image_extractor.extract_images_from_html(cleaned_html)
        extracted_data['images'] = images
        
        # Extract structured data từ cleaned HTML patterns
        extracted_data = self.html_parser.extract_from_html_patterns(cleaned_html, extracted_data)
        
        # Extract từ markdown content
        # extracted_data = self.markdown_parser.extract_from_markdown(markdown_content, extracted_data)
        
        return extracted_data
    
    def validate_and_create_property_model(self, data: Dict[str, Any]):
        """
        Validate và tạo PropertyModel từ extracted data
        """
        return PropertyUtils.validate_and_create_property_model(data)