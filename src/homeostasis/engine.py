"""
Homeostatic Engine Module
Adjusts city zones slowly to maintain target calmness using EMA smoothing.
"""

import numpy as np
from typing import Optional


class HomeostaticEngine:
    """
    Adjusts city zones slowly to maintain target calmness.
    - Uses Exponential Moving Average (EMA) for smoothing
    """
    
    def __init__(self, target: float = 0.5, eta: float = 0.01):
        """
        Initialize homeostatic engine.
        
        Args:
            target: Desired calmness level (0-1)
            eta: Slow learning rate (adjustment factor)
        """
        self.target = target  # desired calmness level
        self.eta = eta        # slow learning rate
        self.ema: Optional[np.ndarray] = None       # EMA placeholder

    def update(self, activity: np.ndarray) -> np.ndarray:
        """
        Smooth activity using EMA and apply small adjustment towards target.
        
        Args:
            activity: Current activity levels
            
        Returns:
            Adjusted activity levels
        """
        if self.ema is None:
            self.ema = activity.copy()
        else:
            self.ema = 0.97 * self.ema + 0.03 * activity  # EMA smoothing

        # Compute slow adjustment
        error = self.target - self.ema
        adjustment = self.eta * error
        return np.clip(activity + adjustment, 0, 1)  # keep in [0,1]
    
    def get_ema(self) -> Optional[np.ndarray]:
        """
        Get current EMA values.
        
        Returns:
            Current EMA values or None if not initialized
        """
        return self.ema.copy() if self.ema is not None else None
    
    def reset(self) -> None:
        """Reset EMA to None for fresh start."""
        self.ema = None
