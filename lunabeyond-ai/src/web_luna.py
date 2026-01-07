#!/usr/bin/env python3
"""
LunaBeyond AI - Web Interface
Web-based conversational AI that integrates with the BHCS dashboard
"""

import asyncio
import json
import time
from datetime import datetime
from typing import Dict, List
from pathlib import Path
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse

# Add parent directories for imports
sys.path.append(str(Path(__file__).parent.parent.parent))
sys.path.append(str(Path(__file__).parent))

from enhanced_ai import EnhancedLunaBeyondAI
from test_system import BHCS, BioCore
from luna_conversation import LunaConversation

class LunaWebInterface(BaseHTTPRequestHandler):
    """Web interface for LunaBeyond AI"""
    
    def __init__(self, *args, **kwargs):
        self.luna = None  # Will be initialized in do_GET
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/':
            self.serve_dashboard()
        elif self.path == '/api/status':
            self.serve_api_status()
        elif self.path.startswith('/api/'):
            self.serve_api_response()
        else:
            self.send_error(404)
    
    def do_POST(self):
        """Handle POST requests"""
        if self.path == '/api/chat':
            self.handle_chat_request()
        elif self.path == '/api/command':
            self.handle_command_request()
        else:
            self.send_error(404)
    
    def serve_dashboard(self):
        """Serve the main dashboard with Luna integration"""
        html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BHCS + LunaBeyond AI - Integrated System</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 50%, #16213e 100%);
            color: white;
            min-height: 100vh;
            line-height: 1.6;
        }

        .container {
            max-width: 1600px;
            margin: 0 auto;
            padding: 20px;
        }

        .header {
            text-align: center;
            margin-bottom: 30px;
        }

        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
            background: linear-gradient(45deg, #4CAF50, #9C27B0, #2196F3);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .main-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 20px;
        }

        .panel {
            background: rgba(255,255,255,0.05);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 20px;
            border: 1px solid rgba(255,255,255,0.1);
            transition: transform 0.3s ease;
        }

        .panel:hover {
            transform: translateY(-2px);
        }

        .panel h2 {
            color: #64B5F6;
            margin-bottom: 15px;
            font-size: 1.3rem;
        }

        /* BHCS System Styles */
        .zones-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 10px;
        }

        .zone-card {
            background: rgba(255,255,255,0.1);
            border-radius: 8px;
            padding: 10px;
            text-align: center;
            transition: all 0.3s ease;
        }

        .zone-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        }

        .zone-state {
            display: inline-block;
            padding: 2px 6px;
            border-radius: 8px;
            font-size: 0.7rem;
            font-weight: 600;
            margin-bottom: 5px;
        }

        .state-calm { background: #4CAF50; color: white; }
        .state-overstimulated { background: #FF9800; color: white; }
        .state-emergent { background: #f44336; color: white; }
        .state-critical { background: #9C27B0; color: white; }

        .zone-activity {
            font-size: 1rem;
            font-weight: bold;
            color: #FFD700;
        }

        /* Luna AI Chat Styles */
        .chat-container {
            height: 400px;
            display: flex;
            flex-direction: column;
        }

        .chat-messages {
            flex: 1;
            overflow-y: auto;
            background: rgba(0,0,0,0.2);
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 10px;
        }

        .message {
            margin-bottom: 15px;
            padding: 10px;
            border-radius: 10px;
            max-width: 80%;
        }

        .message.user {
            background: rgba(76, 175, 80, 0.2);
            margin-left: auto;
            text-align: right;
        }

        .message.luna {
            background: rgba(156, 39, 176, 0.2);
        }

        .message-sender {
            font-weight: bold;
            margin-bottom: 5px;
            font-size: 0.9rem;
        }

        .chat-input-container {
            display: flex;
            gap: 10px;
        }

        .chat-input {
            flex: 1;
            padding: 10px;
            border: 1px solid rgba(255,255,255,0.3);
            border-radius: 8px;
            background: rgba(255,255,255,0.1);
            color: white;
            font-size: 0.9rem;
        }

        .chat-send {
            padding: 10px 20px;
            border: none;
            border-radius: 8px;
            background: linear-gradient(135deg, #9C27B0, #673AB7);
            color: white;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
        }

        .chat-send:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        }

        /* Control Panel Styles */
        .control-panel {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
        }

        .control-group {
            display: flex;
            flex-direction: column;
            gap: 5px;
        }

        .control-group label {
            font-weight: 600;
            opacity: 0.9;
            font-size: 0.9rem;
        }

        .control-group select,
        .control-group input {
            padding: 8px;
            border: 1px solid rgba(255,255,255,0.3);
            border-radius: 6px;
            background: rgba(255,255,255,0.1);
            color: white;
            font-size: 0.9rem;
        }

        .control-group select option {
            background: #1a1f3a;
            color: white;
        }

        .control-buttons {
            display: flex;
            gap: 10px;
            margin-top: 15px;
        }

        .btn {
            padding: 10px 15px;
            border: none;
            border-radius: 6px;
            font-size: 0.8rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            flex: 1;
        }

        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        }

        .btn-primary { background: linear-gradient(135deg, #4CAF50, #45a049); color: white; }
        .btn-secondary { background: linear-gradient(135deg, #9C27B0, #673AB7); color: white; }
        .btn-danger { background: linear-gradient(135deg, #f44336, #d32f2f); color: white; }

        /* Metrics Styles */
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 10px;
            margin-bottom: 15px;
        }

        .metric-card {
            background: rgba(255,255,255,0.1);
            border-radius: 8px;
            padding: 10px;
            text-align: center;
        }

        .metric-value {
            font-size: 1.5rem;
            font-weight: bold;
            color: #FFD700;
        }

        .metric-label {
            font-size: 0.8rem;
            opacity: 0.8;
        }

        /* Status Indicator */
        .status-indicator {
            display: inline-block;
            width: 10px;
            height: 10px;
            border-radius: 50%;
            margin-right: 5px;
            animation: pulse 2s infinite;
        }

        .status-online { background: #4CAF50; }
        .status-learning { background: #9C27B0; }
        .status-warning { background: #FF9800; }

        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.5; }
            100% { opacity: 1; }
        }

        /* Responsive */
        @media (max-width: 1200px) {
            .main-grid {
                grid-template-columns: 1fr;
            }
            
            .metrics-grid {
                grid-template-columns: repeat(2, 1fr);
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>BHCS + LunaBeyond AI</h1>
            <p>Integrated Homeostatic System with Conversational AI</p>
        </div>

        <div class="main-grid">
            <!-- BHCS System Panel -->
            <div class="panel">
                <h2>🧠 BHCS System</h2>
                
                <div class="metrics-grid">
                    <div class="metric-card">
                        <div class="metric-value" id="systemHealth">20%</div>
                        <div class="metric-label">System Health</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value" id="avgActivity">0.65</div>
                        <div class="metric-label">Avg Activity</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value" id="aiAccuracy">50%</div>
                        <div class="metric-label">AI Accuracy</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value" id="riskLevel">Low</div>
                        <div class="metric-label">Risk Level</div>
                    </div>
                </div>

                <div class="zones-grid" id="zonesGrid">
                    <!-- Zones will be populated here -->
                </div>

                <div class="control-panel">
                    <div class="control-group">
                        <label for="zoneSelect">Zone</label>
                        <select id="zoneSelect">
                            <option value="0">Zone 0</option>
                            <option value="1">Zone 1</option>
                            <option value="2">Zone 2</option>
                            <option value="3">Zone 3</option>
                            <option value="4">Zone 4</option>
                        </select>
                    </div>
                    <div class="control-group">
                        <label for="plantSelect">Plant</label>
                        <select id="plantSelect">
                            <option value="Ginkgo">🌿 Ginkgo</option>
                            <option value="Aloe">🌱 Aloe</option>
                            <option value="Turmeric">🌿 Turmeric</option>
                            <option value="Ginseng">🌿 Ginseng</option>
                            <option value="Ashwagandha">🌿 Ashwagandha</option>
                        </select>
                    </div>
                    <div class="control-group">
                        <label for="drugSelect">Drug</label>
                        <select id="drugSelect">
                            <option value="DrugA">💊 DrugA</option>
                            <option value="DrugB">💊 DrugB</option>
                            <option value="DrugC">💊 DrugC</option>
                            <option value="DrugD">💊 DrugD</option>
                            <option value="DrugE">💊 DrugE</option>
                        </select>
                    </div>
                    <div class="control-group">
                        <label for="synergySlider">Synergy: <span id="synergyValue">0.7</span></label>
                        <input type="range" id="synergySlider" min="0.1" max="1.0" step="0.1" value="0.7">
                    </div>
                </div>

                <div class="control-buttons">
                    <button class="btn btn-primary" onclick="applyBiocore()">🌿 Apply BioCore</button>
                    <button class="btn btn-secondary" onclick="optimizeSystem()">🧠 Optimize</button>
                    <button class="btn btn-danger" onclick="resetSystem()">🔄 Reset</button>
                </div>
            </div>

            <!-- Luna AI Chat Panel -->
            <div class="panel">
                <h2>🌙 LunaBeyond AI <span class="status-indicator status-learning"></span></h2>
                
                <div class="chat-container">
                    <div class="chat-messages" id="chatMessages">
                        <div class="message luna">
                            <div class="message-sender">🌙 LunaBeyond</div>
                            <div>Hello! I'm LunaBeyond, your AI companion. I'm monitoring the BHCS system and learning from its behavior. Ask me anything about the system or type '/help' for commands!</div>
                        </div>
                    </div>
                    
                    <div class="chat-input-container">
                        <input type="text" class="chat-input" id="chatInput" placeholder="Ask Luna about the system..." onkeypress="handleKeyPress(event)">
                        <button class="chat-send" onclick="sendMessage()">Send</button>
                    </div>
                </div>

                <div style="margin-top: 15px;">
                    <h3 style="color: #64B5F6; margin-bottom: 10px;">Quick Commands</h3>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px;">
                        <button class="btn btn-primary" onclick="sendCommand('/status')">📊 Status</button>
                        <button class="btn btn-primary" onclick="sendCommand('/zones')">🧠 Zones</button>
                        <button class="btn btn-primary" onclick="sendCommand('/ai')">🤖 AI Info</button>
                        <button class="btn btn-primary" onclick="sendCommand('/predict')">🔮 Predict</button>
                        <button class="btn btn-secondary" onclick="sendCommand('/learn')">📚 Learn</button>
                        <button class="btn btn-secondary" onclick="sendCommand('/evolve')">🌙 Evolve</button>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        // BHCS System + Luna Integration
        class IntegratedSystem {
            constructor() {
                this.zones = [
                    { id: 0, activity: 0.8, state: "OVERSTIMULATED" },
                    { id: 1, activity: 0.6, state: "OVERSTIMULATED" },
                    { id: 2, activity: 0.3, state: "CALM" },
                    { id: 3, activity: 0.7, state: "OVERSTIMULATED" },
                    { id: 4, activity: 0.5, state: "CALM" }
                ];
                
                this.init();
            }

            init() {
                this.setupEventListeners();
                this.updateDisplay();
                this.startSystemSimulation();
                this.startApiPolling();
            }

            setupEventListeners() {
                document.getElementById('synergySlider').addEventListener('input', (e) => {
                    document.getElementById('synergyValue').textContent = e.target.value;
                });
            }

            updateDisplay() {
                // Update zones
                const zonesGrid = document.getElementById('zonesGrid');
                zonesGrid.innerHTML = '';

                this.zones.forEach(zone => {
                    const zoneCard = document.createElement('div');
                    zoneCard.className = 'zone-card';
                    zoneCard.innerHTML = `
                        <div class="zone-id">Zone ${zone.id}</div>
                        <div class="zone-state state-${zone.state.toLowerCase()}">${zone.state}</div>
                        <div class="zone-activity">${zone.activity.toFixed(3)}</div>
                    `;
                    zonesGrid.appendChild(zoneCard);
                });

                // Update metrics
                const systemHealth = this.calculateSystemHealth();
                document.getElementById('systemHealth').textContent = `${(systemHealth * 100).toFixed(0)}%`;
                document.getElementById('avgActivity').textContent = this.calculateAvgActivity().toFixed(3);
                
                const riskLevel = this.calculateRiskLevel();
                document.getElementById('riskLevel').textContent = riskLevel;
            }

            calculateSystemHealth() {
                const calmZones = this.zones.filter(z => z.state === "CALM").length;
                return calmZones / this.zones.length;
            }

            calculateAvgActivity() {
                return this.zones.reduce((sum, zone) => sum + zone.activity, 0) / this.zones.length;
            }

            calculateRiskLevel() {
                const avgActivity = this.calculateAvgActivity();
                if (avgActivity > 0.8) return "High";
                if (avgActivity > 0.6) return "Medium";
                return "Low";
            }

            startSystemSimulation() {
                setInterval(() => {
                    this.zones.forEach(zone => {
                        const change = (Math.random() - 0.5) * 0.02;
                        zone.activity = Math.max(0.0, Math.min(1.0, zone.activity + change));
                        zone.state = this.determineState(zone.activity);
                    });

                    this.updateDisplay();
                }, 2000);
            }

            determineState(activity) {
                if (activity < 0.4) return "CALM";
                if (activity < 0.7) return "OVERSTIMULATED";
                if (activity < 0.9) return "EMERGENT";
                return "CRITICAL";
            }

            startApiPolling() {
                // Poll for AI status updates
                setInterval(async () => {
                    try {
                        const response = await fetch('/api/status');
                        const data = await response.json();
                        
                        if (data.ai_accuracy) {
                            document.getElementById('aiAccuracy').textContent = `${(data.ai_accuracy * 100).toFixed(0)}%`;
                        }
                    } catch (error) {
                        console.log('API polling error:', error);
                    }
                }, 5000);
            }

            async applyBiocore() {
                const zoneId = parseInt(document.getElementById('zoneSelect').value);
                const plant = document.getElementById('plantSelect').value;
                const drug = document.getElementById('drugSelect').value;
                const synergy = parseFloat(document.getElementById('synergySlider').value);

                const zone = this.zones[zoneId];
                zone.activity = Math.max(0.0, Math.min(1.0, zone.activity - 0.2));
                zone.state = this.determineState(zone.activity);

                this.updateDisplay();
                this.addChatMessage(`Applied ${plant} + ${drug} to Zone ${zoneId}`, 'user');
                
                // Simulate Luna response
                setTimeout(() => {
                    this.addChatMessage(`🌿 BioCore intervention applied! Zone ${zoneId} is now ${zone.state} with activity ${zone.activity.toFixed(3)}.`, 'luna');
                }, 500);
            }

            optimizeSystem() {
                this.zones.forEach(zone => {
                    zone.activity = 0.5 + (Math.random() - 0.5) * 0.1;
                    zone.state = this.determineState(zone.activity);
                });

                this.updateDisplay();
                this.addChatMessage('System optimization initiated', 'user');
                
                setTimeout(() => {
                    this.addChatMessage('🧠 System optimized! All zones are now balanced around the optimal activity level.', 'luna');
                }, 500);
            }

            resetSystem() {
                this.zones = [
                    { id: 0, activity: 0.8, state: "OVERSTIMULATED" },
                    { id: 1, activity: 0.6, state: "OVERSTIMULATED" },
                    { id: 2, activity: 0.3, state: "CALM" },
                    { id: 3, activity: 0.7, state: "OVERSTIMULATED" },
                    { id: 4, activity: 0.5, state: "CALM" }
                ];
                
                this.updateDisplay();
                this.addChatMessage('System reset', 'user');
                
                setTimeout(() => {
                    this.addChatMessage('🔄 System reset to initial state. All zones restored.', 'luna');
                }, 500);
            }

            addChatMessage(message, sender) {
                const chatMessages = document.getElementById('chatMessages');
                const messageDiv = document.createElement('div');
                messageDiv.className = `message ${sender}`;
                messageDiv.innerHTML = `
                    <div class="message-sender">${sender === 'user' ? '👤 You' : '🌙 LunaBeyond'}</div>
                    <div>${message}</div>
                `;
                chatMessages.appendChild(messageDiv);
                chatMessages.scrollTop = chatMessages.scrollHeight;
            }

            async sendChatMessage(message) {
                this.addChatMessage(message, 'user');
                
                try {
                    const response = await fetch('/api/chat', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ message: message })
                    });
                    
                    const data = await response.json();
                    this.addChatMessage(data.response, 'luna');
                } catch (error) {
                    // Fallback to simulated response
                    this.simulateLunaResponse(message);
                }
            }

            simulateLunaResponse(message) {
                const responses = {
                    'status': `📊 Current system health is ${(this.calculateSystemHealth() * 100).toFixed(0)}% with ${this.calculateAvgActivity().toFixed(3)} average activity.`,
                    'zones': `🧠 All zones are currently: ${this.zones.map(z => `${z.id}(${z.state})`).join(', ')}`,
                    'ai': '🤖 I\'m currently learning from the system behavior and our conversations!',
                    'help': '💡 Available commands: /status, /zones, /ai, /predict, /learn, /evolve'
                };

                const lowerMessage = message.toLowerCase();
                let response = "🤔 I'm processing that thought!";

                for (const [key, value] of Object.entries(responses)) {
                    if (lowerMessage.includes(key)) {
                        response = value;
                        break;
                    }
                }

                setTimeout(() => {
                    this.addChatMessage(response, 'luna');
                }, 500);
            }
        }

        // Initialize system
        const system = new IntegratedSystem();

        // Global functions
        function applyBiocore() {
            system.applyBiocore();
        }

        function optimizeSystem() {
            system.optimizeSystem();
        }

        function resetSystem() {
            system.resetSystem();
        }

        function sendMessage() {
            const input = document.getElementById('chatInput');
            const message = input.value.trim();
            
            if (message) {
                system.sendChatMessage(message);
                input.value = '';
            }
        }

        function sendCommand(command) {
            system.sendChatMessage(command);
        }

        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }
    </script>
</body>
</html>
        """
        
        self.send_response(200, 'text/html', html_content)
    
    def serve_api_status(self):
        """Serve API status"""
        if not self.luna:
            self.luna = LunaConversation()
        
        status_data = {
            'system_health': self.luna.bhcs.get_system_health(),
            'ai_accuracy': self.luna.ai.performance_metrics['accuracy'],
            'ai_generation': self.luna.ai.generation,
            'conversations': len(self.luna.conversation_history),
            'timestamp': time.time()
        }
        
        self.send_json_response(200, status_data)
    
    def serve_api_response(self):
        """Serve general API responses"""
        if not self.luna:
            self.luna = LunaConversation()
        
        # Handle different API endpoints
        if self.path == '/api/zones':
            zones_data = []
            for zone in self.luna.bhcs.zones:
                zones_data.append({
                    'id': zone.id,
                    'activity': zone.activity,
                    'state': zone.state
                })
            self.send_json_response(200, {'zones': zones_data})
        else:
            self.send_error(404)
    
    def handle_chat_request(self):
        """Handle chat requests"""
        if not self.luna:
            self.luna = LunaConversation()
        
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
            message = data.get('message', '')
            
            # Process message asynchronously
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                response = loop.run_until_complete(self.luna.process_conversation(message))
                
                # Learn from interaction
                loop.run_until_complete(self.luna.learn_from_interaction(message, response))
                
                self.send_json_response(200, {'response': response})
            finally:
                loop.close()
                
        except Exception as e:
            self.send_json_response(500, {'error': str(e)})
    
    def handle_command_request(self):
        """Handle command requests"""
        if not self.luna:
            self.luna = LunaConversation()
        
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
            command = data.get('command', '')
            
            # Process command asynchronously
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                response = loop.run_until_complete(self.luna.handle_command(command))
                self.send_json_response(200, {'response': response})
            finally:
                loop.close()
                
        except Exception as e:
            self.send_json_response(500, {'error': str(e)})
    
    def send_response(self, status_code, content_type, content):
        """Send HTTP response"""
        self.send_response(status_code, content_type, content.encode('utf-8'))
    
    def send_json_response(self, status_code, data):
        """Send JSON response"""
        json_data = json.dumps(data, indent=2)
        self.send_response(status_code, 'application/json', json_data.encode('utf-8'))

def run_luna_web_server(port=8080):
    """Run the Luna web interface server"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, LunaWebInterface)
    
    print(f"🌙 LunaBeyond AI Web Server Starting...")
    print(f"📱 Open http://localhost:{port} to chat with Luna!")
    print(f"🧠 Integrated BHCS system with conversational AI")
    print(f"🚀 Press Ctrl+C to stop the server")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print(f"\n🛑 LunaBeyond AI Web Server stopped")
        httpd.shutdown()

if __name__ == "__main__":
    run_luna_web_server()
