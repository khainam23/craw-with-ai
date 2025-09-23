"""
URL Extractor for Property Listings

Extracts property URLs from paginated listing pages and feeds them to the main crawler.
"""

import asyncio
import aiohttp
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from typing import List, Set, Optional
import re
from datetime import datetime

class PropertyURLExtractor:
    """Extract property URLs from listing pages with pagination support"""
    
    def __init__(self, max_pages: int = 10, delay: float = 1.0):
        """
        Initialize URL extractor
        
        Args:
            max_pages: Maximum number of pages to crawl
            delay: Delay between requests (seconds)
        """
        self.max_pages = max_pages
        self.delay = delay
        self.session = None
        self.extracted_urls: Set[str] = set()
        
    async def __aenter__(self):
        """Async context manager entry"""
        import ssl
        # Create SSL context that doesn't verify certificates
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        connector = aiohttp.TCPConnector(ssl=ssl_context)
        
        self.session = aiohttp.ClientSession(
            connector=connector,
            timeout=aiohttp.ClientTimeout(total=30),
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
        )
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
    
    async def fetch_page(self, url: str) -> Optional[str]:
        """Fetch a single page content"""
        try:
            async with self.session.get(url) as response:
                if response.status == 200:
                    return await response.text()
                else:
                    print(f"❌ Failed to fetch {url}: Status {response.status}")
                    return None
        except Exception as e:
            print(f"❌ Error fetching {url}: {e}")
            return None
    
    def extract_property_urls(self, html: str, base_url: str, url_pattern: str = None) -> List[str]:
        """
        Extract property URLs from HTML content
        
        Args:
            html: HTML content
            base_url: Base URL for resolving relative links
            url_pattern: Regex pattern to match property URLs (optional)
        
        Returns:
            List of property URLs
        """
        soup = BeautifulSoup(html, 'html.parser')
        urls = []
        
        # Common selectors for property links
        selectors = [
            'a[href*="/property/"]',
            'a[href*="/tatemono/"]', 
            'a[href*="/room/"]',
            'a[href*="/detail/"]',
            'a[href*="/item/"]',
            '.property-item a',
            '.listing-item a',
            '.property-card a',
            '.room-item a'
        ]
        
        for selector in selectors:
            links = soup.select(selector)
            for link in links:
                href = link.get('href')
                if href:
                    full_url = urljoin(base_url, href)
                    
                    # Apply URL pattern filter if provided
                    if url_pattern:
                        if re.search(url_pattern, full_url):
                            urls.append(full_url)
                    else:
                        urls.append(full_url)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_urls = []
        for url in urls:
            if url not in seen:
                seen.add(url)
                unique_urls.append(url)
                
        return unique_urls
    
    def find_next_page_url(self, html: str, base_url: str, current_page: int = 1) -> Optional[str]:
        """
        Find next page URL from pagination
        
        Args:
            html: HTML content
            base_url: Base URL for resolving relative links
            current_page: Current page number
            
        Returns:
            Next page URL or None
        """
        soup = BeautifulSoup(html, 'html.parser')
        
        # Common pagination selectors
        next_selectors = [
            'a.next',
            'a[rel="next"]',
            '.pagination .next a',
            '.pager .next a',
            'a:contains("次へ")',
            'a:contains("Next")',
            'a:contains(">")',
            f'a[href*="page={current_page + 1}"]',
            f'a[href*="p={current_page + 1}"]'
        ]
        
        for selector in next_selectors:
            try:
                if ':contains(' in selector:
                    # Handle text-based selectors
                    text = selector.split(':contains("')[1].split('")')[0]
                    links = soup.find_all('a', string=re.compile(text))
                else:
                    links = soup.select(selector)
                
                if links:
                    href = links[0].get('href')
                    if href:
                        return urljoin(base_url, href)
            except:
                continue
                
        return None
    
    async def extract_urls_from_listing(
        self, 
        start_url: str, 
        url_pattern: str = None,
        max_pages: int = None
    ) -> List[str]:
        """
        Extract all property URLs from a listing page with pagination
        
        Args:
            start_url: Starting URL of the listing page
            url_pattern: Regex pattern to filter property URLs
            max_pages: Override default max_pages
            
        Returns:
            List of all extracted property URLs
        """
        if max_pages is None:
            max_pages = self.max_pages
            
        all_urls = []
        current_url = start_url
        page_num = 1
        
        print(f"🔍 Starting URL extraction from: {start_url}")
        print(f"📄 Max pages to crawl: {max_pages}")
        
        while current_url and page_num <= max_pages:
            print(f"\n📖 Processing page {page_num}: {current_url}")
            
            # Fetch page content
            html = await self.fetch_page(current_url)
            if not html:
                break
                
            # Extract property URLs from current page
            page_urls = self.extract_property_urls(html, current_url, url_pattern)
            new_urls = [url for url in page_urls if url not in self.extracted_urls]
            
            if new_urls:
                all_urls.extend(new_urls)
                self.extracted_urls.update(new_urls)
                print(f"✅ Found {len(new_urls)} new URLs on page {page_num}")
            else:
                print(f"⚠️ No new URLs found on page {page_num}")
            
            # Find next page
            next_url = self.find_next_page_url(html, current_url, page_num)
            if next_url and next_url != current_url:
                current_url = next_url
                page_num += 1
                
                # Add delay between requests
                if self.delay > 0:
                    await asyncio.sleep(self.delay)
            else:
                print(f"🏁 No more pages found or reached max pages")
                break
        
        print(f"\n🎯 Total URLs extracted: {len(all_urls)}")
        return all_urls


async def extract_property_urls(
    listing_url: str,
    url_pattern: str = None,
    max_pages: int = 10,
    delay: float = 1.0
) -> List[str]:
    """
    Convenience function to extract property URLs
    
    Args:
        listing_url: URL of the listing page
        url_pattern: Regex pattern to filter URLs (optional)
        max_pages: Maximum pages to crawl
        delay: Delay between requests
        
    Returns:
        List of property URLs
    """
    async with PropertyURLExtractor(max_pages=max_pages, delay=delay) as extractor:
        return await extractor.extract_urls_from_listing(listing_url, url_pattern, max_pages)