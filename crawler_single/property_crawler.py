"""
Enhanced Property Crawler - Class chính
"""

import asyncio
from datetime import datetime
from typing import Dict, List, Any
from .property_extractor import PropertyExtractor
from .utils import FileUtils


class EnhancedPropertyCrawler:
    def __init__(self):
        self.extractor = PropertyExtractor()

    async def _crawl_single_property(self, url: str, verbose: bool = True) -> Dict[str, Any]:
        """
        Private method để crawl một property
        
        Args:
            url: URL to crawl
            verbose: Whether to print progress messages (default: True)
        """
        if verbose:
            print(f"🚀 Crawling: {url}")
        
        try:
            # Extract dữ liệu bằng crawl4ai
            result = await self.extractor.extract_property_data(url)
            
            if result['success']:
                # Validate và tạo PropertyModel
                property_model = self.extractor.validate_and_create_property_model(
                    result['property_data']
                )
                
                # Convert về dict để serialize JSON
                property_dict = property_model.dict(exclude_none=True)
                
                # Chuyển đổi images thành các field riêng biệt
                if 'images' in property_dict and isinstance(property_dict['images'], list):
                    images_list = property_dict.pop('images', [])
                    for i, img in enumerate(images_list):
                        img_num = i + 1
                        if isinstance(img, dict):
                            if 'url' in img or 'category' in img:
                                entry = {}
                                if 'url' in img:
                                    entry['url'] = img['url']
                                if 'category' in img:
                                    entry['category'] = img['category']
                                property_dict[f'image_{img_num}'] = entry
                
                result['property_data'] = property_dict
                
                if verbose:
                    print(f"✅ Success: Extracted {len(result['property_data'])} fields")
            else:
                if verbose:
                    print(f"❌ Failed: {result.get('error', 'Unknown error')}")
            
            return result['property_data']
            
        except Exception as e:
            error_result = {
                'success': False,
                'url': url,
                'error': str(e),
            }
            if verbose:
                print(f"❌ Exception crawling {url}: {e}")
            return error_result

    async def crawl_multiple_properties(self, urls: List[str]) -> List[Dict[str, Any]]:
        """
        Crawl nhiều properties cùng lúc
        """
        print(f"🏘️ Crawling {len(urls)} properties...")
        
        # Tạo tasks cho tất cả URLs
        tasks = [self._crawl_single_property(url) for url in urls]
        
        # Chạy parallel với error handling
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Xử lý exceptions
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                print(f"❌ Error crawling {urls[i]}: {result}")
                processed_results.append({
                    'success': False,
                    'url': urls[i],
                    'error': str(result),
                })
            else:
                processed_results.append(result)
        
        # Thống kê
        success_count = sum(1 for r in processed_results if r.get('success', False))
        print(f"📊 Results: {success_count}/{len(urls)} successful")
        
        return processed_results
    
    def save_results_to_json(self, results: List[Dict[str, Any]], filename: str = None) -> str:
        """
        Lưu kết quả crawl vào file JSON
        """
        return FileUtils.save_json_results(results, filename)