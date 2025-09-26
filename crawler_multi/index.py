import requests
from bs4 import BeautifulSoup

def collect_property_urls(num_pages=2):
    """
    Collect property URLs from multiple pages of Mitsui Chintai search results
    
    Args:
        num_pages (int): Number of pages to crawl
        
    Returns:
        list: List of property URLs
    """
    url = "https://www.mitsui-chintai.co.jp/rf/result?"
    item_selector = "tr.c-room-list__body-row[data-js-room-link]"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    collected_urls = []
    
    for page in range(1, num_pages + 1):
        params = {"page": page}
        resp = requests.get(url, params=params, headers=headers)
        if resp.status_code != 200:
            print(f"❌ Lỗi tải trang {page}")
            continue
        
        soup = BeautifulSoup(resp.text, "html.parser")
        items = soup.select(item_selector)
        
        print(f"Trang {page}: tìm thấy {len(items)} items")
        
        for item in items:
            link = item.get("data-js-room-link")
            if link:
                collected_urls.append(link)
                print("  -", link)
    
    print(f"\n✅ Tổng cộng thu thập được {len(collected_urls)} URLs")
    return collected_urls

# Keep the original functionality when run directly
if __name__ == "__main__":
    urls = collect_property_urls(2)
    print(f"\nCollected {len(urls)} URLs:")
