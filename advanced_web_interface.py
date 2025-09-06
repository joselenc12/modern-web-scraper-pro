#!/usr/bin/env python3
"""
🚀 Advanced Web Interface - Complete Content Viewer & Search
Enhanced web interface with full content visualization and search capabilities

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
from advanced_scraper_with_exports import AdvancedWebScraperPro

class AdvancedScraperHandler(http.server.SimpleHTTPRequestHandler):
    """Advanced handler with content viewing and search capabilities"""
    
    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        query_params = urllib.parse.parse_qs(parsed_path.query)
        
        if path == '/' or path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html_content = self.get_main_page()
            self.wfile.write(html_content.encode('utf-8'))
            
        elif path == '/demo':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            demo_content = self.get_demo_page()
            self.wfile.write(demo_content.encode('utf-8'))
            
        elif path == '/viewer':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            viewer_content = self.get_content_viewer_page()
            self.wfile.write(viewer_content.encode('utf-8'))
            
        elif path == '/search':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            search_content = self.get_search_page()
            self.wfile.write(search_content.encode('utf-8'))
            
        elif path.startswith('/api/'):
            self.handle_api_request(path, query_params)
            
        else:
            super().do_GET()
    
    def do_POST(self):
        """Handle POST requests"""
        if self.path.startswith('/api/scrape'):
            self.handle_scrape_api()
        elif self.path.startswith('/api/search'):
            self.handle_search_api()
        elif self.path.startswith('/api/export'):
            self.handle_export_api()
        else:
            self.send_response(404)
            self.end_headers()
    
    def get_main_page(self):
        """Generate enhanced main page"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🚀 Advanced Web Scraper Pro - Complete System</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; min-height: 100vh; padding: 20px;
        }
        .container { max-width: 1200px; margin: 0 auto; }
        .header { text-align: center; margin-bottom: 40px; }
        .header h1 { font-size: 3em; margin-bottom: 10px; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); }
        .header p { font-size: 1.2em; opacity: 0.9; }
        
        .features { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 30px; margin: 40px 0; }
        .feature { 
            background: rgba(255,255,255,0.1); padding: 30px; border-radius: 15px; 
            backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.2);
            transition: transform 0.3s ease; text-align: center;
        }}
        .feature:hover { transform: translateY(-5px); }
        .feature h3 { font-size: 1.5em; margin-bottom: 15px; color: #00d4ff; }
        .feature p { margin-bottom: 20px; opacity: 0.9; }
        
        .btn { 
            display: inline-block; padding: 15px 30px; background: #00d4ff; 
            color: white; text-decoration: none; border-radius: 8px; 
            font-weight: bold; margin: 10px; transition: all 0.3s ease;
        }
        .btn:hover { background: #00a8cc; transform: translateY(-2px); }
        .btn.secondary { background: rgba(255,255,255,0.2); }
        .btn.secondary:hover { background: rgba(255,255,255,0.3); }
        
        .tech-stack { display: flex; justify-content: center; flex-wrap: wrap; gap: 15px; margin: 30px 0; }
        .tech { 
            background: rgba(255,255,255,0.2); padding: 10px 20px; 
            border-radius: 25px; font-weight: bold;
        }
        .footer { text-align: center; margin-top: 60px; opacity: 0.8; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Advanced Web Scraper Pro</h1>
            <p>Complete Web Scraping System with Content Viewer & Search</p>
            <p><strong>Developed by Jose L Encarnacion (JoseTusabe)</strong></p>
        </div>
        
        <div class="tech-stack">
            <div class="tech">🔍 Content Viewer</div>
            <div class="tech">🔎 Advanced Search</div>
            <div class="tech">📊 6 Export Formats</div>
            <div class="tech">🤖 AI Training Ready</div>
            <div class="tech">📱 Real-time Interface</div>
        </div>
        
        <div class="features">
            <div class="feature">
                <h3>🧪 Interactive Demo</h3>
                <p>Test the scraper with real URLs and see results instantly</p>
                <a href="/demo" class="btn">🚀 Launch Demo</a>
            </div>
            
            <div class="feature">
                <h3>🔍 Content Viewer</h3>
                <p>View and analyze scraped content with advanced visualization</p>
                <a href="/viewer" class="btn">👁️ View Content</a>
            </div>
            
            <div class="feature">
                <h3>🔎 Advanced Search</h3>
                <p>Search through scraped content with powerful filters</p>
                <a href="/search" class="btn">🔍 Search Content</a>
            </div>
            
            <div class="feature">
                <h3>📊 Export Options</h3>
                <p>Export in 6 formats: JSON, CSV, XML, HTML, JSONL, TXT</p>
                <a href="/demo" class="btn secondary">📄 Export Data</a>
            </div>
        </div>
        
        <div class="footer">
            <p>🏢 SoloYLibre Web Dev • 📍 New York, United States • 📧 admin@soloylibre.com</p>
            <p>🌐 GitHub: @joselenc12 • 🔗 Website: SoloYLibre.com</p>
            <p>© 2024 Jose L Encarnacion (JoseTusabe) - Made with ❤️</p>
        </div>
    </div>
</body>
</html>
        """
    
    def get_demo_page(self):
        """Generate enhanced demo page with content viewing"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🧪 Advanced Scraper Demo - Complete System</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; min-height: 100vh; padding: 20px;
        }
        .container { max-width: 1400px; margin: 0 auto; }
        .header { text-align: center; margin-bottom: 30px; }
        .demo-panel { 
            background: rgba(255,255,255,0.1); padding: 30px; border-radius: 15px; 
            backdrop-filter: blur(10px); margin-bottom: 30px;
        }
        .input-group { margin: 20px 0; }
        .input-group label { display: block; margin-bottom: 8px; font-weight: bold; }
        .input-group input, .input-group textarea, .input-group select { 
            width: 100%; padding: 12px; border: none; border-radius: 8px; 
            background: rgba(255,255,255,0.9); color: #333; font-size: 14px;
        }
        .btn { 
            padding: 12px 25px; background: #00d4ff; color: white; 
            border: none; border-radius: 8px; cursor: pointer; 
            font-weight: bold; margin: 10px 5px; transition: all 0.3s ease;
        }
        .btn:hover { background: #00a8cc; transform: translateY(-2px); }
        .btn.secondary { background: rgba(255,255,255,0.2); }
        .btn.secondary:hover { background: rgba(255,255,255,0.3); }
        
        .results { 
            background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; 
            margin-top: 20px; max-height: 600px; overflow-y: auto;
        }
        .result-item { 
            background: rgba(255,255,255,0.1); padding: 20px; margin: 15px 0; 
            border-radius: 10px; border-left: 4px solid #00d4ff;
        }
        .result-item.success { border-left-color: #28a745; }
        .result-item.error { border-left-color: #dc3545; }
        
        .status { padding: 4px 8px; border-radius: 4px; font-size: 0.8em; font-weight: bold; }
        .status.success { background: #28a745; }
        .status.error { background: #dc3545; }
        
        .content-preview { 
            background: rgba(255,255,255,0.1); padding: 15px; 
            border-radius: 8px; margin-top: 10px; max-height: 200px; overflow-y: auto;
        }
        .content-actions { margin-top: 10px; }
        .content-actions button { 
            padding: 5px 10px; margin: 2px; border: none; border-radius: 5px; 
            background: #00d4ff; color: white; cursor: pointer; font-size: 12px;
        }
        .content-actions button:hover { background: #00a8cc; }
        
        .back-btn { 
            position: fixed; top: 20px; left: 20px; 
            background: rgba(255,255,255,0.2); padding: 10px 15px; 
            border-radius: 8px; text-decoration: none; color: white;
        }
        .export-panel {
            background: rgba(0, 212, 255, 0.1); padding: 20px; border-radius: 10px;
            margin-top: 20px; border: 1px solid rgba(0, 212, 255, 0.3);
        }
    </style>
</head>
<body>
    <a href="/" class="back-btn">← Back to Home</a>
    
    <div class="container">
        <div class="header">
            <h1>🧪 Advanced Web Scraper Demo</h1>
            <p>Complete scraping with content viewing and export options</p>
        </div>
        
        <div class="demo-panel">
            <h3>🌐 URLs to Scrape</h3>
            
            <div class="input-group">
                <label>Enter URLs (one per line):</label>
                <textarea id="urls" rows="5" placeholder="https://example.com
https://httpbin.org/html
https://httpbin.org/json"></textarea>
            </div>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px;">
                <div class="input-group">
                    <label>Max Concurrent:</label>
                    <input type="number" id="concurrent" value="3" min="1" max="10">
                </div>
                <div class="input-group">
                    <label>Export Format:</label>
                    <select id="exportFormat">
                        <option value="all">All Formats</option>
                        <option value="json">JSON Only</option>
                        <option value="csv">CSV Only</option>
                        <option value="html">HTML Report Only</option>
                        <option value="jsonl">AI Training (JSONL)</option>
                        <option value="xml">XML Only</option>
                        <option value="txt">Text Summary Only</option>
                    </select>
                </div>
                <div class="input-group">
                    <label>Content Analysis:</label>
                    <select id="analysisLevel">
                        <option value="full">Full Analysis</option>
                        <option value="basic">Basic Only</option>
                        <option value="metadata">Metadata Only</option>
                    </select>
                </div>
            </div>
            
            <button class="btn" onclick="startAdvancedScraping()">🚀 Start Advanced Scraping</button>
            <button class="btn secondary" onclick="loadPresets()">🎯 Load Test URLs</button>
            <button class="btn secondary" onclick="clearResults()">🗑️ Clear Results</button>
            
            <div id="status" style="margin-top: 20px;"></div>
        </div>
        
        <div id="results" class="results" style="display: none;">
            <h3>📊 Scraping Results with Content Viewer</h3>
            <div id="results-content"></div>
        </div>
        
        <div id="export-panel" class="export-panel" style="display: none;">
            <h3>📄 Export Options</h3>
            <div id="export-content"></div>
        </div>
    </div>
    
    <script>
        let scrapingResults = [];
        
        function loadPresets() {
            document.getElementById('urls').value = `https://httpbin.org/html
https://httpbin.org/json
https://example.com
https://httpbin.org/user-agent
https://httpbin.org/headers`;
        }
        
        function clearResults() {
            document.getElementById('results').style.display = 'none';
            document.getElementById('export-panel').style.display = 'none';
            document.getElementById('results-content').innerHTML = '';
            document.getElementById('status').innerHTML = '';
            scrapingResults = [];
        }
        
        function startAdvancedScraping() {
            const urls = document.getElementById('urls').value.split('\\n').filter(url => url.trim());
            const concurrent = document.getElementById('concurrent').value;
            const exportFormat = document.getElementById('exportFormat').value;
            const analysisLevel = document.getElementById('analysisLevel').value;
            
            if (urls.length === 0) {
                alert('Please enter at least one URL');
                return;
            }
            
            document.getElementById('status').innerHTML = `
                <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 8px;">
                    🚀 Starting advanced scrape of ${urls.length} URLs...
                    <br>📊 Export Format: ${exportFormat} | Analysis: ${analysisLevel}
                </div>
            `;
            
            // Call real scraping API
            realAdvancedScraping(urls, concurrent, exportFormat, analysisLevel);
        }
        
        function realAdvancedScraping(urls, concurrent, exportFormat, analysisLevel) {
            const resultsDiv = document.getElementById('results');
            const contentDiv = document.getElementById('results-content');
            
            resultsDiv.style.display = 'block';
            contentDiv.innerHTML = '';
            
            fetch('/api/scrape', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    urls: urls,
                    concurrent: parseInt(concurrent),
                    export_format: exportFormat,
                    analysis_level: analysisLevel
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.results) {
                    scrapingResults = data.results;
                    displayAdvancedResults(data);
                    showExportOptions(data.exported_files, data.export_info);
                } else {
                    showError(data.message || 'Unknown error');
                }
            })
            .catch(error => showError(error.message));
        }
        
        function displayAdvancedResults(data) {
            const contentDiv = document.getElementById('results-content');
            
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
                        <strong>📝 Title:</strong> ${result.title || 'No title'}
                    </div>
                    
                    <div style="margin-bottom: 10px;">
                        <strong>🌍 Language:</strong> ${result.language || 'Unknown'} | 
                        <strong>📄 Type:</strong> ${result.content_type || 'Unknown'} | 
                        <strong>💾 Size:</strong> ${(result.response_size || 0).toLocaleString()} bytes
                    </div>
                    
                    <div style="display: flex; gap: 15px; margin-bottom: 15px; flex-wrap: wrap;">
                        <span style="background: rgba(255,255,255,0.2); padding: 5px 10px; border-radius: 15px; font-size: 0.9em;">
                            ⏱️ ${result.load_time}s
                        </span>
                        <span style="background: rgba(255,255,255,0.2); padding: 5px 10px; border-radius: 15px; font-size: 0.9em;">
                            📄 ${(result.word_count || 0).toLocaleString()} words
                        </span>
                        <span style="background: rgba(255,255,255,0.2); padding: 5px 10px; border-radius: 15px; font-size: 0.9em;">
                            🔗 ${result.links_found || 0} links
                        </span>
                        <span style="background: rgba(255,255,255,0.2); padding: 5px 10px; border-radius: 15px; font-size: 0.9em;">
                            🖼️ ${result.images_found || 0} images
                        </span>
                        ${result.has_structured_data ? '<span style="background: rgba(0,212,255,0.3); padding: 5px 10px; border-radius: 15px; font-size: 0.9em;">🔍 Structured Data</span>' : ''}
                    </div>
                    
                    ${result.meta_description ? `
                    <div style="margin-bottom: 10px;">
                        <strong>📋 Description:</strong> ${result.meta_description}
                    </div>
                    ` : ''}
                    
                    <div class="content-preview" id="preview-${index}">
                        <strong>📄 Content Preview:</strong>
                        <div style="margin-top: 10px; font-style: italic; opacity: 0.9; max-height: 100px; overflow: hidden;">
                            ${(result.content || 'No content').substring(0, 300)}...
                        </div>
                        <div class="content-actions">
                            <button onclick="viewFullContent(${index})">👁️ View Full Content</button>
                            <button onclick="searchInContent(${index})">🔍 Search in Content</button>
                            <button onclick="analyzeContent(${index})">📊 Analyze Content</button>
                            <button onclick="exportSingle(${index})">📄 Export This</button>
                        </div>
                    </div>
                `;
                
                contentDiv.appendChild(resultItem);
            });
            
            // Update status
            const successful = data.results.filter(r => r.status_code === 200).length;
            document.getElementById('status').innerHTML = `
                <div style="background: rgba(40, 167, 69, 0.3); padding: 15px; border-radius: 8px;">
                    🎉 Advanced scraping completed! ${successful}/${data.results.length} successful (${(successful/data.results.length*100).toFixed(1)}% success rate)
                    <br><strong>📊 Total:</strong> ${data.stats.total_words || 0} words, ${data.stats.total_links || 0} links, ${data.stats.total_images || 0} images
                    <br><strong>⏱️ Avg Load Time:</strong> ${data.stats.avg_load_time || 0}s
                </div>
            `;
        }
        
        function showExportOptions(exportedFiles, exportInfo) {
            const exportPanel = document.getElementById('export-panel');
            const exportContent = document.getElementById('export-content');
            
            exportPanel.style.display = 'block';
            
            let exportHtml = '<div style="margin-bottom: 15px;"><strong>📊 Generated Export Files:</strong></div>';
            
            if (exportedFiles && exportedFiles.length > 0) {
                exportedFiles.forEach(file => {
                    const fileName = file.split('/').pop();
                    const fileType = fileName.split('.').pop().toUpperCase();
                    exportHtml += `
                        <div style="margin: 10px 0; padding: 10px; background: rgba(255,255,255,0.1); border-radius: 5px;">
                            <strong>📄 ${fileName}</strong>
                            <span style="float: right;">
                                <button onclick="downloadFile('${file}')" style="padding: 5px 10px; background: #00d4ff; border: none; border-radius: 3px; color: white; cursor: pointer;">
                                    💾 Download ${fileType}
                                </button>
                            </span>
                        </div>
                    `;
                });
            }
            
            exportHtml += `
                <div style="margin-top: 20px; padding: 15px; background: rgba(0,212,255,0.1); border-radius: 8px;">
                    <strong>🤖 AI Training Ready:</strong> JSONL format available for machine learning<br>
                    <strong>📊 Available Formats:</strong> ${exportInfo ? exportInfo.formats.join(', ') : 'Multiple formats'}<br>
                    <strong>📁 Location:</strong> exports/ directory
                </div>
            `;
            
            exportContent.innerHTML = exportHtml;
        }
        
        function viewFullContent(index) {
            const result = scrapingResults[index];
            const newWindow = window.open('', '_blank', 'width=800,height=600');
            newWindow.document.write(`
                <html>
                <head>
                    <title>Full Content - ${result.title}</title>
                    <style>
                        body { font-family: Arial, sans-serif; padding: 20px; line-height: 1.6; }
                        .header { background: #f4f4f4; padding: 15px; border-radius: 5px; margin-bottom: 20px; }
                        .content { white-space: pre-wrap; }
                    </style>
                </head>
                <body>
                    <div class="header">
                        <h2>${result.title}</h2>
                        <p><strong>URL:</strong> ${result.url}</p>
                        <p><strong>Words:</strong> ${result.word_count} | <strong>Language:</strong> ${result.language}</p>
                    </div>
                    <div class="content">${result.content || 'No content available'}</div>
                </body>
                </html>
            `);
        }
        
        function searchInContent(index) {
            const result = scrapingResults[index];
            const searchTerm = prompt('Enter search term:');
            if (searchTerm) {
                const content = result.content || '';
                const regex = new RegExp(searchTerm, 'gi');
                const matches = content.match(regex);
                const matchCount = matches ? matches.length : 0;
                
                if (matchCount > 0) {
                    const highlightedContent = content.replace(regex, `<mark style="background: yellow;">$&</mark>`);
                    const newWindow = window.open('', '_blank', 'width=800,height=600');
                    newWindow.document.write(`
                        <html>
                        <head>
                            <title>Search Results - ${searchTerm}</title>
                            <style>
                                body { font-family: Arial, sans-serif; padding: 20px; line-height: 1.6; }
                                .header { background: #f4f4f4; padding: 15px; border-radius: 5px; margin-bottom: 20px; }
                                .content { white-space: pre-wrap; }
                                mark { background: yellow; padding: 2px; }
                            </style>
                        </head>
                        <body>
                            <div class="header">
                                <h2>Search Results for "${searchTerm}"</h2>
                                <p><strong>Found:</strong> ${matchCount} matches in ${result.title}</p>
                                <p><strong>URL:</strong> ${result.url}</p>
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
        
        function analyzeContent(index) {
            const result = scrapingResults[index];
            const content = result.content || '';
            
            // Basic content analysis
            const sentences = content.split(/[.!?]+/).filter(s => s.trim().length > 0);
            const paragraphs = content.split(/\n\s*\n/).filter(p => p.trim().length > 0);
            const avgWordsPerSentence = sentences.length > 0 ? (result.word_count / sentences.length).toFixed(1) : 0;
            
            alert(`📊 Content Analysis for ${result.title}:
            
📄 Words: ${result.word_count}
📝 Sentences: ${sentences.length}
📋 Paragraphs: ${paragraphs.length}
📊 Avg words per sentence: ${avgWordsPerSentence}
🔗 Links: ${result.links_found}
🖼️ Images: ${result.images_found}
🌍 Language: ${result.language}
💾 Size: ${result.response_size} bytes`);
        }
        
        function exportSingle(index) {
            const result = scrapingResults[index];
            // Create a simple export for single result
            const exportData = {
                url: result.url,
                title: result.title,
                content: result.content,
                metadata: {
                    word_count: result.word_count,
                    links_found: result.links_found,
                    images_found: result.images_found,
                    language: result.language,
                    content_type: result.content_type,
                    response_size: result.response_size,
                    load_time: result.load_time
                }
            };
            
            const dataStr = JSON.stringify(exportData, null, 2);
            const dataBlob = new Blob([dataStr], {type: 'application/json'});
            const url = URL.createObjectURL(dataBlob);
            const link = document.createElement('a');
            link.href = url;
            link.download = `single_result_${index + 1}.json`;
            link.click();
        }
        
        function downloadFile(filePath) {
            // In a real implementation, this would download the file
            alert(`Download functionality for ${filePath} would be implemented here.`);
        }
        
        function showError(message) {
            document.getElementById('status').innerHTML = `
                <div style="background: rgba(220, 53, 69, 0.3); padding: 15px; border-radius: 8px;">
                    ❌ Error: ${message}
                </div>
            `;
        }
        
        // Load presets on page load
        window.onload = function() {
            loadPresets();
        };
    </script>
</body>
</html>
        """

    def get_search_page(self):
        """Generate search page placeholder"""
        return "<html><body><h1>Search functionality coming soon!</h1></body></html>"

    def handle_scrape_api(self):
        """Handle advanced scrape API requests"""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            request_data = json.loads(post_data.decode('utf-8'))

            urls = request_data.get('urls', [])
            concurrent = request_data.get('concurrent', 3)
            export_format = request_data.get('export_format', 'all')
            analysis_level = request_data.get('analysis_level', 'full')

            # Perform real scraping
            scraper = AdvancedWebScraperPro()
            results = scraper.scrape_multiple(urls)

            # Export based on format selection
            if export_format == 'all':
                exported_files = scraper.export_all_formats("web_scraping_session")
            else:
                exported_files = []
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                base_name = f"web_scraping_session_{timestamp}"

                if export_format == 'json':
                    exported_files.append(scraper.export_json(f"exports/{base_name}"))
                elif export_format == 'csv':
                    exported_files.append(scraper.export_csv(f"exports/{base_name}"))
                elif export_format == 'html':
                    exported_files.append(scraper.export_html_report(f"exports/{base_name}"))
                elif export_format == 'jsonl':
                    exported_files.append(scraper.export_ai_training_format(f"exports/{base_name}"))
                elif export_format == 'xml':
                    exported_files.append(scraper.export_xml(f"exports/{base_name}"))
                elif export_format == 'txt':
                    exported_files.append(scraper.export_text_summary(f"exports/{base_name}"))

            # Convert results to dict format
            results_data = []
            for result in results:
                result_dict = {
                    "url": result.url,
                    "title": result.title,
                    "content": result.clean_text,
                    "status_code": result.status_code,
                    "load_time": round(result.load_time, 2),
                    "word_count": result.word_count,
                    "links_found": result.links_found,
                    "images_found": result.images_found,
                    "domain": result.domain,
                    "meta_description": result.meta_description,
                    "meta_keywords": result.meta_keywords,
                    "language": result.language,
                    "content_type": result.content_type,
                    "response_size": result.response_size,
                    "encoding": result.encoding,
                    "has_structured_data": bool(result.structured_data)
                }
                results_data.append(result_dict)

            successful_results = [r for r in results if r.status_code == 200]
            total_words = sum(r.word_count for r in successful_results)
            total_links = sum(r.links_found for r in successful_results)
            total_images = sum(r.images_found for r in successful_results)

            response = {
                "status": "success",
                "message": f"Advanced scraping completed for {len(urls)} URLs",
                "results": results_data,
                "stats": {
                    "total_urls": len(urls),
                    "successful": len(successful_results),
                    "failed": len([r for r in results if r.status_code != 200]),
                    "total_words": total_words,
                    "total_links": total_links,
                    "total_images": total_images,
                    "avg_load_time": round(sum(r.load_time for r in successful_results) / len(successful_results), 2) if successful_results else 0
                },
                "exported_files": exported_files,
                "export_info": {
                    "formats": ["JSON", "CSV", "XML", "HTML Report", "AI Training (JSONL)", "Text Summary"],
                    "location": "exports/ directory",
                    "ai_training_ready": True,
                    "html_report_available": True,
                    "selected_format": export_format,
                    "analysis_level": analysis_level
                }
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

    def handle_single_scrape_api(self):
        """Handle single URL scraping for content viewer"""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            request_data = json.loads(post_data.decode('utf-8'))

            url = request_data.get('url', '')

            if not url:
                raise ValueError("URL is required")

            # Perform scraping
            scraper = AdvancedWebScraperPro()
            result = scraper.scrape_page(url)

            # Convert result to dict
            result_dict = {
                "url": result.url,
                "title": result.title,
                "content": result.clean_text,
                "status_code": result.status_code,
                "load_time": round(result.load_time, 2),
                "word_count": result.word_count,
                "links_found": result.links_found,
                "images_found": result.images_found,
                "domain": result.domain,
                "meta_description": result.meta_description,
                "meta_keywords": result.meta_keywords,
                "language": result.language,
                "content_type": result.content_type,
                "response_size": result.response_size,
                "encoding": result.encoding,
                "has_structured_data": bool(result.structured_data),
                "structured_data": result.structured_data,
                "links_list": result.links_list[:10],  # First 10 links
                "images_list": result.images_list[:10]  # First 10 images
            }

            response = {
                "status": "success",
                "message": f"Successfully scraped {url}",
                "result": result_dict
            }

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))

        except Exception as e:
            error_response = {
                "status": "error",
                "message": f"Failed to scrape URL: {str(e)}",
                "result": None
            }

            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(error_response).encode('utf-8'))

def start_advanced_server(port=8000):
    """Start the advanced demo server"""
    try:
        with socketserver.TCPServer(("", port), AdvancedScraperHandler) as httpd:
            print(f"🚀 Advanced Web Scraper Pro - Complete Interface")
            print(f"📍 Server running at: http://localhost:{port}")
            print(f"💻 Developed by Jose L Encarnacion (JoseTusabe)")
            print(f"🏢 SoloYLibre Web Dev - New York, United States")
            print("-" * 60)
            print(f"🌐 Features Available:")
            print(f"   🏠 Main Interface: http://localhost:{port}")
            print(f"   📊 Interactive Demo: http://localhost:{port}/demo")
            print(f"   🔍 Content Viewer: http://localhost:{port}/viewer")
            print(f"   🔎 Advanced Search: http://localhost:{port}/search")
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
    start_advanced_server()
