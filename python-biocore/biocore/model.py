"""
BioCore Model

Abstract biological signal modeling for BHCS simulation.
No real-world biological modeling or medical claims.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
import json
import uuid
from .data import PlantDatabase, DrugDatabase, PlantCompound, DrugTarget
from .pathways import PathwaySimulator, PathwayInteraction


@dataclass
class BioCoreEffect:
    """Abstract BioCore effect data structure"""
    id: str
    zone_id: int
    plant: str
    drug: str
    synergy: float
    magnitude: float
    effects: Dict[str, float]
    timestamp: datetime
    confidence: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            'id': self.id,
            'zone_id': self.zone_id,
            'plant': self.plant,
            'drug': self.drug,
            'synergy': self.synergy,
            'magnitude': self.magnitude,
            'effects': self.effects,
            'timestamp': self.timestamp.isoformat(),
            'confidence': self.confidence
        }


@dataclass
class BioCoreRecommendation:
    """Abstract BioCore recommendation data structure"""
    zone_id: int
    plant: str
    drug: str
    synergy: float
    expected_magnitude: float
    expected_effects: Dict[str, float]
    confidence: float
    rationale: str


class BioCoreModel:
    """Abstract BioCore model for BHCS simulation"""
    
    def __init__(self):
        self.plant_db = PlantDatabase()
        self.drug_db = DrugDatabase()
        self.pathway_sim = PathwaySimulator()
        self.effect_history: List[BioCoreEffect] = []
        self.active_effects: Dict[str, BioCoreEffect] = {}
        
    def calculate_effect(
        self, 
        plant_name: str, 
        drug_name: str, 
        synergy: float
    ) -> BioCoreEffect:
        """Calculate abstract BioCore effect"""
        plant = self.plant_db.get_plant(plant_name)
        drug = self.drug_db.get_drug(drug_name)
        
        if not plant or not drug:
            raise ValueError(f"Unknown plant or drug: {plant_name}, {drug_name}")
        
        # Simulate pathway interactions
        interactions = self.pathway_sim.simulate_interaction(plant, drug, synergy)
        
        # Calculate effect magnitudes
        effects = {
            'calming': self._calculate_calming_effect(plant, drug, interactions),
            'healing': self._calculate_healing_effect(plant, drug, interactions),
            'protection': self._calculate_protection_effect(plant, drug, interactions)
        }
        
        # Overall magnitude
        magnitude = sum(effects.values()) / len(effects)
        
        # Overall confidence
        confidence = self.pathway_sim.calculate_overall_effect(interactions)
        
        effect = BioCoreEffect(
            id=str(uuid.uuid4()),
            zone_id=-1,  # Will be set when applied
            plant=plant_name,
            drug=drug_name,
            synergy=synergy,
            magnitude=magnitude,
            effects=effects,
            timestamp=datetime.now(),
            confidence=confidence
        )
        
        return effect
    
    def _calculate_calming_effect(
        self, 
        plant: PlantCompound, 
        drug: DrugTarget, 
        interactions: List[PathwayInteraction]
    ) -> float:
        """Calculate abstract calming effect"""
        calming_pathways = ['5-HT', 'GABA', 'HPA-axis', 'Cortisol']
        calming_effect = 0.0
        
        for interaction in interactions:
            if interaction.pathway in calming_pathways:
                calming_effect += interaction.effect * interaction.confidence
        
        # Add plant stress reduction property
        calming_effect += plant.properties.get('stress_reduction', 0) * plant.potency
        
        return calming_effect / (len(calming_pathways) + 1)
    
    def _calculate_healing_effect(
        self, 
        plant: PlantCompound, 
        drug: DrugTarget, 
        interactions: List[PathwayInteraction]
    ) -> float:
        """Calculate abstract healing effect"""
        healing_pathways = ['COX-2', 'NF-κB']
        healing_effect = 0.0
        
        for interaction in interactions:
            if interaction.pathway in healing_pathways:
                healing_effect += interaction.effect * interaction.confidence
        
        # Add plant anti-inflammatory property
        healing_effect += plant.properties.get('anti_inflammatory', 0) * plant.potency
        
        return healing_effect / (len(healing_pathways) + 1)
    
    def _calculate_protection_effect(
        self, 
        plant: PlantCompound, 
        drug: DrugTarget, 
        interactions: List[PathwayInteraction]
    ) -> float:
        """Calculate abstract protection effect"""
        protection_pathways = ['MAO', 'Dopamine', 'Serotonin']
        protection_effect = 0.0
        
        for interaction in interactions:
            if interaction.pathway in protection_pathways:
                protection_effect += interaction.effect * interaction.confidence
        
        # Add plant immune modulation property
        protection_effect += plant.properties.get('immune_modulation', 0) * plant.potency
        
        return protection_effect / (len(protection_pathways) + 1)
    
    def get_optimal_for_zone(
        self, 
        zone_activity: float, 
        zone_state: str
    ) -> Optional[BioCoreRecommendation]:
        """Get optimal BioCore recommendation for zone state"""
        best_recommendation = None
        best_score = -1.0
        
        # Try all combinations
        for plant_name in self.plant_db.list_plant_names():
            for drug_name in self.drug_db.list_drug_names():
                for synergy in [0.5, 0.7, 0.9]:
                    try:
                        effect = self.calculate_effect(plant_name, drug_name, synergy)
                        score = self._score_effect_for_zone(effect, zone_activity, zone_state)
                        
                        if score > best_score:
                            best_score = score
                            best_recommendation = BioCoreRecommendation(
                                zone_id=-1,  # Will be set by caller
                                plant=plant_name,
                                drug=drug_name,
                                synergy=synergy,
                                expected_magnitude=effect.magnitude,
                                expected_effects=effect.effects,
                                confidence=effect.confidence,
                                rationale=self._generate_rationale(effect, zone_state)
                            )
                    except ValueError:
                        continue
        
        return best_recommendation
    
    def _score_effect_for_zone(
        self, 
        effect: BioCoreEffect, 
        zone_activity: float, 
        zone_state: str
    ) -> float:
        """Score effect for specific zone state"""
        score = 0.0
        
        if zone_state in ['OVERSTIMULATED', 'EMERGENT', 'CRITICAL']:
            # Prioritize calming effects
            score += effect.effects.get('calming', 0) * 2.0
            score += effect.effects.get('protection', 0) * 1.5
            score += effect.effects.get('healing', 0) * 1.0
        else:
            # For calm zones, prioritize balance
            score += effect.magnitude
            score += effect.confidence * 0.5
        
        # Adjust based on zone activity
        if zone_activity > 0.7:
            score *= 1.5  # Boost score for overstimulated zones
        elif zone_activity < 0.3:
            score *= 0.8  # Reduce score for very calm zones
        
        return score
    
    def _generate_rationale(self, effect: BioCoreEffect, zone_state: str) -> str:
        """Generate rationale for recommendation"""
        rationales = {
            'OVERSTIMULATED': f"Strong calming effect ({effect.effects.get('calming', 0):.2f}) with high confidence ({effect.confidence:.2f})",
            'EMERGENT': f"Balanced healing and protection ({effect.effects.get('healing', 0):.2f}, {effect.effects.get('protection', 0):.2f})",
            'CRITICAL': f"Maximum strength intervention ({effect.magnitude:.2f}) for immediate stabilization",
            'CALM': f"Maintenance effect ({effect.magnitude:.2f}) for optimal balance"
        }
        
        return rationales.get(zone_state, "General homeostatic support")
    
    def apply_effect(self, zone_id: int, effect: BioCoreEffect) -> None:
        """Apply effect to zone (record only)"""
        effect.zone_id = zone_id
        self.active_effects[effect.id] = effect
        self.effect_history.append(effect)
        
        # Keep history manageable
        if len(self.effect_history) > 1000:
            self.effect_history = self.effect_history[-500:]
    
    def get_active_effects(self) -> List[BioCoreEffect]:
        """Get currently active effects"""
        return list(self.active_effects.values())
    
    def get_effect_history(self) -> List[BioCoreEffect]:
        """Get effect history"""
        return self.effect_history.copy()
    
    def decay_effects(self, decay_rate: float = 0.05) -> None:
        """Decay active effects over time"""
        expired_effects = []
        
        for effect_id, effect in self.active_effects.items():
            # Random decay simulation
            if np.random.random() < decay_rate:
                expired_effects.append(effect_id)
        
        for effect_id in expired_effects:
            del self.active_effects[effect_id]
    
    def get_analytics(self) -> Dict[str, Any]:
        """Get analytics data"""
        if not self.effect_history:
            return {}
        
        # Plant usage statistics
        plant_usage = {}
        drug_usage = {}
        total_synergy = 0.0
        
        for effect in self.effect_history:
            plant_usage[effect.plant] = plant_usage.get(effect.plant, 0) + 1
            drug_usage[effect.drug] = drug_usage.get(effect.drug, 0) + 1
            total_synergy += effect.synergy
        
        return {
            'total_effects': len(self.effect_history),
            'average_synergy': total_synergy / len(self.effect_history),
            'most_used_plant': max(plant_usage.items(), key=lambda x: x[1])[0] if plant_usage else None,
            'most_used_drug': max(drug_usage.items(), key=lambda x: x[1])[0] if drug_usage else None,
            'active_effects': len(self.active_effects),
            'plant_usage': plant_usage,
            'drug_usage': drug_usage
        }
    
    def reset(self) -> None:
        """Reset model state"""
        self.effect_history.clear()
        self.active_effects.clear()
