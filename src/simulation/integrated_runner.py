"""
Integrated simulation runner that communicates with Rust homeostatic engine.
"""

import time
import random
from typing import List, Dict, Any
from ..biocore.client import BioCoreClient
from ..biocore.simulator import BioCore


class IntegratedSimulationRunner:
    """Simulation runner that integrates with Rust homeostatic engine."""
    
    def __init__(self, rust_url: str = "http://localhost:3030"):
        self.client = BioCoreClient(rust_url)
        self.biocore = BioCore(
            plants=["Ginkgo", "Aloe", "Turmeric", "Ginseng", "Ashwagandha"],
            drugs=["DrugA", "DrugB", "DrugC", "DrugD", "DrugE"]
        )
    
    def run_integrated_simulation(self, iterations: int = 20, delay: float = 1.0):
        """Run simulation with Rust engine integration."""
        print("🚀 Starting Integrated Simulation with Rust Engine...")
        
        if not self.client.health_check():
            print("❌ Rust engine not available. Please start city_core first.")
            return
        
        for step in range(1, iterations + 1):
            print(f"\n--- Step {step} ---")
            
            # Get current state from Rust
            state = self.client.get_city_state()
            if state:
                print(f"📊 Current zones: {len(state)} active")
                
                # Apply random BioCore effects
                if random.random() < 0.7:  # 70% chance to apply effect
                    zone_id = random.randint(0, 4)
                    plant = self.biocore.get_random_plant()
                    drug = self.biocore.get_random_drug()
                    synergy = random.random()
                    
                    success = self.client.apply_biocore_effect(zone_id, plant, drug, synergy)
                    if success:
                        print(f"🌿 Applied: {plant} + {drug} → Zone {zone_id} (synergy: {synergy:.2f})")
            
            time.sleep(delay)
        
        print("✅ Integrated simulation completed!")
        self.client.close()
