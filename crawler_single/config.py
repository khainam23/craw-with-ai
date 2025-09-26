"""
Cấu hình cho Property Crawler
"""

from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig

class CrawlerConfig:
    """Cấu hình cho crawler"""
    
    # Browser configuration
    BROWSER_CONFIG = BrowserConfig(
        headless=True,
        headers={
            "Accept-Encoding": "gzip, deflate",
            "Cache-Control": "no-cache",
        },
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    )
    
    # Crawler run configuration
    RUN_CONFIG = CrawlerRunConfig(
        wait_for_images=False,
        scan_full_page=False,
        delay_before_return_html=0.1,
        page_timeout=25000,
        remove_overlay_elements=True
    )
    
    # Image extraction limits
    MAX_IMAGES = 16
    
    # Station limits
    MAX_STATIONS = 5
    
    # Skip patterns for images
    IMAGE_SKIP_PATTERNS = ['icon', 'logo', 'button', 'arrow', 'common']
    
    # Valid image extensions
    VALID_IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.webp', '.gif']