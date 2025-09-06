#!/usr/bin/env python3
"""
🚀 Modern Web Scraper Pro - Demo Version
Simple demonstration without heavy dependencies

Developed by Jose L Encarnacion (JoseTusabe)
SoloYLibre Web Dev - New York, United States
"""

import requests
import time
import json
from datetime import datetime
from urllib.parse import urljoin
from dataclasses import dataclass, asdict
from typing import List, Dict, Any

@dataclass
class ScrapedData:
    """Data structure for scraped content"""
    url: str
    title: str
    content: str
    status_code: int
    load_time: float
    timestamp: str

class SimpleModernScraper:
    """🚀 Simple Modern Web Scraper Demo"""
    
    def __init__(self):
        self.session = requests.Session()
        self.results: List[ScrapedData] = []
        
        # Set modern headers
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        })
        
        print("🚀 Simple Modern Scraper initialized")
    
    def scrape_page(self, url: str) -> ScrapedData:
        """Scrape a single page"""
        start_time = time.time()
        
        try:
            print(f"🔍 Scraping: {url}")
            response = self.session.get(url, timeout=30)
            
            # Extract basic info
            title = f"Page from {url}"
            content = response.text[:500] if response.text else "No content"
            
            load_time = time.time() - start_time
            
            result = ScrapedData(
                url=url,
                title=title,
                content=content,
                status_code=response.status_code,
                load_time=load_time,
                timestamp=datetime.now().isoformat()
            )
            
            print(f"✅ Scraped {url} in {load_time:.2f}s - Status: {response.status_code}")
            return result
            
        except Exception as e:
            print(f"❌ Error scraping {url}: {e}")
            return ScrapedData(
                url=url,
                title="ERROR",
                content=str(e),
                status_code=0,
                load_time=time.time() - start_time,
                timestamp=datetime.now().isoformat()
            )
    
    def scrape_multiple(self, urls: List[str]) -> List[ScrapedData]:
        """Scrape multiple URLs"""
        print(f"🚀 Starting scrape of {len(urls)} URLs")
        
        results = []
        for i, url in enumerate(urls, 1):
            print(f"📄 Processing {i}/{len(urls)}")
            result = self.scrape_page(url)
            results.append(result)
            self.results.append(result)
            time.sleep(1)  # Be respectful
        
        return results
    
    def save_results(self, filename: str = "demo_results"):
        """Save results to JSON"""
        json_file = f"{filename}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            data = [asdict(result) for result in self.results]
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"💾 Results saved: {json_file}")
    
    def print_summary(self):
        """Print summary"""
        successful = [r for r in self.results if r.status_code == 200]
        
        print("\n" + "="*60)
        print("🚀 MODERN WEB SCRAPER PRO - DEMO RESULTS")
        print("="*60)
        print(f"📊 Total Pages: {len(self.results)}")
        print(f"✅ Successful: {len(successful)}")
        print(f"❌ Errors: {len(self.results) - len(successful)}")
        print(f"📈 Success Rate: {(len(successful)/len(self.results)*100):.1f}%")
        print("="*60)

def main():
    """Demo function"""
    print("🚀 Modern Web Scraper Pro - Demo")
    print("Developed by Jose L Encarnacion (JoseTusabe)")
    print("-" * 50)
    
    # Test URLs
    test_urls = [
        "https://httpbin.org/html",
        "https://httpbin.org/json", 
        "https://example.com"
    ]
    
    scraper = SimpleModernScraper()
    scraper.scrape_multiple(test_urls)
    scraper.save_results()
    scraper.print_summary()
    
    print(f"\n🎉 Demo completed!")

if __name__ == "__main__":
    main()
