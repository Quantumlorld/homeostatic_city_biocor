"""
City Sensor Module
Simulates human and environmental activity in city zones.
"""

import numpy as np
from typing import List


class CitySensor:
    """
    Simulates human and environmental activity in city zones.
    - activity: 0 (calm) -> 1 (overstimulated)
    """
    
    def __init__(self, zones: int = 5):
        """
        Initialize city sensor with specified number of zones.
        
        Args:
            zones: Number of city zones to simulate
        """
        self.zones = zones
        self.activity = np.random.rand(zones)  # initial random activity [0,1]
        # Assign names to zones for display
        self.zone_names = [f"Zone-{i+1}" for i in range(zones)]

    def update_activity(self) -> np.ndarray:
        """
        Introduce small random fluctuations to simulate real-life dynamics.
        
        Returns:
            Updated activity levels as numpy array
        """
        noise = np.random.normal(0, 0.05, self.zones)  # small random noise
        self.activity = np.clip(self.activity + noise, 0, 1)  # keep in [0,1]
        return self.activity
    
    def get_zone_names(self) -> List[str]:
        """
        Get list of zone names.
        
        Returns:
            List of zone name strings
        """
        return self.zone_names.copy()
    
    def get_activity_levels(self) -> np.ndarray:
        """
        Get current activity levels.
        
        Returns:
            Current activity levels as numpy array
        """
        return self.activity.copy()
