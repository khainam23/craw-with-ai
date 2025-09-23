"""
Crawler Configuration Settings

This file contains configuration presets for different crawling scenarios.
Adjust these settings based on your system resources and crawling requirements.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class CrawlerConfig:
    """Configuration class for crawler settings"""
    
    # Resource Management
    max_concurrent: int = 10
    batch_size: int = 50
    memory_threshold: float = 80.0
    
    # Request Settings
    delay: float = 1.0
    request_timeout: int = 30
    
    # Processing Settings
    max_pages: int = 10
    max_properties: Optional[int] = None
    save_intermediate: bool = True
    intermediate_save_frequency: int = 5  # Save every N batches
    
    # Error Handling
    max_retries: int = 3
    retry_delay: float = 2.0


# Predefined configurations for different scenarios

# Conservative settings for low-resource systems or unstable connections
CONSERVATIVE_CONFIG = CrawlerConfig(
    max_concurrent=3,
    batch_size=10,
    memory_threshold=70.0,
    delay=2.0,
    max_pages=5,
    save_intermediate=True,
    intermediate_save_frequency=3
)

# Balanced settings for normal usage
BALANCED_CONFIG = CrawlerConfig(
    max_concurrent=5,
    batch_size=20,
    memory_threshold=75.0,
    delay=1.0,
    max_pages=10,
    save_intermediate=True,
    intermediate_save_frequency=5
)

# Aggressive settings for high-performance systems
AGGRESSIVE_CONFIG = CrawlerConfig(
    max_concurrent=15,
    batch_size=100,
    memory_threshold=85.0,
    delay=0.5,
    max_pages=20,
    save_intermediate=True,
    intermediate_save_frequency=10
)

# Testing configuration for small-scale testing
TESTING_CONFIG = CrawlerConfig(
    max_concurrent=2,
    batch_size=5,
    memory_threshold=60.0,
    delay=1.0,
    max_pages=2,
    max_properties=20,
    save_intermediate=False
)

# Unlimited configuration for crawling without limits
UNLIMITED_CONFIG = CrawlerConfig(
    max_concurrent=10,
    batch_size=50,
    memory_threshold=80.0,
    delay=1.0,
    max_pages=999999,  # Practically unlimited
    max_properties=None,  # No limit on properties
    save_intermediate=True,
    intermediate_save_frequency=10
)


def get_config_by_name(config_name: str) -> CrawlerConfig:
    """Get configuration by name"""
    configs = {
        'conservative': CONSERVATIVE_CONFIG,
        'balanced': BALANCED_CONFIG,
        'aggressive': AGGRESSIVE_CONFIG,
        'testing': TESTING_CONFIG,
        'unlimited': UNLIMITED_CONFIG
    }
    
    return configs.get(config_name.lower(), BALANCED_CONFIG)


def print_config_info():
    """Print information about available configurations"""
    print("🔧 Available Crawler Configurations:")
    print("="*50)
    
    configs = {
        'Conservative': CONSERVATIVE_CONFIG,
        'Balanced': BALANCED_CONFIG,
        'Aggressive': AGGRESSIVE_CONFIG,
        'Testing': TESTING_CONFIG,
        'Unlimited': UNLIMITED_CONFIG
    }
    
    for name, config in configs.items():
        print(f"\n📋 {name} Configuration:")
        print(f"   🔄 Max Concurrent: {config.max_concurrent}")
        print(f"   📦 Batch Size: {config.batch_size}")
        print(f"   💾 Memory Threshold: {config.memory_threshold}%")
        print(f"   ⏱️ Delay: {config.delay}s")
        print(f"   📄 Max Pages: {config.max_pages}")
        print(f"   🏠 Max Properties: {config.max_properties or 'Unlimited'}")


if __name__ == "__main__":
    print_config_info()