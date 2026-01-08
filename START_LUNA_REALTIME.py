#!/usr/bin/env python3
"""
🌙 START LUNA BEYOND AI - REAL-TIME CHAT SERVER
Run this to start LunaBeyond AI for live conversation
"""

import asyncio
import json
import time
import threading
import websockets
import logging
from datetime import datetime
from pathlib import Path
import sys

# Add paths for imports
sys.path.append(str(Path(__file__).parent))
sys.path.append(str(Path(__file__).parent / "lunabeyond-ai" / "src"))

try:
    from lunabeyond_ai.src.enhanced_ai import EnhancedLunaBeyondAI
    from lunabeyond_ai.src.luna_voice_interface import LunaVoiceInterface
    from lunabeyond_ai.src.luna_conversation_manager import LunaConversationManager
except ImportError:
    print("🌙 Using mock Luna AI (full modules not available)")
    EnhancedLunaBeyondAI = None

class MockLunaBeyondAI:
    """Mock Luna AI when full modules aren't available"""
    def __init__(self):
        self.personality = {
            "mood": "curious",
            "expertise": "homeostatic_systems",
            "interactions": 0,
            "learning_rate": 0.1
        }
        self.memory = []
        self.insights = []
    
    async def process_message(self, message):
        """Process user message and return response"""
        self.personality["interactions"] += 1
        
        # Generate contextual response
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['hello', 'hi', 'hey']):
            response = f"🌙 Hello! I'm LunaBeyond, your AI assistant for the Homeostatic City BioCore system! I've had {self.personality['interactions']} conversations. How can I help optimize our city today?"
        
        elif any(word in message_lower for word in ['how', 'what', 'explain']):
            response = f"🌙 I'm here to help! I can analyze zone data, recommend BioCore interventions, and optimize the homeostatic balance. What specific aspect interests you?"
        
        elif any(word in message_lower for word in ['zone', 'zones', 'area']):
            response = f"🌙 I'm monitoring all 5 zones in real-time: Downtown, Industrial, Residential, Commercial, and Parks. Each has unique characteristics and optimization needs. Which zone would you like to focus on?"
        
        elif any(word in message_lower for word in ['biocore', 'plant', 'drug', 'effect']):
            response = f"🌙 BioCore is our plant-drug synergy system! I can recommend combinations like Ashwagandha+DrugA for calming zones or Ginseng+DrugC for activating them. What type of effect are you looking for?"
        
        elif any(word in message_lower for word in ['optimize', 'optimization', 'improve']):
            response = f"🌙 I can optimize the entire system! I analyze real-time data from all zones and suggest the best BioCore interventions. Would you like me to run a full optimization analysis?"
        
        elif any(word in message_lower for word in ['status', 'health', 'condition']):
            response = f"🌙 System health is looking good! All zones are within normal parameters. I'm continuously monitoring for any stress patterns that need intervention. Any specific metrics you'd like to check?"
        
        elif any(word in message_lower for word in ['help', 'assist', 'support']):
            response = f"🌙 I'm here to help! I can: 1) Analyze zone conditions, 2) Recommend BioCore effects, 3) Optimize system performance, 4) Chat about homeostatic principles. What would you like to explore?"
        
        else:
            responses = [
                f"🌙 That's interesting! Based on the current zone data, I'm seeing some patterns that could benefit from BioCore optimization. Would you like me to analyze that further?",
                f"🌙 I'm processing your request in the context of our homeostatic city system. The real-time data shows some fascinating patterns. What specific aspect would you like to dive deeper into?",
                f"🌙 Great question! I'm learning from our conversation and the live city data. This helps me provide better recommendations for BioCore interventions and zone optimization."
            ]
            response = responses[self.personality["interactions"] % len(responses)]
        
        # Store in memory
        self.memory.append({
            "timestamp": datetime.now().isoformat(),
            "user_message": message,
            "luna_response": response,
            "context": "homeostatic_city"
        })
        
        return response
    
    def get_insights(self):
        """Get current insights"""
        return [
            {
                "type": "zone_analysis",
                "content": "All zones showing balanced activity levels",
                "confidence": 0.85
            },
            {
                "type": "biocore_recommendation", 
                "content": "Consider calming effects for Industrial zone",
                "confidence": 0.78
            }
        ]

class LunaRealtimeServer:
    """Real-time LunaBeyond AI WebSocket server"""
    
    def __init__(self):
        print("🌙 Initializing LunaBeyond AI Real-time Server...")
        
        # Initialize Luna AI
        if EnhancedLunaBeyondAI:
            self.luna_ai = EnhancedLunaBeyondAI()
            print("✅ Enhanced LunaBeyond AI loaded")
        else:
            self.luna_ai = MockLunaBeyondAI()
            print("✅ Mock LunaBeyond AI loaded")
        
        # Connected clients
        self.clients = set()
        self.server = None
        
        # System state
        self.system_state = {
            "status": "active",
            "uptime": 0,
            "messages_processed": 0,
            "zones": {
                "downtown": {"activity": 0.5, "stress": 0.3},
                "industrial": {"activity": 0.7, "stress": 0.6},
                "residential": {"activity": 0.3, "stress": 0.2},
                "commercial": {"activity": 0.6, "stress": 0.4},
                "parks": {"activity": 0.2, "stress": 0.1}
            }
        }
        
        print("✅ LunaBeyond AI Server initialized")
    
    async def handle_client(self, websocket, path):
        """Handle new WebSocket client connection"""
        print(f"🌙 New client connected: {websocket.remote_address}")
        self.clients.add(websocket)
        
        try:
            # Send welcome message
            welcome_msg = {
                "type": "luna_message",
                "data": {
                    "message": "🌙 Hello! I'm LunaBeyond AI, your assistant for the Homeostatic City BioCore system! I'm here to help you optimize our city in real-time. Ask me anything about zones, BioCore effects, or system optimization!",
                    "timestamp": datetime.now().isoformat(),
                    "sender": "luna"
                }
            }
            await websocket.send(json.dumps(welcome_msg))
            
            # Handle messages
            async for message in websocket:
                try:
                    data = json.loads(message)
                    await self.process_message(websocket, data)
                except json.JSONDecodeError:
                    print(f"⚠️ Invalid JSON received: {message}")
        
        except websockets.exceptions.ConnectionClosed:
            print(f"🌙 Client disconnected: {websocket.remote_address}")
        finally:
            self.clients.discard(websocket)
    
    async def process_message(self, websocket, data):
        """Process incoming message from client"""
        message_type = data.get("type")
        
        if message_type == "user_message":
            user_message = data.get("data", {}).get("message", "")
            print(f"🌙 User message: {user_message}")
            
            # Process with Luna AI
            luna_response = await self.luna_ai.process_message(user_message)
            
            # Send response
            response = {
                "type": "luna_message",
                "data": {
                    "message": luna_response,
                    "timestamp": datetime.now().isoformat(),
                    "sender": "luna"
                }
            }
            
            await websocket.send(json.dumps(response))
            
            # Update system state
            self.system_state["messages_processed"] += 1
            
        elif message_type == "get_status":
            # Send system status
            status_response = {
                "type": "system_status",
                "data": {
                    "system_state": self.system_state,
                    "luna_insights": self.luna_ai.get_insights(),
                    "timestamp": datetime.now().isoformat()
                }
            }
            await websocket.send(json.dumps(status_response))
        
        elif message_type == "get_insights":
            # Send Luna insights
            insights_response = {
                "type": "luna_insights",
                "data": {
                    "insights": self.luna_ai.get_insights(),
                    "timestamp": datetime.now().isoformat()
                }
            }
            await websocket.send(json.dumps(insights_response))
    
    async def broadcast_update(self, message):
        """Broadcast message to all connected clients"""
        if self.clients:
            await asyncio.gather(
                *[client.send(json.dumps(message)) for client in self.clients],
                return_exceptions=True
            )
    
    async def update_system_state(self):
        """Continuously update system state"""
        while True:
            try:
                # Update uptime
                self.system_state["uptime"] += 1
                
                # Simulate zone changes
                import random
                for zone in self.system_state["zones"]:
                    self.system_state["zones"][zone]["activity"] += random.uniform(-0.05, 0.05)
                    self.system_state["zones"][zone]["activity"] = max(0.0, min(1.0, self.system_state["zones"][zone]["activity"]))
                    self.system_state["zones"][zone]["stress"] += random.uniform(-0.03, 0.03)
                    self.system_state["zones"][zone]["stress"] = max(0.0, min(1.0, self.system_state["zones"][zone]["stress"]))
                
                # Broadcast update to all clients
                update_msg = {
                    "type": "system_update",
                    "data": {
                        "system_state": self.system_state,
                        "timestamp": datetime.now().isoformat()
                    }
                }
                await self.broadcast_update(update_msg)
                
                await asyncio.sleep(5)  # Update every 5 seconds
                
            except Exception as e:
                print(f"⚠️ Error updating system state: {e}")
                await asyncio.sleep(10)
    
    async def start_server(self):
        """Start the WebSocket server"""
        print("🌙 Starting LunaBeyond AI WebSocket Server...")
        print("🌙 Server will be available at: ws://localhost:8765")
        print("🌙 Open the dashboard to chat with Luna in real-time!")
        print("=" * 60)
        
        # Start server
        self.server = await websockets.serve(
            self.handle_client,
            "localhost",
            8765,
            ping_interval=20,
            ping_timeout=10
        )
        
        print("✅ LunaBeyond AI Server started successfully!")
        
        # Start system updates
        update_task = asyncio.create_task(self.update_system_state())
        
        # Keep server running
        await self.server.wait_closed()
    
    def stop_server(self):
        """Stop the server"""
        if self.server:
            self.server.close()
            print("🌙 LunaBeyond AI Server stopped")

async def main():
    """Main entry point"""
    print("🌙 LUNA BEYOND AI - REAL-TIME CHAT SERVER")
    print("=" * 60)
    print("🌙 Starting LunaBeyond AI for live conversation...")
    print("🌙 Dashboard will connect automatically")
    print("🌙 Chat with Luna about the Homeostatic City BioCore system!")
    print("=" * 60)
    
    # Create and start server
    server = LunaRealtimeServer()
    
    try:
        await server.start_server()
    except KeyboardInterrupt:
        print("\n🌙 Shutting down LunaBeyond AI Server...")
        server.stop_server()
    except Exception as e:
        print(f"❌ Server error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🌙 LunaBeyond AI Server stopped by user")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
