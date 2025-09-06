#!/usr/bin/env python3
"""
🚀 Simple Working Web Scraper
Guaranteed to work - basic but functional

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
import requests
from datetime import datetime
from urllib.parse import urlparse

class SimpleScraperHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html_content = self.get_main_page()
            self.wfile.write(html_content.encode('utf-8'))
        else:
            super().do_GET()
    
    def do_POST(self):
        if self.path == '/api/scrape':
            self.handle_scrape()
        else:
            self.send_response(404)
            self.end_headers()
    
    def handle_scrape(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            request_data = json.loads(post_data.decode('utf-8'))
            
            urls = request_data.get('urls', [])
            results = []
            
            for url in urls:
                if url.strip():
                    result = self.scrape_url(url.strip())
                    results.append(result)
            
            # Save results
            os.makedirs("exports", exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            json_file = f"exports/results_{timestamp}.json"
            
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            
            successful = [r for r in results if r['status_code'] == 200]
            
            response = {
                "status": "success",
                "results": results,
                "stats": {
                    "total": len(urls),
                    "successful": len(successful),
                    "failed": len(results) - len(successful),
                    "total_words": sum(r['word_count'] for r in successful)
                },
                "exported_file": json_file
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
            
        except Exception as e:
            error_response = {"status": "error", "message": str(e)}
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(error_response).encode('utf-8'))
    
    def scrape_url(self, url):
        start_time = time.time()
        
        try:
            print(f"🔍 Scraping: {url}")
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=30)
            content = response.text
            domain = urlparse(url).netloc
            
            # Basic analysis
            word_count = len(content.split())
            links_count = content.count('<a ')
            images_count = content.count('<img ')
            
            # Try to get title
            title = domain
            try:
                import re
                title_match = re.search(r'<title[^>]*>([^<]+)</title>', content, re.IGNORECASE)
                if title_match:
                    title = title_match.group(1).strip()
            except:
                pass
            
            load_time = time.time() - start_time
            
            result = {
                "url": url,
                "title": title,
                "content": content[:5000],  # First 5000 chars
                "full_content": content,
                "status_code": response.status_code,
                "load_time": round(load_time, 2),
                "word_count": word_count,
                "links_found": links_count,
                "images_found": images_count,
                "domain": domain,
                "timestamp": datetime.now().isoformat()
            }
            
            print(f"✅ Success: {word_count} words")
            return result
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return {
                "url": url,
                "title": "ERROR",
                "content": str(e),
                "full_content": str(e),
                "status_code": 0,
                "load_time": round(time.time() - start_time, 2),
                "word_count": 0,
                "links_found": 0,
                "images_found": 0,
                "domain": urlparse(url).netloc if url else "unknown",
                "timestamp": datetime.now().isoformat()
            }
    
    def get_main_page(self):
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🚀 Simple Working Web Scraper</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: Arial, sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; 
            min-height: 100vh; 
            padding: 20px;
        }
        .container { max-width: 1000px; margin: 0 auto; }
        .header { 
            text-align: center; 
            background: rgba(255,255,255,0.1);
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 30px;
        }
        .panel { 
            background: rgba(255,255,255,0.1); 
            padding: 20px; 
            border-radius: 10px; 
            margin-bottom: 20px;
        }
        textarea { 
            width: 100%; 
            padding: 10px; 
            border: none; 
            border-radius: 5px; 
            background: rgba(255,255,255,0.9); 
            color: #333;
        }
        button { 
            padding: 10px 20px; 
            background: #007bff; 
            color: white; 
            border: none; 
            border-radius: 5px; 
            cursor: pointer; 
            margin: 5px;
        }
        button:hover { background: #0056b3; }
        button:disabled { background: #666; cursor: not-allowed; }
        .results { 
            background: rgba(255,255,255,0.1); 
            padding: 20px; 
            border-radius: 10px; 
            margin-top: 20px;
            display: none;
        }
        .result-item { 
            background: rgba(255,255,255,0.1); 
            padding: 15px; 
            margin: 10px 0; 
            border-radius: 8px;
        }
        .success { border-left: 4px solid #28a745; }
        .error { border-left: 4px solid #dc3545; }
        .content-box { 
            background: rgba(0,0,0,0.3); 
            padding: 10px; 
            border-radius: 5px; 
            margin: 10px 0;
            max-height: 150px;
            overflow-y: auto;
            font-family: monospace;
            font-size: 12px;
        }
        .actions { margin-top: 10px; }
        .actions button { 
            padding: 5px 10px; 
            font-size: 12px; 
            background: #28a745;
        }
        .actions button:hover { background: #1e7e34; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Simple Working Web Scraper</h1>
            <p>Guaranteed to work - Real scraping with visible results</p>
            <p><strong>By Jose L Encarnacion (JoseTusabe)</strong></p>
        </div>
        
        <div class="panel">
            <h3>🌐 Enter URLs to Scrape</h3>
            <textarea id="urls" rows="5" placeholder="https://example.com
https://httpbin.org/html
https://httpbin.org/json"></textarea>
            <br><br>
            <button onclick="startScraping()" id="scrapeBtn">🚀 Start Scraping</button>
            <button onclick="loadSamples()">📄 Load Samples</button>
            <button onclick="clearAll()">🗑️ Clear</button>
            
            <div id="status" style="margin-top: 15px;"></div>
        </div>
        
        <div id="results" class="results">
            <h3>📊 Results</h3>
            <div id="results-content"></div>
        </div>
    </div>
    
    <script>
        let allResults = [];
        
        function loadSamples() {
            document.getElementById('urls').value = `https://example.com
https://httpbin.org/html
https://httpbin.org/json`;
        }
        
        function clearAll() {
            document.getElementById('urls').value = '';
            document.getElementById('results').style.display = 'none';
            document.getElementById('status').innerHTML = '';
            allResults = [];
        }
        
        function startScraping() {
            const urls = document.getElementById('urls').value.split('\\n').filter(u => u.trim());
            const btn = document.getElementById('scrapeBtn');
            
            if (urls.length === 0) {
                alert('Please enter URLs');
                return;
            }
            
            btn.disabled = true;
            btn.textContent = '🔄 Scraping...';
            
            document.getElementById('status').innerHTML = `
                <div style="background: rgba(255,255,255,0.1); padding: 10px; border-radius: 5px;">
                    🚀 Scraping ${urls.length} URLs...
                </div>
            `;
            
            fetch('/api/scrape', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ urls: urls })
            })
            .then(response => response.json())
            .then(data => {
                btn.disabled = false;
                btn.textContent = '🚀 Start Scraping';
                
                if (data.status === 'success') {
                    allResults = data.results;
                    showResults(data);
                } else {
                    showError(data.message);
                }
            })
            .catch(error => {
                btn.disabled = false;
                btn.textContent = '🚀 Start Scraping';
                showError(error.message);
            });
        }
        
        function showResults(data) {
            const resultsDiv = document.getElementById('results');
            const contentDiv = document.getElementById('results-content');
            
            resultsDiv.style.display = 'block';
            contentDiv.innerHTML = '';
            
            data.results.forEach((result, index) => {
                const div = document.createElement('div');
                div.className = 'result-item ' + (result.status_code === 200 ? 'success' : 'error');
                
                div.innerHTML = `
                    <h4>${result.status_code === 200 ? '✅' : '❌'} ${result.title}</h4>
                    <p><strong>URL:</strong> ${result.url}</p>
                    <p><strong>Status:</strong> ${result.status_code} | <strong>Time:</strong> ${result.load_time}s | <strong>Words:</strong> ${result.word_count}</p>
                    <p><strong>Links:</strong> ${result.links_found} | <strong>Images:</strong> ${result.images_found}</p>
                    
                    <div class="content-box">
                        <strong>Content Preview:</strong><br>
                        ${result.content}
                    </div>
                    
                    <div class="actions">
                        <button onclick="viewFull(${index})">👁️ View Full</button>
                        <button onclick="searchIn(${index})">🔍 Search</button>
                        <button onclick="exportOne(${index})">📄 Export</button>
                    </div>
                `;
                
                contentDiv.appendChild(div);
            });
            
            document.getElementById('status').innerHTML = `
                <div style="background: rgba(40,167,69,0.3); padding: 10px; border-radius: 5px;">
                    ✅ Completed! ${data.stats.successful}/${data.stats.total} successful
                    <br>📄 Total words: ${data.stats.total_words}
                    <br>💾 Saved: ${data.exported_file}
                </div>
            `;
        }
        
        function viewFull(index) {
            const result = allResults[index];
            const win = window.open('', '_blank', 'width=900,height=600');
            win.document.write(`
                <html>
                <head><title>Full Content - ${result.title}</title></head>
                <body style="font-family: Arial; padding: 20px;">
                    <h2>${result.title}</h2>
                    <p><strong>URL:</strong> ${result.url}</p>
                    <p><strong>Words:</strong> ${result.word_count} | <strong>Load time:</strong> ${result.load_time}s</p>
                    <hr>
                    <pre style="white-space: pre-wrap; font-size: 12px;">${result.full_content}</pre>
                </body>
                </html>
            `);
        }
        
        function searchIn(index) {
            const result = allResults[index];
            const term = prompt('Search term:');
            if (term) {
                const content = result.full_content;
                const regex = new RegExp(term, 'gi');
                const matches = content.match(regex);
                
                if (matches) {
                    const highlighted = content.replace(regex, `<mark>$&</mark>`);
                    const win = window.open('', '_blank', 'width=900,height=600');
                    win.document.write(`
                        <html>
                        <head><title>Search: ${term}</title></head>
                        <body style="font-family: Arial; padding: 20px;">
                            <h2>Search Results for "${term}"</h2>
                            <p>Found ${matches.length} matches in ${result.title}</p>
                            <hr>
                            <div style="white-space: pre-wrap; font-size: 12px;">${highlighted}</div>
                        </body>
                        </html>
                    `);
                } else {
                    alert('No matches found');
                }
            }
        }
        
        function exportOne(index) {
            const result = allResults[index];
            const data = JSON.stringify(result, null, 2);
            const blob = new Blob([data], {type: 'application/json'});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `scraped_${result.domain}.json`;
            a.click();
            URL.revokeObjectURL(url);
        }
        
        function showError(message) {
            document.getElementById('status').innerHTML = `
                <div style="background: rgba(220,53,69,0.3); padding: 10px; border-radius: 5px;">
                    ❌ Error: ${message}
                </div>
            `;
        }
        
        // Load samples on start
        loadSamples();
    </script>
</body>
</html>
        """

def start_server(port=8000):
    try:
        with socketserver.TCPServer(("", port), SimpleScraperHandler) as httpd:
            print(f"🚀 Simple Working Web Scraper")
            print(f"📍 Running at: http://localhost:{port}")
            print(f"💻 Jose L Encarnacion (JoseTusabe)")
            print("-" * 50)
            
            def open_browser():
                time.sleep(1)
                webbrowser.open(f'http://localhost:{port}')
            
            threading.Thread(target=open_browser, daemon=True).start()
            
            print("🌐 Opening browser...")
            print("Press Ctrl+C to stop")
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n🔒 Server stopped")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    start_server()
