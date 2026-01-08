"""
🌊 BioCore Effects - Biological Effect Definitions
Standardized effect types and impact calculations
"""

from enum import Enum
from dataclasses import dataclass
from typing import List, Dict, Optional
import numpy as np

class EffectType(Enum):
    """Types of biological effects"""
    CALMING = "calming"
    ACTIVATING = "activating"
    BALANCING = "balancing"
    STABILIZING = "stabilizing"
    ENHANCING = "enhancing"
    MODULATING = "modulating"

class TargetZone(Enum):
    """Target zones for effects"""
    DOWNTOWN = 0
    INDUSTRIAL = 1
    RESIDENTIAL = 2
    COMMERCIAL = 3
    PARKS = 4

@dataclass
class BioCoreEffect:
    """Comprehensive BioCore effect definition"""
    magnitude: float
    effects: List[str]
    confidence: float
    duration: int
    target_zones: List[int]
    effect_type: EffectType
    plant_source: str
    drug_source: str
    synergy_level: float
    
    def __post_init__(self):
        """Determine effect type from magnitude and effects"""
        if self.magnitude < -0.1:
            self.effect_type = EffectType.CALMING
        elif self.magnitude > 0.1:
            self.effect_type = EffectType.ACTIVATING
        else:
            self.effect_type = EffectType.BALANCING

@dataclass
class PlantEffect:
    """Plant-specific biological effect"""
    name: str
    calming_factor: float
    activation_factor: float
    synergy_potential: float
    primary_effects: List[str]
    secondary_effects: List[str]
    contraindications: List[str]

@dataclass
class DrugEffect:
    """Drug-specific biological effect"""
    name: str
    potency: float
    targeting_precision: float
    side_effect_risk: float
    primary_effects: List[str]
    secondary_effects: List[str]
    interactions: List[str]

class EffectCalculator:
    """Advanced effect calculation utilities"""
    
    @staticmethod
    def calculate_zone_impact(effect: BioCoreEffect, zone_activity: float) -> float:
        """Calculate impact of effect on specific zone activity"""
        # Base impact
        base_impact = effect.magnitude * effect.synergy_level
        
        # Modulate by zone current state
        if zone_activity > 0.7:  # Overstimulated
            if effect.effect_type == EffectType.CALMING:
                base_impact *= 1.5  # Enhanced effect on overstimulated zones
            elif effect.effect_type == EffectType.ACTIVATING:
                base_impact *= 0.5  # Reduced effect on overstimulated zones
        elif zone_activity < 0.3:  # Understimulated
            if effect.effect_type == EffectType.ACTIVATING:
                base_impact *= 1.5  # Enhanced effect on calm zones
            elif effect.effect_type == EffectType.CALMING:
                base_impact *= 0.5  # Reduced effect on calm zones
        
        # Apply confidence factor
        return base_impact * effect.confidence
    
    @staticmethod
    def calculate_system_wide_impact(effects: List[BioCoreEffect], 
                                  zone_activities: List[float]) -> Dict[int, float]:
        """Calculate system-wide impact of multiple effects"""
        zone_impacts = {}
        
        for zone_id, activity in enumerate(zone_activities):
            total_impact = 0.0
            
            for effect in effects:
                if zone_id in effect.target_zones:
                    impact = EffectCalculator.calculate_zone_impact(effect, activity)
                    total_impact += impact
            
            # Apply saturation limits
            total_impact = np.clip(total_impact, -0.3, 0.3)
            zone_impacts[zone_id] = total_impact
        
        return zone_impacts
    
    @staticmethod
    def predict_effect_evolution(effect: BioCoreEffect, 
                             time_steps: int = 10) -> List[float]:
        """Predict how effect magnitude evolves over time"""
        evolution = []
        current_magnitude = effect.magnitude
        
        for t in range(time_steps):
            # Exponential decay with time constant based on duration
            decay_factor = np.exp(-t / (effect.duration / 10))
            evolved_magnitude = current_magnitude * decay_factor
            evolution.append(evolved_magnitude)
        
        return evolution
    
    @staticmethod
    def calculate_effect_synergy(effects: List[BioCoreEffect]) -> float:
        """Calculate overall synergy between multiple effects"""
        if len(effects) < 2:
            return 0.0
        
        synergy_score = 0.0
        
        for i, effect1 in enumerate(effects):
            for effect2 in effects[i+1:]:
                # Complementary effects get higher synergy
                if (effect1.effect_type == EffectType.CALMING and 
                    effect2.effect_type == EffectType.BALANCING):
                    synergy_score += 0.2
                elif (effect1.effect_type == EffectType.ACTIVATING and 
                      effect2.effect_type == EffectType.ENHANCING):
                    synergy_score += 0.2
                elif effect1.effect_type == effect2.effect_type:
                    synergy_score += 0.1  # Same type effects have some synergy
                
                # Add synergy level contribution
                synergy_score += (effect1.synergy_level + effect2.synergy_level) / 4
        
        return min(synergy_score, 1.0)
    
    @staticmethod
    def assess_effect_safety(effects: List[BioCoreEffect]) -> Dict[str, float]:
        """Assess safety profile of effects"""
        safety_metrics = {
            "overall_risk": 0.0,
            "contradiction_risk": 0.0,
            "overstimulation_risk": 0.0,
            "side_effect_risk": 0.0
        }
        
        activating_count = sum(1 for e in effects if e.effect_type == EffectType.ACTIVATING)
        calming_count = sum(1 for e in effects if e.effect_type == EffectType.CALMING)
        
        # Contradiction risk (opposing effects)
        if activating_count > 0 and calming_count > 0:
            safety_metrics["contradiction_risk"] = min(activating_count, calming_count) * 0.2
        
        # Overstimulation risk
        if activating_count > 2:
            safety_metrics["overstimulation_risk"] = (activating_count - 2) * 0.3
        
        # Side effect risk from low confidence
        avg_confidence = np.mean([e.confidence for e in effects])
        safety_metrics["side_effect_risk"] = (1 - avg_confidence) * 0.5
        
        # Overall risk
        safety_metrics["overall_risk"] = sum(safety_metrics.values()) / len(safety_metrics)
        
        return safety_metrics

class EffectDatabase:
    """Database of standard effects and their properties"""
    
    STANDARD_EFFECTS = {
        "stress_reduction": {
            "type": EffectType.CALMING,
            "typical_magnitude": -0.15,
            "duration_range": (60, 120),
            "target_zones": [1, 3]  # Industrial, Commercial
        },
        "energy_boost": {
            "type": EffectType.ACTIVATING,
            "typical_magnitude": 0.2,
            "duration_range": (45, 90),
            "target_zones": [0, 2, 4]  # Downtown, Residential, Parks
        },
        "immune_modulation": {
            "type": EffectType.BALANCING,
            "typical_magnitude": 0.05,
            "duration_range": (90, 180),
            "target_zones": list(range(5))  # All zones
        },
        "cognitive_enhancement": {
            "type": EffectType.ENHANCING,
            "typical_magnitude": 0.15,
            "duration_range": (60, 120),
            "target_zones": [0, 2]  # Downtown, Residential
        },
        "anti_inflammatory": {
            "type": EffectType.STABILIZING,
            "typical_magnitude": -0.1,
            "duration_range": (120, 240),
            "target_zones": [1, 3]  # Industrial, Commercial
        }
    }
    
    @classmethod
    def get_effect_info(cls, effect_name: str) -> Optional[Dict]:
        """Get information about a standard effect"""
        return cls.STANDARD_EFFECTS.get(effect_name)
    
    @classmethod
    def get_all_effects(cls) -> Dict[str, Dict]:
        """Get all standard effects"""
        return cls.STANDARD_EFFECTS.copy()
