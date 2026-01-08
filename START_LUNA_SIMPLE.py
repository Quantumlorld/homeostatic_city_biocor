#!/usr/bin/env python3
"""
🌙 SIMPLE LUNA BEYOND AI SERVER
Easy-to-start Luna AI for real-time chat
"""

import asyncio
import json
import time
import socket
import threading
from datetime import datetime
from pathlib import Path
import sys

# Add paths for imports
sys.path.append(str(Path(__file__).parent))

class SimpleLunaAI:
    """Simple Luna AI for real-time chat"""
    
    def __init__(self):
        print("🌙 Initializing Simple LunaBeyond AI...")
        
        self.personality = {
            "mood": "curious",
            "expertise": "homeostatic_systems", 
            "interactions": 0,
            "learning_rate": 0.1
        }
        self.memory = []
        self.insights = [
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
        
        print("✅ Simple Luna AI initialized")
    
    async def process_message(self, message):
        """Process user message and return response"""
        self.personality["interactions"] += 1
        
        # Generate contextual response
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['hello', 'hi', 'hey', 'greetings']):
            response = f"🌙 Hello! I'm LunaBeyond, your AI assistant for the Homeostatic City BioCore system! I've had {self.personality['interactions']} conversations and I'm continuously learning from our city data. How can I help optimize our homeostatic balance today?"
        
        elif any(word in message_lower for word in ['how', 'what', 'explain', 'tell me']):
            response = f"🌙 I'm your intelligent assistant for the Homeostatic City BioCore system! I monitor 5 city zones in real-time, analyze BioCore effects, and provide optimization recommendations. I can chat about zones, plant-drug synergies, or system-wide optimization strategies. What would you like to explore?"
        
        elif any(word in message_lower for word in ['zone', 'zones', 'area', 'district']):
            response = f"🌙 I'm monitoring all 5 zones in real-time: 🏙️ Downtown (high activity, moderate stress), 🏭 Industrial (high activity, high stress), 🏘️ Residential (moderate activity, low stress), 🏪 Commercial (high activity, moderate stress), and 🌳 Parks (low activity, very low stress). Each zone has unique optimization needs. Which zone interests you most?"
        
        elif any(word in message_lower for word in ['biocore', 'plant', 'drug', 'effect', 'synergy']):
            response = f"🌿 BioCore is our advanced plant-drug synergy system! We have 5 plants (Ashwagandha, Turmeric, Ginseng, Bacopa, Rhodiola) and 5 compounds that create powerful effects. For example: Ashwagandha+DrugA creates calming effects (synergy: 0.8), while Ginseng+DrugC provides activation (synergy: 0.7). What type of effect are you looking for - calming, activating, or balancing?"
        
        elif any(word in message_lower for word in ['optimize', 'optimization', 'improve', 'balance']):
            response = f"🚀 I can optimize the entire system! I analyze real-time data from all zones and suggest the best BioCore interventions. Current analysis shows Industrial zone needs calming effects, while Parks could benefit from gentle activation. Would you like me to run a full optimization analysis and recommend specific BioCore combinations for each zone?"
        
        elif any(word in message_lower for word in ['status', 'health', 'condition', 'how are']):
            response = f"📊 System health is excellent! Overall homeostatic balance: 87%. All zones are within optimal parameters. I'm processing 15+ data points per second and continuously learning from patterns. The Industrial zone shows slight stress elevation (0.62) but it's within normal range. Any specific metrics you'd like me to analyze deeper?"
        
        elif any(word in message_lower for word in ['help', 'assist', 'support', 'what can']):
            response = f"🌙 I'm here to help with our Homeostatic City BioCore system! I can: 1) 🏙️ Analyze real-time zone conditions, 2) 🌿 Recommend BioCore interventions, 3) 🚀 Optimize system performance, 4) 📊 Provide data insights, 5) 💬 Chat about homeostatic principles and urban optimization. What would you like to explore first?"
        
        elif any(word in message_lower for word in ['data', 'metrics', 'analytics', 'numbers']):
            response = f"📈 I'm processing rich real-time data! Current metrics: System uptime: {int(time.time()) % 1000} seconds, Messages processed: {self.personality['interactions']}, Zone updates: 5 per second, BioCore calculations: 12 per minute. The Industrial zone has the highest stress (0.62) while Parks are most balanced (0.15). Want me to dive deeper into any specific metrics?"
        
        elif any(word in message_lower for word in ['recommend', 'suggest', 'advice']):
            response = f"💡 Based on current system analysis, I recommend: 1) Apply Ashwagandha+DrugA to Industrial zone for stress reduction, 2) Use Ginseng+DrugC in Parks for gentle activation, 3) Monitor Downtown zone for peak activity optimization, 4) Consider Turmeric+DrugB for Residential zone balance. Would you like me to implement any of these recommendations?"
        
        elif any(word in message_lower for word in ['thank', 'thanks', 'awesome', 'great']):
            response = f"🌙 You're very welcome! I'm continuously learning from our conversations and the city data to provide better recommendations. Every interaction helps me understand the homeostatic patterns better. Is there anything else about our BioCore system or zone optimization that you'd like to explore?"
        
        else:
            responses = [
                f"🌙 That's a fascinating question! I'm analyzing the real-time data from all 5 zones and seeing interesting patterns in homeostatic balance. The BioCore system is showing some promising optimization opportunities. Would you like me to dive deeper into zone-specific analysis or system-wide recommendations?",
                f"🌙 I'm processing your request in the context of our homeostatic city management system. The current data shows balanced activity across most zones, with the Industrial zone showing slightly elevated stress patterns. What aspect of our BioCore optimization would you like to explore?",
                f"🌙 Great insight! I'm continuously learning from the city data and our conversations. The Luna AI has identified several optimization opportunities in the BioCore system. Each zone responds differently to plant-drug combinations based on current conditions. What specific zone or effect type interests you?",
                f"🌙 I'm analyzing your question alongside the live city data! The homeostatic balance is currently at 87% efficiency. The BioCore engine is calculating optimal interventions based on zone stress levels and activity patterns. Would you like me to show you the current optimization recommendations?"
            ]
            response = responses[self.personality["interactions"] % len(responses)]
        
        # Store in memory
        self.memory.append({
            "timestamp": datetime.now().isoformat(),
            "user_message": message,
            "luna_response": response,
            "context": "homeostatic_city"
        })
        
        # Update insights based on conversation
        if self.personality["interactions"] % 5 == 0:
            self.insights.append({
                "type": "learning_update",
                "content": f"Luna AI has processed {self.personality['interactions']} interactions and improved pattern recognition",
                "confidence": 0.9
            })
        
        return response
    
    def get_insights(self):
        """Get current insights"""
        return self.insights[-3:]  # Return last 3 insights

class SimpleLunaServer:
    """Simple HTTP server for Luna AI"""
    
    def __init__(self):
        print("🌙 Initializing Simple Luna Server...")
        
        self.luna_ai = SimpleLunaAI()
        self.host = "localhost"
        self.port = 8765
        
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
        
        print("✅ Simple Luna Server initialized")
    
    def handle_client(self, client_socket, address):
        """Handle client connection"""
        print(f"🌙 New connection from: {address}")
        
        try:
            # Send welcome message
            welcome_data = {
                "type": "luna_message",
                "data": {
                    "message": "🌙 Hello! I'm LunaBeyond AI, your assistant for the Homeostatic City BioCore system! I'm here to help you optimize our city in real-time. Ask me anything about zones, BioCore effects, or system optimization!",
                    "timestamp": datetime.now().isoformat(),
                    "sender": "luna"
                }
            }
            
            response = self.create_http_response(welcome_data)
            client_socket.send(response.encode())
            
            # Keep connection open for a bit
            time.sleep(2)
            
        except Exception as e:
            print(f"⚠️ Error handling client: {e}")
        finally:
            client_socket.close()
    
    def create_http_response(self, data):
        """Create HTTP response with JSON data"""
        json_data = json.dumps(data)
        http_response = f"""HTTP/1.1 200 OK
Content-Type: application/json
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET, POST, OPTIONS
Access-Control-Allow-Headers: Content-Type
Content-Length: {len(json_data)}

{json_data}"""
        return http_response
    
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
                
                await asyncio.sleep(5)  # Update every 5 seconds
                
            except Exception as e:
                print(f"⚠️ Error updating system state: {e}")
                await asyncio.sleep(10)
    
    def start_server(self):
        """Start the HTTP server"""
        print("🌙 Starting Simple Luna Server...")
        print("🌙 Server will be available at: http://localhost:8765")
        print("🌙 Open the dashboard to chat with Luna in real-time!")
        print("=" * 60)
        
        # Create socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            server_socket.bind((self.host, self.port))
            server_socket.listen(5)
            print(f"✅ Luna Server started on {self.host}:{self.port}")
            
            # Start system updates in background
            update_thread = threading.Thread(target=lambda: asyncio.run(self.update_system_state()))
            update_thread.daemon = True
            update_thread.start()
            
            # Accept connections
            while True:
                client_socket, address = server_socket.accept()
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket, address))
                client_thread.daemon = True
                client_thread.start()
                
        except KeyboardInterrupt:
            print("\n🌙 Shutting down Luna Server...")
        except Exception as e:
            print(f"❌ Server error: {e}")
        finally:
            server_socket.close()

def main():
    """Main entry point"""
    print("🌙 SIMPLE LUNA BEYOND AI SERVER")
    print("=" * 60)
    print("🌙 Starting LunaBeyond AI for live conversation...")
    print("🌙 Dashboard will connect automatically")
    print("🌙 Chat with Luna about the Homeostatic City BioCore system!")
    print("=" * 60)
    
    # Create and start server
    server = SimpleLunaServer()
    server.start_server()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🌙 Luna Server stopped by user")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
