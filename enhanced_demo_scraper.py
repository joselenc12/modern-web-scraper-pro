#!/usr/bin/env python3
"""
🚀 Modern Web Scraper Pro - Enhanced Demo Version
Advanced demonstration with real scraping and beautiful results display

Developed by Jose L Encarnacion (JoseTusabe)
SoloYLibre Web Dev - New York, United States
"""

import requests
import time
import json
from datetime import datetime
from urllib.parse import urljoin, urlparse
from dataclasses import dataclass, asdict
from typing import List, Dict, Any
import re
import os

@dataclass
class ScrapedData:
    """Enhanced data structure for scraped content"""
    url: str
    title: str
    content: str
    status_code: int
    load_time: float
    timestamp: str
    word_count: int
    links_found: int
    images_found: int
    domain: str
    content_type: str
    meta_description: str

class EnhancedModernScraper:
    """🚀 Enhanced Modern Web Scraper with Beautiful Results Display"""
    
    def __init__(self):
        self.session = requests.Session()
        self.results: List[ScrapedData] = []
        
        # Set modern headers with rotation
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        ]
        
        self.session.headers.update({
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        
        print("🚀 Enhanced Modern Scraper initialized with advanced features")
    
    def scrape_page(self, url: str) -> ScrapedData:
        """Enhanced scrape with detailed extraction"""
        start_time = time.time()
        
        try:
            # Rotate user agent
            import random
            self.session.headers['User-Agent'] = random.choice(self.user_agents)
            
            print(f"🔍 Scraping: {url}")
            response = self.session.get(url, timeout=30)
            
            # Parse domain
            domain = urlparse(url).netloc
            content_type = response.headers.get('content-type', 'unknown')
            
            # Basic extraction for demo
            if 'json' in content_type.lower():
                # Handle JSON responses
                try:
                    json_data = response.json()
                    title = f"JSON Data from {domain}"
                    content = json.dumps(json_data, indent=2)[:1000]
                    word_count = len(content.split())
                    links_found = 0
                    images_found = 0
                    meta_description = "JSON API Response"
                except:
                    title = f"JSON Response from {domain}"
                    content = response.text[:1000]
                    word_count = len(content.split())
                    links_found = 0
                    images_found = 0
                    meta_description = "JSON data"
            else:
                # Handle HTML responses
                try:
                    from bs4 import BeautifulSoup
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Extract title
                    title_tag = soup.find('title')
                    title = title_tag.get_text(strip=True) if title_tag else f"Page from {domain}"
                    
                    # Extract meta description
                    meta_desc = soup.find('meta', attrs={'name': 'description'})
                    meta_description = meta_desc.get('content', '')[:200] if meta_desc else "No description"
                    
                    # Extract links and images
                    links = soup.find_all('a', href=True)
                    images = soup.find_all('img', src=True)
                    links_found = len(links)
                    images_found = len(images)
                    
                    # Extract clean text
                    for script in soup(["script", "style"]):
                        script.decompose()
                    content = soup.get_text(strip=True, separator=' ')[:1000]
                    word_count = len(content.split())
                    
                except ImportError:
                    # Fallback without BeautifulSoup
                    title = f"Page from {domain}"
                    content = response.text[:1000]
                    word_count = len(content.split())
                    links_found = content.count('<a ')
                    images_found = content.count('<img ')
                    meta_description = "HTML content"
            
            load_time = time.time() - start_time
            
            result = ScrapedData(
                url=url,
                title=title,
                content=content,
                status_code=response.status_code,
                load_time=load_time,
                timestamp=datetime.now().isoformat(),
                word_count=word_count,
                links_found=links_found,
                images_found=images_found,
                domain=domain,
                content_type=content_type,
                meta_description=meta_description
            )
            
            print(f"✅ Scraped {url} in {load_time:.2f}s - Status: {response.status_code}")
            print(f"   📄 Words: {word_count}, 🔗 Links: {links_found}, 🖼️ Images: {images_found}")
            return result
            
        except Exception as e:
            print(f"❌ Error scraping {url}: {e}")
            return ScrapedData(
                url=url,
                title="ERROR",
                content=str(e),
                status_code=0,
                load_time=time.time() - start_time,
                timestamp=datetime.now().isoformat(),
                word_count=0,
                links_found=0,
                images_found=0,
                domain=urlparse(url).netloc if url else "unknown",
                content_type="error",
                meta_description="Error occurred"
            )
    
    def scrape_multiple(self, urls: List[str]) -> List[ScrapedData]:
        """Scrape multiple URLs with progress tracking"""
        print(f"🚀 Starting enhanced scrape of {len(urls)} URLs")
        print("="*60)
        
        results = []
        for i, url in enumerate(urls, 1):
            print(f"\n📄 Processing {i}/{len(urls)}: {url}")
            result = self.scrape_page(url)
            results.append(result)
            self.results.append(result)
            
            # Progress indicator
            progress = (i / len(urls)) * 100
            print(f"📊 Progress: {progress:.1f}% complete")
            
            # Be respectful with delays
            if i < len(urls):
                time.sleep(1)
        
        return results
    
    def save_results(self, filename: str = "enhanced_demo_results"):
        """Save enhanced results with multiple formats"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_filename = f"{filename}_{timestamp}"
        
        # Create results directory
        os.makedirs("results", exist_ok=True)
        
        # Save as JSON
        json_file = f"results/{base_filename}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            data = [asdict(result) for result in self.results]
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        # Save as CSV (if pandas available)
        try:
            import pandas as pd
            csv_file = f"results/{base_filename}.csv"
            df = pd.DataFrame([asdict(result) for result in self.results])
            df.to_csv(csv_file, index=False, encoding='utf-8')
            print(f"💾 Results saved: {json_file}, {csv_file}")
        except ImportError:
            print(f"💾 Results saved: {json_file}")
    
    def generate_html_report(self, filename: str = "scraping_report"):
        """Generate beautiful HTML report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        html_file = f"results/{filename}_{timestamp}.html"
        
        # Create results directory
        os.makedirs("results", exist_ok=True)
        
        html_content = self._create_html_report()
        
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"📊 HTML report generated: {html_file}")
        return html_file
    
    def _create_html_report(self) -> str:
        """Create beautiful HTML report"""
        successful = [r for r in self.results if r.status_code == 200]
        total_words = sum(r.word_count for r in successful)
        total_links = sum(r.links_found for r in successful)
        total_images = sum(r.images_found for r in successful)
        avg_load_time = sum(r.load_time for r in successful) / len(successful) if successful else 0
        
        results_html = ""
        for i, result in enumerate(self.results, 1):
            status_class = "success" if result.status_code == 200 else "error"
            results_html += f"""
            <div class="result-card {status_class}">
                <div class="result-header">
                    <h3>#{i}. {result.title}</h3>
                    <span class="status status-{status_class}">{result.status_code}</span>
                </div>
                <div class="result-details">
                    <p><strong>🌐 URL:</strong> <a href="{result.url}" target="_blank">{result.url}</a></p>
                    <p><strong>🏢 Domain:</strong> {result.domain}</p>
                    <p><strong>📄 Description:</strong> {result.meta_description}</p>
                    <div class="metrics">
                        <span class="metric">⏱️ {result.load_time:.2f}s</span>
                        <span class="metric">📝 {result.word_count} words</span>
                        <span class="metric">🔗 {result.links_found} links</span>
                        <span class="metric">🖼️ {result.images_found} images</span>
                    </div>
                    <div class="content-preview">
                        <strong>📋 Content Preview:</strong>
                        <p>{result.content[:200]}...</p>
                    </div>
                </div>
            </div>
            """
        
        return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🚀 Modern Web Scraper Pro - Results Report</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; min-height: 100vh; padding: 20px;
        }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .header {{ text-align: center; margin-bottom: 40px; }}
        .header h1 {{ font-size: 2.5em; margin-bottom: 10px; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); }}
        .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 40px; }}
        .stat-card {{ 
            background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; 
            text-align: center; backdrop-filter: blur(10px);
        }}
        .stat-card h3 {{ font-size: 2em; margin-bottom: 5px; color: #00d4ff; }}
        .result-card {{ 
            background: rgba(255,255,255,0.1); margin: 20px 0; padding: 20px; 
            border-radius: 10px; backdrop-filter: blur(10px);
        }}
        .result-card.success {{ border-left: 5px solid #28a745; }}
        .result-card.error {{ border-left: 5px solid #dc3545; }}
        .result-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; }}
        .result-header h3 {{ color: #00d4ff; }}
        .status {{ padding: 5px 10px; border-radius: 5px; font-weight: bold; }}
        .status-success {{ background: #28a745; }}
        .status-error {{ background: #dc3545; }}
        .metrics {{ display: flex; gap: 15px; margin: 10px 0; flex-wrap: wrap; }}
        .metric {{ 
            background: rgba(255,255,255,0.2); padding: 5px 10px; 
            border-radius: 15px; font-size: 0.9em;
        }}
        .content-preview {{ 
            background: rgba(255,255,255,0.1); padding: 15px; 
            border-radius: 8px; margin-top: 10px;
        }}
        .content-preview p {{ 
            font-style: italic; opacity: 0.9; 
            max-height: 60px; overflow: hidden;
        }}
        a {{ color: #00d4ff; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
        .footer {{ text-align: center; margin-top: 40px; opacity: 0.8; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Modern Web Scraper Pro</h1>
            <p>Enhanced Scraping Results Report</p>
            <p><strong>Generated:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <h3>{len(self.results)}</h3>
                <p>Total Pages</p>
            </div>
            <div class="stat-card">
                <h3>{len(successful)}</h3>
                <p>Successful</p>
            </div>
            <div class="stat-card">
                <h3>{(len(successful)/len(self.results)*100):.1f}%</h3>
                <p>Success Rate</p>
            </div>
            <div class="stat-card">
                <h3>{avg_load_time:.2f}s</h3>
                <p>Avg Load Time</p>
            </div>
            <div class="stat-card">
                <h3>{total_words:,}</h3>
                <p>Total Words</p>
            </div>
            <div class="stat-card">
                <h3>{total_links:,}</h3>
                <p>Total Links</p>
            </div>
        </div>
        
        <div class="results">
            <h2>📋 Detailed Results</h2>
            {results_html}
        </div>
        
        <div class="footer">
            <p>🚀 <strong>Modern Web Scraper Pro</strong> - Developed by <strong>Jose L Encarnacion (JoseTusabe)</strong></p>
            <p>🏢 SoloYLibre Web Dev • 📍 New York, United States • 📧 admin@soloylibre.com</p>
        </div>
    </div>
</body>
</html>
        """
    
    def print_beautiful_summary(self):
        """Print beautiful summary with colors and formatting"""
        successful = [r for r in self.results if r.status_code == 200]
        errors = [r for r in self.results if r.status_code != 200]
        
        print("\n" + "🔮" + "="*70 + "🔮")
        print("🚀 MODERN WEB SCRAPER PRO - ENHANCED RESULTS SUMMARY")
        print("🔮" + "="*70 + "🔮")
        
        # Overall stats
        print(f"\n📊 OVERALL STATISTICS:")
        print(f"   📄 Total Pages Processed: {len(self.results)}")
        print(f"   ✅ Successful Scrapes: {len(successful)}")
        print(f"   ❌ Failed Scrapes: {len(errors)}")
        print(f"   📈 Success Rate: {(len(successful)/len(self.results)*100):.1f}%")
        
        if successful:
            avg_load_time = sum(r.load_time for r in successful) / len(successful)
            total_words = sum(r.word_count for r in successful)
            total_links = sum(r.links_found for r in successful)
            total_images = sum(r.images_found for r in successful)
            
            print(f"\n⚡ PERFORMANCE METRICS:")
            print(f"   ⏱️ Average Load Time: {avg_load_time:.2f} seconds")
            print(f"   📝 Total Words Extracted: {total_words:,}")
            print(f"   🔗 Total Links Found: {total_links:,}")
            print(f"   🖼️ Total Images Found: {total_images:,}")
        
        # Detailed results
        print(f"\n📋 DETAILED RESULTS:")
        print("-" * 70)
        
        for i, result in enumerate(self.results, 1):
            status_emoji = "✅" if result.status_code == 200 else "❌"
            print(f"\n{i}. {status_emoji} {result.title}")
            print(f"   🌐 URL: {result.url}")
            print(f"   🏢 Domain: {result.domain}")
            print(f"   📊 Status: {result.status_code} | ⏱️ {result.load_time:.2f}s")
            print(f"   📄 Content: {result.word_count} words, {result.links_found} links, {result.images_found} images")
            if result.meta_description:
                print(f"   📝 Description: {result.meta_description[:100]}...")
        
        print("\n" + "🔮" + "="*70 + "🔮")
        print("💻 Developed by Jose L Encarnacion (JoseTusabe)")
        print("🏢 SoloYLibre Web Dev - New York, United States")
        print("📧 admin@soloylibre.com")
        print("🔮" + "="*70 + "🔮")

def main():
    """Enhanced demo function with beautiful results"""
    print("🚀 Modern Web Scraper Pro - Enhanced Demo")
    print("Developed by Jose L Encarnacion (JoseTusabe)")
    print("SoloYLibre Web Dev - New York, United States")
    print("-" * 60)
    
    # Enhanced test URLs with variety
    test_urls = [
        "https://httpbin.org/html",
        "https://httpbin.org/json", 
        "https://example.com",
        "https://httpbin.org/user-agent",
        "https://httpbin.org/headers"
    ]
    
    scraper = EnhancedModernScraper()
    
    # Scrape URLs
    results = scraper.scrape_multiple(test_urls)
    
    # Save results in multiple formats
    scraper.save_results("enhanced_demo")
    
    # Generate HTML report
    html_file = scraper.generate_html_report("enhanced_scraping_report")
    
    # Print beautiful summary
    scraper.print_beautiful_summary()
    
    print(f"\n🎉 Enhanced demo completed!")
    print(f"📊 HTML Report: {html_file}")
    print(f"💾 Results saved in 'results/' directory")
    print(f"🌐 Open the HTML report in your browser for beautiful visualization!")

if __name__ == "__main__":
    main()
