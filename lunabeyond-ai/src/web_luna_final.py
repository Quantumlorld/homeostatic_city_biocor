#!/usr/bin/env python3
"""
🌙 LunaBeyond AI Web Server - FINAL WORKING VERSION
Fixed all button and JavaScript issues
"""

import json
import time
import asyncio
import threading
import logging
from datetime import datetime
from urllib.parse import urlparse, parse_qs
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Dict, Any

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class LunaWebServer(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        clean_path = parsed_path.path
        
        if clean_path == '/' or clean_path == '':
            self.serve_dashboard()
        elif clean_path == '/api/status':
            self.serve_api_response(self.get_status())
        elif clean_path == '/api/zones':
            self.serve_api_response(self.get_zones())
        else:
            self.send_error(404, "Not Found")
    
    def do_POST(self):
        parsed_path = urlparse(self.path)
        clean_path = parsed_path.path
        
        if clean_path == '/api/chat':
            self.handle_chat_request()
        else:
            self.send_error(404, "Not Found")
    
    def serve_api_response(self, data):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        response = json.dumps(data, indent=2)
        self.wfile.write(response.encode('utf-8'))
    
    def get_status(self):
        return {
            "status": "active",
            "timestamp": datetime.now().isoformat(),
            "ai_generation": 2,
            "system_health": 0.924,
            "zones_active": 5
        }
    
    def get_zones(self):
        zones = [
            {"id": 0, "name": "Downtown", "activity": 0.42, "state": "CALM"},
            {"id": 1, "name": "Industrial", "activity": 0.54, "state": "OVERSTIMULATED"},
            {"id": 2, "name": "Residential", "activity": 0.41, "state": "CALM"},
            {"id": 3, "name": "Commercial", "activity": 0.48, "state": "OVERSTIMULATED"},
            {"id": 4, "name": "Tech Park", "activity": 0.45, "state": "CALM"}
        ]
        
        return {
            "zones": zones,
            "timestamp": datetime.now().isoformat(),
            "system_health": 0.924
        }
    
    def handle_chat_request(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            
            if not post_data:
                self.serve_api_response({"error": "No message received"})
                return
            
            try:
                data = json.loads(post_data.decode('utf-8'))
                message = data.get('message', '').strip()
                
                if not message:
                    self.serve_api_response({"error": "Empty message"})
                    return
                
                response = self.generate_luna_response(message)
                
                self.serve_api_response({
                    "response": response,
                    "timestamp": datetime.now().isoformat(),
                    "message_received": message
                })
                
            except json.JSONDecodeError:
                self.serve_api_response({"error": "Invalid JSON"})
                
        except Exception as e:
            logger.error(f"Chat error: {e}")
            self.serve_api_response({"error": f"Chat processing error: {e}"})
    
    def generate_luna_response(self, message):
        message_lower = message.lower()
        
        if message_lower == '/status':
            return "📊 System Health: 92.4%, Average Activity: 0.46, Recovery Confidence: 87%"
        
        if message_lower == '/zones':
            return "🌆 Zones: Downtown(CALM), Industrial(OVERSTIMULATED), Residential(CALM), Commercial(OVERSTIMULATED), Tech Park(CALM)"
        
        if message_lower == '/evolve':
            return "🧬 AI evolved to Generation 3! Enhanced pattern recognition and prediction accuracy."
        
        if message_lower == '/help':
            return "💡 Commands: /status, /zones, /evolve. Ask me anything about the system!"
        
        if 'health' in message_lower:
            return "📊 System health is 92.4% - excellent! All zones maintaining homeostatic balance."
        
        if 'zone' in message_lower:
            return "🌆 Monitoring 5 zones: 3 in CALM state, 2 requiring attention. Need interventions?"
        
        if 'hello' in message_lower or 'hi' in message_lower:
            return "🌙 Hello! I'm LunaBeyond, monitoring BHCS system. How can I help you today?"
        
        return f"🌙 I received your message: '{message}'. System is running well with 92.4% health."
    
    def serve_dashboard(self):
        html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🦀🌙 BHCS + Luna AI - WORKING</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #0f1419 0%, #1a1f2e 50%, #2d3748 100%);
            color: #e2e8f0;
            min-height: 100vh;
            line-height: 1.6;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
        }
        .header h1 {
            font-size: 2.5rem;
            background: linear-gradient(45deg, #4CAF50, #9C27B0, #2196F3);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 10px;
        }
        .main-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }
        .panel {
            background: rgba(255,255,255,0.05);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 20px;
            border: 1px solid rgba(255,255,255,0.1);
        }
        .zones-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
        }
        .zone-card {
            background: rgba(255,255,255,0.05);
            border-radius: 10px;
            padding: 15px;
            border: 1px solid rgba(255,255,255,0.1);
        }
        .chat-container {
            display: flex;
            flex-direction: column;
            height: 500px;
        }
        .chat-messages {
            flex: 1;
            background: rgba(0,0,0,0.3);
            border-radius: 10px;
            padding: 15px;
            overflow-y: auto;
            margin-bottom: 15px;
            min-height: 300px;
        }
        .message {
            margin-bottom: 15px;
            padding: 10px;
            border-radius: 8px;
        }
        .message.user {
            background: rgba(33, 150, 243, 0.2);
            margin-left: auto;
            text-align: right;
            max-width: 80%;
        }
        .message.luna {
            background: rgba(156, 39, 176, 0.2);
            max-width: 80%;
        }
        .chat-input-container {
            display: flex;
            gap: 10px;
        }
        .chat-input {
            flex: 1;
            padding: 12px;
            background: rgba(0,0,0,0.5);
            border: 1px solid rgba(255,255,255,0.2);
            border-radius: 8px;
            color: white;
            font-size: 14px;
        }
        .send-button {
            padding: 12px 20px;
            background: linear-gradient(45deg, #4CAF50, #9C27B0);
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-weight: bold;
        }
        .send-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(76, 175, 80, 0.3);
        }
        .quick-commands {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 8px;
            margin-top: 10px;
        }
        .command-btn {
            padding: 8px 12px;
            background: rgba(33, 150, 243, 0.2);
            color: white;
            border: 1px solid rgba(33, 150, 243, 0.3);
            border-radius: 6px;
            cursor: pointer;
            font-size: 12px;
        }
        .command-btn:hover {
            background: rgba(33, 150, 243, 0.3);
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🦀🌙 BHCS + Luna AI</h1>
            <p>Homeostatic City BioCore with Conversational AI</p>
        </div>

        <div class="main-grid">
            <div class="panel">
                <h3>🌆 Zone Status</h3>
                <div class="zones-grid" id="zonesGrid">
                    <div class="zone-card">
                        <strong>Downtown</strong><br>
                        State: CALM<br>
                        Activity: 0.42
                    </div>
                    <div class="zone-card">
                        <strong>Industrial</strong><br>
                        State: OVERSTIMULATED<br>
                        Activity: 0.54
                    </div>
                    <div class="zone-card">
                        <strong>Residential</strong><br>
                        State: CALM<br>
                        Activity: 0.41
                    </div>
                    <div class="zone-card">
                        <strong>Commercial</strong><br>
                        State: OVERSTIMULATED<br>
                        Activity: 0.48
                    </div>
                    <div class="zone-card">
                        <strong>Tech Park</strong><br>
                        State: CALM<br>
                        Activity: 0.45
                    </div>
                </div>
            </div>

            <div class="panel">
                <h3>🌙 Luna AI Chat</h3>
                <div class="chat-container">
                    <div class="chat-messages" id="chatMessages">
                        <div class="message luna">
                            🌙 Hello! I'm LunaBeyond, your AI companion. Ask me anything about the BHCS system!
                        </div>
                    </div>
                    <div class="chat-input-container">
                        <input type="text" class="chat-input" id="chatInput" 
                               placeholder="Ask Luna about system status..." 
                               onkeypress="handleKeyPress(event)">
                        <button class="send-button" onclick="sendMessage()">
                            📤 Send
                        </button>
                    </div>
                    <div class="quick-commands">
                        <button class="command-btn" onclick="sendCommand('/status')">📊 Status</button>
                        <button class="command-btn" onclick="sendCommand('/zones')">🌆 Zones</button>
                        <button class="command-btn" onclick="sendCommand('/help')">💡 Help</button>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Global dashboard instance
        let dashboard = null;

        // Initialize when DOM is loaded
        document.addEventListener('DOMContentLoaded', function() {
            console.log('🚀 Dashboard loaded');
            dashboard = new Dashboard();
            window.dashboard = dashboard; // Make it global for debugging
        });

        class Dashboard {
            constructor() {
                console.log('🔧 Dashboard constructor called');
                this.setupEventListeners();
            }

            setupEventListeners() {
                console.log('🎯 Setting up event listeners');
                
                // Test button directly
                const sendBtn = document.querySelector('.send-button');
                console.log('🔍 Send button found:', sendBtn);
                
                if (sendBtn) {
                    sendBtn.addEventListener('click', (e) => {
                        console.log('🎯 Button clicked via addEventListener');
                        e.preventDefault();
                        this.sendMessage();
                    });
                }
            }

            async sendMessage() {
                console.log('📤 sendMessage() called');
                
                const input = document.getElementById('chatInput');
                const message = input.value.trim();
                
                console.log('📝 Message:', message);
                
                if (!message) {
                    console.log('❌ Empty message');
                    return;
                }

                // Add user message
                this.addMessage(message, 'user');
                input.value = '';

                // Send to Luna
                await this.sendToLuna(message);
            }

            async sendToLuna(message) {
                console.log('🌙 Sending to Luna:', message);

                try {
                    const response = await fetch('/api/chat', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ message: message })
                    });

                    console.log('📡 Response status:', response.status);

                    if (!response.ok) {
                        throw new Error(`HTTP ${response.status}`);
                    }

                    const data = await response.json();
                    const lunaResponse = data.response || data.error || 'No response';

                    console.log('🌙 Luna response:', lunaResponse);
                    this.addMessage(lunaResponse, 'luna');

                } catch (error) {
                    console.error('❌ Error:', error);
                    this.addMessage(`❌ Error: ${error.message}`, 'luna');
                }
            }

            addMessage(content, sender) {
                console.log('💬 Adding message:', sender, content);
                
                const chatMessages = document.getElementById('chatMessages');
                const messageDiv = document.createElement('div');
                messageDiv.className = `message ${sender}`;
                messageDiv.innerHTML = `<strong>${sender === 'user' ? 'You' : 'Luna'}:</strong> ${content}`;
                
                chatMessages.appendChild(messageDiv);
                chatMessages.scrollTop = chatMessages.scrollHeight;
            }

            sendCommand(command) {
                console.log('⚡ Command:', command);
                document.getElementById('chatInput').value = command;
                this.sendMessage();
            }
        }

        // Global functions for onclick handlers
        function sendMessage() {
            console.log('🌍 Global sendMessage() called');
            if (window.dashboard) {
                window.dashboard.sendMessage();
            } else {
                console.error('❌ Dashboard not initialized');
            }
        }

        function sendCommand(command) {
            console.log('⚡ Global sendCommand() called:', command);
            if (window.dashboard) {
                window.dashboard.sendCommand(command);
            } else {
                console.error('❌ Dashboard not initialized');
            }
        }

        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }

        console.log('🎯 Script loaded, functions defined');
    </script>
</body>
</html>"""
        
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(html_content.encode('utf-8'))

def run_server(port=8095):
    server_address = ('', port)
    httpd = HTTPServer(server_address, LunaWebServer)
    
    print(f"🌙 LunaBeyond AI Web Server Starting...")
    print(f"📱 Open http://localhost:{port}")
    print(f"🚀 Press Ctrl+C to stop")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
        httpd.server_close()

if __name__ == "__main__":
    run_server()
