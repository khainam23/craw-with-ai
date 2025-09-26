import asyncio
from datetime import datetime
from .property_crawler import EnhancedPropertyCrawler
from utils.utils import FileUtils

async def main():
    start = datetime.now()
    urls = [
        "https://www.mitsui-chintai.co.jp/rf/tatemono/6757", 
    ]

    crawler = EnhancedPropertyCrawler()
    print("\n=== 😶‍🌫️☀️😁😂😑🤷‍♂️ ===")
    results = await crawler.crawl_multiple_properties(urls)
    json_file = FileUtils.save_json_results(results)

    end = datetime.now()
    duration = end - start

    print(f"""
        === Summary ===
        Total URLs: {len(urls)}
        JSON saved: {json_file or "None"}
        Start: {start:%Y%m%d_%H%M%S} | End: {end:%Y%m%d_%H%M%S} | 🕒 Duration: {duration}
    """)

if __name__ == "__main__":
    asyncio.run(main())