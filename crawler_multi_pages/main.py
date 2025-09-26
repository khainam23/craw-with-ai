import asyncio
from datetime import datetime
from .integrated_crawler import IntegratedPropertyCrawler
from .crawler_config import get_config_by_name, print_config_info

async def main():
    """Main function to run integrated property crawler with configurable settings"""
    
    print("🚀 Starting Integrated Property Crawler - Optimized Version")
    print("="*60)
    
    # Show available configurations
    print_config_info()
    print()
    
    # Choose configuration based on your needs
    # Options: 'conservative', 'balanced', 'aggressive', 'testing', 'unlimited'
    config_name = 'unlimited'  # Change this to suit your needs
    config = get_config_by_name(config_name)
    
    print(f"🔧 Using '{config_name.upper()}' configuration")
    print("="*40)
    
    # Main crawling configuration
    listing_url = "https://www.mitsui-chintai.co.jp/rf/result?are=36&get=area"
    url_pattern = r"/rf/tatemono/\d+"
    
    print(f"📋 Crawling Configuration:")
    print(f"   🔗 Listing URL: {listing_url}")
    print(f"   🎯 URL Pattern: {url_pattern}")
    print(f"   📄 Max Pages: {config.max_pages}")
    print(f"   🏠 Max Properties: {config.max_properties or 'Unlimited'}")
    print(f"   ⏱️ Delay: {config.delay}s")
    print(f"   🔄 Max Concurrent: {config.max_concurrent}")
    print(f"   📦 Batch Size: {config.batch_size}")
    print(f"   💾 Memory Threshold: {config.memory_threshold}%")
    print(f"   💾 Save Intermediate: {config.save_intermediate}")
    print()
    
    # Create crawler with configuration
    integrated_crawler = IntegratedPropertyCrawler(
        max_concurrent=config.max_concurrent,
        batch_size=config.batch_size,
        memory_threshold=config.memory_threshold
    )
    
    try:
        # Run the integrated crawling process
        extracted_urls, results, json_file = await integrated_crawler.crawl_from_listing(
            listing_url=listing_url,
            url_pattern=url_pattern,
            max_pages=config.max_pages,
            max_properties=config.max_properties,
            delay=config.delay,
            save_intermediate=config.save_intermediate
        )
        
        # Display sample results
        if results and any(r.get("success") for r in results):
            print(f"\n🔍 Sample Crawled Properties:")
            print("-" * 40)
            
            successful_results = [r for r in results if r.get("success") and r.get("data")]
            
            for i, result in enumerate(successful_results[:3], 1):  # Show first 3 successful
                data = result["data"]
                print(f"\n  🏠 Property {i}:")
                print(f"     URL: {result.get('url', 'N/A')}")
                print(f"     Title: {data.get('title', 'N/A')[:50]}...")
                print(f"     Rent: {data.get('rent', 'N/A')}")
                print(f"     Location: {data.get('location', 'N/A')}")
                print(f"     Size: {data.get('size', 'N/A')}")
                
            if len(successful_results) > 3:
                print(f"\n     ... and {len(successful_results) - 3} more successful properties")
        
        print(f"\n✅ Crawling completed successfully!")
        if json_file:
            print(f"💾 Results saved to: {json_file}")
        
        # Performance summary
        total_properties = len(results)
        successful_properties = sum(1 for r in results if r.get("success"))
        success_rate = (successful_properties / total_properties * 100) if total_properties > 0 else 0
        
        print(f"\n📊 Performance Summary:")
        print(f"   🎯 Success Rate: {success_rate:.1f}% ({successful_properties}/{total_properties})")
        print(f"   ⚙️ Configuration Used: {config_name.upper()}")
        
    except KeyboardInterrupt:
        print(f"\n⚠️ Crawling interrupted by user")
        print("💡 Tip: Intermediate results may have been saved if enabled")
    except Exception as e:
        print(f"\n❌ Error during crawling: {e}")
        print(f"   Please check your internet connection and URL configuration")
        print(f"   Consider using 'conservative' configuration for unstable connections")

def show_usage_tips():
    """Show usage tips for different scenarios"""
    print("\n💡 Usage Tips:")
    print("="*30)
    print("🔧 Configuration Selection:")
    print("   • 'testing' - For small tests (20 properties max)")
    print("   • 'conservative' - For slow/unstable connections")
    print("   • 'balanced' - For normal usage (recommended)")
    print("   • 'aggressive' - For high-performance systems")
    print("   • 'unlimited' - For crawling without page/property limits")
    print()
    print("⚠️ Memory Management:")
    print("   • Monitor system resources during large crawls")
    print("   • Intermediate saves prevent data loss")
    print("   • Lower batch_size if experiencing memory issues")
    print()
    print("🌐 Network Considerations:")
    print("   • Increase delay for rate-limited websites")
    print("   • Reduce max_concurrent for unstable connections")
    print("   • Use conservative config for shared hosting")

if __name__ == "__main__":
    print("🏠 Property Crawler - Optimized Version")
    print("Press Ctrl+C to stop at any time")
    
    show_usage_tips()
    print()
    
    asyncio.run(main())