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
from urllib.parse import urlparse

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
        parsed_path = urlparse(self.path).path
        if parsed_path == '/':
            self.serve_dashboard()
        elif parsed_path == '/api/status':
            self.serve_api_status()
        elif parsed_path.startswith('/api/'):
            self.serve_api_response()
        else:
            self.send_error(404)
    
    def do_POST(self):
        """Handle POST requests"""
        parsed_path = urlparse(self.path).path
        if parsed_path == '/api/chat':
            self.handle_chat_request()
        elif parsed_path == '/api/command':
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

        /* Header */
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

        /* Main Grid Layout */
        .main-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            margin-bottom: 40px;
        }

        /* Left Column - System Overview */
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

        /* Zones Grid */
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

        .state-emergent {
            background: rgba(245, 101, 101, 0.2);
            color: #f56565;
            border: 1px solid rgba(245, 101, 101, 0.3);
        }

        .state-critical {
            background: rgba(159, 122, 234, 0.2);
            color: #9f7aea;
            border: 1px solid rgba(159, 122, 234, 0.3);
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

        /* Right Column - Luna AI Chat */
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

        /* Control Panel */
        .control-panel {
            background: rgba(45, 55, 72, 0.5);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(66, 153, 225, 0.2);
            border-radius: 16px;
            padding: 20px;
        }

        .control-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 12px;
        }

        .control-group {
            display: flex;
            flex-direction: column;
            gap: 6px;
        }

        .control-label {
            color: #a0aec0;
            font-size: 0.875rem;
            font-weight: 500;
            margin-bottom: 4px;
        }

        .control-input {
            padding: 8px 12px;
            background: rgba(26, 32, 44, 0.8);
            border: 1px solid rgba(66, 153, 225, 0.3);
            border-radius: 6px;
            color: #e2e8f0;
            font-size: 0.875rem;
            transition: all 0.2s ease;
        }

        .control-input:focus {
            outline: none;
            border-color: #4299e1;
            box-shadow: 0 0 0 3px rgba(66, 153, 225, 0.1);
        }

        .apply-btn {
            padding: 10px 20px;
            background: linear-gradient(135deg, #4299e1, #667eea);
            color: white;
            border: none;
            border-radius: 6px;
            font-weight: 600;
            font-size: 0.875rem;
            cursor: pointer;
            transition: all 0.2s ease;
        }

        .apply-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(66, 153, 225, 0.3);
        }

        /* Responsive */
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
        <!-- Header -->
        <header class="header">
            <h1>🦀🌙 BHCS + Luna AI</h1>
            <div class="subtitle">Homeostatic City BioCore with Conversational AI</div>
            <div class="status-indicator">
                <div class="status-dot"></div>
                <span>System Online</span>
            </div>
        </header>

        <!-- Main Grid -->
        <div class="main-grid">
            <!-- Left Column - System Overview -->
            <div class="system-section">
                <!-- System Metrics -->
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

                <!-- Zones Section -->
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

                <!-- Control Panel -->
                <div class="control-panel">
                    <div class="section-header">
                        <h3 class="section-title">🎛️ BioCore Control</h3>
                        <div class="status-indicator">
                            <div class="status-dot"></div>
                            <span>Ready</span>
                        </div>
                    </div>
                    
                    <div class="control-grid">
                        <div class="control-group">
                            <label class="control-label">Target Zone</label>
                            <select class="control-input" id="zoneSelect">
                                <option value="0">Downtown</option>
                                <option value="1">Industrial</option>
                                <option value="2">Residential</option>
                                <option value="3">Commercial</option>
                                <option value="4">Tech Park</option>
                            </select>
                        </div>
                        
                        <div class="control-group">
                            <label class="control-label">Magnitude</label>
                            <input type="range" class="control-input" id="magnitudeSlider" 
                                   min="-0.2" max="0.2" step="0.01" value="0">
                        </div>
                        
                        <div class="control-group">
                            <label class="control-label">Synergy</label>
                            <input type="range" class="control-input" id="synergySlider" 
                                   min="0.0" max="1.0" step="0.1" value="0.5">
                        </div>
                        
                        <div class="control-group">
                            <label class="control-label">&nbsp;</label>
                            <button class="apply-btn" onclick="applyBioCore()">
                                🌿 Apply BioCore
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Right Column - Luna AI Chat -->
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
                this.connectToLunaAPI();
            }
            
            initializeDashboard() {
                console.log('🦀🌙 Initializing BHCS + Luna AI Dashboard');
                
                // Initialize zones
                this.initializeZones();
                
                // Setup event listeners
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
                // Magnitude slider
                const magnitudeSlider = document.getElementById('magnitudeSlider');
                magnitudeSlider.addEventListener('input', (e) => {
                    console.log('Magnitude:', e.target.value);
                });
                
                // Synergy slider
                const synergySlider = document.getElementById('synergySlider');
                synergySlider.addEventListener('input', (e) => {
                    console.log('Synergy:', e.target.value);
                });
            }
            
            startRealTimeUpdates() {
                // Update system metrics
                setInterval(() => {
                    this.updateSystemMetrics();
                    this.simulateZoneChanges();
                }, 3000);
            }
            
            updateSystemMetrics() {
                // Simulate metric changes
                this.systemMetrics.health += (Math.random() - 0.5) * 0.02;
                this.systemMetrics.health = Math.max(0, Math.min(1, this.systemMetrics.health));
                
                this.systemMetrics.avgActivity += (Math.random() - 0.5) * 0.01;
                this.systemMetrics.avgActivity = Math.max(0, Math.min(1, this.systemMetrics.avgActivity));
                
                this.systemMetrics.recoveryConfidence += (Math.random() - 0.5) * 0.01;
                this.systemMetrics.recoveryConfidence = Math.max(0, Math.min(1, this.systemMetrics.recoveryConfidence));
                
                // Update UI
                document.getElementById('systemHealth').textContent = `${(this.systemMetrics.health * 100).toFixed(1)}%`;
                document.getElementById('avgActivity').textContent = this.systemMetrics.avgActivity.toFixed(2);
                document.getElementById('recoveryConfidence').textContent = `${(this.systemMetrics.recoveryConfidence * 100).toFixed(0)}%`;
                document.getElementById('aiGeneration').textContent = this.systemMetrics.aiGeneration;
            }
            
            simulateZoneChanges() {
                this.zones.forEach(zone => {
                    // Simulate homeostatic regulation
                    const balanceError = zone.target - zone.activity;
                    const adjustment = 0.03 * balanceError;
                    const decay = zone.activity > zone.target ? -0.01 : 0;
                    
                    zone.activity += adjustment + decay;
                    zone.activity = Math.max(0, Math.min(1, zone.activity));
                    
                    // Update state
                    if (zone.activity < 0.3) zone.state = 'CALM';
                    else if (zone.activity < 0.6) zone.state = 'OVERSTIMULATED';
                    else if (zone.activity < 0.8) zone.state = 'EMERGENT';
                    else zone.state = 'CRITICAL';
                });
                
                this.renderZones();
            }
            
            connectToLunaAPI() {
                console.log('🌙 Connecting to Luna AI API...');
                this.lunaAPIConnected = true;
            }
            
            async sendMessage() {
                const input = document.getElementById('chatInput');
                const message = input.value.trim();
                
                if (!message) return;
                
                // Add user message
                this.addMessage(message, 'user');
                input.value = '';
                
                // Send to Luna API
                await this.sendToLunaAPI(message);
            }
            
            async sendToLunaAPI(message) {
                try {
                    console.log('🌙 Sending to Luna API:', message);
                    
                    // Connect to real Luna API
                    const response = await fetch('/api/chat', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ message: message })
                    });
                    
                    console.log('📡 Response status:', response.status);
                    console.log('📡 Response headers:', response.headers);
                    
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
            
            applyBioCore() {
                const zoneId = parseInt(document.getElementById('zoneSelect').value);
                const magnitude = parseFloat(document.getElementById('magnitudeSlider').value);
                const synergy = parseFloat(document.getElementById('synergySlider').value);
                
                const zone = this.zones[zoneId];
                if (zone) {
                    const finalMagnitude = magnitude * (0.5 + 0.5 * synergy);
                    zone.activity += finalMagnitude;
                    zone.activity = Math.max(0, Math.min(1, zone.activity));
                    
                    // Update state
                    if (zone.activity < 0.3) zone.state = 'CALM';
                    else if (zone.activity < 0.6) zone.state = 'OVERSTIMULATED';
                    else if (zone.activity < 0.8) zone.state = 'EMERGENT';
                    else zone.state = 'CRITICAL';
                    
                    this.renderZones();
                    
                    // Inform Luna
                    this.addMessage(`🌿 BioCore intervention applied to ${zone.name}: magnitude ${finalMagnitude.toFixed(3)}, synergy ${synergy.toFixed(1)}`, 'luna');
                }
            }
        }
        
        // Initialize dashboard
        document.addEventListener('DOMContentLoaded', () => {
            new BHCSLunaDashboard();
        });
    </script>
</body>
</html>
        """
        
        self._send_bytes(200, 'text/html', html_content.encode('utf-8'))

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
                <div id="connectionStatus" style="margin-bottom: 10px; font-size: 0.9rem; opacity: 0.9;">Connecting…</div>
                
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
        console.log('🚀 JavaScript loading...');
        
        // BHCS System + Luna Integration
        class IntegratedSystem {
            constructor() {
                console.log('🔧 Initializing IntegratedSystem...');
                this.zones = []; // Will be populated from server
                this.aiAccuracy = 0.85;
                this.systemHealth = 0.75;
                this.optimizationPotential = 0.40;
                this.riskProbability = 0.33;
                this.avgActivity = 0.536;
                this.generation = 1;
                
                this.initializeEventListeners();
                this.updateDisplay();
                this.startApiPolling();
                this.runSelfTest();
                console.log('✅ IntegratedSystem initialized - waiting for server data...');
            }

            setConnectionStatus(text, isError = false) {
                const el = document.getElementById('connectionStatus');
                if (!el) return;
                el.textContent = text;
                el.style.color = isError ? '#ff6b6b' : '#9ef0a6';
            }

            async runSelfTest() {
                try {
                    this.setConnectionStatus('Self-test: checking API…');

                    const statusResp = await fetch('/api/status');
                    if (!statusResp.ok) {
                        this.setConnectionStatus(`API error: /api/status → HTTP ${statusResp.status}`, true);
                        return;
                    }

                    const zonesResp = await fetch('/api/zones');
                    if (!zonesResp.ok) {
                        this.setConnectionStatus(`API error: /api/zones → HTTP ${zonesResp.status}`, true);
                        return;
                    }
                    const zonesData = await zonesResp.json();
                    if (zonesData && zonesData.zones) {
                        this.updateZonesFromServer(zonesData.zones);
                    }

                    const chatResp = await fetch('/api/chat', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ message: 'hello' })
                    });
                    if (!chatResp.ok) {
                        this.setConnectionStatus(`API error: /api/chat → HTTP ${chatResp.status}`, true);
                        return;
                    }
                    const chatData = await chatResp.json();
                    if (chatData && chatData.response) {
                        this.addChatMessage(chatData.response, 'luna');
                    }

                    this.setConnectionStatus('Connected ✅');
                } catch (e) {
                    this.setConnectionStatus(`API exception: ${e && e.message ? e.message : e}`, true);
                }
            }

            initializeEventListeners() {
                console.log('🔧 Setting up event listeners...');
                const slider = document.getElementById('synergySlider');
                const valueDisplay = document.getElementById('synergyValue');
                
                if (slider && valueDisplay) {
                    slider.addEventListener('input', (e) => {
                        valueDisplay.textContent = e.target.value;
                        console.log('📊 Synergy changed:', e.target.value);
                    });
                    console.log('✅ Event listeners setup complete');
                } else {
                    console.error('❌ Could not find slider elements');
                }
            }

            updateDisplay() {
                console.log('🔄 Updating display with zones:', this.zones.length, 'zones');
                
                // Update zones with names
                const zonesGrid = document.getElementById('zonesGrid');
                if (!zonesGrid) {
                    console.error('❌ zonesGrid element not found');
                    return;
                }
                
                zonesGrid.innerHTML = '';

                if (this.zones.length === 0) {
                    zonesGrid.innerHTML = '<div style="color: #666; text-align: center; padding: 20px;">Loading zones...</div>';
                    console.log('⏳ Showing loading message');
                    return;
                }

                this.zones.forEach(zone => {
                    const zoneCard = document.createElement('div');
                    zoneCard.className = 'zone-card';
                    zoneCard.innerHTML = `
                        <div class="zone-id">${zone.name || 'Zone ' + zone.id}</div>
                        <div class="zone-state state-${zone.state.toLowerCase()}">${zone.state}</div>
                        <div class="zone-activity">${zone.activity.toFixed(3)}</div>
                    `;
                    zonesGrid.appendChild(zoneCard);
                    console.log(`📍 Added zone: ${zone.name || zone.id} - ${zone.state}`);
                });

                // Update metrics
                const systemHealthEl = document.getElementById('systemHealth');
                const avgActivityEl = document.getElementById('avgActivity');
                const riskLevelEl = document.getElementById('riskLevel');
                
                if (systemHealthEl) systemHealthEl.textContent = `${(this.calculateSystemHealth() * 100).toFixed(0)}%`;
                if (avgActivityEl) avgActivityEl.textContent = this.calculateAvgActivity().toFixed(3);
                if (riskLevelEl) riskLevelEl.textContent = this.calculateRiskLevel();
                
                console.log('🔄 Display updated - zones:', this.zones.map(z => `${z.name || z.id}: ${z.state} (${z.activity.toFixed(3)})`));
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
                console.log('🔄 Starting API polling...');
                
                // Poll for AI status updates
                setInterval(async () => {
                    try {
                        const response = await fetch('/api/status');
                        if (response.ok) {
                            const data = await response.json();
                            console.log('📊 Status update:', data);
                            
                            if (data.ai_accuracy) {
                                document.getElementById('aiAccuracy').textContent = `${(data.ai_accuracy * 100).toFixed(0)}%`;
                            }
                        } else {
                            console.log('❌ Status API error:', response.status, response.statusText);
                        }
                    } catch (error) {
                        console.log('❌ Status polling error:', error);
                    }
                }, 5000);
                
                // Poll for live zone updates every 2 seconds
                setInterval(async () => {
                    try {
                        const response = await fetch('/api/zones');
                        if (response.ok) {
                            const data = await response.json();
                            console.log('🧠 Zone update:', data.zones);
                            if (data.zones) {
                                this.updateZonesFromServer(data.zones);
                            }
                        } else {
                            console.log('❌ Zones API error:', response.status, response.statusText);
                        }
                    } catch (error) {
                        console.log('❌ Zone polling error:', error);
                    }
                }, 2000);
            }
            
            updateZonesFromServer(serverZones) {
                console.log('🔄 Updating zones from server:', serverZones.length, 'zones');
                this.zones = serverZones; // Replace entire zones array
                this.updateDisplay();
            }
            
            animateZoneStateChange(zoneId, oldState, newState) {
                const zoneCard = document.querySelector(`#zonesGrid .zone-card:nth-child(${zoneId + 1})`);
                if (zoneCard) {
                    zoneCard.style.transition = 'all 0.8s ease';
                    zoneCard.style.transform = 'scale(1.05)';
                    setTimeout(() => {
                        zoneCard.style.transform = 'scale(1)';
                    }, 800);
                }
                console.log(`🔄 Zone ${zoneId}: ${oldState} → ${newState}`);
            }
            
            animateActivityChange(zoneId, oldActivity, newActivity) {
                const zoneCard = document.querySelector(`#zonesGrid .zone-card:nth-child(${zoneId + 1})`);
                if (zoneCard) {
                    const activityEl = zoneCard.querySelector('.zone-activity');
                    if (activityEl) {
                        activityEl.style.transition = 'color 0.5s ease';
                        activityEl.style.color = '#FFD700';
                        setTimeout(() => {
                            activityEl.style.color = '#FFD700';
                        }, 500);
                    }
                }
                console.log(`📈 Zone ${zoneId} activity: ${oldActivity.toFixed(3)} → ${newActivity.toFixed(3)}`);
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
                console.log('📤 Sending chat message:', message);
                
                // Add user message to chat
                this.addChatMessage(message, 'user');
                
                // Clear input
                const input = document.getElementById('chatInput');
                if (input) {
                    input.value = '';
                }
                
                try {
                    const response = await fetch('/api/chat', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ message: message })
                    });
                    
                    if (!response.ok) {
                        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                    }
                    
                    const data = await response.json();
                    console.log('📥 Received:', data);
                    this.addChatMessage(data.response, 'luna');
                } catch (error) {
                    console.error('❌ Chat error:', error);
                    this.addChatMessage(`❌ Error: ${error.message}`, 'luna');
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
        
        self._send_bytes(200, 'text/html', html_content.encode('utf-8'))

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
        parsed_path = urlparse(self.path).path
        if parsed_path == '/api/zones':
            zones_data = []
            zone_names = ['Downtown Residential', 'Industrial District', 'Commercial Hub', 'Tech Park', 'Medical Zone']
            for i, zone in enumerate(self.luna.bhcs.zones):
                zones_data.append({
                    'id': zone.id,
                    'name': zone_names[i] if i < len(zone_names) else f'Zone {zone.id}',
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
            
            # Simple response for now to avoid async issues
            if message.strip().startswith('/'):
                if message.strip() == '/status':
                    response = "📊 SYSTEM STATUS:\n   Health: 20.0%\n   Average Activity: 0.593\n   Risk Probability: 36.3%\n🧠 AI INSIGHTS:\n   I predict the system health will be 100.0% in the next hour."
                elif message.strip() == '/evolve':
                    response = "🌙 I've evolved to Generation 2! My neural networks have mutated and adapted."
                elif message.strip() == '/learn':
                    response = "📚 Not enough data for learning yet. Let's chat more!"
                elif message.strip() == '/zones':
                    zones_info = []
                    zone_names = ['Downtown Residential', 'Industrial District', 'Commercial Hub', 'Tech Park', 'Medical Zone']
                    for i, zone in enumerate(self.luna.bhcs.zones):
                        zones_info.append(f"{zone_names[i]}: {zone.state} ({zone.activity:.3f})")
                    response = "🧠 ZONE STATUS:\n" + "\n".join(zones_info)
                else:
                    response = "💡 Available commands: /status, /zones, /ai, /predict, /learn, /evolve"
            else:
                # Simple conversational response
                responses = [
                    "🌙 Hello! I'm LunaBeyond, your AI companion. I'm here to help you understand and optimize the BHCS system.",
                    "🧠 I'm monitoring the system behavior and learning from our interactions.",
                    "📊 The system appears to be functioning normally. How can I assist you today?",
                    "🌿 I'm ready to help you explore the BioCore interventions and zone optimizations."
                ]
                import random
                response = random.choice(responses)
            
            self.send_json_response(200, {'response': response})
                
        except Exception as e:
            print(f"Chat error: {e}")
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

    def _send_bytes(self, status_code: int, content_type: str, content: bytes):
        super().send_response(status_code)
        self.send_header('Content-type', content_type)
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        self.send_header('Content-Length', str(len(content)))
        self.end_headers()
        self.wfile.write(content)
    
    def send_json_response(self, status_code, data):
        """Send JSON response"""
        json_data = json.dumps(data, indent=2).encode('utf-8')
        self._send_bytes(status_code, 'application/json', json_data)

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
    port = 8080
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            port = 8080
    run_luna_web_server(port)
