"""
Cấu hình cho Property Crawler
"""

from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig
from crawl4ai.async_configs import CacheMode

class CrawlerConfig:
    """Cấu hình cho crawler"""
    
    # Browser configuration
    BROWSER_CONFIG = BrowserConfig(
        headless=True,
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    )
    
    # Crawler run configuration
    RUN_CONFIG = CrawlerRunConfig(
        wait_for_images=True,
        scan_full_page=True,
        scroll_delay=1,
        delay_before_return_html=3.0,
        page_timeout=45000,
        remove_overlay_elements=True,
        cache_mode=CacheMode.BYPASS,
        js_code="""
        // Function to click tab selector and wait for images to load
        async function clickTabForImages() {
            try {
                // Look for the exterior tab selector
                const tabSelector = document.querySelector('[data-js-buildroom-slide-tab="exterior"]');
                if (tabSelector) {
                    console.log('🖱️ Clicking exterior tab...');
                    tabSelector.click();
                    
                    // Wait for images to load
                    await new Promise(resolve => setTimeout(resolve, 3000));
                    
                    // Wait for any lazy-loaded images
                    const images = document.querySelectorAll('img[loading="lazy"]');
                    if (images.length > 0) {
                        console.log(`⏳ Waiting for ${images.length} lazy images to load...`);
                        await new Promise(resolve => setTimeout(resolve, 2000));
                    }
                    
                    console.log('✅ Tab clicked and images loaded');
                    return true;
                } else {
                    console.log('ℹ️ No exterior tab found');
                    return false;
                }
            } catch (error) {
                console.error('❌ Error clicking tab:', error);
                return false;
            }
        }
        
        // Execute the tab clicking function
        await clickTabForImages();
        """,
    )
    
    # Image extraction limits
    MAX_IMAGES = 50
    
    # Station limits
    MAX_STATIONS = 5
    
    # Skip patterns for images
    IMAGE_SKIP_PATTERNS = ['icon', 'logo', 'button', 'arrow', 'common']
    
    # Valid image extensions
    VALID_IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.webp', '.gif']