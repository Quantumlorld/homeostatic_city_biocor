#!/usr/bin/env python3
"""
🌦 Enhanced Mock Engine - Real Weather Integration
Combines mock zone simulation with real weather data
"""

import time
import json
import threading
from datetime import datetime
from typing import Dict, List, Any
from real_weather_engine import RealWeatherEngine

class EnhancedMockEngine:
    """Enhanced mock engine with real weather integration"""
    
    def __init__(self):
        self.zones = [
            {"id": 0, "name": "Downtown", "activity": 0.5, "state": "CALM"},
            {"id": 1, "name": "Industrial", "activity": 0.6, "state": "OVERSTIMULATED"},
            {"id": 2, "name": "Residential", "activity": 0.4, "state": "CALM"},
            {"id": 3, "name": "Commercial", "activity": 0.7, "state": "EMERGENT"},
            {"id": 4, "name": "Tech Park", "activity": 0.3, "state": "CALM"}
        ]
        
        self.weather_engine = RealWeatherEngine()
        self.target = 0.5
        self.ema = [0.5] * len(self.zones)
        self.eta = 0.1
        self.running = True
        self.weather_impacts = [0.0] * len(self.zones)
        
        print("🌦 Enhanced Mock Engine Initialized")
        print(f"🌦 Weather Engine: {self.weather_engine.__class__.__name__}")
        print(f"📍 Zones: {len(self.zones)}")
        
    def _background_update(self):
        """Background thread with weather-aware updates"""
        while self.running:
            # Get current weather for all zones
            city_weather = self.weather_engine.get_city_weather()
            
            # Update each zone based on weather
            for i, zone in enumerate(self.zones):
                zone_weather = city_weather["city_weather"].get(f"zone_{i}")
                if zone_weather:
                    # Calculate weather impact on activity
                    weather_impact = self.weather_engine.get_weather_impact_on_activity(zone_weather)
                    self.weather_impacts[i] = weather_impact
                    
                    # Update zone activity with weather influence
                    base_activity = 0.5 + (i * 0.1)  # Base pattern
                    weather_adjusted = base_activity + weather_impact
                    
                    # EMA smoothing
                    self.ema[i] = 0.97 * self.ema[i] + 0.03 * weather_adjusted
                    
                    # Apply some randomness for realism
                    noise = (time.time() % 7) * 0.02 - 0.07  # Time-based noise
                    final_activity = max(0.0, min(1.0, weather_adjusted + noise))
                    
                    # Update zone
                    zone["activity"] = final_activity
                    zone["state"] = self._calculate_state(final_activity)
            
            time.sleep(1)
    
    def _calculate_state(self, activity: float) -> str:
        """Calculate zone state from activity"""
        if activity < 0.4:
            return "CALM"
        elif activity < 0.7:
            return "OVERSTIMULATED"
        else:
            return "EMERGENT"
    
    def get_state(self) -> Dict[str, Any]:
        """Get current city state with weather data"""
        system_health = sum(zone["activity"] for zone in self.zones) / len(self.zones)
        
        return {
            "zones": self.zones,
            "weather_impacts": self.weather_impacts,
            "system_health": system_health,
            "timestamp": datetime.now().isoformat(),
            "engine": "Enhanced Mock Engine v1.0"
        }
    
    def apply_biocore_effect(self, effect_data: Dict[str, Any]) -> Dict[str, Any]:
        """Apply BioCore effect with weather consideration"""
        zone_id = effect_data.get("zone_id")
        magnitude = effect_data.get("magnitude", 0.0)
        
        if zone_id >= len(self.zones):
            return {
                "success": False,
                "error": f"Zone {zone_id} not found",
                "timestamp": datetime.now().isoformat()
            }
        
        zone = self.zones[zone_id]
        current_weather_impact = self.weather_impacts[zone_id]
        
        # Adjust magnitude based on current weather
        weather_adjusted_magnitude = magnitude
        if current_weather_impact < -0.1:  # Bad weather reduces effectiveness
            weather_adjusted_magnitude = magnitude * 0.7
        elif current_weather_impact > 0.05:  # Good weather enhances effectiveness
            weather_adjusted_magnitude = magnitude * 1.2
        
        # Apply effect with weather adjustment
        zone["activity"] = max(0.0, min(1.0, zone["activity"] + weather_adjusted_magnitude))
        zone["state"] = self._calculate_state(zone["activity"])
        
        return {
            "success": True,
            "zone_id": zone_id,
            "original_magnitude": magnitude,
            "weather_adjusted_magnitude": weather_adjusted_magnitude,
            "weather_impact": current_weather_impact,
            "timestamp": datetime.now().isoformat()
        }
    
    def start_engine(self):
        """Start the enhanced engine with weather integration"""
        print("🚀 Starting Enhanced Mock Engine...")
        
        # Start background update thread
        self.update_thread = threading.Thread(target=self._background_update, daemon=True)
        self.update_thread.start()
        
        print("✅ Enhanced Mock Engine Running")
        print("🌦 Real weather data integrated")
        print("📍 Zones will respond to weather conditions")
    
    def shutdown(self):
        """Shutdown the enhanced engine"""
        self.running = False
        if hasattr(self, 'update_thread'):
            self.update_thread.join(timeout=2)
        print("🛑 Enhanced Mock Engine Shutdown")

# Test the enhanced engine
if __name__ == "__main__":
    print("🌦 Enhanced Mock Engine Test")
    print("=" * 50)
    
    engine = EnhancedMockEngine()
    
    # Start the engine
    engine.start_engine()
    
    # Test for a few seconds to see weather effects
    print("🔄 Testing weather integration...")
    time.sleep(3)
    
    # Get state with weather data
    state = engine.get_state()
    print(f"State with weather: {json.dumps(state, indent=2)}")
    
    # Test BioCore effect with weather consideration
    effect = engine.apply_biocore_effect({
        "zone_id": 0,
        "magnitude": -0.1  # Calming effect
    })
    print(f"BioCore effect with weather: {json.dumps(effect, indent=2)}")
    
    engine.shutdown()
    print("✅ Enhanced Mock Engine test complete")
