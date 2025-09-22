"""
Enhanced Property Crawler - Refactored Version

File này đã được tách thành các module nhỏ hơn trong thư mục crawler/
để dễ đọc, dễ bảo trì và có thể mở rộng.
"""

import asyncio
import json
from datetime import datetime
from typing import List
from crawler import EnhancedPropertyCrawler


async def main():
    """
    Example usage của Enhanced Property Crawler
    """
    time_start = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Test URLs (thay bằng URLs thực tế)
    test_urls = [
        "https://rent.tokyu-housing-lease.co.jp/rent/8034884/117024"
    ]
    
    # Tạo crawler
    crawler = EnhancedPropertyCrawler()
    
    # Crawl multiple properties
    print("\n=== Testing Multiple Properties Crawl ===")
    results = await crawler.crawl_multiple_properties(test_urls)
    
    # Save results
    json_file = crawler.save_results_to_json(results)    
    print(f"\n=== Summary ===")
    print(f"Total URLs: {len(test_urls)}")
    print(f"Successful: {sum(1 for r in results if r.get('success'))}")
    print(f"Failed: {sum(1 for r in results if not r.get('success'))}")
    if json_file:
        print(f"JSON saved: {json_file}")
        
    time_end = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    duration = datetime.strptime(time_end, "%Y%m%d_%H%M%S") - datetime.strptime(time_start, "%Y%m%d_%H%M%S")

    print(
        f"Start time: {time_start}, End time: {time_end} 🕒 Duration: {duration}"
    )
    
    # trung bình 9 - 34s / property tùy trang web và cấu hình máy


if __name__ == "__main__":
    asyncio.run(main())