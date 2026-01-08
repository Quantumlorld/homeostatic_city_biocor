#!/usr/bin/env python3
"""
🚀 LUNABEYOND AI - FASTAPI BACKEND SERVER
High-performance async backend for LunaBeyond AI system
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Dict, List, Any, Optional
import asyncio
import json
import time
import uuid
from datetime import datetime
import logging

# Import Luna modules (mocked for now)
# from lunabeyond_ai.src.luna_learning_engine import luna_learning_engine
# from lunabeyond_ai.src.luna_fast_response import luna_fast_response
# from lunabeyond_ai.src.luna_biocore_learning import luna_biocore_learning
# from lunabeyond_ai.src.luna_conversation_manager import luna_conversation_manager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(
    title="LunaBeyond AI Backend",
    description="High-performance async backend for LunaBeyond AI system",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
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
class GlobalState:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.session_data: Dict[str, Any] = {}
        self.system_metrics: Dict[str, Any] = {}
        self.performance_stats: Dict[str, Any] = {}
        
    async def add_connection(self, websocket: WebSocket, session_id: str):
        self.active_connections.append(websocket)
        self.session_data[session_id] = {
            'websocket': websocket,
            'connected_at': datetime.now(),
            'interactions': 0,
            'last_activity': datetime.now()
        }
        
    async def remove_connection(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            
        # Remove session data
        session_to_remove = None
        for session_id, data in self.session_data.items():
            if data['websocket'] == websocket:
                session_to_remove = session_id
                break
                
        if session_to_remove:
            del self.session_data[session_to_remove]

global_state = GlobalState()

# Pydantic models
class ChatMessage(BaseModel):
    message: str
    session_id: Optional[str] = None
    user_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = {}

class VoiceCommand(BaseModel):
    command: str
    session_id: Optional[str] = None
    voice_data: Optional[Dict[str, Any]] = {}

class BHCSCommand(BaseModel):
    command: str
    parameters: Optional[Dict[str, Any]] = {}
    session_id: Optional[str] = None

class SystemStatus(BaseModel):
    health: float
    zones: List[Dict[str, Any]]
    timestamp: datetime

class LearningRequest(BaseModel):
    query: str
    context: Optional[Dict[str, Any]] = {}
    session_id: Optional[str] = None

# API Endpoints
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "LunaBeyond AI Backend Server",
        "version": "2.0.0",
        "status": "running",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "active_connections": len(global_state.active_connections),
        "active_sessions": len(global_state.session_data),
        "performance": global_state.performance_stats
    }

@app.post("/api/chat")
async def chat_endpoint(message: ChatMessage):
    """
    💬 Fast chat endpoint with LunaBeyond AI
    """
    start_time = time.time()
    
    try:
        # Generate session ID if not provided
        session_id = message.session_id or str(uuid.uuid4())
        
        # Create context
        context = {
            'timestamp': datetime.now().isoformat(),
            'session_id': session_id,
            'user_id': message.user_id,
            'interaction_type': 'chat',
            **message.context
        }
        
        # Process through fast response system
        response_data = await luna_fast_response.generate_response(message.message, context)
        
        # Update session data
        if session_id in global_state.session_data:
            global_state.session_data[session_id]['interactions'] += 1
            global_state.session_data[session_id]['last_activity'] = datetime.now()
        
        # Update performance stats
        processing_time = time.time() - start_time
        global_state.performance_stats['last_chat_time'] = processing_time
        global_state.performance_stats['total_chats'] = global_state.performance_stats.get('total_chats', 0) + 1
        
        logger.info(f"Chat processed in {processing_time:.3f}s for session {session_id}")
        
        return {
            "success": True,
            "session_id": session_id,
            "response": response_data,
            "processing_time": processing_time,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Chat endpoint error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/voice")
async def voice_endpoint(command: VoiceCommand):
    """
    🎤 Voice command processing endpoint
    """
    start_time = time.time()
    
    try:
        session_id = command.session_id or str(uuid.uuid4())
        
        # Process voice command through conversation manager
        context = {
            'timestamp': datetime.now().isoformat(),
            'session_id': session_id,
            'interaction_type': 'voice',
            'voice_data': command.voice_data
        }
        
        response_data = await luna_conversation_manager.process_user_input(command.command, context)
        
        # Update performance stats
        processing_time = time.time() - start_time
        global_state.performance_stats['last_voice_time'] = processing_time
        global_state.performance_stats['total_voice_commands'] = global_state.performance_stats.get('total_voice_commands', 0) + 1
        
        logger.info(f"Voice command processed in {processing_time:.3f}s")
        
        return {
            "success": True,
            "session_id": session_id,
            "response": response_data,
            "processing_time": processing_time,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Voice endpoint error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/bhcs")
async def bhcs_endpoint(command: BHCSCommand):
    """
    🧬 BHCS system control endpoint
    """
    start_time = time.time()
    
    try:
        session_id = command.session_id or str(uuid.uuid4())
        
        # Process BHCS command
        if command.command == "status":
            # Get system status
            status_data = await get_system_status()
            
        elif command.command == "apply_biocore":
            # Apply BioCore intervention
            status_data = await apply_biocore(command.parameters)
            
        elif command.command == "optimize":
            # Optimize system
            status_data = await optimize_system(command.parameters)
            
        elif command.command == "predict":
            # Get predictions
            status_data = await get_predictions(command.parameters)
            
        else:
            raise HTTPException(status_code=400, detail=f"Unknown BHCS command: {command.command}")
        
        # Update performance stats
        processing_time = time.time() - start_time
        global_state.performance_stats['last_bhcs_time'] = processing_time
        global_state.performance_stats['total_bhcs_commands'] = global_state.performance_stats.get('total_bhcs_commands', 0) + 1
        
        logger.info(f"BHCS command '{command.command}' processed in {processing_time:.3f}s")
        
        return {
            "success": True,
            "session_id": session_id,
            "command": command.command,
            "result": status_data,
            "processing_time": processing_time,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"BHCS endpoint error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/learn")
async def learn_endpoint(request: LearningRequest):
    """
    🧠 Advanced learning endpoint
    """
    start_time = time.time()
    
    try:
        session_id = request.session_id or str(uuid.uuid4())
        
        # Process learning request
        context = {
            'timestamp': datetime.now().isoformat(),
            'session_id': session_id,
            'interaction_type': 'learning',
            **request.context
        }
        
        # Cognitive processing
        cognitive_result = await luna_learning_engine.cognitive_processing(request.query, context)
        
        # BioCore learning
        biocore_patterns = await luna_biocore_learning.learn_from_biocore_data(request.context)
        
        # Update performance stats
        processing_time = time.time() - start_time
        global_state.performance_stats['last_learning_time'] = processing_time
        global_state.performance_stats['total_learning_requests'] = global_state.performance_stats.get('total_learning_requests', 0) + 1
        
        logger.info(f"Learning request processed in {processing_time:.3f}s")
        
        return {
            "success": True,
            "session_id": session_id,
            "cognitive_result": cognitive_result,
            "biocore_patterns": biocore_patterns,
            "processing_time": processing_time,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Learning endpoint error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/status")
async def get_system_status():
    """
    📊 Get comprehensive system status
    """
    try:
        # Get learning engine status
        learning_status = luna_learning_engine.get_learning_status()
        
        # Get BioCore learning status
        biocore_status = luna_biocore_learning.get_biocore_learning_status()
        
        # Get conversation manager status
        conversation_status = luna_conversation_manager.get_conversation_status()
        
        # Get fast response status
        fast_response_status = luna_fast_response.get_cache_stats()
        
        # Simulate BHCS system data
        bhcs_data = {
            "system_health": 0.85 + (time.time() % 10) / 100,
            "zones": [
                {"id": 0, "activity": 0.3, "state": "CALM"},
                {"id": 1, "activity": 0.6, "state": "OVERSTIMULATED"},
                {"id": 2, "activity": 0.2, "state": "CALM"},
                {"id": 3, "activity": 0.8, "state": "EMERGENT"},
                {"id": 4, "activity": 0.4, "state": "CALM"}
            ],
            "timestamp": datetime.now().isoformat()
        }
        
        return {
            "system_health": bhcs_data["system_health"],
            "zones": bhcs_data["zones"],
            "learning_engine": learning_status,
            "biocore_learning": biocore_status,
            "conversation_manager": conversation_status,
            "fast_response": fast_response_status,
            "active_sessions": len(global_state.session_data),
            "performance_stats": global_state.performance_stats,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Status endpoint error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# WebSocket endpoint for real-time communication
@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """
    🌐 WebSocket endpoint for real-time communication
    """
    await websocket.accept()
    
    try:
        await global_state.add_connection(websocket, session_id)
        logger.info(f"WebSocket connection established for session {session_id}")
        
        # Send welcome message
        await websocket.send_json({
            "type": "connection",
            "message": "Connected to LunaBeyond AI Backend",
            "session_id": session_id,
            "timestamp": datetime.now().isoformat()
        })
        
        # Keep connection alive
        while True:
            try:
                # Receive message
                data = await websocket.receive_json()
                
                # Process message based on type
                message_type = data.get("type", "unknown")
                
                if message_type == "chat":
                    # Process chat message
                    response = await process_chat_message(data, session_id)
                    await websocket.send_json(response)
                    
                elif message_type == "voice":
                    # Process voice command
                    response = await process_voice_message(data, session_id)
                    await websocket.send_json(response)
                    
                elif message_type == "bhcs":
                    # Process BHCS command
                    response = await process_bhcs_message(data, session_id)
                    await websocket.send_json(response)
                    
                elif message_type == "ping":
                    # Respond to ping
                    await websocket.send_json({
                        "type": "pong",
                        "timestamp": datetime.now().isoformat()
                    })
                    
                else:
                    # Unknown message type
                    await websocket.send_json({
                        "type": "error",
                        "message": f"Unknown message type: {message_type}",
                        "timestamp": datetime.now().isoformat()
                    })
                    
            except WebSocketDisconnect:
                break
                
    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected for session {session_id}")
        
    except Exception as e:
        logger.error(f"WebSocket error for session {session_id}: {e}")
        
    finally:
        await global_state.remove_connection(websocket)

# Helper functions
async def process_chat_message(data: Dict, session_id: str) -> Dict:
    """Process chat message through WebSocket"""
    try:
        message = data.get("message", "")
        context = data.get("context", {})
        
        # Process through fast response
        response_data = await luna_fast_response.generate_response(message, context)
        
        return {
            "type": "chat_response",
            "session_id": session_id,
            "response": response_data,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Chat message processing error: {e}")
        return {
            "type": "error",
            "message": str(e),
            "timestamp": datetime.now().isoformat()
        }

async def process_voice_message(data: Dict, session_id: str) -> Dict:
    """Process voice message through WebSocket"""
    try:
        command = data.get("command", "")
        voice_data = data.get("voice_data", {})
        
        # Process through conversation manager
        context = {
            'session_id': session_id,
            'interaction_type': 'voice',
            'voice_data': voice_data
        }
        
        response_data = await luna_conversation_manager.process_user_input(command, context)
        
        return {
            "type": "voice_response",
            "session_id": session_id,
            "response": response_data,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Voice message processing error: {e}")
        return {
            "type": "error",
            "message": str(e),
            "timestamp": datetime.now().isoformat()
        }

async def process_bhcs_message(data: Dict, session_id: str) -> Dict:
    """Process BHCS message through WebSocket"""
    try:
        command = data.get("command", "")
        parameters = data.get("parameters", {})
        
        # Process BHCS command
        if command == "status":
            result = await get_system_status()
        elif command == "apply_biocore":
            result = await apply_biocore(parameters)
        elif command == "optimize":
            result = await optimize_system(parameters)
        else:
            raise ValueError(f"Unknown BHCS command: {command}")
        
        return {
            "type": "bhcs_response",
            "session_id": session_id,
            "command": command,
            "result": result,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"BHCS message processing error: {e}")
        return {
            "type": "error",
            "message": str(e),
            "timestamp": datetime.now().isoformat()
        }

# BHCS helper functions
async def apply_biocore(parameters: Dict) -> Dict:
    """Apply BioCore intervention"""
    # Simulate BioCore application
    await asyncio.sleep(0.1)  # Simulate processing time
    
    return {
        "action": "biocore_applied",
        "parameters": parameters,
        "result": "BioCore intervention successful",
        "system_health": 0.9,
        "timestamp": datetime.now().isoformat()
    }

async def optimize_system(parameters: Dict) -> Dict:
    """Optimize system"""
    # Simulate optimization
    await asyncio.sleep(0.2)  # Simulate processing time
    
    return {
        "action": "optimization_applied",
        "parameters": parameters,
        "result": "System optimization successful",
        "improvement": 0.15,
        "timestamp": datetime.now().isoformat()
    }

async def get_predictions(parameters: Dict) -> Dict:
    """Get system predictions"""
    # Simulate prediction
    await asyncio.sleep(0.15)  # Simulate processing time
    
    return {
        "prediction": "System health will reach 92% in 1 hour",
        "confidence": 0.85,
        "risk_factors": ["Zone 3 activity"],
        "timestamp": datetime.now().isoformat()
    }

# Background tasks
@app.on_event("startup")
async def startup_event():
    """Startup background tasks"""
    logger.info("LunaBeyond AI Backend Server starting up...")
    
    # Start background monitoring
    asyncio.create_task(background_monitoring())

async def background_monitoring():
    """Background monitoring task"""
    while True:
        try:
            # Update performance stats
            global_state.performance_stats['monitoring_timestamp'] = datetime.now().isoformat()
            
            # Clean up inactive sessions
            current_time = datetime.now()
            inactive_sessions = []
            
            for session_id, data in global_state.session_data.items():
                if (current_time - data['last_activity']).seconds > 3600:  # 1 hour
                    inactive_sessions.append(session_id)
            
            for session_id in inactive_sessions:
                await global_state.remove_connection(global_state.session_data[session_id]['websocket'])
                logger.info(f"Cleaned up inactive session: {session_id}")
            
            await asyncio.sleep(60)  # Check every minute
            
        except Exception as e:
            logger.error(f"Background monitoring error: {e}")
            await asyncio.sleep(60)

if __name__ == "__main__":
    import uvicorn
    
    # Run the server
    uvicorn.run(
        "fastapi_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
