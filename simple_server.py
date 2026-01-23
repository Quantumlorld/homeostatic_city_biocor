#!/usr/bin/env python3
"""
🚀 Simple Backend Server for Homeostatic City BioCore Dashboard
FastAPI server with WebSocket support for real-time updates
Enhanced with AI-powered BioCore prediction system
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import json
import asyncio
import time
import random
from typing import List, Dict, Any
import logging
from simple_biocore_ai import SimpleBioCoreAI
from iot_sensor_network import sensor_network, start_sensor_monitoring
from neural_interface import neural_interface, start_neural_monitoring
from global_network import global_network, start_global_network_monitoring
from simple_transcendent_evolution import simple_transcendent_evolution

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(
    title="Homeostatic City BioCore API",
    description="Backend API for the futuristic dashboard",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state
class CityState:
    def __init__(self):
        self.zones = [
            {"name": "Downtown", "activity": 0.3, "state": "calm", "zone_type": "downtown"},
            {"name": "Industrial", "activity": 0.7, "state": "overstimulated", "zone_type": "industrial"},
            {"name": "Residential", "activity": 0.2, "state": "calm", "zone_type": "residential"},
            {"name": "Commercial", "activity": 0.5, "state": "calm", "zone_type": "downtown"},
            {"name": "Tech District", "activity": 0.8, "state": "overstimulated", "zone_type": "tech"},
            {"name": "Medical Center", "activity": 0.4, "state": "calm", "zone_type": "medical"},
            {"name": "Educational", "activity": 0.6, "state": "overstimulated", "zone_type": "residential"},
            {"name": "Recreational", "activity": 0.1, "state": "calm", "zone_type": "residential"}
        ]
        self.connections: List[WebSocket] = []
        self.running = True
        self.ai_predictor = SimpleBioCoreAI()
        self.sensor_network = sensor_network
        self.neural_interface = neural_interface
        self.global_network = global_network
        self.transcendent_evolution = simple_transcendent_evolution

city_state = CityState()

def update_zone_state(zone):
    """Update zone state based on activity level"""
    if zone["activity"] < 0.3:
        zone["state"] = "calm"
    elif zone["activity"] < 0.7:
        zone["state"] = "overstimulated"
    else:
        zone["state"] = "emergent"

# API Endpoints
@app.get("/")
async def root():
    """Serve the dashboard"""
    try:
        with open("dashboard/futuristic_dashboard.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return {"message": "Dashboard file not found"}

@app.get("/api/zones")
async def get_zones():
    """Get current city zones state"""
    return {"zones": city_state.zones}

@app.get("/api/stats")
async def get_stats():
    """Get city statistics"""
    zones = city_state.zones
    avg_activity = sum(zone["activity"] for zone in zones) / len(zones)
    calm_zones = sum(1 for zone in zones if zone["state"] == "calm")
    active_zones = sum(1 for zone in zones if zone["state"] == "overstimulated")
    emergent_zones = sum(1 for zone in zones if zone["state"] == "emergent")
    
    return {
        "avg_activity": avg_activity,
        "calm_zones": calm_zones,
        "active_zones": active_zones,
        "emergent_zones": emergent_zones
    }

@app.post("/api/biocore")
async def apply_biocore_effect(data: Dict[str, Any]):
    """Apply BioCore effect to a zone"""
    try:
        zone_index = data.get("zone")
        plant = data.get("plant")
        drug = data.get("drug")
        synergy = data.get("synergy", 0.5)
        
        if zone_index is None or zone_index < 0 or zone_index >= len(city_state.zones):
            return {"success": False, "message": "Invalid zone"}
        
        zone = city_state.zones[zone_index]
        
        # Calculate effect based on synergy
        effect = (synergy * 0.3) - 0.15
        zone["activity"] = max(0, min(1, zone["activity"] + effect))
        update_zone_state(zone)
        
        # Broadcast update to all connected clients
        await broadcast_update()
        
        return {
            "success": True,
            "message": f"Applied {plant} + {drug} to {zone['name']}",
            "zone": zone
        }
    
    except Exception as e:
        logger.error(f"Error applying BioCore effect: {e}")
        return {"success": False, "message": str(e)}

@app.post("/api/emergency-reset")
async def emergency_reset():
    """Emergency reset all zones to baseline"""
    for zone in city_state.zones:
        zone["activity"] = 0.3
        zone["state"] = "calm"
    
    await broadcast_update()
    return {"success": True, "message": "Emergency reset completed"}

@app.get("/api/ai-predict/{zone_index}")
async def ai_predict_optimal(zone_index: int):
    """AI prediction for optimal BioCore combination for a zone"""
    try:
        if zone_index < 0 or zone_index >= len(city_state.zones):
            return {"success": False, "message": "Invalid zone"}
        
        zone = city_state.zones[zone_index]
        zone_type = zone["zone_type"]
        
        # Check if AI models are trained
        if not hasattr(city_state.ai_predictor, 'plants'):
            return {"success": False, "message": "AI system not initialized. Please try again."}
        
        # Get AI prediction
        optimal = city_state.ai_predictor.predict_optimal_combination(zone_type)
        
        if not optimal:
            return {"success": False, "message": "Failed to generate AI prediction"}
        
        return {
            "success": True,
            "zone": zone["name"],
            "zone_type": zone_type,
            "optimal_combination": optimal,
            "top_combinations": city_state.ai_predictor.get_top_combinations(zone_type, 5)
        }
    
    except Exception as e:
        logger.error(f"AI prediction error: {e}")
        return {"success": False, "message": f"AI prediction failed: {str(e)}"}

@app.get("/api/ai-train")
async def train_ai_models():
    """Train or retrain AI models"""
    try:
        # Train models
        city_state.ai_predictor.train_models()
        city_state.ai_predictor.save_models()
        
        return {
            "success": True,
            "message": "AI models trained successfully",
            "models_available": list(city_state.ai_predictor.trained_models.keys())
        }
    
    except Exception as e:
        logger.error(f"AI training error: {e}")
        return {"success": False, "message": str(e)}

@app.get("/api/iot/sensors")
async def get_iot_sensors():
    """Get current IoT sensor readings for all zones"""
    try:
        readings = city_state.sensor_network.get_all_readings()
        return {
            "success": True,
            "timestamp": datetime.now().isoformat(),
            "sensors": readings
        }
    except Exception as e:
        logger.error(f"IOT sensor error: {e}")
        return {"success": False, "message": str(e)}

@app.get("/api/iot/zone/{zone_type}")
async def get_zone_iot_data(zone_type: str):
    """Get IoT sensor data for a specific zone"""
    try:
        readings = city_state.sensor_network.get_zone_readings(zone_type)
        health_score = city_state.sensor_network.get_zone_health_score(zone_type)
        
        return {
            "success": True,
            "zone": zone_type,
            "health_score": health_score,
            "readings": readings,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Zone IoT data error: {e}")
        return {"success": False, "message": str(e)}

@app.get("/api/iot/alerts")
async def get_iot_alerts():
    """Get recent IoT alerts"""
    try:
        alerts = city_state.sensor_network.get_recent_alerts(20)
        return {
            "success": True,
            "alerts": alerts,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"IOT alerts error: {e}")
        return {"success": False, "message": str(e)}

@app.get("/api/smart-city/overview")
async def get_smart_city_overview():
    """Get comprehensive smart city overview"""
    try:
        overview = {
            "zones": {},
            "total_alerts": len(city_state.sensor_network.alerts),
            "critical_alerts": len([a for a in city_state.sensor_network.alerts if a.get('severity') == 'critical']),
            "timestamp": datetime.now().isoformat()
        }
        
        for zone in city_state.zones:
            zone_type = zone["zone_type"]
            iot_data = city_state.sensor_network.get_zone_readings(zone_type)
            health_score = city_state.sensor_network.get_zone_health_score(zone_type)
            
            overview["zones"][zone["name"]] = {
                "zone_type": zone_type,
                "activity": zone["activity"],
                "state": zone["state"],
                "health_score": health_score,
                "air_quality": iot_data.get("air_quality", {}),
                "noise_level": iot_data.get("noise_pollution", {}).get("decibels", 0),
                "traffic_congestion": iot_data.get("traffic_flow", {}).get("congestion", 0),
                "stress_level": iot_data.get("biometric", {}).get("stress_level", 0)
            }
        
        return {
            "success": True,
            "overview": overview
        }
    except Exception as e:
        logger.error(f"Smart city overview error: {e}")
        return {"success": False, "message": str(e)}

@app.get("/api/neural/metrics")
async def get_neural_metrics():
    """Get neural interface metrics"""
    try:
        metrics = city_state.neural_interface.get_neural_metrics()
        return {
            "success": True,
            "neural_metrics": metrics,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Neural metrics error: {e}")
        return {"success": False, "message": str(e)}

@app.get("/api/neural/connected-minds")
async def get_connected_minds():
    """Get information about connected minds"""
    try:
        minds = city_state.neural_interface.connected_minds
        return {
            "success": True,
            "connected_minds": minds,
            "total_connected": len(minds),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Connected minds error: {e}")
        return {"success": False, "message": str(e)}

@app.post("/api/neural/connect-mind")
async def connect_mind(data: Dict[str, Any]):
    """Connect a new mind to the collective consciousness"""
    try:
        mind_id = data.get('mind_id')
        name = data.get('name')
        neural_signature = data.get('neural_signature')
        
        if not all([mind_id, name, neural_signature]):
            return {"success": False, "message": "Missing required fields"}
        
        mind = city_state.neural_interface.connect_mind(mind_id, name, neural_signature)
        
        return {
            "success": True,
            "message": f"Mind '{name}' connected successfully",
            "mind": mind
        }
    except Exception as e:
        logger.error(f"Connect mind error: {e}")
        return {"success": False, "message": str(e)}

@app.get("/api/neural/consciousness-events")
async def get_consciousness_events():
    """Get recent consciousness events"""
    try:
        events = city_state.neural_interface.consciousness_events[-10:]
        return {
            "success": True,
            "events": events,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Consciousness events error: {e}")
        return {"success": False, "message": str(e)}

@app.get("/api/global/network-status")
async def get_global_network_status():
    """Get global network status"""
    try:
        status = city_state.global_network.get_global_network_status()
        return {
            "success": True,
            "global_status": status,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Global network status error: {e}")
        return {"success": False, "message": str(e)}

@app.get("/api/global/connected-cities")
async def get_connected_cities():
    """Get information about connected cities"""
    try:
        cities = city_state.global_network.connected_cities
        return {
            "success": True,
            "connected_cities": cities,
            "total_cities": len(cities),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Connected cities error: {e}")
        return {"success": False, "message": str(e)}

@app.post("/api/global/connect-city")
async def connect_city(data: Dict[str, Any]):
    """Connect a new city to the global network"""
    try:
        city_id = data.get('city_id')
        city_template = data.get('city_template')
        
        if not all([city_id, city_template]):
            return {"success": False, "message": "Missing required fields"}
        
        city = city_state.global_network.connect_city(city_id, city_template)
        
        if not city:
            return {"success": False, "message": "Invalid city template"}
        
        return {
            "success": True,
            "message": f"City '{city['name']}' connected to global network",
            "city": city
        }
    except Exception as e:
        logger.error(f"Connect city error: {e}")
        return {"success": False, "message": str(e)}

@app.get("/api/global/events")
async def get_global_events():
    """Get recent global events"""
    try:
        events = city_state.global_network.global_events[-10:]
        return {
            "success": True,
            "events": events,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Global events error: {e}")
        return {"success": False, "message": str(e)}

@app.get("/api/transcendent/status")
async def get_transcendent_status():
    """Get transcendent evolution status"""
    try:
        status = city_state.transcendent_evolution.get_transcendent_status()
        return {
            "success": True,
            "transcendent_status": status,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Transcendent status error: {e}")
        return {"success": False, "message": str(e)}

@app.get("/api/transcendent/uploaded-consciousness")
async def get_uploaded_consciousness():
    """Get uploaded consciousness information"""
    try:
        consciousness = city_state.transcendent_evolution.uploaded_consciousness
        return {
            "success": True,
            "uploaded_consciousness": consciousness,
            "total_uploaded": len(consciousness),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Uploaded consciousness error: {e}")
        return {"success": False, "message": str(e)}

@app.post("/api/transcendent/upload-consciousness")
async def upload_consciousness(data: Dict[str, Any]):
    """Upload a new consciousness to the transcendent system"""
    try:
        consciousness_id = data.get('consciousness_id')
        name = data.get('name')
        essence = data.get('essence')
        complexity = data.get('complexity', 0.8)
        
        if not all([consciousness_id, name, essence]):
            return {"success": False, "message": "Missing required fields"}
        
        fragment = city_state.transcendent_evolution.upload_consciousness(
            consciousness_id, name, essence, complexity
        )
        
        return {
            "success": True,
            "message": f"Consciousness '{name}' uploaded successfully",
            "fragment": fragment
        }
    except Exception as e:
        logger.error(f"Upload consciousness error: {e}")
        return {"success": False, "message": str(e)}

@app.get("/api/transcendent/dimensional-layers")
async def get_dimensional_layers():
    """Get dimensional layer access information"""
    try:
        layers = city_state.transcendent_evolution.dimensional_layers
        return {
            "success": True,
            "dimensional_layers": layers,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Dimensional layers error: {e}")
        return {"success": False, "message": str(e)}

@app.get("/api/transcendent/events")
async def get_transcendent_events():
    """Get recent transcendent events"""
    try:
        events = city_state.transcendent_evolution.transcendent_events[-10:]
        return {
            "success": True,
            "transcendent_events": events,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Transcendent events error: {e}")
        return {"success": False, "message": str(e)}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates"""
    await websocket.accept()
    city_state.connections.append(websocket)
    
    try:
        # Send initial state
        await websocket.send_text(json.dumps({
            "type": "initial_state",
            "zones": city_state.zones
        }))
        
        while True:
            try:
                message = await websocket.receive_text()
                data = json.loads(message)
                
                # Handle different message types
                if data.get("type") == "ping":
                    await websocket.send_text(json.dumps({"type": "pong"}))
                elif data.get("type") == "chat":
                    # Handle chat messages
                    response = generate_ai_response(data.get("message", ""))
                    await websocket.send_text(json.dumps({
                        "type": "chat_response",
                        "message": response
                    }))
                    
            except WebSocketDisconnect:
                break
            except Exception as e:
                logger.error(f"WebSocket error: {e}")
                break
                
    except WebSocketDisconnect:
        pass
    finally:
        if websocket in city_state.connections:
            city_state.connections.remove(websocket)

async def broadcast_update():
    """Broadcast state update to all connected clients"""
    if city_state.connections:
        message = json.dumps({
            "type": "state_update",
            "zones": city_state.zones
        })
        
        # Send to all connected clients
        disconnected = []
        for connection in city_state.connections:
            try:
                await connection.send_text(message)
            except:
                disconnected.append(connection)
        
        # Remove disconnected clients
        for conn in disconnected:
            if conn in city_state.connections:
                city_state.connections.remove(conn)

def generate_ai_response(message: str) -> str:
    """Generate AI response for chat messages"""
    message_lower = message.lower()
    
    if "hello" in message_lower or "hi" in message_lower:
        return "🌟 Hello! I'm Luna, your AI assistant for Homeostatic City BioCore. How can I help optimize the city today?"
    elif "zone" in message_lower:
        return "🏙️ The city zones are currently showing varied activity levels. I recommend focusing on balancing the overstimulated areas."
    elif "biocore" in message_lower:
        return "🧬 BioCore systems are functioning optimally. The plant-drug synergy is within expected parameters."
    elif "emergency" in message_lower:
        return "🚨 Emergency protocols are ready. I can initiate a system reset if needed."
    elif "status" in message_lower or "how" in message_lower:
        return "📊 All systems are operational. The city is maintaining homeostatic balance within acceptable thresholds."
    else:
        responses = [
            "🌟 I'm analyzing the city's current state. The metrics look promising!",
            "🔬 Based on current data, the homeostatic balance is stable.",
            "📈 The urban dynamics are showing positive trends.",
            "🧪 BioCore integration is performing within expected parameters.",
            "🏙️ City systems are functioning optimally."
        ]
        return random.choice(responses)

async def simulate_city_dynamics():
    """Simulate real-time city dynamics"""
    while city_state.running:
        # Randomly update zone activities
        for zone in city_state.zones:
            change = (random.random() - 0.5) * 0.1
            zone["activity"] = max(0, min(1, zone["activity"] + change))
            update_zone_state(zone)
        
        # Broadcast updates
        await broadcast_update()
        
        # Wait before next update
        await asyncio.sleep(3)

@app.on_event("startup")
async def startup_event():
    """Start background simulation and IoT monitoring"""
    logger.info("Starting Homeostatic City BioCore server...")
    asyncio.create_task(simulate_city_dynamics())
    # Initialize AI models
    try:
        city_state.ai_predictor.train_models()
        logger.info("AI system initialized successfully")
    except Exception as e:
        logger.error(f"AI initialization error: {e}")
    # Start IoT monitoring
    try:
        asyncio.create_task(start_sensor_monitoring())
        logger.info("IoT monitoring started")
    except Exception as e:
        logger.error(f"IoT startup error: {e}")
    
    # Start neural monitoring
    try:
        asyncio.create_task(start_neural_monitoring())
        logger.info("Neural interface monitoring started")
    except Exception as e:
        logger.error(f"Neural startup error: {e}")
    
    # Start global network monitoring
    try:
        asyncio.create_task(start_global_network_monitoring())
        logger.info("Global network monitoring started")
    except Exception as e:
        logger.error(f"Global network startup error: {e}")
    
    # Start transcendent evolution
    try:
        asyncio.create_task(start_simple_transcendent_evolution())
        logger.info("Transcendent evolution monitoring started")
    except Exception as e:
        logger.error(f"Transcendent startup error: {e}")

async def start_simple_transcendent_evolution():
    """Start continuous transcendent evolution"""
    while True:
        city_state.transcendent_evolution.evolve_transcendence()
        await asyncio.sleep(15)  # Update every 15 seconds

@app.on_event("shutdown")
async def shutdown_event():
    """Clean up on shutdown"""
    city_state.running = False
    logger.info("Server shutting down...")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
