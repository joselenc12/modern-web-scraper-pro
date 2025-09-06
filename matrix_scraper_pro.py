#!/usr/bin/env python3
"""
🔥 Matrix Web Scraper Pro - Cyberpunk Edition
Advanced web scraper with Matrix theme and perfect text visibility

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
import re

class MatrixScraperHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html_content = self.get_matrix_page()
            self.wfile.write(html_content.encode('utf-8'))
        else:
            super().do_GET()
    
    def do_POST(self):
        if self.path == '/api/scrape':
            self.handle_matrix_scrape()
        else:
            self.send_response(404)
            self.end_headers()
    
    def handle_matrix_scrape(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            request_data = json.loads(post_data.decode('utf-8'))
            
            urls = request_data.get('urls', [])
            results = []
            
            for url in urls:
                if url.strip():
                    result = self.matrix_scrape_url(url.strip())
                    results.append(result)
            
            # Save results
            os.makedirs("matrix_exports", exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            json_file = f"matrix_exports/matrix_results_{timestamp}.json"
            
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
                    "total_words": sum(r['word_count'] for r in successful),
                    "total_chars": sum(r['char_count'] for r in successful)
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
    
    def matrix_scrape_url(self, url):
        start_time = time.time()
        
        try:
            print(f"🔍 MATRIX SCRAPING: {url}")
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=30)
            raw_content = response.text
            domain = urlparse(url).netloc
            
            # Extract title
            title = domain
            try:
                title_match = re.search(r'<title[^>]*>([^<]+)</title>', raw_content, re.IGNORECASE)
                if title_match:
                    title = title_match.group(1).strip()
            except:
                pass
            
            # Clean content for display
            clean_content = self.clean_html_content(raw_content)
            
            # Basic analysis
            word_count = len(clean_content.split())
            char_count = len(clean_content)
            links_count = raw_content.count('<a ')
            images_count = raw_content.count('<img ')
            
            load_time = time.time() - start_time
            
            result = {
                "url": url,
                "title": title,
                "content": clean_content[:2000],  # First 2000 chars for preview
                "full_content": clean_content,
                "raw_html": raw_content,
                "status_code": response.status_code,
                "load_time": round(load_time, 2),
                "word_count": word_count,
                "char_count": char_count,
                "links_found": links_count,
                "images_found": images_count,
                "domain": domain,
                "timestamp": datetime.now().isoformat(),
                "content_type": response.headers.get('content-type', 'unknown')
            }
            
            print(f"✅ MATRIX SUCCESS: {word_count} words, {char_count} chars")
            return result
            
        except Exception as e:
            print(f"❌ MATRIX ERROR: {e}")
            return {
                "url": url,
                "title": "MATRIX ERROR",
                "content": f"ERROR: {str(e)}",
                "full_content": f"ERROR: {str(e)}",
                "raw_html": "",
                "status_code": 0,
                "load_time": round(time.time() - start_time, 2),
                "word_count": 0,
                "char_count": 0,
                "links_found": 0,
                "images_found": 0,
                "domain": urlparse(url).netloc if url else "unknown",
                "timestamp": datetime.now().isoformat(),
                "content_type": "error"
            }
    
    def clean_html_content(self, html_content):
        """Clean HTML and extract readable text"""
        try:
            # Remove script and style elements
            html_content = re.sub(r'<script[^>]*>.*?</script>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
            html_content = re.sub(r'<style[^>]*>.*?</style>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
            
            # Remove HTML tags
            clean_text = re.sub(r'<[^>]+>', ' ', html_content)
            
            # Clean up whitespace
            clean_text = re.sub(r'\s+', ' ', clean_text)
            clean_text = clean_text.strip()
            
            return clean_text
            
        except Exception as e:
            return f"Error cleaning content: {str(e)}"
    
    def get_matrix_page(self):
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🔥 Matrix Web Scraper Pro</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Courier+Prime:wght@400;700&display=swap');
        
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body { 
            font-family: 'Orbitron', 'Courier Prime', monospace; 
            background: #000000;
            background-image: 
                radial-gradient(rgba(0, 255, 0, 0.1) 1px, transparent 1px),
                linear-gradient(0deg, rgba(0, 255, 0, 0.05) 50%, transparent 50%);
            background-size: 20px 20px, 100% 2px;
            color: #00ff00; 
            min-height: 100vh; 
            padding: 20px;
            position: relative;
            overflow-x: hidden;
        }
        
        body::before {
            content: '';
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background: linear-gradient(90deg, 
                transparent 0%, 
                rgba(0, 255, 0, 0.03) 50%, 
                transparent 100%);
            animation: matrix-scan 4s linear infinite;
            pointer-events: none;
            z-index: 1;
        }
        
        @keyframes matrix-scan {
            0% { transform: translateX(-100%); }
            100% { transform: translateX(100vw); }
        }
        
        @keyframes matrix-glow {
            0%, 100% { text-shadow: 0 0 5px #00ff00, 0 0 10px #00ff00; }
            50% { text-shadow: 0 0 10px #00ff00, 0 0 20px #00ff00, 0 0 30px #00ff00; }
        }
        
        @keyframes matrix-flicker {
            0%, 98% { opacity: 1; }
            99% { opacity: 0.8; }
            100% { opacity: 1; }
        }
        
        .container { max-width: 1200px; margin: 0 auto; position: relative; z-index: 2; }
        
        .header { 
            text-align: center; 
            background: rgba(0, 0, 0, 0.9);
            border: 2px solid #00ff00;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 0 30px rgba(0, 255, 0, 0.3);
        }
        
        .header h1 { 
            font-size: 3em; 
            margin-bottom: 15px; 
            animation: matrix-glow 2s ease-in-out infinite;
            text-transform: uppercase;
            letter-spacing: 3px;
        }
        
        .header p {
            font-family: 'Courier Prime', monospace;
            animation: matrix-flicker 4s infinite;
            font-size: 1.1em;
        }
        
        .panel { 
            background: rgba(0, 0, 0, 0.9); 
            border: 2px solid #00ff00;
            padding: 25px; 
            border-radius: 10px; 
            margin-bottom: 25px;
            box-shadow: 0 0 20px rgba(0, 255, 0, 0.2);
        }
        
        .panel h3 {
            color: #00ff00;
            margin-bottom: 20px;
            text-transform: uppercase;
            letter-spacing: 2px;
            font-size: 1.3em;
        }
        
        textarea { 
            width: 100%; 
            padding: 15px; 
            border: 2px solid #00ff00; 
            border-radius: 8px; 
            background: rgba(0, 0, 0, 0.8); 
            color: #00ff00;
            font-family: 'Courier Prime', monospace;
            font-size: 14px;
            resize: vertical;
        }
        
        textarea:focus {
            outline: none;
            box-shadow: 0 0 15px rgba(0, 255, 0, 0.5);
            border-color: #00ff00;
        }
        
        button { 
            padding: 12px 25px; 
            background: linear-gradient(45deg, #00ff00, #008800);
            color: #000000; 
            border: 2px solid #00ff00; 
            border-radius: 8px; 
            cursor: pointer; 
            font-weight: bold; 
            margin: 8px 5px; 
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 1px;
            font-family: 'Orbitron', monospace;
            position: relative;
            overflow: hidden;
        }
        
        button::before {
            content: '';
            position: absolute;
            top: 0; left: -100%;
            width: 100%; height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
            transition: left 0.5s ease;
        }
        
        button:hover::before { left: 100%; }
        button:hover { 
            background: #00ff00;
            transform: translateY(-2px); 
            box-shadow: 0 5px 20px rgba(0, 255, 0, 0.4);
        }
        
        button:disabled {
            background: rgba(0, 100, 0, 0.3);
            color: #004400;
            cursor: not-allowed;
            transform: none;
        }
        
        .results { 
            background: rgba(0, 0, 0, 0.9); 
            border: 2px solid #00ff00;
            padding: 25px; 
            border-radius: 10px; 
            margin-top: 25px;
            box-shadow: 0 0 20px rgba(0, 255, 0, 0.2);
            display: none;
        }
        
        .results h3 {
            color: #00ff00;
            margin-bottom: 25px;
            text-transform: uppercase;
            letter-spacing: 2px;
            text-align: center;
            font-size: 1.5em;
        }
        
        .result-item { 
            background: rgba(0, 0, 0, 0.8); 
            border: 1px solid #00ff00;
            padding: 25px; 
            margin: 20px 0; 
            border-radius: 10px;
            transition: all 0.3s ease;
            position: relative;
        }
        
        .result-item::before {
            content: '';
            position: absolute;
            top: -1px; left: -1px; right: -1px; bottom: -1px;
            background: linear-gradient(45deg, #00ff00, #008800, #00ff00);
            z-index: -1;
            border-radius: 10px;
            opacity: 0;
            transition: opacity 0.3s ease;
        }
        
        .result-item:hover::before { opacity: 0.3; }
        .result-item:hover { 
            transform: translateY(-3px);
            box-shadow: 0 10px 30px rgba(0, 255, 0, 0.3);
        }
        
        .success { border-left: 5px solid #00ff00; }
        .error { border-left: 5px solid #ff0000; }
        
        .result-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }
        
        .result-title {
            color: #00ff00;
            font-size: 1.2em;
            font-weight: bold;
            margin: 0;
        }
        
        .status-badge {
            padding: 8px 15px;
            border-radius: 20px;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 1px;
            font-size: 0.9em;
        }
        
        .status-success {
            background: rgba(0, 255, 0, 0.2);
            color: #00ff00;
            border: 1px solid #00ff00;
        }
        
        .status-error {
            background: rgba(255, 0, 0, 0.2);
            color: #ff0000;
            border: 1px solid #ff0000;
        }
        
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }
        
        .metric-card {
            background: rgba(0, 255, 0, 0.1);
            border: 1px solid #008800;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
        }
        
        .metric-value {
            font-size: 1.5em;
            font-weight: bold;
            color: #00ff00;
            display: block;
        }
        
        .metric-label {
            font-size: 0.9em;
            opacity: 0.8;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .content-display {
            background: rgba(0, 0, 0, 0.6);
            border: 1px solid #008800;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
            font-family: 'Courier Prime', monospace;
            font-size: 13px;
            line-height: 1.6;
            max-height: 300px;
            overflow-y: auto;
            white-space: pre-wrap;
            word-wrap: break-word;
        }
        
        .content-display::-webkit-scrollbar {
            width: 8px;
        }
        
        .content-display::-webkit-scrollbar-track {
            background: rgba(0, 0, 0, 0.3);
        }
        
        .content-display::-webkit-scrollbar-thumb {
            background: #00ff00;
            border-radius: 4px;
        }
        
        .actions {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 20px;
        }
        
        .action-btn {
            padding: 10px 18px;
            background: rgba(0, 0, 0, 0.8);
            color: #00ff00;
            border: 1px solid #00ff00;
            border-radius: 6px;
            cursor: pointer;
            font-size: 12px;
            font-family: 'Orbitron', monospace;
            text-transform: uppercase;
            letter-spacing: 1px;
            transition: all 0.3s ease;
        }
        
        .action-btn:hover {
            background: rgba(0, 255, 0, 0.2);
            box-shadow: 0 0 15px rgba(0, 255, 0, 0.3);
        }
        
        .summary-panel {
            background: rgba(0, 255, 0, 0.1);
            border: 2px solid #00ff00;
            padding: 25px;
            border-radius: 10px;
            margin-top: 30px;
            text-align: center;
        }
        
        .summary-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        
        .summary-stat {
            background: rgba(0, 0, 0, 0.6);
            padding: 20px;
            border-radius: 8px;
            border: 1px solid #008800;
        }
        
        .summary-number {
            font-size: 2em;
            font-weight: bold;
            color: #00ff00;
            display: block;
        }
        
        .summary-label {
            font-size: 0.9em;
            opacity: 0.8;
            text-transform: uppercase;
            margin-top: 5px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔥 Matrix Web Scraper Pro</h1>
            <p>Advanced Cyberpunk Web Scraping with Perfect Text Visibility</p>
            <p><strong>Developed by Jose L Encarnacion (JoseTusabe)</strong></p>
            <p>SoloYLibre Web Dev - New York, United States</p>
        </div>
        
        <div class="panel">
            <h3>🌐 Matrix Scraping Interface</h3>
            <textarea id="urls" rows="6" placeholder="https://example.com
https://httpbin.org/html
https://httpbin.org/json
https://httpbin.org/user-agent"></textarea>
            <br><br>
            <button onclick="startMatrixScraping()" id="scrapeBtn">🔥 Start Matrix Scraping</button>
            <button onclick="loadMatrixSamples()">📄 Load Matrix Samples</button>
            <button onclick="clearMatrix()">🗑️ Clear Matrix</button>
            
            <div id="status" style="margin-top: 20px;"></div>
        </div>
        
        <div id="results" class="results">
            <h3>🔥 Matrix Scraping Results</h3>
            <div id="results-content"></div>
        </div>
    </div>
    
    <script>
        let matrixResults = [];
        
        function loadMatrixSamples() {
            document.getElementById('urls').value = `https://example.com
https://httpbin.org/html
https://httpbin.org/json
https://httpbin.org/user-agent`;
        }
        
        function clearMatrix() {
            document.getElementById('urls').value = '';
            document.getElementById('results').style.display = 'none';
            document.getElementById('status').innerHTML = '';
            matrixResults = [];
        }
        
        function startMatrixScraping() {
            const urls = document.getElementById('urls').value.split('\\n').filter(u => u.trim());
            const btn = document.getElementById('scrapeBtn');
            
            if (urls.length === 0) {
                alert('🔥 MATRIX ERROR: Please enter URLs to hack');
                return;
            }
            
            btn.disabled = true;
            btn.textContent = '🔄 Matrix Processing...';
            
            document.getElementById('status').innerHTML = `
                <div style="background: rgba(0, 255, 0, 0.1); border: 1px solid #00ff00; padding: 15px; border-radius: 8px;">
                    🔥 MATRIX INITIATED: Hacking ${urls.length} targets...
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
                btn.textContent = '🔥 Start Matrix Scraping';
                
                if (data.status === 'success') {
                    matrixResults = data.results;
                    showMatrixResults(data);
                } else {
                    showMatrixError(data.message);
                }
            })
            .catch(error => {
                btn.disabled = false;
                btn.textContent = '🔥 Start Matrix Scraping';
                showMatrixError(error.message);
            });
        }
        
        function showMatrixResults(data) {
            const resultsDiv = document.getElementById('results');
            const contentDiv = document.getElementById('results-content');
            
            resultsDiv.style.display = 'block';
            contentDiv.innerHTML = '';
            
            console.log('Matrix Results:', data);
            
            if (!data.results || data.results.length === 0) {
                contentDiv.innerHTML = '<p style="text-align: center; color: #ff0000;">🔥 MATRIX ERROR: No data extracted</p>';
                return;
            }
            
            data.results.forEach((result, index) => {
                const div = document.createElement('div');
                div.className = 'result-item ' + (result.status_code === 200 ? 'success' : 'error');
                
                div.innerHTML = `
                    <div class="result-header">
                        <h4 class="result-title">🔥 ${result.title || 'MATRIX TARGET'}</h4>
                        <span class="status-badge ${result.status_code === 200 ? 'status-success' : 'status-error'}">
                            ${result.status_code === 200 ? '✅ HACKED' : '❌ FAILED'} ${result.status_code}
                        </span>
                    </div>
                    
                    <div style="margin-bottom: 15px;">
                        <strong>🌐 TARGET:</strong> <span style="word-break: break-all; color: #00ff00;">${result.url}</span>
                    </div>
                    
                    <div class="metrics-grid">
                        <div class="metric-card">
                            <span class="metric-value">${result.load_time}s</span>
                            <span class="metric-label">⏱️ Hack Time</span>
                        </div>
                        <div class="metric-card">
                            <span class="metric-value">${result.word_count.toLocaleString()}</span>
                            <span class="metric-label">📄 Words</span>
                        </div>
                        <div class="metric-card">
                            <span class="metric-value">${result.char_count.toLocaleString()}</span>
                            <span class="metric-label">🔤 Characters</span>
                        </div>
                        <div class="metric-card">
                            <span class="metric-value">${result.links_found}</span>
                            <span class="metric-label">🔗 Links</span>
                        </div>
                        <div class="metric-card">
                            <span class="metric-value">${result.images_found}</span>
                            <span class="metric-label">🖼️ Images</span>
                        </div>
                    </div>
                    
                    <div style="margin: 20px 0;">
                        <strong style="color: #00ff00;">🔥 EXTRACTED DATA:</strong>
                        <div class="content-display">${result.content || 'No content extracted'}</div>
                    </div>
                    
                    <div class="actions">
                        <button class="action-btn" onclick="viewMatrixFull(${index})">👁️ Full Matrix View</button>
                        <button class="action-btn" onclick="searchMatrix(${index})">🔍 Matrix Search</button>
                        <button class="action-btn" onclick="exportMatrix(${index})">📄 Export Matrix</button>
                        <button class="action-btn" onclick="analyzeMatrix(${index})">📊 Matrix Analysis</button>
                    </div>
                `;
                
                contentDiv.appendChild(div);
            });
            
            // Add summary panel
            const summaryDiv = document.createElement('div');
            summaryDiv.className = 'summary-panel';
            summaryDiv.innerHTML = `
                <h3 style="color: #00ff00; margin-bottom: 20px;">🔥 MATRIX HACK SUMMARY</h3>
                <div class="summary-grid">
                    <div class="summary-stat">
                        <span class="summary-number">${data.stats.successful}</span>
                        <span class="summary-label">✅ Successful Hacks</span>
                    </div>
                    <div class="summary-stat">
                        <span class="summary-number">${data.stats.failed}</span>
                        <span class="summary-label">❌ Failed Attempts</span>
                    </div>
                    <div class="summary-stat">
                        <span class="summary-number">${data.stats.total_words.toLocaleString()}</span>
                        <span class="summary-label">📄 Total Words</span>
                    </div>
                    <div class="summary-stat">
                        <span class="summary-number">${data.stats.total_chars.toLocaleString()}</span>
                        <span class="summary-label">🔤 Total Characters</span>
                    </div>
                    <div class="summary-stat">
                        <span class="summary-number">${Math.round((data.stats.successful / data.stats.total) * 100)}%</span>
                        <span class="summary-label">📈 Success Rate</span>
                    </div>
                </div>
                <div style="margin-top: 20px; padding: 15px; background: rgba(0, 0, 0, 0.6); border-radius: 8px; border: 1px solid #008800;">
                    <strong>💾 MATRIX DATA SAVED:</strong> ${data.exported_file}
                </div>
            `;
            contentDiv.appendChild(summaryDiv);
            
            // Update status
            document.getElementById('status').innerHTML = `
                <div style="background: rgba(0, 255, 0, 0.2); border: 2px solid #00ff00; padding: 20px; border-radius: 10px;">
                    <strong>🔥 MATRIX HACK COMPLETED!</strong><br>
                    ✅ ${data.stats.successful}/${data.stats.total} targets successfully hacked<br>
                    📄 ${data.stats.total_words.toLocaleString()} words extracted from the Matrix<br>
                    💾 Data archived in: ${data.exported_file}
                </div>
            `;
        }
        
        function viewMatrixFull(index) {
            const result = matrixResults[index];
            if (!result) {
                alert('🔥 MATRIX ERROR: Target data not found');
                return;
            }
            
            const win = window.open('', '_blank', 'width=1200,height=800');
            win.document.write(`
                <html>
                <head>
                    <title>🔥 Matrix Full View - ${result.title}</title>
                    <style>
                        body { 
                            font-family: 'Courier New', monospace; 
                            background: #000000; 
                            color: #00ff00; 
                            padding: 20px; 
                            margin: 0;
                        }
                        .header { 
                            background: rgba(0, 255, 0, 0.1); 
                            border: 2px solid #00ff00;
                            padding: 20px; 
                            border-radius: 10px; 
                            margin-bottom: 20px;
                        }
                        .content { 
                            background: rgba(0, 0, 0, 0.8);
                            border: 1px solid #008800;
                            padding: 20px;
                            border-radius: 8px;
                            white-space: pre-wrap;
                            font-size: 14px;
                            line-height: 1.6;
                            max-height: 600px;
                            overflow-y: auto;
                        }
                        h2 { color: #00ff00; text-transform: uppercase; letter-spacing: 2px; }
                    </style>
                </head>
                <body>
                    <div class="header">
                        <h2>🔥 ${result.title}</h2>
                        <p><strong>🌐 TARGET:</strong> ${result.url}</p>
                        <p><strong>📊 STATUS:</strong> ${result.status_code} | <strong>⏱️ TIME:</strong> ${result.load_time}s</p>
                        <p><strong>📄 WORDS:</strong> ${result.word_count.toLocaleString()} | <strong>🔤 CHARS:</strong> ${result.char_count.toLocaleString()}</p>
                    </div>
                    <div class="content">${result.full_content || 'No content available'}</div>
                </body>
                </html>
            `);
        }
        
        function searchMatrix(index) {
            const result = matrixResults[index];
            if (!result) {
                alert('🔥 MATRIX ERROR: Target not found');
                return;
            }
            
            const term = prompt('🔍 MATRIX SEARCH\\n\\nEnter search term:');
            if (term && term.trim()) {
                const content = result.full_content || '';
                const regex = new RegExp(term.trim(), 'gi');
                const matches = content.match(regex);
                
                if (matches && matches.length > 0) {
                    const highlighted = content.replace(regex, `<mark style="background: #00ff00; color: #000000; padding: 2px; font-weight: bold;">$&</mark>`);
                    const win = window.open('', '_blank', 'width=1200,height=800');
                    win.document.write(`
                        <html>
                        <head>
                            <title>🔍 Matrix Search Results - ${term}</title>
                            <style>
                                body { 
                                    font-family: 'Courier New', monospace; 
                                    background: #000000; 
                                    color: #00ff00; 
                                    padding: 20px; 
                                    margin: 0;
                                }
                                .header { 
                                    background: rgba(0, 255, 0, 0.1); 
                                    border: 2px solid #00ff00;
                                    padding: 20px; 
                                    border-radius: 10px; 
                                    margin-bottom: 20px;
                                }
                                .content { 
                                    background: rgba(0, 0, 0, 0.8);
                                    border: 1px solid #008800;
                                    padding: 20px;
                                    border-radius: 8px;
                                    white-space: pre-wrap;
                                    font-size: 14px;
                                    line-height: 1.6;
                                    max-height: 600px;
                                    overflow-y: auto;
                                }
                                mark { 
                                    background: #00ff00; 
                                    color: #000000; 
                                    padding: 3px 6px; 
                                    font-weight: bold;
                                    border-radius: 3px;
                                    animation: glow 1s ease-in-out infinite alternate;
                                }
                                @keyframes glow {
                                    from { box-shadow: 0 0 5px #00ff00; }
                                    to { box-shadow: 0 0 15px #00ff00; }
                                }
                                h2 { color: #00ff00; text-transform: uppercase; letter-spacing: 2px; }
                            </style>
                        </head>
                        <body>
                            <div class="header">
                                <h2>🔍 MATRIX SEARCH RESULTS</h2>
                                <p><strong>🎯 SEARCH TERM:</strong> "${term}"</p>
                                <p><strong>🔢 MATCHES FOUND:</strong> ${matches.length}</p>
                                <p><strong>🌐 TARGET:</strong> ${result.url}</p>
                            </div>
                            <div class="content">${highlighted}</div>
                        </body>
                        </html>
                    `);
                } else {
                    alert(`🔥 MATRIX SEARCH FAILED\\n\\nNo matches found for "${term}"\\n\\nTry different search terms.`);
                }
            }
        }
        
        function exportMatrix(index) {
            const result = matrixResults[index];
            if (!result) {
                alert('🔥 MATRIX ERROR: Target not found');
                return;
            }
            
            const exportData = {
                matrix_export: {
                    version: "Matrix Web Scraper Pro v1.0",
                    exported_at: new Date().toISOString(),
                    developer: "Jose L Encarnacion (JoseTusabe)",
                    company: "SoloYLibre Web Dev",
                    location: "New York, United States"
                },
                target_data: result,
                analysis: {
                    content_quality: result.word_count > 100 ? "HIGH" : result.word_count > 50 ? "MEDIUM" : "LOW",
                    extraction_success: result.status_code === 200,
                    data_richness: {
                        has_links: result.links_found > 0,
                        has_images: result.images_found > 0,
                        substantial_content: result.word_count > 200
                    }
                }
            };
            
            const data = JSON.stringify(exportData, null, 2);
            const blob = new Blob([data], {type: 'application/json'});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `matrix_${result.domain}_${new Date().toISOString().slice(0,10)}.json`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
            
            alert(`🔥 MATRIX EXPORT SUCCESSFUL!\\n\\nFile: matrix_${result.domain}_${new Date().toISOString().slice(0,10)}.json\\nSize: ${(data.length / 1024).toFixed(2)} KB\\nWords: ${result.word_count.toLocaleString()}\\nCharacters: ${result.char_count.toLocaleString()}`);
        }
        
        function analyzeMatrix(index) {
            const result = matrixResults[index];
            if (!result) {
                alert('🔥 MATRIX ERROR: Target not found');
                return;
            }
            
            const content = result.full_content || '';
            const sentences = content.split(/[.!?]+/).filter(s => s.trim().length > 0);
            const paragraphs = content.split(/\\n\\s*\\n/).filter(p => p.trim().length > 0);
            const avgWordsPerSentence = sentences.length > 0 ? (result.word_count / sentences.length).toFixed(1) : 0;
            
            // Word frequency analysis
            const words = content.toLowerCase().match(/\\b\\w+\\b/g) || [];
            const wordCount = {};
            words.forEach(word => {
                if (word.length > 3) {
                    wordCount[word] = (wordCount[word] || 0) + 1;
                }
            });
            
            const topWords = Object.entries(wordCount)
                .sort(([,a], [,b]) => b - a)
                .slice(0, 10)
                .map(([word, count]) => `${word}: ${count}`)
                .join('\\n');
            
            const analysisText = `🔥 MATRIX ANALYSIS COMPLETE

🌐 TARGET: ${result.url}
📊 STATUS: ${result.status_code}
⏱️ HACK TIME: ${result.load_time}s

📄 CONTENT METRICS:
• Words: ${result.word_count.toLocaleString()}
• Characters: ${result.char_count.toLocaleString()}
• Sentences: ${sentences.length.toLocaleString()}
• Paragraphs: ${paragraphs.length.toLocaleString()}
• Avg words/sentence: ${avgWordsPerSentence}

🔗 WEB ELEMENTS:
• Links extracted: ${result.links_found}
• Images found: ${result.images_found}
• Content type: ${result.content_type}
• Domain: ${result.domain}

📈 TOP 10 WORDS (>3 chars):
${topWords || 'No significant words found'}

🔍 QUALITY ASSESSMENT:
• Content quality: ${result.word_count > 100 ? 'HIGH' : result.word_count > 50 ? 'MEDIUM' : 'LOW'}
• Extraction success: ${result.status_code === 200 ? 'SUCCESSFUL' : 'FAILED'}
• Data richness: ${result.word_count > 200 ? 'RICH' : 'BASIC'}`;
            
            alert(analysisText);
        }
        
        function showMatrixError(message) {
            document.getElementById('status').innerHTML = `
                <div style="background: rgba(255, 0, 0, 0.2); border: 2px solid #ff0000; padding: 15px; border-radius: 8px;">
                    🔥 MATRIX ERROR: ${message}
                </div>
            `;
        }
        
        // Load samples on start
        window.onload = function() {
            loadMatrixSamples();
        };
    </script>
</body>
</html>
        """

def start_matrix_server(port=8000):
    try:
        with socketserver.TCPServer(("", port), MatrixScraperHandler) as httpd:
            print(f"🔥 Matrix Web Scraper Pro")
            print(f"📍 Running at: http://localhost:{port}")
            print(f"💻 Jose L Encarnacion (JoseTusabe)")
            print(f"🏢 SoloYLibre Web Dev - New York, United States")
            print("-" * 60)
            
            def open_browser():
                time.sleep(1)
                webbrowser.open(f'http://localhost:{port}')
            
            threading.Thread(target=open_browser, daemon=True).start()
            
            print("🔥 Opening Matrix interface...")
            print("Press Ctrl+C to exit the Matrix")
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n🔥 Matrix connection terminated")
    except Exception as e:
        print(f"🔥 Matrix error: {e}")

if __name__ == "__main__":
    start_matrix_server()
