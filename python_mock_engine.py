#!/usr/bin/env python3
"""
🐍 Python Mock Engine - Rust Engine Replacement
Provides the same API as the Rust engine for testing without Rust
"""

import json
import time
import threading
from datetime import datetime
from typing import Dict, List, Any
from enum import Enum
import random

class ZoneState(Enum):
    CALM = "CALM"
    OVERSTIMULATED = "OVERSTIMULATED"
    EMERGENT = "EMERGENT"

class Zone:
    def __init__(self, id: int, name: str, activity: float = 0.5):
        self.id = id
        self.name = name
        self.activity = activity
        self.state = self._calculate_state()
    
    def _calculate_state(self) -> ZoneState:
        if self.activity < 0.4:
            return ZoneState.CALM
        elif self.activity < 0.7:
            return ZoneState.OVERSTIMULATED
        else:
            return ZoneState.EMERGENT
    
    def update_activity(self, delta: float):
        self.activity = max(0.0, min(1.0, self.activity + delta))
        self.state = self._calculate_state()

class MockRustEngine:
    """Python mock of the Rust homeostatic engine"""
    
    def __init__(self):
        self.zones = [
            Zone(0, "Downtown", 0.3),
            Zone(1, "Industrial", 0.6),
            Zone(2, "Residential", 0.2),
            Zone(3, "Commercial", 0.8),
            Zone(4, "Parks", 0.4)
        ]
        
        self.ema = [0.5] * len(self.zones)
        self.target = 0.5
        self.eta = 0.1
        self.running = True
        
        # Start background update thread
        self.update_thread = threading.Thread(target=self._background_update, daemon=True)
        self.update_thread.start()
    
    def _background_update(self):
        """Background thread for updating zones"""
        while self.running:
            self._update_zones()
            time.sleep(1)
    
    def _update_zones(self):
        """Update all zones using homeostatic algorithm"""
        for i, zone in enumerate(self.zones):
            # EMA smoothing
            self.ema[i] = 0.97 * self.ema[i] + 0.03 * zone.activity
            
            # Error-driven adjustment
            error = self.target - self.ema[i]
            adjustment = self.eta * error
            
            # Add some random noise for realism
            noise = (random.random() - 0.5) * 0.02
            
            zone.update_activity(adjustment + noise)
    
    def get_health(self) -> Dict[str, Any]:
        """Get health status"""
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "engine": "Python Mock Engine v1.0.0"
        }
    
    def get_state(self) -> Dict[str, Any]:
        """Get current city state"""
        system_health = sum(zone.activity for zone in self.zones) / len(self.zones)
        
        return {
            "zones": [
                {
                    "id": zone.id,
                    "name": zone.name,
                    "activity": zone.activity,
                    "state": zone.state.value
                }
                for zone in self.zones
            ],
            "timestamp": datetime.now().isoformat(),
            "system_health": system_health
        }
    
    def apply_biocore_effect(self, effect_data: Dict[str, Any]) -> Dict[str, Any]:
        """Apply BioCore effect"""
        zone_id = effect_data.get("zone_id")
        magnitude = effect_data.get("magnitude", 0.0)
        effects = effect_data.get("effects", [])
        
        if zone_id >= len(self.zones):
            return {
                "success": False,
                "error": f"Zone {zone_id} not found",
                "timestamp": datetime.now().isoformat()
            }
        
        zone = self.zones[zone_id]
        zone.update_activity(magnitude)
        
        return {
            "success": True,
            "effect": effect_data,
            "timestamp": datetime.now().isoformat()
        }
    
    def apply_influence(self, influence_data: Dict[str, Any]) -> Dict[str, Any]:
        """Apply direct influence"""
        zone_id = influence_data.get("zone_id")
        influence = influence_data.get("influence", 0.0)
        
        if zone_id >= len(self.zones):
            return {
                "success": False,
                "error": f"Zone {zone_id} not found",
                "timestamp": datetime.now().isoformat()
            }
        
        zone = self.zones[zone_id]
        zone.update_activity(influence)
        
        return {
            "success": True,
            "zone_id": zone_id,
            "influence": influence,
            "timestamp": datetime.now().isoformat()
        }
    
    def shutdown(self):
        """Shutdown the engine"""
        self.running = False

# Global instance
_mock_engine = None

def get_mock_engine():
    """Get or create mock engine instance"""
    global _mock_engine
    if _mock_engine is None:
        _mock_engine = MockRustEngine()
    return _mock_engine

if __name__ == "__main__":
    # Test the mock engine
    engine = get_mock_engine()
    
    print("🐍 Python Mock Engine Test")
    print("=" * 40)
    
    # Test health
    health = engine.get_health()
    print(f"Health: {health}")
    
    # Test state
    state = engine.get_state()
    print(f"State: {json.dumps(state, indent=2)}")
    
    # Test BioCore effect
    effect = {
        "zone_id": 2,
        "magnitude": -0.1,
        "effects": ["Test Effect"]
    }
    result = engine.apply_biocore_effect(effect)
    print(f"BioCore Effect: {result}")
    
    # Run for a few seconds to see updates
    print("\n🔄 Running for 5 seconds...")
    time.sleep(5)
    
    final_state = engine.get_state()
    print(f"Final State: {json.dumps(final_state, indent=2)}")
    
    engine.shutdown()
    print("✅ Mock engine test complete")
