"""
Utility functions cho Property Crawler
"""

import re
from datetime import datetime
from typing import Dict, Any
from .models import PropertyModel, PropertyImage


class PropertyUtils:
    """Utility functions cho property processing"""
    
    @staticmethod
    def generate_property_id(url: str) -> str:
        """Tạo property ID từ URL"""
        # Extract ID từ URL
        match = re.search(r'/(\d+)/?$', url)
        if match:
            return f"PROP_{match.group(1)}"
        
        # Extract từ path
        path_match = re.search(r'/([^/]+)/?$', url)
        if path_match:
            return f"PROP_{path_match.group(1)}"
        
        # Fallback: timestamp
        return f"PROP_{int(datetime.now().timestamp())}"
    
    @staticmethod
    def validate_and_create_property_model(data: Dict[str, Any]) -> PropertyModel:
        """
        Validate và tạo PropertyModel từ extracted data
        """
        try:
            # Xử lý images nếu có
            if 'images' in data and isinstance(data['images'], list):
                processed_images = []
                for i, img in enumerate(data['images']):
                    if isinstance(img, dict) and 'url' in img:
                        processed_images.append(PropertyImage(**img))
                    else:
                        print(f"⚠️ Skipping invalid image data: {img}")
                data['images'] = processed_images
            
            # Tạo PropertyModel
            property_model = PropertyModel(**data)
            return property_model
            
        except Exception as e:
            print(f"❌ Error creating PropertyModel: {e}")
            print(f"🔍 Data causing error: {data}")
            import traceback
            traceback.print_exc()
            
            # Tạo model với dữ liệu cơ bản
            basic_data = {
                'link': data.get('link'),
                'property_csv_id': data.get('property_csv_id'),
                'create_date': data.get('create_date')
            }
            return PropertyModel(**basic_data)
    
    @staticmethod
    def create_crawl_result(success: bool, url: str, property_data: Dict[str, Any] = None, 
                           error: str = None) -> Dict[str, Any]:
        """Tạo cấu trúc kết quả crawl chuẩn"""
        result = {
            'success': success,
            'url': url,
        }
        
        if success and property_data:
            result.update({
                'property_data': property_data,
            })
        else:
            result['error'] = error or 'Unknown error'
        
        return result
    
    @staticmethod
    def count_extracted_fields(data: Dict[str, Any]) -> int:
        """Đếm số fields có dữ liệu"""
        return len([k for k, v in data.items() if v is not None and v != []])
    
    @staticmethod
    def print_crawl_success(url: str, data: Dict[str, Any]):
        """In thông báo crawl thành công"""
        print(f"✅ Successfully crawled: {url}")
        print(f"🔍 Title: {data.get('building_name_ja', 'N/A')}")
        print(f"🔍 Extracted {PropertyUtils.count_extracted_fields(data)} fields with data")
    
    @staticmethod
    def print_crawl_error(url: str, error: str):
        """In thông báo crawl lỗi"""
        print(f"❌ Failed to crawl: {url}")
        print(f"🔍 Error: {error}")


class FileUtils:
    """Utility functions cho file operations"""
    
    @staticmethod
    def generate_filename(prefix: str, extension: str) -> str:
        """Tạo filename với timestamp"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{prefix}_{timestamp}.{extension}"
    
    @staticmethod
    def save_json_results(results: list, filename: str = None) -> str:
        """Lưu kết quả vào file JSON"""
        import json
        
        if filename is None:
            filename = FileUtils.generate_filename("crawl_results", "json")
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            print(f"💾 Saved results to: {filename}")
            return filename
        except Exception as e:
            print(f"❌ Error saving to JSON: {e}")
            return None