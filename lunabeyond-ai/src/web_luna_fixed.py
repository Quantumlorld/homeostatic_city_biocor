#!/usr/bin/env python3
"""
🌙 LunaBeyond AI Web Server with Beautiful Dashboard
Fixed version - serves integrated dashboard with Luna AI
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

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class LunaWebServer(BaseHTTPRequestHandler):
    """Enhanced web server with Luna AI integration"""
    
    def do_GET(self):
        """Handle GET requests with query string support"""
        try:
            # Parse path ignoring query strings
            parsed_path = urlparse(self.path)
            clean_path = parsed_path.path
            
            # Route to handlers
            if clean_path == '/' or clean_path == '':
                self.serve_dashboard()
            elif clean_path == '/api/status':
                self.serve_api_response(self.get_status())
            elif clean_path == '/api/zones':
                self.serve_api_response(self.get_zones())
            elif clean_path == '/api/chat':
                self.send_error(405, "Method Not Allowed - Use POST for chat")
            else:
                self.send_error(404, "Not Found")
        except Exception as e:
            logger.error(f"GET error: {e}")
            self.send_error(500, f"Internal Server Error: {e}")
    
    def do_POST(self):
        """Handle POST requests"""
        try:
            # Parse path ignoring query strings
            parsed_path = urlparse(self.path)
            clean_path = parsed_path.path
            
            if clean_path == '/api/chat':
                self.handle_chat_request()
            else:
                self.send_error(404, "Not Found")
        except Exception as e:
            logger.error(f"POST error: {e}")
            self.send_error(500, f"Internal Server Error: {e}")
    
    def serve_api_response(self, data):
        """Serve JSON API response"""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        response = json.dumps(data, indent=2)
        self.wfile.write(response.encode('utf-8'))
    
    def get_status(self):
        """Get system status"""
        return {
            "status": "active",
            "timestamp": datetime.now().isoformat(),
            "ai_generation": 2,
            "system_health": 0.924,
            "zones_active": 5,
            "message": "BHCS system operational with Luna AI integration"
        }
    
    def get_zones(self):
        """Get zone data"""
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
        """Handle chat requests"""
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
                
                # Generate Luna response
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
        """Generate Luna AI response"""
        message_lower = message.lower()
        
        # Command responses
        if message_lower == '/status':
            return """📊 **System Status Report:**
System Health: 92.4%
Average Activity: 0.46
Recovery Confidence: 87%
AI Generation: 2

All zones are maintaining homeostatic balance within acceptable parameters."""
        
        if message_lower == '/zones':
            return """🌆 **Zone Status:**
**Downtown**: CALM (0.420)
**Industrial**: OVERSTIMULATED (0.540)
**Residential**: CALM (0.410)
**Commercial**: OVERSTIMULATED (0.480)
**Tech Park**: CALM (0.450)

3 zones in CALM state, 2 zones requiring attention."""
        
        if message_lower == '/evolve':
            return """🧬 **AI Evolution Complete!**
I have evolved to Generation 3!
My neural networks have mutated and adapted.
New capabilities: Enhanced pattern recognition, improved prediction accuracy."""
        
        if message_lower == '/learn':
            return """📚 **Learning Mode Active**
I'm currently analyzing zone patterns and environmental factors.
Recent observations: 3 zones in CALM state
Learning confidence: 87%"""
        
        if message_lower == '/predict':
            return """🔮 **System Predictions:**
Downtown: decreasing trend expected
Industrial: stable trend expected
Residential: increasing trend expected
Commercial: stable trend expected
Tech Park: increasing trend expected"""
        
        if message_lower == '/help':
            return """💡 **Available Commands:**
📊 /status - System health and metrics
🌆 /zones - Detailed zone status
🧬 /evolve - Evolve AI to next generation
📚 /learn - Show learning progress
🔮 /predict - Zone trend predictions
💡 /help - Show this help message

You can also ask me questions about system in natural language!"""
        
        # Natural language responses
        if 'health' in message_lower:
            return """📊 The system health is currently 92.4%, which is excellent. All zones are maintaining proper homeostatic balance."""
        
        if 'zone' in message_lower:
            return """🌆 **Zone Analysis:**
I'm monitoring all 5 zones in real-time:
- Downtown: CALM state, well balanced
- Industrial: OVERSTIMULATED, requiring attention
- Residential: CALM state, stable
- Commercial: OVERSTIMULATED, moderate activity
- Tech Park: CALM state, optimal

Would you like me to apply any interventions?"""
        
        if 'intervention' in message_lower or 'apply' in message_lower:
            return """🌿 **BioCore Intervention Ready**
I can help you apply interventions to specific zones. Use the control panel to:
1. Select target zone
2. Set magnitude (-0.2 to +0.2)
3. Adjust synergy modifier (0.0 to 1.0)
4. Click "Apply BioCore"

All interventions respect homeostatic principles."""
        
        # Default conversational response
        responses = [
            "I'm monitoring the BHCS system and all zones are functioning within normal parameters. The current system health is 92.4%.",
            "Based on my analysis, 3 zones are currently in CALM state, which indicates good homeostatic balance.",
            "The system is maintaining stability with an average activity level of 0.46. All zones are gradually moving toward their target states.",
            "I've detected interesting patterns in zone transitions. Would you like me to provide detailed analysis or apply any interventions?"
            "The BioCore interventions are working effectively. Recovery confidence is at 87% and improving."
        ]
        
        return responses[hash(message) % len(responses)]
    
    def serve_dashboard(self):
        """Serve the beautiful integrated dashboard"""
        html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🦀🌙 BHCS + Luna AI - Integrated Dashboard</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #0f1419 0%, #1a1f2e 50%, #2d3748 100%);
            color: #e2e8f0;
            min-height: 100vh;
            line-height: 1.6;
            overflow-x: hidden;
        }

        .dashboard-container {
            max-width: 2000px;
            margin: 0 auto;
            padding: 20px;
            animation: fadeIn 0.8s ease-out;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .header {
            text-align: center;
            margin-bottom: 40px;
            position: relative;
        }

        .header h1 {
            font-size: 3rem;
            font-weight: 700;
            background: linear-gradient(135deg, #4299e1, #667eea, #764ba2, #f687b3);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 10px;
            letter-spacing: -0.02em;
        }

        .header .subtitle {
            color: #a0aec0;
            font-size: 1.1rem;
            font-weight: 300;
        }

        .status-indicator {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            margin-top: 15px;
            padding: 8px 16px;
            background: rgba(66, 153, 225, 0.1);
            border: 1px solid rgba(66, 153, 225, 0.3);
            border-radius: 20px;
            font-size: 0.9rem;
        }

        .status-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #4299e1;
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }

        .main-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            margin-bottom: 40px;
        }

        .system-section {
            display: flex;
            flex-direction: column;
            gap: 20px;
        }

        .system-overview {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
        }

        .metric-card {
            background: rgba(45, 55, 72, 0.5);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(66, 153, 225, 0.2);
            border-radius: 16px;
            padding: 20px;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }

        .metric-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, #4299e1, #667eea);
            animation: shimmer 3s infinite;
        }

        @keyframes shimmer {
            0% { transform: translateX(-100%); }
            100% { transform: translateX(100%); }
        }

        .metric-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.25);
            border-color: rgba(66, 153, 225, 0.4);
        }

        .metric-label {
            color: #a0aec0;
            font-size: 0.875rem;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 8px;
        }

        .metric-value {
            font-size: 2rem;
            font-weight: 700;
            color: #e2e8f0;
            margin-bottom: 8px;
        }

        .metric-change {
            font-size: 0.875rem;
            font-weight: 500;
            display: flex;
            align-items: center;
            gap: 4px;
        }

        .change-positive { color: #48bb78; }
        .change-negative { color: #f56565; }
        .change-neutral { color: #a0aec0; }

        .zones-section {
            background: rgba(45, 55, 72, 0.5);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(66, 153, 225, 0.2);
            border-radius: 16px;
            padding: 20px;
        }

        .section-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }

        .section-title {
            font-size: 1.25rem;
            font-weight: 600;
            color: #e2e8f0;
        }

        .zones-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
        }

        .zone-card {
            background: rgba(26, 32, 44, 0.6);
            border: 1px solid rgba(66, 153, 225, 0.2);
            border-radius: 12px;
            padding: 16px;
            transition: all 0.3s ease;
            position: relative;
        }

        .zone-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
        }

        .zone-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
        }

        .zone-name {
            font-size: 1rem;
            font-weight: 600;
            color: #e2e8f0;
        }

        .zone-state {
            padding: 3px 8px;
            border-radius: 10px;
            font-size: 0.7rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        .state-calm {
            background: rgba(72, 187, 120, 0.2);
            color: #48bb78;
            border: 1px solid rgba(72, 187, 120, 0.3);
        }

        .state-overstimulated {
            background: rgba(237, 137, 54, 0.2);
            color: #ed8936;
            border: 1px solid rgba(237, 137, 54, 0.3);
        }

        .zone-activity {
            margin: 12px 0;
        }

        .activity-bar {
            height: 6px;
            background: rgba(66, 153, 225, 0.2);
            border-radius: 3px;
            overflow: hidden;
            position: relative;
        }

        .activity-fill {
            height: 100%;
            background: linear-gradient(90deg, #4299e1, #667eea);
            border-radius: 3px;
            transition: width 0.6s ease;
        }

        .luna-section {
            display: flex;
            flex-direction: column;
            gap: 20px;
            height: fit-content;
        }

        .luna-chat {
            background: rgba(45, 55, 72, 0.5);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(66, 153, 225, 0.2);
            border-radius: 16px;
            padding: 20px;
            display: flex;
            flex-direction: column;
            height: 600px;
        }

        .luna-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 16px;
            padding-bottom: 12px;
            border-bottom: 1px solid rgba(66, 153, 225, 0.2);
        }

        .luna-title {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 1.25rem;
            font-weight: 600;
            color: #e2e8f0;
        }

        .luna-status {
            display: flex;
            align-items: center;
            gap: 6px;
            padding: 4px 10px;
            background: rgba(246, 135, 179, 0.2);
            border: 1px solid rgba(246, 135, 179, 0.3);
            border-radius: 12px;
            font-size: 0.8rem;
            color: #f687b3;
        }

        .chat-messages {
            flex: 1;
            overflow-y: auto;
            background: rgba(26, 32, 44, 0.6);
            border-radius: 12px;
            padding: 16px;
            margin-bottom: 16px;
            border: 1px solid rgba(66, 153, 225, 0.1);
        }

        .message {
            margin-bottom: 16px;
            padding: 12px;
            border-radius: 12px;
            max-width: 85%;
            animation: messageSlide 0.3s ease-out;
        }

        @keyframes messageSlide {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .message.user {
            background: rgba(66, 153, 225, 0.1);
            border: 1px solid rgba(66, 153, 225, 0.2);
            margin-left: auto;
            text-align: right;
        }

        .message.luna {
            background: rgba(246, 135, 179, 0.1);
            border: 1px solid rgba(246, 135, 179, 0.2);
        }

        .message-sender {
            font-weight: 600;
            margin-bottom: 6px;
            font-size: 0.875rem;
        }

        .message.user .message-sender {
            color: #4299e1;
        }

        .message.luna .message-sender {
            color: #f687b3;
        }

        .message-content {
            color: #e2e8f0;
            line-height: 1.5;
        }

        .chat-input-container {
            display: flex;
            gap: 12px;
        }

        .chat-input {
            flex: 1;
            padding: 12px 16px;
            background: rgba(26, 32, 44, 0.8);
            border: 1px solid rgba(66, 153, 225, 0.3);
            border-radius: 8px;
            color: #e2e8f0;
            font-size: 0.9rem;
            transition: all 0.2s ease;
        }

        .chat-input:focus {
            outline: none;
            border-color: #4299e1;
            box-shadow: 0 0 0 3px rgba(66, 153, 225, 0.1);
        }

        .send-button {
            padding: 12px 24px;
            background: linear-gradient(135deg, #f687b3, #764ba2);
            color: white;
            border: none;
            border-radius: 8px;
            font-weight: 600;
            font-size: 0.9rem;
            cursor: pointer;
            transition: all 0.2s ease;
        }

        .send-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(246, 135, 179, 0.3);
        }

        .send-button:active {
            transform: translateY(0);
        }

        .quick-commands {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 8px;
            margin-top: 12px;
        }

        .command-btn {
            padding: 8px 12px;
            background: rgba(66, 153, 225, 0.1);
            color: #4299e1;
            border: 1px solid rgba(66, 153, 225, 0.3);
            border-radius: 6px;
            font-size: 0.8rem;
            cursor: pointer;
            transition: all 0.2s ease;
        }

        .command-btn:hover {
            background: rgba(66, 153, 225, 0.2);
            transform: translateY(-1px);
        }

        @media (max-width: 1200px) {
            .main-grid {
                grid-template-columns: 1fr;
            }
            
            .system-overview {
                grid-template-columns: repeat(2, 1fr);
            }
        }

        @media (max-width: 768px) {
            .dashboard-container {
                padding: 12px;
            }
            
            .header h1 {
                font-size: 2rem;
            }
            
            .zones-grid {
                grid-template-columns: 1fr;
            }
            
            .quick-commands {
                grid-template-columns: repeat(2, 1fr);
            }
        }
    </style>
</head>
<body>
    <div class="dashboard-container">
        <header class="header">
            <h1>🦀🌙 BHCS + Luna AI</h1>
            <div class="subtitle">Homeostatic City BioCore with Conversational AI</div>
            <div class="status-indicator">
                <div class="status-dot"></div>
                <span>System Online</span>
            </div>
        </header>

        <div class="main-grid">
            <div class="system-section">
                <div class="system-overview">
                    <div class="metric-card">
                        <div class="metric-label">System Health</div>
                        <div class="metric-value" id="systemHealth">92.4%</div>
                        <div class="metric-change change-positive">
                            <span>↑</span> 2.1%
                        </div>
                    </div>
                    
                    <div class="metric-card">
                        <div class="metric-label">Average Activity</div>
                        <div class="metric-value" id="avgActivity">0.46</div>
                        <div class="metric-change change-neutral">
                            <span>→</span> Target: 0.50
                        </div>
                    </div>
                    
                    <div class="metric-card">
                        <div class="metric-label">Recovery Confidence</div>
                        <div class="metric-value" id="recoveryConfidence">87%</div>
                        <div class="metric-change change-positive">
                            <span>↑</span> 5%
                        </div>
                    </div>
                    
                    <div class="metric-card">
                        <div class="metric-label">AI Generation</div>
                        <div class="metric-value" id="aiGeneration">2</div>
                        <div class="metric-change change-positive">
                            <span>↑</span> Evolved
                        </div>
                    </div>
                </div>

                <div class="zones-section">
                    <div class="section-header">
                        <h3 class="section-title">🌆 Zone Status</h3>
                        <div class="status-indicator">
                            <div class="status-dot"></div>
                            <span>Live</span>
                        </div>
                    </div>
                    
                    <div class="zones-grid" id="zonesGrid">
                        <!-- Zones will be populated here -->
                    </div>
                </div>
            </div>

            <div class="luna-section">
                <div class="luna-chat">
                    <div class="luna-header">
                        <div class="luna-title">
                            🌙 LunaBeyond AI
                        </div>
                        <div class="luna-status">
                            <div class="status-dot"></div>
                            <span>Online</span>
                        </div>
                    </div>
                    
                    <div class="chat-messages" id="chatMessages">
                        <div class="message luna">
                            <div class="message-sender">🌙 LunaBeyond</div>
                            <div class="message-content">
                                Hello! I'm LunaBeyond, your AI companion for BHCS system. I'm monitoring all zones and learning from their homeostatic patterns. Ask me anything about system status, zone analysis, or request interventions!
                            </div>
                        </div>
                    </div>
                    
                    <div class="chat-input-container">
                        <input type="text" class="chat-input" id="chatInput" 
                               placeholder="Ask Luna about system status, zones, or interventions..." 
                               onkeypress="handleKeyPress(event)">
                        <button class="send-button" onclick="sendMessage()">
                            📤 Send
                        </button>
                    </div>
                    
                    <div class="quick-commands">
                        <button class="command-btn" onclick="sendCommand('/status')">📊 Status</button>
                        <button class="command-btn" onclick="sendCommand('/zones')">🌆 Zones</button>
                        <button class="command-btn" onclick="sendCommand('/evolve')">🧬 Evolve</button>
                        <button class="command-btn" onclick="sendCommand('/learn')">📚 Learn</button>
                        <button class="command-btn" onclick="sendCommand('/predict')">🔮 Predict</button>
                        <button class="command-btn" onclick="sendCommand('/help')">💡 Help</button>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        // BHCS + Luna AI Integrated Dashboard
        class BHCSLunaDashboard {
            constructor() {
                this.zones = [];
                this.systemMetrics = {
                    health: 0.924,
                    avgActivity: 0.46,
                    recoveryConfidence: 0.87,
                    aiGeneration: 2
                };
                
                this.initializeDashboard();
                this.startRealTimeUpdates();
            }
            
            initializeDashboard() {
                console.log('🦀🌙 Initializing BHCS + Luna AI Dashboard');
                
                this.initializeZones();
                this.setupEventListeners();
                
                console.log('✅ BHCS + Luna AI Dashboard ready');
            }
            
            initializeZones() {
                this.zones = [
                    { id: 0, name: 'Downtown', activity: 0.42, state: 'CALM', target: 0.5 },
                    { id: 1, name: 'Industrial', activity: 0.54, state: 'OVERSTIMULATED', target: 0.5 },
                    { id: 2, name: 'Residential', activity: 0.41, state: 'CALM', target: 0.5 },
                    { id: 3, name: 'Commercial', activity: 0.48, state: 'OVERSTIMULATED', target: 0.5 },
                    { id: 4, name: 'Tech Park', activity: 0.45, state: 'CALM', target: 0.5 }
                ];
                
                this.renderZones();
            }
            
            renderZones() {
                const zonesGrid = document.getElementById('zonesGrid');
                zonesGrid.innerHTML = '';
                
                this.zones.forEach(zone => {
                    const zoneCard = document.createElement('div');
                    zoneCard.className = 'zone-card';
                    zoneCard.innerHTML = `
                        <div class="zone-header">
                            <div class="zone-name">${zone.name}</div>
                            <div class="zone-state state-${zone.state.toLowerCase()}">${zone.state}</div>
                        </div>
                        <div class="zone-activity">
                            <div class="activity-bar">
                                <div class="activity-fill" style="width: ${zone.activity * 100}%"></div>
                            </div>
                        </div>
                    `;
                    zonesGrid.appendChild(zoneCard);
                });
            }
            
            setupEventListeners() {
                console.log('Setting up event listeners');
            }
            
            startRealTimeUpdates() {
                setInterval(() => {
                    this.updateSystemMetrics();
                    this.simulateZoneChanges();
                }, 3000);
            }
            
            updateSystemMetrics() {
                this.systemMetrics.health += (Math.random() - 0.5) * 0.02;
                this.systemMetrics.health = Math.max(0, Math.min(1, this.systemMetrics.health));
                
                this.systemMetrics.avgActivity += (Math.random() - 0.5) * 0.01;
                this.systemMetrics.avgActivity = Math.max(0, Math.min(1, this.systemMetrics.avgActivity));
                
                this.systemMetrics.recoveryConfidence += (Math.random() - 0.5) * 0.01;
                this.systemMetrics.recoveryConfidence = Math.max(0, Math.min(1, this.systemMetrics.recoveryConfidence));
                
                document.getElementById('systemHealth').textContent = `${(this.systemMetrics.health * 100).toFixed(1)}%`;
                document.getElementById('avgActivity').textContent = this.systemMetrics.avgActivity.toFixed(2);
                document.getElementById('recoveryConfidence').textContent = `${(this.systemMetrics.recoveryConfidence * 100).toFixed(0)}%`;
                document.getElementById('aiGeneration').textContent = this.systemMetrics.aiGeneration;
            }
            
            simulateZoneChanges() {
                this.zones.forEach(zone => {
                    const balanceError = zone.target - zone.activity;
                    const adjustment = 0.03 * balanceError;
                    const decay = zone.activity > zone.target ? -0.01 : 0;
                    
                    zone.activity += adjustment + decay;
                    zone.activity = Math.max(0, Math.min(1, zone.activity));
                    
                    if (zone.activity < 0.3) zone.state = 'CALM';
                    else if (zone.activity < 0.6) zone.state = 'OVERSTIMULATED';
                    else if (zone.activity < 0.8) zone.state = 'EMERGENT';
                    else zone.state = 'CRITICAL';
                });
                
                this.renderZones();
            }
            
            async sendMessage() {
                const input = document.getElementById('chatInput');
                const message = input.value.trim();
                
                console.log('🔍 Send button clicked. Message:', message);
                
                if (!message) {
                    console.log('❌ Empty message, not sending');
                    return;
                }
                
                console.log('✅ Adding user message to chat');
                this.addMessage(message, 'user');
                input.value = '';
                
                console.log('📡 Sending to Luna API...');
                await this.sendToLunaAPI(message);
            }
            
            async sendToLunaAPI(message) {
                try {
                    console.log('🌙 Sending to Luna API:', message);
                    
                    const response = await fetch('/api/chat', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ message: message })
                    });
                    
                    console.log('📡 Response status:', response.status);
                    
                    if (!response.ok) {
                        const errorText = await response.text();
                        throw new Error(`HTTP ${response.status}: ${errorText}`);
                    }
                    
                    const data = await response.json();
                    const lunaResponse = data.response || data.error || 'No response received';
                    
                    this.addMessage(lunaResponse, 'luna');
                    console.log('🌙 Luna response:', lunaResponse);
                    
                } catch (error) {
                    console.error('❌ Luna API error:', error);
                    this.addMessage(`❌ Error: ${error.message}`, 'luna');
                }
            }
            
            sendCommand(command) {
                document.getElementById('chatInput').value = command;
                this.sendMessage();
            }
            
            handleKeyPress(event) {
                if (event.key === 'Enter') {
                    this.sendMessage();
                }
            }
            
            addMessage(content, sender) {
                const chatMessages = document.getElementById('chatMessages');
                const messageDiv = document.createElement('div');
                messageDiv.className = `message ${sender}`;
                messageDiv.innerHTML = `
                    <div class="message-sender">${sender === 'user' ? '👤 You' : '🌙 LunaBeyond'}</div>
                    <div class="message-content">${content}</div>
                `;
                chatMessages.appendChild(messageDiv);
                chatMessages.scrollTop = chatMessages.scrollHeight;
            }
        }
        
        // Initialize dashboard
        document.addEventListener('DOMContentLoaded', () => {
            new BHCSLunaDashboard();
        });
    </script>
</body>
</html>"""
        
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(html_content.encode('utf-8'))

def run_server(port=8095):
    """Run the Luna web server"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, LunaWebServer)
    
    print(f"🌙 LunaBeyond AI Web Server Starting...")
    print(f"📱 Open http://localhost:{port} to chat with Luna!")
    print(f"🧠 Integrated BHCS system with conversational AI")
    print(f"🚀 Press Ctrl+C to stop the server")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        httpd.server_close()

if __name__ == "__main__":
    run_server()
