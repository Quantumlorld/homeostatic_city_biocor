#!/usr/bin/env python3
"""
🌍 Homeostatic City + BioCore - Main Entry Point
Python simulation with Rust engine integration
"""

import sys
import time
import requests
import json
from pathlib import Path

class HomeostaticCity:
    def __init__(self):
        self.rust_url = "http://localhost:3030"
        self.running = True
        
    def check_rust_engine(self):
        """Check if Rust engine is running"""
        try:
            response = requests.get(f"{self.rust_url}/health", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def get_city_state(self):
        """Get current city state from Rust engine"""
        try:
            response = requests.get(f"{self.rust_url}/state", timeout=5)
            if response.status_code == 200:
                return response.json()
            return None
        except:
            return None
    
    def apply_biocore_effect(self, zone_id: int, plant: str, drug: str, synergy: float):
        """Apply BioCore effect to zone"""
        effect_data = {
            "zone_id": zone_id,
            "magnitude": synergy * 0.2 - 0.1,  # Scale to [-0.1, 0.1]
            "effects": [f"{plant}+{drug}", f"synergy_{synergy:.2f}"]
        }
        
        try:
            response = requests.post(f"{self.rust_url}/biocore", 
                                  json=effect_data, timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def display_state(self, state):
        """Display city state"""
        if not state:
            print("❌ Unable to get city state")
            return
        
        print("\n" + "="*60)
        print(f"🌍 HOMEOSTATIC CITY STATUS - {state['timestamp']}")
        print("="*60)
        print(f"📊 System Health: {state['system_health']:.3f}")
        print("\n🏙️  ZONE STATUS:")
        
        for zone in state['zones']:
            state_emoji = {
                'CALM': '🟢',
                'OVERSTIMULATED': '🟡', 
                'EMERGENT': '🔴'
            }.get(zone['state'], '⚪')
            
            print(f"  Zone {zone['id']} ({zone['name']}): {state_emoji} {zone['state']} - Activity: {zone['activity']:.3f}")
    
    def run_simulation(self):
        """Main simulation loop"""
        print("🌍 Starting Homeostatic City Simulation...")
        
        if not self.check_rust_engine():
            print("❌ Rust engine not running! Please start it first:")
            print("   cd city_core && cargo run")
            return
        
        print("✅ Connected to Rust engine")
        
        # Demo BioCore effects
        effects_to_apply = [
            (0, "Ashwagandha", "DrugA", 0.8),
            (1, "Turmeric", "DrugB", 0.9),
            (2, "Ginseng", "DrugC", 0.7),
        ]
        
        effect_index = 0
        
        try:
            while self.running:
                # Get and display current state
                state = self.get_city_state()
                self.display_state(state)
                
                # Apply BioCore effect periodically
                if effect_index < len(effects_to_apply) and int(time.time()) % 10 == 0:
                    zone_id, plant, drug, synergy = effects_to_apply[effect_index]
                    print(f"\n🌿 Applying BioCore effect to Zone {zone_id}: {plant}+{drug} (synergy: {synergy})")
                    
                    if self.apply_biocore_effect(zone_id, plant, drug, synergy):
                        print("✅ BioCore effect applied successfully")
                    else:
                        print("❌ Failed to apply BioCore effect")
                    
                    effect_index += 1
                
                print("\n⏸️  Press Ctrl+C to stop simulation...")
                time.sleep(2)
                
        except KeyboardInterrupt:
            print("\n🛑 Stopping simulation...")
            self.running = False

def main():
    """Main entry point"""
    print("🌍 Homeostatic City + BioCore")
    print("="*50)
    
    city = HomeostaticCity()
    city.run_simulation()
    
    print("👋 Simulation ended")

if __name__ == "__main__":
    main()