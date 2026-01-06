"""
Simulation Runner Module
Orchestrates the complete homeostatic city + BioCore simulation.
"""

import time
import numpy as np
from typing import Optional

from ..city.sensor import CitySensor
from ..homeostasis.engine import HomeostaticEngine
from ..biocore.simulator import BioCore
from ..visualization.display import display_city, display_summary


class SimulationRunner:
    """
    Main simulation runner that coordinates all modules.
    """
    
    def __init__(self, zones: int = 5, target_calmness: float = 0.5, learning_rate: float = 0.02):
        """
        Initialize simulation runner.
        
        Args:
            zones: Number of city zones
            target_calmness: Target activity level for homeostasis
            learning_rate: Learning rate for homeostatic adjustments
        """
        self.zones = zones
        self.city = CitySensor(zones=zones)
        self.homeostasis = HomeostaticEngine(target=target_calmness, eta=learning_rate)
        self.biocore = BioCore(
            plants=["Ginkgo", "Aloe", "Turmeric", "Ginseng", "Ashwagandha"],
            drugs=["DrugA", "DrugB", "DrugC", "DrugD", "DrugE"]
        )
        
    def run_step(self, step_num: int) -> np.ndarray:
        """
        Run a single simulation step.
        
        Args:
            step_num: Current step number for display
            
        Returns:
            Adjusted activity levels after the step
        """
        print(f"Step {step_num}")
        
        # Step 1: Update city activity
        activity = self.city.update_activity()
        
        # Step 2: Homeostatic slow learning adjustment
        adjusted_activity = self.homeostasis.update(activity)
        
        # Step 3: Apply BioCore effects
        for i in range(self.zones):
            plant = self.biocore.get_random_plant()
            drug = self.biocore.get_random_drug()
            bio_effect = self.biocore.simulate_interaction(plant, drug)
            zone_effect = self.biocore.zone_effect(adjusted_activity[i])
            
            # Adjust activity based on BioCore effect
            adjusted_activity[i] = np.clip(
                adjusted_activity[i] - 0.05 * bio_effect + 0.03 * zone_effect,
                0, 1
            )
        
        # Step 4: Display current zone states
        display_city(self.city, adjusted_activity)
        
        return adjusted_activity
    
    def run_simulation(self, iterations: int = 20, delay: float = 0.5, show_summary: bool = True) -> None:
        """
        Run the complete simulation.
        
        Args:
            iterations: Number of time steps to simulate
            delay: Delay between steps for readability
            show_summary: Whether to show summary at the end
        """
        print("🏙️  Starting Homeostatic City + BioCore Simulation...\n")
        
        activity_history = []
        
        for step in range(1, iterations + 1):
            adjusted_activity = self.run_step(step)
            activity_history.append(adjusted_activity.copy())
            
            if delay > 0:
                time.sleep(delay)
        
        if show_summary:
            final_activity = activity_history[-1]
            display_summary(final_activity)
        
        print(f"✅ Simulation completed after {iterations} iterations.")
        return activity_history
    
    def reset(self) -> None:
        """Reset the simulation to initial state."""
        self.city = CitySensor(zones=self.zones)
        self.homeostasis.reset()
        self.biocore.clear_cache()
