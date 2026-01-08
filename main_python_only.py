#!/usr/bin/env python3
"""
🌍 Homeostatic City + BioCore - Python Only Version
Complete system simulation without Rust dependency
"""

import sys
import time
import threading
import json
from pathlib import Path
from python_mock_engine import get_mock_engine
from src.biocore.engine import BioCoreEngine

class PythonOnlyBHCSSystem:
    def __init__(self):
        self.mock_engine = get_mock_engine()
        self.biocore_engine = BioCoreEngine()
        self.running = True
        
    def get_city_state(self):
        """Get current city state"""
        return self.mock_engine.get_state()
    
    def apply_biocore_effect(self, zone_id: int, plant: str, drug: str, synergy: float):
        """Apply BioCore effect using the BioCore engine"""
        try:
            # Calculate effect using BioCore engine
            effect = self.biocore_engine.calculate_effect(plant, drug, synergy)
            
            # Apply to mock engine
            effect_data = {
                "zone_id": zone_id,
                "magnitude": effect.magnitude,
                "effects": effect.effects
            }
            
            result = self.mock_engine.apply_biocore_effect(effect_data)
            return result, effect
            
        except Exception as e:
            return {"success": False, "error": str(e)}, None
    
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
    
    def display_biocore_info(self):
        """Display BioCore engine information"""
        print("\n🌿 BIOCORE ENGINE INFO:")
        print(f"  Available Plants: {list(self.biocore_engine.plants.keys())}")
        print(f"  Available Drugs: {list(self.biocore_engine.drugs.keys())}")
        
        # Show some example synergies
        print("\n📊 EXAMPLE SYNERGIES:")
        examples = [
            ("Ashwagandha", "DrugA"),
            ("Turmeric", "DrugB"),
            ("Ginseng", "DrugC")
        ]
        
        for plant, drug in examples:
            try:
                effect = self.biocore_engine.calculate_effect(plant, drug, 0.8)
                print(f"  {plant} + {drug}: {effect.magnitude:.3f} magnitude, {effect.effects[:2]}")
            except:
                pass
    
    def get_recommendations(self, state):
        """Get BioCore recommendations based on current state"""
        zone_states = [zone['state'] for zone in state['zones']]
        recommendations = self.biocore_engine.get_recommendations(zone_states)
        
        print("\n💡 BIOCORE RECOMMENDATIONS:")
        if recommendations:
            for i, (plant, drug, synergy) in enumerate(recommendations, 1):
                print(f"  {i}. {plant} + {drug} (synergy: {synergy:.3f})")
        else:
            print("  No specific recommendations at this time")
    
    def run_simulation(self):
        """Main simulation loop"""
        print("🌍 Starting Python-Only Homeostatic City Simulation...")
        print("🐍 Using Python Mock Engine (no Rust required)")
        
        # Display BioCore info
        self.display_biocore_info()
        
        # Demo BioCore effects to apply
        effects_to_apply = [
            (0, "Ashwagandha", "DrugA", 0.8),
            (1, "Turmeric", "DrugB", 0.9),
            (2, "Ginseng", "DrugC", 0.7),
            (3, "Bacopa", "DrugD", 0.6),
            (4, "Rhodiola", "DrugE", 0.8),
        ]
        
        effect_index = 0
        update_counter = 0
        
        try:
            while self.running:
                # Get and display current state
                state = self.get_city_state()
                self.display_state(state)
                
                # Get recommendations every 10 updates
                if update_counter % 10 == 0:
                    self.get_recommendations(state)
                
                # Apply BioCore effect periodically
                if effect_index < len(effects_to_apply) and update_counter % 15 == 0:
                    zone_id, plant, drug, synergy = effects_to_apply[effect_index]
                    print(f"\n🌿 Applying BioCore effect to Zone {zone_id}: {plant}+{drug} (synergy: {synergy})")
                    
                    result, effect = self.apply_biocore_effect(zone_id, plant, drug, synergy)
                    
                    if result["success"]:
                        print(f"✅ BioCore effect applied successfully")
                        if effect:
                            print(f"   Magnitude: {effect.magnitude:.3f}")
                            print(f"   Effects: {', '.join(effect.effects[:3])}")
                            print(f"   Confidence: {effect.confidence:.3f}")
                            print(f"   Duration: {effect.duration}s")
                    else:
                        print(f"❌ Failed to apply BioCore effect: {result.get('error', 'Unknown error')}")
                    
                    effect_index += 1
                
                print("\n⏸️  Press Ctrl+C to stop simulation...")
                update_counter += 1
                time.sleep(2)
                
        except KeyboardInterrupt:
            print("\n🛑 Stopping simulation...")
            self.running = False
        
        finally:
            self.mock_engine.shutdown()

def main():
    """Main entry point"""
    print("🌍 Homeostatic City + BioCore - Python Only Version")
    print("=" * 60)
    print("🐍 Python Mock Engine + 🧠 BioCore Engine")
    print("🌐 Dashboard: Open dashboard/index.html manually")
    print("=" * 60)
    
    system = PythonOnlyBHCSSystem()
    system.run_simulation()
    
    print("👋 Simulation ended")

if __name__ == "__main__":
    main()
