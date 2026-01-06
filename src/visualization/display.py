"""
Display Module
Handles console visualization of city zones and their states.
"""

import numpy as np
from typing import List, Tuple
from ..city.sensor import CitySensor


def get_zone_state(level: float) -> Tuple[str, str]:
    """
    Determine zone state based on activity level.
    
    Args:
        level: Activity level (0-1)
        
    Returns:
        Tuple of (state_name, emoji_indicator)
    """
    if level < 0.4:
        return "CALM", "🟢"
    elif level < 0.7:
        return "OVERSTIMULATED", "🟡"
    else:
        return "EMERGENT", "🔴"


def display_city(zones: CitySensor, activity_levels: np.ndarray) -> None:
    """
    Display city zones in console with color-coded states:
    - Calm: 0-0.4 🟢
    - Overstimulated: 0.4-0.7 🟡
    - Emergent/Mad: 0.7-1 🔴
    
    Args:
        zones: CitySensor instance with zone information
        activity_levels: Current activity levels for each zone
    """
    zone_names = zones.get_zone_names()
    
    for i, level in enumerate(activity_levels):
        state_name, emoji = get_zone_state(level)
        print(f"{zone_names[i]}: {level:.2f} -> {state_name} {emoji}")
    
    print("-" * 40)


def display_summary(activity_levels: np.ndarray) -> None:
    """
    Display summary statistics for all zones.
    
    Args:
        activity_levels: Current activity levels for each zone
    """
    avg_activity = np.mean(activity_levels)
    max_activity = np.max(activity_levels)
    min_activity = np.min(activity_levels)
    
    calm_count = np.sum(activity_levels < 0.4)
    overstimulated_count = np.sum((activity_levels >= 0.4) & (activity_levels < 0.7))
    emergent_count = np.sum(activity_levels >= 0.7)
    
    print(f"\n📊 SUMMARY:")
    print(f"   Average Activity: {avg_activity:.2f}")
    print(f"   Range: {min_activity:.2f} - {max_activity:.2f}")
    print(f"   Zones - Calm: {calm_count}, Overstimulated: {overstimulated_count}, Emergent: {emergent_count}")
    print("-" * 40)
