"""
BioCore Simulator Module
Simulates plant-drug synergy for disease or environmental benefit.
"""

import random
import numpy as np
from typing import List, Dict


class BioCore:
    """
    Simulates plant-drug synergy for disease or environmental benefit.
    - Replace random scoring with real ML model later.
    """
    
    def __init__(self, plants: List[str], drugs: List[str]):
        """
        Initialize BioCore simulator.
        
        Args:
            plants: List of plant names
            drugs: List of drug names
        """
        self.plants = plants
        self.drugs = drugs
        self._interaction_cache: Dict[str, float] = {}

    def simulate_interaction(self, plant: str, drug: str) -> float:
        """
        Predict synergy score for a plant-drug pair (0-1)
        Placeholder uses random number with caching for consistency.
        
        Args:
            plant: Plant name
            drug: Drug name
            
        Returns:
            Synergy score between 0 and 1
        """
        if plant not in self.plants or drug not in self.drugs:
            raise ValueError(f"Unknown plant '{plant}' or drug '{drug}'")
        
        # Use cache for consistent results
        cache_key = f"{plant}-{drug}"
        if cache_key not in self._interaction_cache:
            synergy_score = random.random()  # placeholder
            self._interaction_cache[cache_key] = synergy_score
        
        return self._interaction_cache[cache_key]

    def zone_effect(self, activity_level: float) -> float:
        """
        Maps BioCore effect to city zones
        - Calm zones: small influence
        - Overstimulated zones: larger influence
        
        Args:
            activity_level: Current activity level of zone (0-1)
            
        Returns:
            Effect strength between 0 and 1
        """
        effect_strength = activity_level * random.random()
        return np.clip(effect_strength, 0, 1)
    
    def get_random_plant(self) -> str:
        """Get a random plant from the list."""
        return random.choice(self.plants)
    
    def get_random_drug(self) -> str:
        """Get a random drug from the list."""
        return random.choice(self.drugs)
    
    def clear_cache(self) -> None:
        """Clear the interaction cache."""
        self._interaction_cache.clear()
