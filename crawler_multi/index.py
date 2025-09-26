import requests
from crawler_single import crawl_pages
from bs4 import BeautifulSoup
import asyncio

url = "https://www.mitsui-chintai.co.jp/rf/result?"
item_selector = "tr.c-room-list__body-row[data-js-room-link]"  # dùng CSS selector
num_page = 74

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

for page in range(1, num_page + 1):
    params = {"page": page}
    resp = requests.get(url, params=params, headers=headers)
    if resp.status_code != 200:
        print(f"❌ Lỗi tải trang {page}")
        continue
    
    soup = BeautifulSoup(resp.text, "html.parser")
    items = soup.select(item_selector)
    
    print(f"Trang {page}: tìm thấy {len(items)} items")
    urls = []
    
    for item in items:
        # Có thể lấy link cụ thể trong data-js-room-link
        link = item.get("data-js-room-link")
        urls.append(link)
        
    
asyncio.run(crawl_pages(urls, batch_size=3))  # Giảm batch size để tránh timeout
