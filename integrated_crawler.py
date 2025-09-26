import asyncio
from datetime import datetime
from crawler_multi import collect_property_urls
from crawler_single.main import main as crawl_properties

async def integrated_crawl(num_pages=2):
    """
    Integrated crawler that:
    1. Collects property URLs from multiple pages
    2. Crawls detailed information for each property
    
    Args:
        num_pages (int): Number of pages to collect URLs from
    """
    print("🚀 Starting integrated property crawler...")
    start_time = datetime.now()
    
    # Step 1: Collect URLs from multiple pages
    print(f"\n📋 Step 1: Collecting URLs from {num_pages} pages...")
    urls = collect_property_urls(num_pages)
    
    if not urls:
        print("❌ No URLs collected. Exiting...")
        return
    
    print(f"✅ Collected {len(urls)} URLs")
    
    # Step 2: Crawl detailed information for each property
    print(f"\n🔍 Step 2: Crawling detailed information for {len(urls)} properties...")
    await crawl_properties(urls)
    
    # Summary
    end_time = datetime.now()
    duration = end_time - start_time
    
    print(f"""
    🎉 === Integration Complete ===
    📊 URLs collected: {len(urls)}
    ⏱️  Total duration: {duration}
    🕐 Started: {start_time:%Y-%m-%d %H:%M:%S}
    🕐 Finished: {end_time:%Y-%m-%d %H:%M:%S}
    """)

if __name__ == "__main__":
    # You can adjust the number of pages here
    asyncio.run(integrated_crawl(num_pages=1))