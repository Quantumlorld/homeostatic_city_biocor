"""
Nuclear Simulator Module
Advanced nuclear scenario modeling for defense and emergency response.
"""

import numpy as np
from typing import List, Dict, Tuple, Optional
from enum import Enum
import math


class ThreatLevel(Enum):
    """Threat level enumeration for nuclear scenarios."""
    NORMAL = "NORMAL"
    ELEVATED = "ELEVATED"
    HIGH = "HIGH"
    SEVERE = "SEVERE"
    CRITICAL = "CRITICAL"


class NuclearSimulator:
    """
    Nuclear scenario simulator for defense system modeling.
    Simulates radiation patterns, evacuation zones, and response protocols.
    """
    
    def __init__(self, city_zones: int = 5):
        """
        Initialize nuclear simulator.
        
        Args:
            city_zones: Number of city zones to simulate
        """
        self.city_zones = city_zones
        self.radiation_levels = np.zeros(city_zones)
        self.wind_speed = 0.0  # m/s
        self.wind_direction = 0.0  # degrees
        self.time_since_incident = 0  # hours
        self.threat_level = ThreatLevel.NORMAL
        
        # Nuclear incident parameters
        self.detonation_yield = 0.0  # kilotons
        self.ground_zero = None  # zone index
        self.fallout_pattern = np.zeros((city_zones, city_zones))
        
        # Emergency response parameters
        self.evacuation_zones = set()
        self.shelter_capacity = np.zeros(city_zones)
        self.medical_resources = np.zeros(city_zones)
        
    def simulate_nuclear_incident(self, ground_zero: int, yield_kt: float) -> Dict:
        """
        Simulate a nuclear incident in the specified zone.
        
        Args:
            ground_zero: Zone where incident occurs
            yield_kt: Detonation yield in kilotons
            
        Returns:
            Incident simulation results
        """
        self.ground_zero = ground_zero
        self.detonation_yield = yield_kt
        self.time_since_incident = 0
        
        # Calculate initial radiation levels
        self._calculate_initial_radiation()
        
        # Calculate fallout patterns
        self._calculate_fallout_pattern()
        
        # Determine threat level
        self._update_threat_level()
        
        # Initialize emergency response
        self._initialize_emergency_response()
        
        return {
            'incident_type': 'nuclear_detonation',
            'ground_zero': ground_zero,
            'yield_kt': yield_kt,
            'initial_radiation': self.radiation_levels.copy(),
            'threat_level': self.threat_level.value,
            'evacuation_zones': list(self.evacuation_zones),
            'timestamp': self.time_since_incident
        }
    
    def _calculate_initial_radiation(self) -> None:
        """Calculate initial radiation levels after detonation."""
        if self.ground_zero is None:
            return
        
        # Radiation intensity based on yield and distance
        for zone in range(self.city_zones):
            distance = self._calculate_distance(self.ground_zero, zone)
            
            # Simplified radiation calculation (inverse square law)
            if distance == 0:
                # Ground zero: lethal radiation
                self.radiation_levels[zone] = 1000.0  # Sv/h
            else:
                # Radiation decreases with distance
                radiation = (self.detonation_yield * 100) / (distance ** 2)
                self.radiation_levels[zone] = min(radiation, 1000.0)
    
    def _calculate_fallout_pattern(self) -> None:
        """Calculate radioactive fallout patterns based on wind."""
        if self.ground_zero is None:
            return
        
        for source in range(self.city_zones):
            for target in range(self.city_zones):
                if source == target:
                    continue
                
                # Calculate fallout deposition
                distance = self._calculate_distance(source, target)
                angle = self._calculate_angle(self.ground_zero, source, target)
                
                # Wind effect on fallout
                wind_factor = self._calculate_wind_effect(angle)
                
                # Fallout intensity
                fallout = (self.detonation_yield * wind_factor) / (distance ** 1.5)
                self.fallout_pattern[source, target] = min(fallout, 100.0)
    
    def _calculate_distance(self, zone1: int, zone2: int) -> float:
        """Calculate distance between two zones (simplified)."""
        # Assuming zones are in a line for simplicity
        return abs(zone1 - zone2) + 1.0
    
    def _calculate_angle(self, reference: int, zone1: int, zone2: int) -> float:
        """Calculate angle between zones relative to wind direction."""
        # Simplified angle calculation
        angle1 = math.degrees(math.atan2(zone1 - reference, 1))
        angle2 = math.degrees(math.atan2(zone2 - reference, 1))
        return abs(angle2 - angle1)
    
    def _calculate_wind_effect(self, angle: float) -> float:
        """Calculate wind effect on fallout dispersion."""
        # Wind carries fallout downwind
        wind_alignment = math.cos(math.radians(angle - self.wind_direction))
        return max(0.1, 1.0 + wind_alignment * self.wind_speed / 10.0)
    
    def _update_threat_level(self) -> None:
        """Update threat level based on radiation levels."""
        max_radiation = np.max(self.radiation_levels)
        
        if max_radiation < 0.1:
            self.threat_level = ThreatLevel.NORMAL
        elif max_radiation < 1.0:
            self.threat_level = ThreatLevel.ELEVATED
        elif max_radiation < 10.0:
            self.threat_level = ThreatLevel.HIGH
        elif max_radiation < 100.0:
            self.threat_level = ThreatLevel.SEVERE
        else:
            self.threat_level = ThreatLevel.CRITICAL
    
    def _initialize_emergency_response(self) -> None:
        """Initialize emergency response protocols."""
        # Evacuate high-radiation zones
        for zone in range(self.city_zones):
            if self.radiation_levels[zone] > 1.0:  # > 1 Sv/h
                self.evacuation_zones.add(zone)
        
        # Allocate medical resources based on population and radiation
        for zone in range(self.city_zones):
            population_factor = 1.0  # Could be zone-specific
            radiation_factor = min(self.radiation_levels[zone] / 10.0, 1.0)
            self.medical_resources[zone] = population_factor * radiation_factor * 100
            
            # Shelter capacity based on zone infrastructure
            self.shelter_capacity[zone] = population_factor * 1000
    
    def update_scenario(self, time_step: float = 0.1) -> Dict:
        """
        Update nuclear scenario over time.
        
        Args:
            time_step: Time step in hours
            
        Returns:
            Updated scenario state
        """
        self.time_since_incident += time_step
        
        # Radiation decay (radioactive decay)
        decay_rate = 0.1  # Simplified decay rate
        self.radiation_levels *= (1.0 - decay_rate * time_step)
        
        # Fallout dispersion
        self._update_fallout_dispersion(time_step)
        
        # Update threat level
        self._update_threat_level()
        
        # Update emergency response
        self._update_emergency_response()
        
        return {
            'time_since_incident': self.time_since_incident,
            'radiation_levels': self.radiation_levels.copy(),
            'threat_level': self.threat_level.value,
            'evacuation_zones': list(self.evacuation_zones),
            'medical_resources': self.medical_resources.copy(),
            'shelter_capacity': self.shelter_capacity.copy()
        }
    
    def _update_fallout_dispersion(self, time_step: float) -> None:
        """Update fallout dispersion over time."""
        # Fallout spreads and decays over time
        dispersion_rate = 0.05
        self.fallout_pattern *= (1.0 - dispersion_rate * time_step)
    
    def _update_emergency_response(self) -> None:
        """Update emergency response based on current conditions."""
        # Dynamic evacuation based on changing radiation levels
        for zone in range(self.city_zones):
            if self.radiation_levels[zone] > 1.0:
                self.evacuation_zones.add(zone)
            elif self.radiation_levels[zone] < 0.1:
                self.evacuation_zones.discard(zone)
    
    def get_zone_safety_status(self, zone: int) -> Dict:
        """
        Get safety status for a specific zone.
        
        Args:
            zone: Zone index
            
        Returns:
            Zone safety information
        """
        radiation = self.radiation_levels[zone]
        is_evacuated = zone in self.evacuation_zones
        
        # Calculate safety recommendations
        if radiation < 0.01:
            safety_status = "SAFE"
            recommendation = "Normal activities permitted"
        elif radiation < 0.1:
            safety_status = "CAUTION"
            recommendation = "Limit outdoor activities"
        elif radiation < 1.0:
            safety_status = "DANGER"
            recommendation = "Seek shelter immediately"
        else:
            safety_status = "CRITICAL"
            recommendation = "Evacuate immediately"
        
        return {
            'zone': zone,
            'radiation_level': radiation,
            'safety_status': safety_status,
            'recommendation': recommendation,
            'is_evacuated': is_evacuated,
            'medical_resources': self.medical_resources[zone],
            'shelter_capacity': self.shelter_capacity[zone]
        }
    
    def set_wind_conditions(self, speed: float, direction: float) -> None:
        """
        Set wind conditions for fallout modeling.
        
        Args:
            speed: Wind speed in m/s
            direction: Wind direction in degrees
        """
        self.wind_speed = speed
        self.wind_direction = direction
    
    def get_emergency_protocols(self) -> Dict[str, List[str]]:
        """
        Get emergency protocols based on current threat level.
        
        Returns:
            Emergency protocols by category
        """
        protocols = {
            'public_safety': [],
            'medical_response': [],
            'infrastructure': [],
            'communication': []
        }
        
        if self.threat_level in [ThreatLevel.HIGH, ThreatLevel.SEVERE, ThreatLevel.CRITICAL]:
            protocols['public_safety'].extend([
                "Activate emergency broadcast system",
                "Implement traffic control for evacuation routes",
                "Deploy radiation monitoring teams"
            ])
            
        if self.threat_level in [ThreatLevel.SEVERE, ThreatLevel.CRITICAL]:
            protocols['medical_response'].extend([
                "Activate mass casualty protocols",
                "Deploy radiation treatment teams",
                "Prepare decontamination centers"
            ])
            
            protocols['infrastructure'].extend([
                "Shut down critical infrastructure in affected zones",
                "Activate backup power systems",
                "Secure water and food supplies"
            ])
            
            protocols['communication'].extend([
                "Activate emergency communication networks",
                "Coordinate with federal agencies",
                "Implement public information hotlines"
            ])
        
        return protocols
    
    def reset_scenario(self) -> None:
        """Reset the nuclear scenario."""
        self.radiation_levels = np.zeros(self.city_zones)
        self.wind_speed = 0.0
        self.wind_direction = 0.0
        self.time_since_incident = 0
        self.threat_level = ThreatLevel.NORMAL
        self.detonation_yield = 0.0
        self.ground_zero = None
        self.fallout_pattern = np.zeros((self.city_zones, self.city_zones))
        self.evacuation_zones.clear()
        self.shelter_capacity = np.zeros(self.city_zones)
        self.medical_resources = np.zeros(self.city_zones)
