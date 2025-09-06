#!/usr/bin/env python3
"""
🚀 Working Web Scraper Pro - Fully Functional Version
Complete working scraper with modern theme and all features

Developed by Jose L Encarnacion (JoseTusabe)
SoloYLibre Web Dev - New York, United States
"""

import http.server
import socketserver
import webbrowser
import threading
import time
import json
import os
import urllib.parse
from datetime import datetime
import requests
from urllib.parse import urljoin, urlparse
from dataclasses import dataclass, asdict
from typing import List, Dict, Any

@dataclass
class ScrapedResult:
    """Simple data structure for scraped content"""
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

class WorkingScraper:
    """Simple working scraper"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
    
    def scrape_url(self, url: str) -> ScrapedResult:
        """Scrape a single URL"""
        start_time = time.time()
        
        try:
            print(f"🔍 Scraping: {url}")
            response = self.session.get(url, timeout=30)
            
            domain = urlparse(url).netloc
            title = f"Content from {domain}"
            content = response.text
            word_count = len(content.split())
            links_found = content.count('<a ')
            images_found = content.count('<img ')
            
            # Try to extract title
            try:
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(response.content, 'html.parser')
                title_tag = soup.find('title')
                if title_tag:
                    title = title_tag.get_text(strip=True)
                
                # Clean content
                for script in soup(["script", "style"]):
                    script.decompose()
                content = soup.get_text(strip=True, separator=' ')
                word_count = len(content.split())
                links_found = len(soup.find_all('a', href=True))
                images_found = len(soup.find_all('img', src=True))
            except ImportError:
                # Fallback without BeautifulSoup
                pass
            
            load_time = time.time() - start_time
            
            result = ScrapedResult(
                url=url,
                title=title,
                content=content,
                status_code=response.status_code,
                load_time=load_time,
                timestamp=datetime.now().isoformat(),
                word_count=word_count,
                links_found=links_found,
                images_found=images_found,
                domain=domain
            )
            
            print(f"✅ Success: {word_count} words, {links_found} links, {images_found} images")
            return result
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return ScrapedResult(
                url=url,
                title="ERROR",
                content=str(e),
                status_code=0,
                load_time=time.time() - start_time,
                timestamp=datetime.now().isoformat(),
                word_count=0,
                links_found=0,
                images_found=0,
                domain=urlparse(url).netloc if url else "unknown"
            )

class WorkingScraperHandler(http.server.SimpleHTTPRequestHandler):
    """Working handler with all functionality"""
    
    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html_content = self.get_main_page()
            self.wfile.write(html_content.encode('utf-8'))
        else:
            super().do_GET()
    
    def do_POST(self):
        """Handle POST requests"""
        if self.path == '/api/scrape':
            self.handle_scrape_api()
        else:
            self.send_response(404)
            self.end_headers()
    
    def handle_scrape_api(self):
        """Handle scraping API"""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            request_data = json.loads(post_data.decode('utf-8'))
            
            urls = request_data.get('urls', [])
            
            # Perform scraping
            scraper = WorkingScraper()
            results = []
            
            for url in urls:
                if url.strip():
                    result = scraper.scrape_url(url.strip())
                    results.append(asdict(result))
            
            # Save results
            os.makedirs("exports", exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Save JSON
            json_file = f"exports/scraping_results_{timestamp}.json"
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            
            # Save CSV
            csv_file = f"exports/scraping_results_{timestamp}.csv"
            try:
                import pandas as pd
                df = pd.DataFrame(results)
                df.to_csv(csv_file, index=False, encoding='utf-8')
            except ImportError:
                csv_file = None
            
            successful = [r for r in results if r['status_code'] == 200]
            
            response = {
                "status": "success",
                "message": f"Scraping completed for {len(urls)} URLs",
                "results": results,
                "stats": {
                    "total_urls": len(urls),
                    "successful": len(successful),
                    "failed": len(results) - len(successful),
                    "total_words": sum(r['word_count'] for r in successful),
                    "total_links": sum(r['links_found'] for r in successful),
                    "total_images": sum(r['images_found'] for r in successful)
                },
                "exported_files": [json_file] + ([csv_file] if csv_file else [])
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
            
        except Exception as e:
            error_response = {
                "status": "error",
                "message": f"Scraping failed: {str(e)}",
                "results": []
            }
            
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(error_response).encode('utf-8'))
    
    def get_main_page(self):
        """Generate main page with working functionality"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🚀 Working Web Scraper Pro</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white; 
            min-height: 100vh; 
            padding: 20px;
        }
        
        .container { max-width: 1200px; margin: 0 auto; }
        
        .header { 
            text-align: center; 
            margin-bottom: 40px; 
            background: rgba(255,255,255,0.1);
            padding: 30px;
            border-radius: 15px;
            backdrop-filter: blur(10px);
        }
        
        .header h1 { 
            font-size: 3em; 
            margin-bottom: 10px; 
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .scraper-panel { 
            background: rgba(255,255,255,0.1); 
            padding: 30px; 
            border-radius: 15px; 
            backdrop-filter: blur(10px); 
            margin-bottom: 30px;
        }
        
        .input-group { margin: 20px 0; }
        .input-group label { 
            display: block; 
            margin-bottom: 8px; 
            font-weight: bold; 
        }
        
        .input-group textarea { 
            width: 100%; 
            padding: 12px; 
            border: none; 
            border-radius: 8px; 
            background: rgba(255,255,255,0.9); 
            color: #333; 
            font-size: 14px;
            resize: vertical;
        }
        
        .btn { 
            padding: 12px 25px; 
            background: #00d4ff; 
            color: white; 
            border: none; 
            border-radius: 8px; 
            cursor: pointer; 
            font-weight: bold; 
            margin: 10px 5px; 
            transition: all 0.3s ease;
        }
        
        .btn:hover { 
            background: #00a8cc; 
            transform: translateY(-2px); 
        }
        
        .btn:disabled {
            background: #666;
            cursor: not-allowed;
            transform: none;
        }
        
        .results { 
            background: rgba(255,255,255,0.1); 
            padding: 20px; 
            border-radius: 10px; 
            margin-top: 20px; 
            max-height: 600px; 
            overflow-y: auto;
            display: none;
        }
        
        .result-item { 
            background: rgba(255,255,255,0.1); 
            padding: 20px; 
            margin: 15px 0; 
            border-radius: 10px; 
            border-left: 4px solid #00d4ff;
        }
        
        .result-item.success { border-left-color: #28a745; }
        .result-item.error { border-left-color: #dc3545; }
        
        .status { 
            padding: 4px 8px; 
            border-radius: 4px; 
            font-size: 0.8em; 
            font-weight: bold; 
        }
        .status.success { background: #28a745; }
        .status.error { background: #dc3545; }
        
        .content-preview { 
            background: rgba(255,255,255,0.1); 
            padding: 15px; 
            border-radius: 8px; 
            margin-top: 10px; 
            max-height: 200px; 
            overflow-y: auto;
            font-family: monospace;
            font-size: 12px;
        }
        
        .action-buttons { margin-top: 15px; }
        .action-buttons button { 
            padding: 8px 15px; 
            margin: 5px; 
            border: none; 
            border-radius: 5px; 
            background: #007bff; 
            color: white; 
            cursor: pointer; 
            font-size: 12px;
        }
        
        .action-buttons button:hover { background: #0056b3; }
        
        .export-info {
            background: rgba(40, 167, 69, 0.2);
            padding: 15px;
            border-radius: 8px;
            margin-top: 20px;
            border: 1px solid rgba(40, 167, 69, 0.3);
        }
        
        .footer { 
            text-align: center; 
            margin-top: 60px; 
            opacity: 0.8; 
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Working Web Scraper Pro</h1>
            <p>Advanced Web Scraping with Real Results</p>
            <p><strong>Developed by Jose L Encarnacion (JoseTusabe)</strong></p>
        </div>
        
        <div class="scraper-panel">
            <h3>🌐 Web Scraping Interface</h3>
            
            <div class="input-group">
                <label>Enter URLs to scrape (one per line):</label>
                <textarea id="urls" rows="6" placeholder="https://example.com
https://httpbin.org/html
https://httpbin.org/json
https://httpbin.org/user-agent"></textarea>
            </div>
            
            <button class="btn" onclick="startScraping()" id="scrapeBtn">🚀 Start Scraping</button>
            <button class="btn" onclick="loadSamples()">📄 Load Samples</button>
            <button class="btn" onclick="clearResults()">🗑️ Clear Results</button>
            
            <div id="status" style="margin-top: 20px;"></div>
        </div>
        
        <div id="results" class="results">
            <h3>📊 Scraping Results</h3>
            <div id="results-content"></div>
        </div>
        
        <div class="footer">
            <p>🏢 SoloYLibre Web Dev • 📍 New York, United States • 📧 admin@soloylibre.com</p>
            <p>© 2024 Jose L Encarnacion (JoseTusabe) - Made with ❤️</p>
        </div>
    </div>
    
    <script>
        let scrapingResults = [];
        
        function loadSamples() {
            document.getElementById('urls').value = `https://httpbin.org/html
https://httpbin.org/json
https://example.com
https://httpbin.org/user-agent`;
        }
        
        function clearResults() {
            document.getElementById('results').style.display = 'none';
            document.getElementById('results-content').innerHTML = '';
            document.getElementById('status').innerHTML = '';
            scrapingResults = [];
        }
        
        function startScraping() {
            const urls = document.getElementById('urls').value.split('\\n').filter(url => url.trim());
            const scrapeBtn = document.getElementById('scrapeBtn');
            
            if (urls.length === 0) {
                alert('Please enter at least one URL');
                return;
            }
            
            scrapeBtn.disabled = true;
            scrapeBtn.textContent = '🔄 Scraping...';
            
            document.getElementById('status').innerHTML = `
                <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 8px;">
                    🚀 Starting scrape of ${urls.length} URLs...
                </div>
            `;
            
            fetch('/api/scrape', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ urls: urls })
            })
            .then(response => response.json())
            .then(data => {
                scrapeBtn.disabled = false;
                scrapeBtn.textContent = '🚀 Start Scraping';
                
                if (data.results) {
                    scrapingResults = data.results;
                    displayResults(data);
                } else {
                    showError(data.message || 'Unknown error');
                }
            })
            .catch(error => {
                scrapeBtn.disabled = false;
                scrapeBtn.textContent = '🚀 Start Scraping';
                showError(error.message);
            });
        }
        
        function displayResults(data) {
            const resultsDiv = document.getElementById('results');
            const contentDiv = document.getElementById('results-content');
            
            resultsDiv.style.display = 'block';
            contentDiv.innerHTML = '';
            
            data.results.forEach((result, index) => {
                const resultItem = document.createElement('div');
                resultItem.className = 'result-item ' + (result.status_code === 200 ? 'success' : 'error');
                
                resultItem.innerHTML = `
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                        <strong>🌐 ${result.url}</strong>
                        <span class="status ${result.status_code === 200 ? 'success' : 'error'}">
                            ${result.status_code === 200 ? '✅ ' + result.status_code : '❌ ' + result.status_code}
                        </span>
                    </div>
                    
                    <div style="margin-bottom: 10px;">
                        <strong>📝 Title:</strong> ${result.title}
                    </div>
                    
                    <div style="display: flex; gap: 15px; margin-bottom: 15px; flex-wrap: wrap;">
                        <span style="background: rgba(255,255,255,0.2); padding: 5px 10px; border-radius: 15px; font-size: 0.9em;">
                            ⏱️ ${result.load_time.toFixed(2)}s
                        </span>
                        <span style="background: rgba(255,255,255,0.2); padding: 5px 10px; border-radius: 15px; font-size: 0.9em;">
                            📄 ${result.word_count.toLocaleString()} words
                        </span>
                        <span style="background: rgba(255,255,255,0.2); padding: 5px 10px; border-radius: 15px; font-size: 0.9em;">
                            🔗 ${result.links_found} links
                        </span>
                        <span style="background: rgba(255,255,255,0.2); padding: 5px 10px; border-radius: 15px; font-size: 0.9em;">
                            🖼️ ${result.images_found} images
                        </span>
                    </div>
                    
                    <div class="content-preview">
                        <strong>📄 Content Preview:</strong><br>
                        ${(result.content || 'No content').substring(0, 300)}...
                    </div>
                    
                    <div class="action-buttons">
                        <button onclick="viewFullContent(${index})">👁️ View Full</button>
                        <button onclick="searchContent(${index})">🔍 Search</button>
                        <button onclick="exportSingle(${index})">📄 Export</button>
                        <button onclick="analyzeContent(${index})">📊 Analyze</button>
                    </div>
                `;
                
                contentDiv.appendChild(resultItem);
            });
            
            // Show export info
            if (data.exported_files && data.exported_files.length > 0) {
                const exportInfo = document.createElement('div');
                exportInfo.className = 'export-info';
                exportInfo.innerHTML = `
                    <h4>📄 Files Exported:</h4>
                    ${data.exported_files.map(file => `<p>💾 ${file}</p>`).join('')}
                `;
                contentDiv.appendChild(exportInfo);
            }
            
            // Update status
            const successful = data.results.filter(r => r.status_code === 200).length;
            document.getElementById('status').innerHTML = `
                <div style="background: rgba(40, 167, 69, 0.3); padding: 15px; border-radius: 8px;">
                    🎉 Scraping completed! ${successful}/${data.results.length} successful
                    <br><strong>📊 Total:</strong> ${data.stats.total_words} words, ${data.stats.total_links} links, ${data.stats.total_images} images
                </div>
            `;
        }
        
        function viewFullContent(index) {
            const result = scrapingResults[index];
            if (!result) return;
            
            const newWindow = window.open('', '_blank', 'width=1000,height=700');
            newWindow.document.write(`
                <html>
                <head>
                    <title>Full Content - ${result.title}</title>
                    <style>
                        body { font-family: Arial, sans-serif; padding: 20px; line-height: 1.6; }
                        .header { background: #f4f4f4; padding: 15px; border-radius: 5px; margin-bottom: 20px; }
                        .content { white-space: pre-wrap; font-family: monospace; }
                    </style>
                </head>
                <body>
                    <div class="header">
                        <h2>${result.title}</h2>
                        <p><strong>URL:</strong> ${result.url}</p>
                        <p><strong>Words:</strong> ${result.word_count} | <strong>Links:</strong> ${result.links_found} | <strong>Images:</strong> ${result.images_found}</p>
                    </div>
                    <div class="content">${result.content}</div>
                </body>
                </html>
            `);
        }
        
        function searchContent(index) {
            const result = scrapingResults[index];
            if (!result) return;
            
            const searchTerm = prompt('Enter search term:');
            if (searchTerm) {
                const content = result.content || '';
                const regex = new RegExp(searchTerm, 'gi');
                const matches = content.match(regex);
                const matchCount = matches ? matches.length : 0;
                
                if (matchCount > 0) {
                    const highlightedContent = content.replace(regex, `<mark style="background: yellow;">$&</mark>`);
                    const newWindow = window.open('', '_blank', 'width=1000,height=700');
                    newWindow.document.write(`
                        <html>
                        <head>
                            <title>Search Results - ${searchTerm}</title>
                            <style>
                                body { font-family: Arial, sans-serif; padding: 20px; line-height: 1.6; }
                                .header { background: #f4f4f4; padding: 15px; border-radius: 5px; margin-bottom: 20px; }
                                .content { white-space: pre-wrap; font-family: monospace; }
                                mark { background: yellow; padding: 2px; }
                            </style>
                        </head>
                        <body>
                            <div class="header">
                                <h2>Search Results for "${searchTerm}"</h2>
                                <p><strong>Found:</strong> ${matchCount} matches in ${result.title}</p>
                            </div>
                            <div class="content">${highlightedContent}</div>
                        </body>
                        </html>
                    `);
                } else {
                    alert(`No matches found for "${searchTerm}"`);
                }
            }
        }
        
        function exportSingle(index) {
            const result = scrapingResults[index];
            if (!result) return;
            
            const exportData = {
                url: result.url,
                title: result.title,
                content: result.content,
                metadata: {
                    word_count: result.word_count,
                    links_found: result.links_found,
                    images_found: result.images_found,
                    domain: result.domain,
                    load_time: result.load_time,
                    status_code: result.status_code,
                    timestamp: result.timestamp
                }
            };
            
            const dataStr = JSON.stringify(exportData, null, 2);
            const dataBlob = new Blob([dataStr], {type: 'application/json'});
            const url = URL.createObjectURL(dataBlob);
            const link = document.createElement('a');
            link.href = url;
            link.download = `scraped_${result.domain}_${new Date().toISOString().slice(0,10)}.json`;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            URL.revokeObjectURL(url);
        }
        
        function analyzeContent(index) {
            const result = scrapingResults[index];
            if (!result) return;
            
            const content = result.content || '';
            const sentences = content.split(/[.!?]+/).filter(s => s.trim().length > 0);
            const paragraphs = content.split(/\\n\\s*\\n/).filter(p => p.trim().length > 0);
            const avgWordsPerSentence = sentences.length > 0 ? (result.word_count / sentences.length).toFixed(1) : 0;
            
            alert(`📊 Content Analysis for ${result.title}:
            
📄 Words: ${result.word_count}
📝 Sentences: ${sentences.length}
📋 Paragraphs: ${paragraphs.length}
📊 Avg words per sentence: ${avgWordsPerSentence}
🔗 Links: ${result.links_found}
🖼️ Images: ${result.images_found}
⏱️ Load time: ${result.load_time.toFixed(2)}s`);
        }
        
        function showError(message) {
            document.getElementById('status').innerHTML = `
                <div style="background: rgba(220, 53, 69, 0.3); padding: 15px; border-radius: 8px;">
                    ❌ Error: ${message}
                </div>
            `;
        }
        
        // Load samples on page load
        window.onload = function() {
            loadSamples();
        };
    </script>
</body>
</html>
        """

def start_working_server(port=8000):
    """Start the working server"""
    try:
        with socketserver.TCPServer(("", port), WorkingScraperHandler) as httpd:
            print(f"🚀 Working Web Scraper Pro")
            print(f"📍 Server running at: http://localhost:{port}")
            print(f"💻 Developed by Jose L Encarnacion (JoseTusabe)")
            print(f"🏢 SoloYLibre Web Dev - New York, United States")
            print("-" * 60)
            
            # Open browser automatically
            def open_browser():
                time.sleep(1)
                webbrowser.open(f'http://localhost:{port}')
            
            browser_thread = threading.Thread(target=open_browser)
            browser_thread.daemon = True
            browser_thread.start()
            
            print(f"🌐 Opening browser automatically...")
            print(f"🔧 Press Ctrl+C to stop the server")
            
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print(f"\n🔒 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

if __name__ == "__main__":
    start_working_server()
