"""
Integrated Property Crawler

Combines URL extraction from listing pages with detailed property crawling.
Optimized for large-scale crawling with memory management and batch processing.
"""

import asyncio
import gc
import psutil
import os
from datetime import datetime
from typing import List, Optional, AsyncGenerator
from .url_extractor import extract_property_urls
from crawler_single import EnhancedPropertyCrawler


class IntegratedPropertyCrawler:
    """Integrated crawler that extracts URLs from listings and crawls each property"""
    
    def __init__(self, max_concurrent: int = 10, batch_size: int = 50, memory_threshold: float = 80.0):
        """
        Initialize crawler with resource management settings
        
        Args:
            max_concurrent: Maximum concurrent requests (default: 10)
            batch_size: Number of properties to process in each batch (default: 50)
            memory_threshold: Memory usage threshold to trigger cleanup (default: 80%)
        """
        self.crawler = EnhancedPropertyCrawler()
        self.max_concurrent = max_concurrent
        self.batch_size = batch_size
        self.memory_threshold = memory_threshold
        self.semaphore = asyncio.Semaphore(max_concurrent)
        
    def _check_memory_usage(self) -> float:
        """Check current memory usage percentage"""
        return psutil.virtual_memory().percent
    
    def _force_garbage_collection(self):
        """Force garbage collection to free memory"""
        gc.collect()
        
    async def _crawl_with_semaphore(self, url: str, verbose: bool = False) -> dict:
        """Crawl single property with semaphore control"""
        async with self.semaphore:
            return await self.crawler._crawl_single_property(url, verbose=verbose)
    
    async def _crawl_batch(self, urls_batch: List[str], batch_num: int) -> List[dict]:
        """Crawl a batch of URLs with memory monitoring"""
        print(f"🔄 Processing batch {batch_num} ({len(urls_batch)} properties)")
        
        # Check memory before processing batch
        memory_before = self._check_memory_usage()
        print(f"💾 Memory usage before batch: {memory_before:.1f}%")
        
        if memory_before > self.memory_threshold:
            print(f"⚠️ Memory usage high ({memory_before:.1f}%), forcing cleanup...")
            self._force_garbage_collection()
            await asyncio.sleep(2)  # Give system time to cleanup
        
        # Create tasks for this batch with semaphore control (reduced verbosity for batch processing)
        tasks = [self._crawl_with_semaphore(url, verbose=False) for url in urls_batch]
        
        # Process batch with error handling
        batch_results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process exceptions
        processed_results = []
        for i, result in enumerate(batch_results):
            if isinstance(result, Exception):
                print(f"❌ Error crawling {urls_batch[i]}: {result}")
                processed_results.append({
                    'success': False,
                    'url': urls_batch[i],
                    'error': str(result),
                })
            else:
                processed_results.append(result)
        
        # Memory cleanup after batch
        memory_after = self._check_memory_usage()
        print(f"💾 Memory usage after batch: {memory_after:.1f}%")
        
        if memory_after > memory_before + 10:  # If memory increased significantly
            print("🧹 Performing garbage collection...")
            self._force_garbage_collection()
        
        success_count = sum(1 for r in processed_results if r.get('success', False))
        print(f"✅ Batch {batch_num} completed: {success_count}/{len(urls_batch)} successful")
        
        return processed_results
    
    async def crawl_from_listing(
        self,
        listing_url: str,
        url_pattern: str = None,
        max_pages: int = 10,
        max_properties: int = None,
        delay: float = 1.0,
        save_intermediate: bool = True
    ) -> tuple[List[str], List[dict], str]:
        """
        Extract URLs from listing pages and crawl each property with batch processing
        
        Args:
            listing_url: URL of the listing page
            url_pattern: Regex pattern to filter property URLs
            max_pages: Maximum pages to crawl for URL extraction
            max_properties: Maximum number of properties to crawl (None = all)
            delay: Delay between requests during URL extraction
            save_intermediate: Save results after each batch (default: True)
            
        Returns:
            Tuple of (extracted_urls, crawl_results, json_file_path)
        """
        print("🚀 Starting integrated property crawling with batch processing...")
        print(f"⚙️ Configuration: max_concurrent={self.max_concurrent}, batch_size={self.batch_size}")
        start_time = datetime.now()
        
        # Step 1: Extract URLs from listing pages
        print("\n" + "="*50)
        print("📋 STEP 1: Extracting URLs from listing pages")
        print("="*50)
        
        extracted_urls = await extract_property_urls(
            listing_url=listing_url,
            url_pattern=url_pattern,
            max_pages=max_pages,
            delay=delay
        )
        
        if not extracted_urls:
            print("❌ No URLs extracted. Stopping.")
            return [], [], None
        
        # Limit number of properties if specified
        if max_properties and len(extracted_urls) > max_properties:
            print(f"⚠️ Limiting to first {max_properties} properties out of {len(extracted_urls)} found")
            extracted_urls = extracted_urls[:max_properties]
        
        # Step 2: Crawl properties in batches
        print("\n" + "="*50)
        print("🏠 STEP 2: Crawling properties in batches")
        print("="*50)
        
        all_results = []
        total_batches = (len(extracted_urls) + self.batch_size - 1) // self.batch_size
        
        print(f"📦 Processing {len(extracted_urls)} properties in {total_batches} batches")
        
        for i in range(0, len(extracted_urls), self.batch_size):
            batch_num = (i // self.batch_size) + 1
            urls_batch = extracted_urls[i:i + self.batch_size]
            
            try:
                batch_results = await self._crawl_batch(urls_batch, batch_num)
                all_results.extend(batch_results)
                
                # Save intermediate results if enabled
                if save_intermediate and batch_num % 5 == 0:  # Save every 5 batches
                    temp_filename = f"temp_crawl_results_batch_{batch_num}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                    self.crawler.save_results_to_json(all_results, temp_filename)
                    print(f"💾 Intermediate results saved to: {temp_filename}")
                
                # Progress update
                progress = (batch_num / total_batches) * 100
                print(f"📊 Progress: {batch_num}/{total_batches} batches ({progress:.1f}%)")
                
                # Small delay between batches to prevent overwhelming the server
                if batch_num < total_batches:
                    await asyncio.sleep(delay)
                    
            except Exception as e:
                print(f"❌ Error processing batch {batch_num}: {e}")
                # Continue with next batch instead of stopping
                continue
        
        # Step 3: Save final results
        print("\n" + "="*50)
        print("💾 STEP 3: Saving final results")
        print("="*50)
        
        json_file = self.crawler.save_results_to_json(all_results)
        
        # Final cleanup
        self._force_garbage_collection()
        
        # Summary
        end_time = datetime.now()
        duration = end_time - start_time
        
        success = sum(1 for r in all_results if r.get("success"))
        failed = len(all_results) - success
        
        print("\n" + "="*60)
        print("📊 INTEGRATED CRAWLING SUMMARY")
        print("="*60)
        print(f"🔗 Listing URL: {listing_url}")
        print(f"📄 Pages crawled for URLs: {max_pages}")
        print(f"🎯 URLs extracted: {len(extracted_urls)}")
        print(f"🏠 Properties crawled: {len(all_results)}")
        print(f"✅ Successful: {success}")
        print(f"❌ Failed: {failed}")
        print(f"📦 Batches processed: {total_batches}")
        print(f"⚙️ Concurrent limit: {self.max_concurrent}")
        print(f"💾 JSON saved: {json_file or 'None'}")
        print(f"⏱️ Total duration: {duration}")
        print(f"🕐 Start: {start_time:%Y-%m-%d %H:%M:%S}")
        print(f"🕐 End: {end_time:%Y-%m-%d %H:%M:%S}")
        print("="*60)
        
        return extracted_urls, all_results, json_file