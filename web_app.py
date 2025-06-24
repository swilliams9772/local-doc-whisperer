#!/usr/bin/env python3
"""
Simple Web Interface for Doc-Whisperer
Using built-in HTTP server for demonstration
"""

import json
import os
import html
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import threading
import webbrowser
from datetime import datetime

from main_enhanced import EnhancedDocWhisperer, ModelProvider, PromptTemplate

class DocWhispererWebHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.doc_whisperer = EnhancedDocWhisperer()
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        path = urlparse(self.path).path
        
        if path == '/':
            self.serve_main_page()
        elif path == '/api/documents':
            self.serve_documents_api()
        elif path == '/api/stats':
            self.serve_stats_api()
        else:
            self.send_error(404)
    
    def do_POST(self):
        path = urlparse(self.path).path
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8')
        
        if path == '/api/ask':
            self.handle_ask_api(post_data)
        elif path == '/api/ingest':
            self.handle_ingest_api(post_data)
        else:
            self.send_error(404)
    
    def serve_main_page(self):
        html_content = self.get_main_html()
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html_content.encode())
    
    def serve_documents_api(self):
        documents = list(self.doc_whisperer.documents.keys())
        response = {'documents': documents}
        self.send_json_response(response)
    
    def serve_stats_api(self):
        total_docs = len(self.doc_whisperer.documents)
        total_chars = sum(doc["file_size"] for doc in self.doc_whisperer.documents.values())
        
        stats = {
            'total_documents': total_docs,
            'total_characters': total_chars,
            'average_size': total_chars // total_docs if total_docs else 0
        }
        self.send_json_response(stats)
    
    def handle_ask_api(self, post_data):
        try:
            data = parse_qs(post_data)
            question = data.get('question', [''])[0]
            provider = data.get('provider', ['claude'])[0]
            
            if not question:
                self.send_json_response({'error': 'No question provided'})
                return
            
            answer = self.doc_whisperer.query_documents(
                question, 
                ModelProvider.CLAUDE if provider == 'claude' else ModelProvider.OPENAI
            )
            
            response = {
                'question': question,
                'answer': answer,
                'provider': provider,
                'timestamp': datetime.now().isoformat()
            }
            self.send_json_response(response)
            
        except Exception as e:
            self.send_json_response({'error': str(e)})
    
    def handle_ingest_api(self, post_data):
        try:
            data = parse_qs(post_data)
            file_path = data.get('file_path', [''])[0]
            provider = data.get('provider', ['claude'])[0]
            template = data.get('template', ['research'])[0]
            
            if not file_path:
                self.send_json_response({'error': 'No file path provided'})
                return
            
            success = self.doc_whisperer.ingest_document(
                file_path,
                ModelProvider.CLAUDE if provider == 'claude' else ModelProvider.OPENAI,
                PromptTemplate(template)
            )
            
            response = {
                'success': success,
                'file_path': file_path,
                'provider': provider,
                'template': template
            }
            self.send_json_response(response)
            
        except Exception as e:
            self.send_json_response({'error': str(e)})
    
    def send_json_response(self, data):
        response = json.dumps(data, indent=2)
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(response.encode())
    
    def get_main_html(self):
        return '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Doc-Whisperer | AI Document Analysis Platform</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            --secondary-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            --success-gradient: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
            --warning-gradient: linear-gradient(135deg, #fc4a1a 0%, #f7b733 100%);
            --glass-bg: rgba(255, 255, 255, 0.15);
            --glass-border: rgba(255, 255, 255, 0.2);
            --text-primary: #1a202c;
            --text-secondary: #4a5568;
            --text-light: #718096;
            --bg-light: #f7fafc;
            --shadow-lg: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
            --shadow-xl: 0 35px 60px -12px rgba(0, 0, 0, 0.35);
            --border-radius: 20px;
            --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: var(--primary-gradient);
            min-height: 100vh;
            line-height: 1.6;
            color: var(--text-primary);
            overflow-x: hidden;
        }
        
        /* Animated background particles */
        body::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: 
                radial-gradient(circle at 20% 80%, rgba(120, 119, 198, 0.3) 0%, transparent 50%),
                radial-gradient(circle at 80% 20%, rgba(255, 119, 198, 0.3) 0%, transparent 50%),
                radial-gradient(circle at 40% 40%, rgba(120, 219, 255, 0.2) 0%, transparent 50%);
            z-index: -1;
            animation: float 6s ease-in-out infinite;
        }
        
        @keyframes float {
            0%, 100% { transform: translate(0, 0) rotate(0deg); }
            33% { transform: translate(30px, -30px) rotate(120deg); }
            66% { transform: translate(-20px, 20px) rotate(240deg); }
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 2rem;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            gap: 2rem;
        }
        
        /* Modern Header */
        .header {
            background: var(--glass-bg);
            backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border);
            border-radius: var(--border-radius);
            padding: 3rem 2rem;
            text-align: center;
            box-shadow: var(--shadow-lg);
            position: relative;
            overflow: hidden;
            animation: slideDown 0.8s ease-out;
        }
        
        .header::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
            animation: shimmer 3s infinite;
        }
        
        @keyframes shimmer {
            0% { left: -100%; }
            100% { left: 100%; }
        }
        
        @keyframes slideDown {
            from { transform: translateY(-50px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
        
        .header h1 {
            font-size: clamp(2.5rem, 5vw, 4rem);
            font-weight: 800;
            margin-bottom: 1rem;
            background: linear-gradient(135deg, #fff 0%, #e2e8f0 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        .header .subtitle {
            font-size: 1.25rem;
            font-weight: 500;
            color: rgba(255, 255, 255, 0.9);
            margin-bottom: 1rem;
        }
        
        .header .version {
            display: inline-block;
            background: var(--secondary-gradient);
            color: white;
            padding: 0.5rem 1.5rem;
            border-radius: 25px;
            font-size: 0.9rem;
            font-weight: 600;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        }
        
        /* Grid Layout */
        .main-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 2rem;
            flex: 1;
        }
        
        .left-column, .right-column {
            display: flex;
            flex-direction: column;
            gap: 2rem;
        }
        
        /* Modern Glass Cards */
        .glass-card {
            background: var(--glass-bg);
            backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border);
            border-radius: var(--border-radius);
            padding: 2rem;
            box-shadow: var(--shadow-lg);
            transition: var(--transition);
            position: relative;
            overflow: hidden;
            animation: fadeInUp 0.8s ease-out;
            animation-fill-mode: both;
        }
        
        .glass-card:nth-child(1) { animation-delay: 0.1s; }
        .glass-card:nth-child(2) { animation-delay: 0.2s; }
        .glass-card:nth-child(3) { animation-delay: 0.3s; }
        .glass-card:nth-child(4) { animation-delay: 0.4s; }
        
        @keyframes fadeInUp {
            from { 
                transform: translateY(30px); 
                opacity: 0; 
            }
            to { 
                transform: translateY(0); 
                opacity: 1; 
            }
        }
        
        .glass-card:hover {
            transform: translateY(-5px);
            box-shadow: var(--shadow-xl);
            border-color: rgba(255, 255, 255, 0.3);
        }
        
        .card-header {
            display: flex;
            align-items: center;
            gap: 1rem;
            margin-bottom: 2rem;
            padding-bottom: 1rem;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .card-icon {
            font-size: 2rem;
            padding: 0.75rem;
            background: var(--secondary-gradient);
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        }
        
        .card-title {
            font-size: 1.5rem;
            font-weight: 700;
            color: white;
            margin: 0;
        }
        
        /* Statistics Grid */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 1.5rem;
            margin-bottom: 2rem;
        }
        
        .stat-card {
            background: var(--secondary-gradient);
            padding: 2rem 1.5rem;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
            transition: var(--transition);
            position: relative;
            overflow: hidden;
        }
        
        .stat-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: rgba(255, 255, 255, 0.5);
        }
        
        .stat-card:hover {
            transform: translateY(-3px) scale(1.02);
        }
        
        .stat-number {
            font-size: 2.5rem;
            font-weight: 800;
            color: white;
            margin-bottom: 0.5rem;
            display: block;
        }
        
        .stat-label {
            font-size: 0.9rem;
            font-weight: 600;
            color: rgba(255, 255, 255, 0.9);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        /* Modern Form Elements */
        .form-group {
            margin-bottom: 1.5rem;
            position: relative;
        }
        
        .form-label {
            display: block;
            font-size: 0.9rem;
            font-weight: 600;
            color: rgba(255, 255, 255, 0.9);
            margin-bottom: 0.5rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .form-input, .form-select, .form-textarea {
            width: 100%;
            padding: 1rem 1.5rem;
            background: rgba(255, 255, 255, 0.1);
            border: 2px solid rgba(255, 255, 255, 0.2);
            border-radius: 12px;
            font-size: 1rem;
            color: white;
            transition: var(--transition);
            backdrop-filter: blur(10px);
        }
        
        .form-input::placeholder, .form-textarea::placeholder {
            color: rgba(255, 255, 255, 0.6);
        }
        
        .form-input:focus, .form-select:focus, .form-textarea:focus {
            outline: none;
            border-color: rgba(255, 255, 255, 0.5);
            background: rgba(255, 255, 255, 0.15);
            box-shadow: 0 0 0 3px rgba(255, 255, 255, 0.1);
        }
        
        .form-select option {
            background: #2d3748;
            color: white;
        }
        
        /* Modern Buttons */
        .btn {
            display: inline-flex;
            align-items: center;
            gap: 0.75rem;
            padding: 1rem 2rem;
            background: var(--secondary-gradient);
            color: white;
            border: none;
            border-radius: 12px;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: var(--transition);
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
            position: relative;
            overflow: hidden;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .btn::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
            transition: var(--transition);
        }
        
        .btn:hover::before {
            left: 100%;
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
        }
        
        .btn:active {
            transform: translateY(0);
        }
        
        .btn-icon {
            font-size: 1.2rem;
        }
        
        /* Response Cards */
        .response-card {
            margin-top: 1.5rem;
            padding: 1.5rem;
            border-radius: 12px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            animation: slideUp 0.3s ease-out;
        }
        
        @keyframes slideUp {
            from { transform: translateY(20px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
        
        .response-success {
            background: rgba(17, 153, 142, 0.2);
            border-color: rgba(56, 239, 125, 0.3);
            color: #68d391;
        }
        
        .response-error {
            background: rgba(252, 74, 26, 0.2);
            border-color: rgba(247, 183, 51, 0.3);
            color: #fc8181;
        }
        
        .response-loading {
            background: rgba(102, 126, 234, 0.2);
            border-color: rgba(118, 75, 162, 0.3);
            color: #a78bfa;
            display: flex;
            align-items: center;
            gap: 1rem;
        }
        
        .response-answer {
            background: rgba(255, 255, 255, 0.1);
            border-color: rgba(255, 255, 255, 0.2);
            color: white;
        }
        
        .answer-header {
            display: flex;
            justify-content: between;
            align-items: center;
            margin-bottom: 1rem;
            padding-bottom: 1rem;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .answer-meta {
            font-size: 0.9rem;
            color: rgba(255, 255, 255, 0.7);
        }
        
        .answer-content {
            line-height: 1.7;
            white-space: pre-wrap;
        }
        
        /* Loading Animation */
        .loading-spinner {
            width: 20px;
            height: 20px;
            border: 2px solid rgba(255, 255, 255, 0.3);
            border-top: 2px solid #a78bfa;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        /* Document Library */
        .document-item {
            display: flex;
            align-items: center;
            gap: 1rem;
            padding: 1rem;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            margin-bottom: 0.75rem;
            transition: var(--transition);
        }
        
        .document-item:hover {
            background: rgba(255, 255, 255, 0.1);
            transform: translateX(5px);
        }
        
        .document-icon {
            font-size: 1.5rem;
            padding: 0.5rem;
            background: var(--secondary-gradient);
            border-radius: 8px;
        }
        
        .document-info {
            flex: 1;
        }
        
        .document-name {
            font-weight: 600;
            color: white;
            margin-bottom: 0.25rem;
        }
        
        .document-path {
            font-size: 0.8rem;
            color: rgba(255, 255, 255, 0.6);
        }
        
        /* Responsive Design */
        @media (max-width: 1024px) {
            .main-grid {
                grid-template-columns: 1fr;
                gap: 1.5rem;
            }
            
            .stats-grid {
                grid-template-columns: repeat(2, 1fr);
            }
        }
        
        @media (max-width: 768px) {
            .container {
                padding: 1rem;
                gap: 1.5rem;
            }
            
            .glass-card {
                padding: 1.5rem;
            }
            
            .header {
                padding: 2rem 1.5rem;
            }
            
            .stats-grid {
                grid-template-columns: 1fr;
                gap: 1rem;
            }
            
            .card-header {
                flex-direction: column;
                text-align: center;
                gap: 0.5rem;
            }
        }
        
        /* Accessibility */
        @media (prefers-reduced-motion: reduce) {
            *, *::before, *::after {
                animation-duration: 0.01ms !important;
                animation-iteration-count: 1 !important;
                transition-duration: 0.01ms !important;
            }
        }
        
        /* Focus styles for accessibility */
        .btn:focus, .form-input:focus, .form-select:focus, .form-textarea:focus {
            outline: 2px solid rgba(255, 255, 255, 0.5);
            outline-offset: 2px;
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Modern Header -->
        <header class="header">
            <h1>🧠 Doc-Whisperer</h1>
            <p class="subtitle">Enhanced Multi-Model AI Document Analysis</p>
            <span class="version">v2.0 • June 2025</span>
        </header>
        
        <div class="main-grid">
            <!-- Left Column -->
            <div class="left-column">
                <!-- Statistics Dashboard -->
                <div class="glass-card">
                    <div class="card-header">
                        <div class="card-icon">📊</div>
                        <h2 class="card-title">Analytics Dashboard</h2>
                    </div>
                    <div class="stats-grid">
                        <div class="stat-card">
                            <span class="stat-number" id="total-docs">-</span>
                            <span class="stat-label">Documents</span>
                        </div>
                        <div class="stat-card">
                            <span class="stat-number" id="total-chars">-</span>
                            <span class="stat-label">Characters</span>
                        </div>
                        <div class="stat-card">
                            <span class="stat-number" id="avg-size">-</span>
                            <span class="stat-label">Avg Size</span>
                        </div>
                    </div>
                </div>
                
                <!-- Document Ingestion -->
                <div class="glass-card">
                    <div class="card-header">
                        <div class="card-icon">📄</div>
                        <h2 class="card-title">Ingest Document</h2>
                    </div>
                    <form id="ingest-form">
                        <div class="form-group">
                            <label class="form-label" for="file-path">Document Path</label>
                            <input type="text" id="file-path" name="file_path" class="form-input" 
                                   placeholder="docs_in/sample_document.md">
                        </div>
                        <div class="form-group">
                            <label class="form-label" for="provider">AI Provider</label>
                            <select id="provider" name="provider" class="form-select">
                                <option value="claude">Claude (Anthropic)</option>
                                <option value="openai">OpenAI GPT</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label class="form-label" for="template">Analysis Template</label>
                            <select id="template" name="template" class="form-select">
                                <option value="research">Research</option>
                                <option value="educational">Educational</option>
                                <option value="business">Business</option>
                                <option value="creative">Creative</option>
                            </select>
                        </div>
                        <button type="submit" class="btn">
                            <span class="btn-icon">🚀</span>
                            Ingest Document
                        </button>
                    </form>
                    <div id="ingest-response"></div>
                </div>
            </div>
            
            <!-- Right Column -->
            <div class="right-column">
                <!-- Question & Answer -->
                <div class="glass-card">
                    <div class="card-header">
                        <div class="card-icon">❓</div>
                        <h2 class="card-title">Ask Questions</h2>
                    </div>
                    <form id="ask-form">
                        <div class="form-group">
                            <label class="form-label" for="question">Your Question</label>
                            <textarea id="question" name="question" rows="4" class="form-textarea" 
                                      placeholder="What are the main benefits of AI in education?"></textarea>
                        </div>
                        <div class="form-group">
                            <label class="form-label" for="ask-provider">AI Provider</label>
                            <select id="ask-provider" name="provider" class="form-select">
                                <option value="claude">Claude (Anthropic)</option>
                                <option value="openai">OpenAI GPT</option>
                            </select>
                        </div>
                        <button type="submit" class="btn">
                            <span class="btn-icon">🔍</span>
                            Ask Question
                        </button>
                    </form>
                    <div id="ask-response"></div>
                </div>
                
                <!-- Document Library -->
                <div class="glass-card">
                    <div class="card-header">
                        <div class="card-icon">📚</div>
                        <h2 class="card-title">Document Library</h2>
                    </div>
                    <div id="documents-list">
                        <div class="response-loading">
                            <div class="loading-spinner"></div>
                            <span>Loading documents...</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        // Load initial data
        loadStats();
        loadDocuments();
        
        // Form handlers
        document.getElementById('ingest-form').addEventListener('submit', handleIngest);
        document.getElementById('ask-form').addEventListener('submit', handleAsk);
        
        async function loadStats() {
            try {
                const response = await fetch('/api/stats');
                const stats = await response.json();
                
                // Animate numbers
                animateNumber('total-docs', stats.total_documents);
                animateNumber('total-chars', stats.total_characters);
                animateNumber('avg-size', stats.average_size);
            } catch (error) {
                console.error('Error loading stats:', error);
            }
        }
        
        function animateNumber(elementId, targetValue) {
            const element = document.getElementById(elementId);
            const startValue = 0;
            const duration = 1000;
            const startTime = performance.now();
            
            function update(currentTime) {
                const elapsedTime = currentTime - startTime;
                const progress = Math.min(elapsedTime / duration, 1);
                const easedProgress = 1 - Math.pow(1 - progress, 3); // Ease-out cubic
                
                const currentValue = Math.floor(startValue + (targetValue - startValue) * easedProgress);
                element.textContent = currentValue.toLocaleString();
                
                if (progress < 1) {
                    requestAnimationFrame(update);
                }
            }
            
            requestAnimationFrame(update);
        }
        
        async function loadDocuments() {
            try {
                const response = await fetch('/api/documents');
                const data = await response.json();
                
                const container = document.getElementById('documents-list');
                if (data.documents.length === 0) {
                    container.innerHTML = `
                        <div class="document-item">
                            <div class="document-icon">📭</div>
                            <div class="document-info">
                                <div class="document-name">No documents yet</div>
                                <div class="document-path">Ingest your first document to get started</div>
                            </div>
                        </div>
                    `;
                } else {
                    container.innerHTML = data.documents.map((doc, index) => `
                        <div class="document-item" style="animation-delay: ${index * 0.1}s">
                            <div class="document-icon">📄</div>
                            <div class="document-info">
                                <div class="document-name">${doc.split('/').pop()}</div>
                                <div class="document-path">${doc}</div>
                            </div>
                        </div>
                    `).join('');
                }
            } catch (error) {
                document.getElementById('documents-list').innerHTML = `
                    <div class="response-card response-error">
                        ❌ Error loading documents
                    </div>
                `;
            }
        }
        
        async function handleIngest(event) {
            event.preventDefault();
            
            const formData = new FormData(event.target);
            const params = new URLSearchParams(formData);
            
            const responseDiv = document.getElementById('ingest-response');
            responseDiv.innerHTML = `
                <div class="response-card response-loading">
                    <div class="loading-spinner"></div>
                    <span>Processing document...</span>
                </div>
            `;
            
            try {
                const response = await fetch('/api/ingest', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/x-www-form-urlencoded'},
                    body: params.toString()
                });
                
                const result = await response.json();
                
                if (result.success) {
                    responseDiv.innerHTML = `
                        <div class="response-card response-success">
                            ✅ Successfully processed: ${result.file_path}
                        </div>
                    `;
                    loadStats();
                    loadDocuments();
                } else {
                    responseDiv.innerHTML = `
                        <div class="response-card response-error">
                            ❌ Error: ${result.error || 'Failed to process document'}
                        </div>
                    `;
                }
            } catch (error) {
                responseDiv.innerHTML = `
                    <div class="response-card response-error">
                        ❌ Error: ${error.message}
                    </div>
                `;
            }
        }
        
        async function handleAsk(event) {
            event.preventDefault();
            
            const formData = new FormData(event.target);
            const params = new URLSearchParams(formData);
            
            const responseDiv = document.getElementById('ask-response');
            responseDiv.innerHTML = `
                <div class="response-card response-loading">
                    <div class="loading-spinner"></div>
                    <span>Getting answer from AI...</span>
                </div>
            `;
            
            try {
                const response = await fetch('/api/ask', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/x-www-form-urlencoded'},
                    body: params.toString()
                });
                
                const result = await response.json();
                
                if (result.error) {
                    responseDiv.innerHTML = `
                        <div class="response-card response-error">
                            ❌ Error: ${result.error}
                        </div>
                    `;
                } else {
                    responseDiv.innerHTML = `
                        <div class="response-card response-answer">
                            <div class="answer-header">
                                <div>
                                    <strong>Question:</strong> ${result.question}
                                </div>
                                <div class="answer-meta">
                                    ${result.provider.toUpperCase()} • ${new Date(result.timestamp).toLocaleTimeString()}
                                </div>
                            </div>
                            <div class="answer-content">${result.answer}</div>
                        </div>
                    `;
                }
            } catch (error) {
                responseDiv.innerHTML = `
                    <div class="response-card response-error">
                        ❌ Error: ${error.message}
                    </div>
                `;
            }
        }
    </script>
</body>
</html>
        '''

def start_server(port=8000):
    """Start the web server."""
    server = HTTPServer(('localhost', port), DocWhispererWebHandler)
    print(f"🌐 Doc-Whisperer Web Interface running at http://localhost:{port}")
    print("Press Ctrl+C to stop the server")
    
    # Open browser automatically
    threading.Timer(1.0, lambda: webbrowser.open(f'http://localhost:{port}')).start()
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Server stopped")
        server.shutdown()

if __name__ == "__main__":
    start_server() 