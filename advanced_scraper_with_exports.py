#!/usr/bin/env python3
"""
🚀 Advanced Web Scraper Pro - Complete Export & Visualization System
Enhanced scraper with multiple export formats and AI training compatibility

Developed by Jose L Encarnacion (JoseTusabe)
SoloYLibre Web Dev - New York, United States
"""

import requests
import time
import json
import csv
import xml.etree.ElementTree as ET
from datetime import datetime
from urllib.parse import urljoin, urlparse
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional
import re
import os
import webbrowser

@dataclass
class EnhancedScrapedData:
    """Complete data structure for scraped content"""
    url: str
    title: str
    content: str
    clean_text: str
    status_code: int
    load_time: float
    timestamp: str
    word_count: int
    links_found: int
    images_found: int
    domain: str
    content_type: str
    meta_description: str
    meta_keywords: str
    headers: Dict[str, str]
    response_size: int
    language: str
    encoding: str
    links_list: List[str]
    images_list: List[str]
    structured_data: Dict[str, Any]

class AdvancedWebScraperPro:
    """🚀 Advanced Web Scraper with Complete Export System"""
    
    def __init__(self):
        self.session = requests.Session()
        self.results: List[EnhancedScrapedData] = []
        
        # Enhanced user agents for better compatibility
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0'
        ]
        
        self.session.headers.update({
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9,es;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0'
        })
        
        print("🚀 Advanced Web Scraper Pro initialized with enhanced export capabilities")
    
    def scrape_page(self, url: str) -> EnhancedScrapedData:
        """Enhanced scraping with complete data extraction"""
        start_time = time.time()
        
        try:
            # Rotate user agent
            import random
            self.session.headers['User-Agent'] = random.choice(self.user_agents)
            
            print(f"🔍 Scraping: {url}")
            response = self.session.get(url, timeout=30)
            
            # Basic info
            domain = urlparse(url).netloc
            content_type = response.headers.get('content-type', 'unknown')
            response_size = len(response.content)
            encoding = response.encoding or 'utf-8'
            
            # Initialize default values
            title = f"Content from {domain}"
            content = ""
            clean_text = ""
            word_count = 0
            links_found = 0
            images_found = 0
            meta_description = ""
            meta_keywords = ""
            language = "en"
            links_list = []
            images_list = []
            structured_data = {}
            
            # Process different content types
            if 'json' in content_type.lower():
                try:
                    json_data = response.json()
                    title = f"JSON API Response from {domain}"
                    content = json.dumps(json_data, indent=2)
                    clean_text = self._extract_text_from_json(json_data)
                    word_count = len(clean_text.split())
                    structured_data = {"json_data": json_data}
                except:
                    content = response.text
                    clean_text = content
                    word_count = len(content.split())
            
            elif 'xml' in content_type.lower():
                title = f"XML Document from {domain}"
                content = response.text
                clean_text = self._extract_text_from_xml(content)
                word_count = len(clean_text.split())
                
            else:
                # HTML content processing
                try:
                    from bs4 import BeautifulSoup
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Extract title
                    title_tag = soup.find('title')
                    title = title_tag.get_text(strip=True) if title_tag else f"Page from {domain}"
                    
                    # Extract meta information
                    meta_desc = soup.find('meta', attrs={'name': 'description'})
                    meta_description = meta_desc.get('content', '')[:500] if meta_desc else ""
                    
                    meta_keys = soup.find('meta', attrs={'name': 'keywords'})
                    meta_keywords = meta_keys.get('content', '') if meta_keys else ""
                    
                    # Extract language
                    html_tag = soup.find('html')
                    language = html_tag.get('lang', 'en') if html_tag else 'en'
                    
                    # Extract links
                    links = soup.find_all('a', href=True)
                    links_list = [urljoin(url, link.get('href', '')) for link in links]
                    links_found = len(links_list)
                    
                    # Extract images
                    images = soup.find_all('img', src=True)
                    images_list = [urljoin(url, img.get('src', '')) for img in images]
                    images_found = len(images_list)
                    
                    # Extract structured data (JSON-LD, microdata)
                    structured_data = self._extract_structured_data(soup)
                    
                    # Extract clean text
                    for script in soup(["script", "style", "nav", "footer", "header"]):
                        script.decompose()
                    
                    content = str(soup)
                    clean_text = soup.get_text(strip=True, separator=' ')
                    clean_text = re.sub(r'\s+', ' ', clean_text)  # Normalize whitespace
                    word_count = len(clean_text.split())
                    
                except ImportError:
                    # Fallback without BeautifulSoup
                    content = response.text
                    clean_text = re.sub(r'<[^>]+>', '', content)  # Remove HTML tags
                    clean_text = re.sub(r'\s+', ' ', clean_text)
                    word_count = len(clean_text.split())
                    links_found = content.count('<a ')
                    images_found = content.count('<img ')
                    links_list = []
                    images_list = []
            
            load_time = time.time() - start_time
            
            result = EnhancedScrapedData(
                url=url,
                title=title,
                content=content,
                clean_text=clean_text,
                status_code=response.status_code,
                load_time=load_time,
                timestamp=datetime.now().isoformat(),
                word_count=word_count,
                links_found=links_found,
                images_found=images_found,
                domain=domain,
                content_type=content_type,
                meta_description=meta_description,
                meta_keywords=meta_keywords,
                headers=dict(response.headers),
                response_size=response_size,
                language=language,
                encoding=encoding,
                links_list=links_list[:50],  # Limit for performance
                images_list=images_list[:30],  # Limit for performance
                structured_data=structured_data
            )
            
            print(f"✅ Scraped {url} in {load_time:.2f}s")
            print(f"   📄 {word_count} words, 🔗 {links_found} links, 🖼️ {images_found} images")
            print(f"   💾 {response_size:,} bytes, 🌐 {language}, 📊 {response.status_code}")
            
            return result
            
        except Exception as e:
            print(f"❌ Error scraping {url}: {e}")
            return EnhancedScrapedData(
                url=url,
                title="ERROR",
                content=str(e),
                clean_text=str(e),
                status_code=0,
                load_time=time.time() - start_time,
                timestamp=datetime.now().isoformat(),
                word_count=0,
                links_found=0,
                images_found=0,
                domain=urlparse(url).netloc if url else "unknown",
                content_type="error",
                meta_description="Error occurred",
                meta_keywords="",
                headers={},
                response_size=0,
                language="en",
                encoding="utf-8",
                links_list=[],
                images_list=[],
                structured_data={"error": str(e)}
            )
    
    def _extract_text_from_json(self, json_data: Any) -> str:
        """Extract readable text from JSON data"""
        if isinstance(json_data, dict):
            text_parts = []
            for key, value in json_data.items():
                if isinstance(value, (str, int, float)):
                    text_parts.append(f"{key}: {value}")
                elif isinstance(value, (list, dict)):
                    text_parts.append(self._extract_text_from_json(value))
            return " ".join(text_parts)
        elif isinstance(json_data, list):
            return " ".join([self._extract_text_from_json(item) for item in json_data])
        else:
            return str(json_data)
    
    def _extract_text_from_xml(self, xml_content: str) -> str:
        """Extract readable text from XML content"""
        try:
            # Remove XML tags and extract text
            clean_text = re.sub(r'<[^>]+>', ' ', xml_content)
            clean_text = re.sub(r'\s+', ' ', clean_text)
            return clean_text.strip()
        except:
            return xml_content
    
    def _extract_structured_data(self, soup) -> Dict[str, Any]:
        """Extract structured data from HTML"""
        structured = {}
        
        try:
            # JSON-LD
            json_ld_scripts = soup.find_all('script', type='application/ld+json')
            if json_ld_scripts:
                json_ld_data = []
                for script in json_ld_scripts:
                    try:
                        data = json.loads(script.string)
                        json_ld_data.append(data)
                    except:
                        pass
                if json_ld_data:
                    structured['json_ld'] = json_ld_data
            
            # Open Graph
            og_tags = soup.find_all('meta', property=lambda x: x and x.startswith('og:'))
            if og_tags:
                og_data = {}
                for tag in og_tags:
                    property_name = tag.get('property', '').replace('og:', '')
                    content = tag.get('content', '')
                    if property_name and content:
                        og_data[property_name] = content
                if og_data:
                    structured['open_graph'] = og_data
            
            # Twitter Cards
            twitter_tags = soup.find_all('meta', attrs={'name': lambda x: x and x.startswith('twitter:')})
            if twitter_tags:
                twitter_data = {}
                for tag in twitter_tags:
                    name = tag.get('name', '').replace('twitter:', '')
                    content = tag.get('content', '')
                    if name and content:
                        twitter_data[name] = content
                if twitter_data:
                    structured['twitter'] = twitter_data
                    
        except Exception as e:
            structured['extraction_error'] = str(e)
        
        return structured
    
    def scrape_multiple(self, urls: List[str]) -> List[EnhancedScrapedData]:
        """Scrape multiple URLs with enhanced progress tracking"""
        print(f"🚀 Starting advanced scrape of {len(urls)} URLs")
        print("="*80)
        
        results = []
        for i, url in enumerate(urls, 1):
            print(f"\n📄 Processing {i}/{len(urls)}: {url}")
            result = self.scrape_page(url)
            results.append(result)
            self.results.append(result)
            
            # Progress indicator
            progress = (i / len(urls)) * 100
            print(f"📊 Progress: {progress:.1f}% complete")
            
            # Respectful delay
            if i < len(urls):
                time.sleep(1.5)
        
        print(f"\n✅ Completed scraping {len(results)} URLs")
        return results

    def export_all_formats(self, base_filename: str = "scraping_results"):
        """Export results in all available formats"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = f"{base_filename}_{timestamp}"

        # Create exports directory
        os.makedirs("exports", exist_ok=True)

        exported_files = []

        # Export JSON
        json_file = self.export_json(f"exports/{base_name}")
        exported_files.append(json_file)

        # Export CSV
        csv_file = self.export_csv(f"exports/{base_name}")
        exported_files.append(csv_file)

        # Export HTML Report
        html_file = self.export_html_report(f"exports/{base_name}")
        exported_files.append(html_file)

        # Export XML
        xml_file = self.export_xml(f"exports/{base_name}")
        exported_files.append(xml_file)

        # Export AI Training Format
        ai_file = self.export_ai_training_format(f"exports/{base_name}")
        exported_files.append(ai_file)

        # Export Text Summary
        txt_file = self.export_text_summary(f"exports/{base_name}")
        exported_files.append(txt_file)

        print(f"\n💾 ALL FORMATS EXPORTED:")
        for file in exported_files:
            print(f"   📄 {file}")

        return exported_files

    def export_json(self, filename: str) -> str:
        """Export results as JSON"""
        json_file = f"{filename}.json"

        export_data = {
            "metadata": {
                "export_timestamp": datetime.now().isoformat(),
                "total_results": len(self.results),
                "successful_scrapes": len([r for r in self.results if r.status_code == 200]),
                "failed_scrapes": len([r for r in self.results if r.status_code != 200]),
                "scraper_version": "Advanced Web Scraper Pro v1.0",
                "developer": "Jose L Encarnacion (JoseTusabe)"
            },
            "results": [asdict(result) for result in self.results]
        }

        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)

        print(f"📄 JSON exported: {json_file}")
        return json_file

    def export_csv(self, filename: str) -> str:
        """Export results as CSV"""
        csv_file = f"{filename}.csv"

        if not self.results:
            return csv_file

        # Flatten the data for CSV
        flattened_data = []
        for result in self.results:
            row = {
                'url': result.url,
                'title': result.title,
                'status_code': result.status_code,
                'load_time': result.load_time,
                'timestamp': result.timestamp,
                'word_count': result.word_count,
                'links_found': result.links_found,
                'images_found': result.images_found,
                'domain': result.domain,
                'content_type': result.content_type,
                'meta_description': result.meta_description,
                'meta_keywords': result.meta_keywords,
                'response_size': result.response_size,
                'language': result.language,
                'encoding': result.encoding,
                'clean_text_preview': result.clean_text[:500] + "..." if len(result.clean_text) > 500 else result.clean_text,
                'has_structured_data': bool(result.structured_data),
                'links_count': len(result.links_list),
                'images_count': len(result.images_list)
            }
            flattened_data.append(row)

        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            if flattened_data:
                writer = csv.DictWriter(f, fieldnames=flattened_data[0].keys())
                writer.writeheader()
                writer.writerows(flattened_data)

        print(f"📊 CSV exported: {csv_file}")
        return csv_file

    def export_xml(self, filename: str) -> str:
        """Export results as XML"""
        xml_file = f"{filename}.xml"

        root = ET.Element("scraping_results")

        # Metadata
        metadata = ET.SubElement(root, "metadata")
        ET.SubElement(metadata, "export_timestamp").text = datetime.now().isoformat()
        ET.SubElement(metadata, "total_results").text = str(len(self.results))
        ET.SubElement(metadata, "scraper_version").text = "Advanced Web Scraper Pro v1.0"
        ET.SubElement(metadata, "developer").text = "Jose L Encarnacion (JoseTusabe)"

        # Results
        results_elem = ET.SubElement(root, "results")

        for i, result in enumerate(self.results):
            result_elem = ET.SubElement(results_elem, "result", id=str(i+1))

            # Basic info
            ET.SubElement(result_elem, "url").text = result.url
            ET.SubElement(result_elem, "title").text = result.title
            ET.SubElement(result_elem, "status_code").text = str(result.status_code)
            ET.SubElement(result_elem, "load_time").text = str(result.load_time)
            ET.SubElement(result_elem, "timestamp").text = result.timestamp
            ET.SubElement(result_elem, "domain").text = result.domain
            ET.SubElement(result_elem, "language").text = result.language

            # Metrics
            metrics = ET.SubElement(result_elem, "metrics")
            ET.SubElement(metrics, "word_count").text = str(result.word_count)
            ET.SubElement(metrics, "links_found").text = str(result.links_found)
            ET.SubElement(metrics, "images_found").text = str(result.images_found)
            ET.SubElement(metrics, "response_size").text = str(result.response_size)

            # Content
            content_elem = ET.SubElement(result_elem, "content")
            ET.SubElement(content_elem, "clean_text").text = result.clean_text[:1000] + "..." if len(result.clean_text) > 1000 else result.clean_text
            ET.SubElement(content_elem, "meta_description").text = result.meta_description
            ET.SubElement(content_elem, "meta_keywords").text = result.meta_keywords

        tree = ET.ElementTree(root)
        tree.write(xml_file, encoding='utf-8', xml_declaration=True)

        print(f"📋 XML exported: {xml_file}")
        return xml_file

    def export_html_report(self, filename: str) -> str:
        """Export beautiful HTML report"""
        html_file = f"{filename}_report.html"

        successful = [r for r in self.results if r.status_code == 200]
        total_words = sum(r.word_count for r in successful)
        total_links = sum(r.links_found for r in successful)
        total_images = sum(r.images_found for r in successful)
        avg_load_time = sum(r.load_time for r in successful) / len(successful) if successful else 0

        # Generate results HTML
        results_html = ""
        for i, result in enumerate(self.results, 1):
            status_class = "success" if result.status_code == 200 else "error"

            # Truncate content for display
            content_preview = result.clean_text[:300] + "..." if len(result.clean_text) > 300 else result.clean_text

            results_html += f"""
            <div class="result-card {status_class}">
                <div class="result-header">
                    <h3>#{i}. {result.title}</h3>
                    <span class="status status-{status_class}">{result.status_code}</span>
                </div>
                <div class="result-details">
                    <p><strong>🌐 URL:</strong> <a href="{result.url}" target="_blank">{result.url}</a></p>
                    <p><strong>🏢 Domain:</strong> {result.domain}</p>
                    <p><strong>🌍 Language:</strong> {result.language}</p>
                    <p><strong>📄 Content Type:</strong> {result.content_type}</p>
                    <p><strong>💾 Size:</strong> {result.response_size:,} bytes</p>
                    {f'<p><strong>📝 Description:</strong> {result.meta_description}</p>' if result.meta_description else ''}
                    {f'<p><strong>🏷️ Keywords:</strong> {result.meta_keywords}</p>' if result.meta_keywords else ''}

                    <div class="metrics">
                        <span class="metric">⏱️ {result.load_time:.2f}s</span>
                        <span class="metric">📝 {result.word_count:,} words</span>
                        <span class="metric">🔗 {result.links_found} links</span>
                        <span class="metric">🖼️ {result.images_found} images</span>
                    </div>

                    <div class="content-preview">
                        <strong>📋 Content Preview:</strong>
                        <div class="content-text">{content_preview}</div>
                    </div>

                    {self._generate_structured_data_html(result.structured_data) if result.structured_data else ''}
                </div>
            </div>
            """

        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🚀 Advanced Web Scraper Pro - Complete Results Report</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; min-height: 100vh; padding: 20px;
        }}
        .container {{ max-width: 1400px; margin: 0 auto; }}
        .header {{ text-align: center; margin-bottom: 40px; }}
        .header h1 {{ font-size: 2.5em; margin-bottom: 10px; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); }}
        .header p {{ font-size: 1.1em; opacity: 0.9; }}

        .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 40px; }}
        .stat-card {{
            background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px;
            text-align: center; backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.2);
        }}
        .stat-card h3 {{ font-size: 2em; margin-bottom: 5px; color: #00d4ff; }}
        .stat-card p {{ font-size: 0.9em; opacity: 0.8; }}

        .export-info {{
            background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px;
            margin-bottom: 30px; backdrop-filter: blur(10px);
        }}

        .result-card {{
            background: rgba(255,255,255,0.1); margin: 20px 0; padding: 25px;
            border-radius: 15px; backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.2);
        }}
        .result-card.success {{ border-left: 5px solid #28a745; }}
        .result-card.error {{ border-left: 5px solid #dc3545; }}

        .result-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }}
        .result-header h3 {{ color: #00d4ff; font-size: 1.3em; }}

        .status {{ padding: 8px 15px; border-radius: 20px; font-weight: bold; font-size: 0.9em; }}
        .status-success {{ background: #28a745; }}
        .status-error {{ background: #dc3545; }}

        .result-details p {{ margin: 8px 0; line-height: 1.4; }}
        .result-details strong {{ color: #00d4ff; }}

        .metrics {{ display: flex; gap: 15px; margin: 15px 0; flex-wrap: wrap; }}
        .metric {{
            background: rgba(255,255,255,0.2); padding: 8px 15px;
            border-radius: 20px; font-size: 0.9em; font-weight: bold;
        }}

        .content-preview {{
            background: rgba(255,255,255,0.1); padding: 20px;
            border-radius: 10px; margin-top: 15px;
        }}
        .content-text {{
            font-style: italic; opacity: 0.9; line-height: 1.5;
            max-height: 120px; overflow: hidden; position: relative;
        }}

        .structured-data {{
            background: rgba(0, 212, 255, 0.1); padding: 15px;
            border-radius: 8px; margin-top: 15px; border: 1px solid rgba(0, 212, 255, 0.3);
        }}

        a {{ color: #00d4ff; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}

        .footer {{ text-align: center; margin-top: 50px; padding: 30px; opacity: 0.8; }}
        .export-buttons {{ text-align: center; margin: 30px 0; }}
        .btn {{
            display: inline-block; padding: 12px 25px; background: #00d4ff;
            color: white; text-decoration: none; border-radius: 25px;
            margin: 5px; font-weight: bold; transition: all 0.3s ease;
        }}
        .btn:hover {{ background: #00a8cc; transform: translateY(-2px); }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Advanced Web Scraper Pro</h1>
            <p>Complete Results Report with Enhanced Data Extraction</p>
            <p><strong>Generated:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
        </div>

        <div class="export-info">
            <h3>📊 Export Information</h3>
            <p><strong>Total URLs Processed:</strong> {len(self.results)}</p>
            <p><strong>Export Formats Available:</strong> JSON, CSV, XML, HTML, AI Training Format, Text Summary</p>
            <p><strong>Developer:</strong> Jose L Encarnacion (JoseTusabe) - SoloYLibre Web Dev</p>
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
            <div class="stat-card">
                <h3>{total_images:,}</h3>
                <p>Total Images</p>
            </div>
        </div>

        <div class="results">
            <h2>📋 Detailed Results</h2>
            {results_html}
        </div>

        <div class="footer">
            <p>🚀 <strong>Advanced Web Scraper Pro</strong> - Developed by <strong>Jose L Encarnacion (JoseTusabe)</strong></p>
            <p>🏢 SoloYLibre Web Dev • 📍 New York, United States • 📧 admin@soloylibre.com</p>
            <p>🌐 GitHub: @joselenc12 • 🔗 Website: SoloYLibre.com</p>
        </div>
    </div>
</body>
</html>
        """

        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"📊 HTML Report exported: {html_file}")
        return html_file

    def _generate_structured_data_html(self, structured_data: Dict[str, Any]) -> str:
        """Generate HTML for structured data display"""
        if not structured_data:
            return ""

        html = '<div class="structured-data"><strong>🔍 Structured Data Found:</strong><br>'

        for key, value in structured_data.items():
            if key == 'json_ld' and isinstance(value, list):
                html += f"<strong>JSON-LD:</strong> {len(value)} schema(s) found<br>"
            elif key == 'open_graph' and isinstance(value, dict):
                html += f"<strong>Open Graph:</strong> {len(value)} properties<br>"
            elif key == 'twitter' and isinstance(value, dict):
                html += f"<strong>Twitter Cards:</strong> {len(value)} properties<br>"
            else:
                html += f"<strong>{key}:</strong> {str(value)[:100]}...<br>"

        html += '</div>'
        return html

    def export_ai_training_format(self, filename: str) -> str:
        """Export in AI training compatible format"""
        ai_file = f"{filename}_ai_training.jsonl"

        with open(ai_file, 'w', encoding='utf-8') as f:
            for result in self.results:
                if result.status_code == 200 and result.clean_text:
                    # Create AI training format (JSONL)
                    training_data = {
                        "url": result.url,
                        "domain": result.domain,
                        "title": result.title,
                        "content": result.clean_text,
                        "metadata": {
                            "language": result.language,
                            "word_count": result.word_count,
                            "content_type": result.content_type,
                            "meta_description": result.meta_description,
                            "meta_keywords": result.meta_keywords,
                            "links_count": result.links_found,
                            "images_count": result.images_found,
                            "timestamp": result.timestamp,
                            "response_size": result.response_size
                        },
                        "structured_data": result.structured_data,
                        "links": result.links_list,
                        "images": result.images_list
                    }

                    f.write(json.dumps(training_data, ensure_ascii=False) + '\n')

        print(f"🤖 AI Training format exported: {ai_file}")
        return ai_file

    def export_text_summary(self, filename: str) -> str:
        """Export text summary for quick review"""
        txt_file = f"{filename}_summary.txt"

        successful = [r for r in self.results if r.status_code == 200]

        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write("🚀 ADVANCED WEB SCRAPER PRO - TEXT SUMMARY REPORT\n")
            f.write("=" * 80 + "\n\n")

            f.write(f"📊 SUMMARY STATISTICS:\n")
            f.write(f"   Total URLs Processed: {len(self.results)}\n")
            f.write(f"   Successful Scrapes: {len(successful)}\n")
            f.write(f"   Failed Scrapes: {len(self.results) - len(successful)}\n")
            f.write(f"   Success Rate: {(len(successful)/len(self.results)*100):.1f}%\n")
            f.write(f"   Export Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            if successful:
                total_words = sum(r.word_count for r in successful)
                total_links = sum(r.links_found for r in successful)
                total_images = sum(r.images_found for r in successful)
                avg_load_time = sum(r.load_time for r in successful) / len(successful)

                f.write(f"📈 PERFORMANCE METRICS:\n")
                f.write(f"   Total Words Extracted: {total_words:,}\n")
                f.write(f"   Total Links Found: {total_links:,}\n")
                f.write(f"   Total Images Found: {total_images:,}\n")
                f.write(f"   Average Load Time: {avg_load_time:.2f} seconds\n\n")

            f.write(f"📋 DETAILED RESULTS:\n")
            f.write("-" * 80 + "\n\n")

            for i, result in enumerate(self.results, 1):
                status_emoji = "✅" if result.status_code == 200 else "❌"
                f.write(f"{i}. {status_emoji} {result.title}\n")
                f.write(f"   URL: {result.url}\n")
                f.write(f"   Domain: {result.domain}\n")
                f.write(f"   Status: {result.status_code} | Load Time: {result.load_time:.2f}s\n")
                f.write(f"   Language: {result.language} | Size: {result.response_size:,} bytes\n")
                f.write(f"   Content: {result.word_count:,} words, {result.links_found} links, {result.images_found} images\n")

                if result.meta_description:
                    f.write(f"   Description: {result.meta_description[:200]}...\n")

                if result.clean_text and result.status_code == 200:
                    f.write(f"   Content Preview: {result.clean_text[:300]}...\n")

                f.write("\n" + "-" * 40 + "\n\n")

            f.write("🚀 Advanced Web Scraper Pro - Developed by Jose L Encarnacion (JoseTusabe)\n")
            f.write("🏢 SoloYLibre Web Dev - New York, United States\n")
            f.write("📧 admin@soloylibre.com | 🌐 GitHub: @joselenc12\n")

        print(f"📄 Text summary exported: {txt_file}")
        return txt_file

    def print_enhanced_summary(self):
        """Print enhanced summary with complete statistics"""
        successful = [r for r in self.results if r.status_code == 200]
        errors = [r for r in self.results if r.status_code != 200]

        print("\n" + "🔮" + "="*80 + "🔮")
        print("🚀 ADVANCED WEB SCRAPER PRO - COMPLETE RESULTS SUMMARY")
        print("🔮" + "="*80 + "🔮")

        # Overall stats
        print(f"\n📊 OVERALL STATISTICS:")
        print(f"   📄 Total Pages Processed: {len(self.results)}")
        print(f"   ✅ Successful Scrapes: {len(successful)}")
        print(f"   ❌ Failed Scrapes: {len(errors)}")
        print(f"   📈 Success Rate: {(len(successful)/len(self.results)*100):.1f}%")
        print(f"   🕐 Processing Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        if successful:
            total_words = sum(r.word_count for r in successful)
            total_links = sum(r.links_found for r in successful)
            total_images = sum(r.images_found for r in successful)
            total_size = sum(r.response_size for r in successful)
            avg_load_time = sum(r.load_time for r in successful) / len(successful)

            print(f"\n⚡ PERFORMANCE METRICS:")
            print(f"   ⏱️ Average Load Time: {avg_load_time:.2f} seconds")
            print(f"   📝 Total Words Extracted: {total_words:,}")
            print(f"   🔗 Total Links Found: {total_links:,}")
            print(f"   🖼️ Total Images Found: {total_images:,}")
            print(f"   💾 Total Data Size: {total_size:,} bytes ({total_size/1024/1024:.2f} MB)")

            # Language distribution
            languages = {}
            for result in successful:
                lang = result.language
                languages[lang] = languages.get(lang, 0) + 1

            print(f"\n🌍 LANGUAGE DISTRIBUTION:")
            for lang, count in sorted(languages.items(), key=lambda x: x[1], reverse=True):
                print(f"   {lang}: {count} pages")

            # Domain distribution
            domains = {}
            for result in successful:
                domain = result.domain
                domains[domain] = domains.get(domain, 0) + 1

            print(f"\n🏢 DOMAIN DISTRIBUTION:")
            for domain, count in sorted(domains.items(), key=lambda x: x[1], reverse=True)[:10]:
                print(f"   {domain}: {count} pages")

        # Export information
        print(f"\n💾 EXPORT FORMATS AVAILABLE:")
        print(f"   📄 JSON - Complete structured data")
        print(f"   📊 CSV - Tabular format for analysis")
        print(f"   📋 XML - Structured markup format")
        print(f"   🌐 HTML - Beautiful visual reports")
        print(f"   🤖 AI Training - JSONL format for ML")
        print(f"   📝 Text Summary - Human-readable overview")

        print("\n" + "🔮" + "="*80 + "🔮")
        print("💻 Developed by Jose L Encarnacion (JoseTusabe)")
        print("🏢 SoloYLibre Web Dev - New York, United States")
        print("📧 admin@soloylibre.com | 🌐 GitHub: @joselenc12")
        print("🔮" + "="*80 + "🔮")

def main():
    """Enhanced demo with complete export functionality"""
    print("🚀 Advanced Web Scraper Pro - Complete Export System Demo")
    print("Developed by Jose L Encarnacion (JoseTusabe)")
    print("SoloYLibre Web Dev - New York, United States")
    print("-" * 80)

    # Enhanced test URLs with variety
    test_urls = [
        "https://httpbin.org/html",
        "https://httpbin.org/json",
        "https://example.com",
        "https://httpbin.org/user-agent",
        "https://httpbin.org/headers",
        "https://httpbin.org/xml"
    ]

    print(f"🎯 Testing with {len(test_urls)} diverse URLs...")

    scraper = AdvancedWebScraperPro()

    # Scrape URLs
    results = scraper.scrape_multiple(test_urls)

    # Export in all formats
    exported_files = scraper.export_all_formats("advanced_demo")

    # Print enhanced summary
    scraper.print_enhanced_summary()

    print(f"\n🎉 Advanced demo completed!")
    print(f"📊 {len(exported_files)} export files generated in 'exports/' directory")
    print(f"🌐 Open the HTML report for beautiful visualization!")

    # Open HTML report automatically
    html_files = [f for f in exported_files if f.endswith('_report.html')]
    if html_files:
        print(f"🌐 Opening HTML report: {html_files[0]}")
        webbrowser.open(f"file:///{os.path.abspath(html_files[0])}")

if __name__ == "__main__":
    main()
