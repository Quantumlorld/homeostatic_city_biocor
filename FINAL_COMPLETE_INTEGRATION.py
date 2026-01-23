#!/usr/bin/env python3
"""
🌙 FINAL COMPLETE INTEGRATION - ALL SYSTEMS COMBINED
Ultimate Homeostatic City BioCore + LunaBeyond AI Integration
"""

import asyncio
import json
import time
import threading
import webbrowser
from pathlib import Path
import sys
from datetime import datetime

# Add all paths for complete integration
sys.path.append(str(Path(__file__).parent))
sys.path.append(str(Path(__file__).parent / "lunabeyond-ai" / "src"))
sys.path.append(str(Path(__file__).parent / "src"))

# Import ALL SYSTEMS
from python_mock_engine import get_mock_engine
from enhanced_mock_engine import EnhancedMockEngine
from weather_integration_adapter import WeatherIntegrationAdapter
from src.biocore.engine import BioCoreEngine
from test_system import BHCS, BioCore

# LunaBeyond AI Systems
try:
    from enhanced_ai import EnhancedLunaBeyondAI
    from ai_dashboard import AIDashboard
    from luna_conversation import LunaConversation
    from luna_voice_interface import LunaVoiceInterface
    LUNA_SYSTEMS_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ LunaBeyond AI systems not fully available: {e}")
    print("🔄 Using mock Luna systems...")
    LUNA_SYSTEMS_AVAILABLE = False

class FinalCompleteIntegration:
    """The ultimate integration of all BHCS and LunaBeyond AI systems with real weather"""
    
    def __init__(self):
        print("🌙 INITIALIZING FINAL COMPLETE INTEGRATION")
        print("=" * 60)
        
        # Initialize Core Systems
        print("🦀 Initializing Core BHCS Engine...")
        self.mock_engine = get_mock_engine()
        self.biocore_engine = BioCoreEngine()
        self.bhcs = BHCS(5)
        self.biocore = BioCore()
        
        # Initialize Weather Integration
        print("🌦 Initializing Weather Integration...")
        self.weather_adapter = WeatherIntegrationAdapter()
        self.enhanced_engine = self.weather_adapter.get_mock_engine()
        
        # Initialize LunaBeyond AI Systems
        print("🧠 Initializing LunaBeyond AI Systems...")
        if LUNA_SYSTEMS_AVAILABLE:
            try:
                self.enhanced_ai = EnhancedLunaBeyondAI()
                self.ai_dashboard = AIDashboard()
                self.luna_conversation = LunaConversation()
                self.voice_interface = LunaVoiceInterface()
                print("✅ All LunaBeyond AI systems loaded")
            except Exception as e:
                print(f"⚠️ Error loading LunaBeyond AI: {e}")
                self._init_mock_luna()
        else:
            self._init_mock_luna()
        
        # Integration State
        self.system_state = {
            'bhcs_active': True,
            'luna_active': True,
            'biocore_active': True,
            'weather_active': True,
            'voice_active': False,
            'dashboard_open': False,
            'integration_level': 'COMPLETE_WITH_WEATHER'
        }
        
        # Performance Metrics
        self.metrics = {
            'start_time': time.time(),
            'total_interactions': 0,
            'biocore_effects_applied': 0,
            'ai_predictions': 0,
            'voice_commands': 0,
            'system_health': 0.85
        }
        
        print("✅ Final Complete Integration Initialized Successfully!")
        print("=" * 60)
    
    def _init_mock_luna(self):
        """Initialize mock Luna systems when full AI not available"""
        class MockLunaAI:
            def process_query(self, query):
                return f"🌙 Luna response: I understand your query about '{query}'. The BHCS system is operational."
            
            def get_status(self):
                return {"status": "active", "mood": "curious", "confidence": 0.85}
            
            def analyze_system(self, zones):
                return {"analysis": "System operating normally", "recommendations": ["Continue monitoring"]}
        
        self.enhanced_ai = MockLunaAI()
        self.ai_dashboard = None
        self.luna_conversation = None
        self.voice_interface = None
        print("🔄 Mock Luna AI systems initialized")
    
    async def start_complete_system(self):
        """Start the complete integrated system"""
        print("🚀 STARTING COMPLETE INTEGRATED SYSTEM")
        print("=" * 60)
        
        # Start all subsystems
        await self._start_bhcs_system()
        await self._start_luna_systems()
        await self._start_integration_services()
        
        # Open dashboard
        self._open_complete_dashboard()
        
        # Main integration loop
        await self._run_integration_loop()
    
    async def _start_bhcs_system(self):
        """Start BHCS core systems with weather integration"""
        print("🦀 Starting BHCS Core Systems with Weather...")
        
        # Start enhanced engine with weather
        self.enhanced_engine.start_engine()
        
        # Start weather integration
        asyncio.create_task(self.weather_adapter.start_weather_integration())
        
        print("✅ BHCS Core Systems Started with Weather Integration")
    
    async def _start_luna_systems(self):
        """Start LunaBeyond AI systems with weather awareness"""
        print("🧠 Starting LunaBeyond AI Systems with Weather Awareness...")
        
        if LUNA_SYSTEMS_AVAILABLE and self.ai_dashboard:
            try:
                # Start AI dashboard in background
                asyncio.create_task(self.ai_dashboard.start_dashboard())
                print("✅ AI Dashboard Started with Weather Integration")
            except Exception as e:
                print(f"⚠️ AI Dashboard start error: {e}")
        
        print("✅ LunaBeyond AI Systems Started with Weather Awareness")
    
    async def _start_integration_services(self):
        """Start integration services between systems"""
        print("🔗 Starting Integration Services...")
        
        # Start data synchronization
        def sync_data():
            while self.system_state['bhcs_active']:
                self._synchronize_systems()
                time.sleep(2)
        
        sync_thread = threading.Thread(target=sync_data, daemon=True)
        sync_thread.start()
        
        print("✅ Integration Services Started")
    
    def _synchronize_systems(self):
        """Synchronize data between all systems with weather data"""
        try:
            # Get current BHCS state with weather
            bhcs_state = self.enhanced_engine.get_state()
            
            # Update metrics with weather impacts
            self.metrics['system_health'] = bhcs_state['system_health']
            self.metrics['total_interactions'] += 1
            
            # Process through Luna AI with weather awareness
            if hasattr(self.enhanced_ai, 'analyze_system'):
                ai_analysis = self.enhanced_ai.analyze_system({
                    'zones': bhcs_state['zones'],
                    'weather_impacts': bhcs_state['weather_impacts'],
                    'weather_data': bhcs_state.get('weather_data', {})
                })
                self.metrics['ai_predictions'] += 1
            
            # Log weather impacts periodically
            if self.metrics['total_interactions'] % 10 == 0:
                print("🌦 Weather Impact Summary:")
                for i, impact in enumerate(bhcs_state['weather_impacts']):
                    zone_name = bhcs_state['zones'][i]['name']
                    print(f"  {zone_name}: {impact:+.3f}")
            
        except Exception as e:
            print(f"⚠️ Synchronization error: {e}")
    
    def _open_complete_dashboard(self):
        """Open the complete integrated dashboard"""
        print("🌐 Opening Complete Integrated Dashboard...")
        
        dashboard_path = Path(__file__).parent / "COMPLETE_INTEGRATED_DASHBOARD.html"
        if dashboard_path.exists():
            webbrowser.open(f"file://{dashboard_path.absolute()}")
            self.system_state['dashboard_open'] = True
            print("✅ Complete Dashboard Opened")
        else:
            print("❌ Complete Dashboard not found - creating it...")
            self._create_emergency_dashboard()
    
    def _create_emergency_dashboard(self):
        """Create emergency dashboard if main one missing"""
        emergency_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>🌙 EMERGENCY BHCS DASHBOARD</title>
            <style>
                body {{ font-family: Arial, sans-serif; background: #1a1f3a; color: white; padding: 20px; }}
                .container {{ max-width: 1200px; margin: 0 auto; }}
                .panel {{ background: rgba(255,255,255,0.1); padding: 20px; margin: 10px 0; border-radius: 10px; }}
                .status {{ color: #4CAF50; font-weight: bold; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🌙 EMERGENCY BHCS DASHBOARD</h1>
                <div class="panel">
                    <h2>System Status</h2>
                    <p class="status">✅ BHCS Core: ACTIVE</p>
                    <p class="status">✅ Luna AI: ACTIVE</p>
                    <p class="status">✅ BioCore: ACTIVE</p>
                    <p>System Health: {self.metrics['system_health']:.3f}</p>
                    <p>Total Interactions: {self.metrics['total_interactions']}</p>
                    <p>BioCore Effects: {self.metrics['biocore_effects_applied']}</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        emergency_path = Path(__file__).parent / "EMERGENCY_DASHBOARD.html"
        with open(emergency_path, 'w') as f:
            f.write(emergency_html)
        
        webbrowser.open(f"file://{emergency_path.absolute()}")
        print("✅ Emergency Dashboard Created and Opened")
    
    async def _run_integration_loop(self):
        """Main integration loop"""
        print("🔄 Starting Main Integration Loop...")
        print("=" * 60)
        print("🌙 COMPLETE SYSTEM IS NOW RUNNING!")
        print("📊 Dashboard: Open in browser")
        print("🦀 BHCS: Active and monitoring")
        print("🧠 Luna AI: Processing and learning")
        print("🌿 BioCore: Ready for interventions")
        print("=" * 60)
        
        try:
            while self.system_state['bhcs_active']:
                # Update system status
                current_time = time.time()
                uptime = current_time - self.metrics['start_time']
                
                # Display status every 10 seconds
                if int(current_time) % 10 == 0:
                    print(f"🌙 System Status: Health={self.metrics['system_health']:.3f}, "
                          f"Interactions={self.metrics['total_interactions']}, "
                          f"Uptime={uptime:.0f}s")
                
                # Check for system optimization opportunities
                if self.metrics['total_interactions'] % 50 == 0:
                    await self._optimize_system()
                
                await asyncio.sleep(1)
                
        except KeyboardInterrupt:
            print("\n🛑 Shutting down Complete Integrated System...")
            await self._shutdown_systems()
    
    async def _optimize_system(self):
        """Optimize integrated system with weather consideration"""
        print("⚡ Running Weather-Aware System Optimization...")
        
        try:
            # Get current state with weather data
            bhcs_state = self.enhanced_engine.get_state()
            
            # Apply intelligent optimizations based on weather
            for i, zone in enumerate(bhcs_state['zones']):
                zone_activity = zone['activity']
                weather_impact = bhcs_state['weather_impacts'][i]
                
                # Consider weather in optimization decisions
                if zone_activity > 0.7:
                    # Zone is overstimulated - apply calming effect
                    # But reduce effectiveness if weather is already calming
                    if weather_impact < -0.1:
                        # Weather already calming - use lighter touch
                        magnitude = -0.05
                    else:
                        # Weather not helping - use normal calming
                        magnitude = -0.1
                    
                    self.enhanced_engine.apply_biocore_effect({
                        'zone_id': i,
                        'magnitude': magnitude,
                        'weather_adjusted': True
                    })
                    self.metrics['biocore_effects_applied'] += 1
                    
                elif zone_activity < 0.3:
                    # Zone is underactive - apply activating effect
                    # But reduce effectiveness if weather is already activating
                    if weather_impact > 0.05:
                        # Weather already activating - use lighter touch
                        magnitude = 0.05
                    else:
                        # Weather not helping - use normal activation
                        magnitude = 0.1
                    
                    self.enhanced_engine.apply_biocore_effect({
                        'zone_id': i,
                        'magnitude': magnitude,
                        'weather_adjusted': True
                    })
                    self.metrics['biocore_effects_applied'] += 1
            
            print("✅ Weather-Aware System Optimization Complete")
            
        except Exception as e:
            print(f"⚠️ Weather-Aware Optimization error: {e}")
    
    async def _shutdown_systems(self):
        """Shutdown all systems gracefully"""
        print("🛑 Shutting Down All Systems...")
        
        # Stop BHCS
        self.system_state['bhcs_active'] = False
        if self.enhanced_engine:
            self.enhanced_engine.shutdown()
        if self.weather_adapter:
            self.weather_adapter.stop_integration()
        
        # Stop Luna systems
        self.system_state['luna_active'] = False
        
        # Final metrics
        total_uptime = time.time() - self.metrics['start_time']
        print("=" * 60)
        print("🌙 FINAL SYSTEM METRICS:")
        print(f"  Total Uptime: {total_uptime:.0f} seconds")
        print(f"  Total Interactions: {self.metrics['total_interactions']}")
        print(f"  BioCore Effects Applied: {self.metrics['biocore_effects_applied']}")
        print(f"  AI Predictions: {self.metrics['ai_predictions']}")
        print(f"  Voice Commands: {self.metrics['voice_commands']}")
        print(f"  Final System Health: {self.metrics['system_health']:.3f}")
        print(f"  Weather Integration: {'ACTIVE' if self.system_state.get('weather_active') else 'INACTIVE'}")
        print("=" * 60)
        print("👋 Complete Integrated System Shutdown Complete")

async def main():
    """Main entry point for final complete integration"""
    print("🌙 HOMEOSTATIC CITY BIOCORE - FINAL COMPLETE INTEGRATION")
    print("=" * 60)
    print("🦀 BHCS Core + 🧠 LunaBeyond AI + 🌿 BioCore")
    print("🔗 Complete System Integration")
    print("=" * 60)
    
    # Initialize and start the complete system
    integration = FinalCompleteIntegration()
    await integration.start_complete_system()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ System error: {e}")
        import traceback
        traceback.print_exc()
