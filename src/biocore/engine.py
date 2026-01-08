"""
🧬 BioCore Engine - Plant-Drug Synergy Calculator
Advanced biological effect modeling for homeostatic city zones
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import json

@dataclass
class BioCoreEffect:
    """Represents a calculated BioCore effect"""
    magnitude: float
    effects: List[str]
    confidence: float
    duration: int
    target_zones: List[int]
    
@dataclass
class PlantProfile:
    """Plant biological profile"""
    name: str
    calming_factor: float
    activation_factor: float
    synergy_potential: float
    primary_effects: List[str]
    
@dataclass
class DrugProfile:
    """Drug biological profile"""
    name: str
    potency: float
    targeting_precision: float
    side_effect_risk: float
    primary_effects: List[str]

class BioCoreEngine:
    """Advanced BioCore effect calculation engine"""
    
    def __init__(self):
        self.plants = self._initialize_plants()
        self.drugs = self._initialize_drugs()
        self.synergy_matrix = self._calculate_synergy_matrix()
        
    def _initialize_plants(self) -> Dict[str, PlantProfile]:
        """Initialize plant database with biological profiles"""
        return {
            "Ashwagandha": PlantProfile(
                name="Ashwagandha",
                calming_factor=0.8,
                activation_factor=0.3,
                synergy_potential=0.9,
                primary_effects=["stress_reduction", "cortisol_regulation", "homeostasis"]
            ),
            "Turmeric": PlantProfile(
                name="Turmeric",
                calming_factor=0.6,
                activation_factor=0.4,
                synergy_potential=0.85,
                primary_effects=["anti_inflammatory", "antioxidant", "immune_modulation"]
            ),
            "Ginseng": PlantProfile(
                name="Ginseng",
                calming_factor=0.4,
                activation_factor=0.8,
                synergy_potential=0.8,
                primary_effects=["energy_boost", "cognitive_enhancement", "adaptogen"]
            ),
            "Bacopa": PlantProfile(
                name="Bacopa",
                calming_factor=0.7,
                activation_factor=0.5,
                synergy_potential=0.75,
                primary_effects=["memory_enhancement", "neuroprotection", "learning"]
            ),
            "Rhodiola": PlantProfile(
                name="Rhodiola",
                calming_factor=0.5,
                activation_factor=0.9,
                synergy_potential=0.85,
                primary_effects=["fatigue_reduction", "stress_resistance", "performance"]
            )
        }
    
    def _initialize_drugs(self) -> Dict[str, DrugProfile]:
        """Initialize drug database with biological profiles"""
        return {
            "DrugA": DrugProfile(
                name="DrugA",
                potency=0.8,
                targeting_precision=0.9,
                side_effect_risk=0.1,
                primary_effects=["targeted_activation", "precision_modulation"]
            ),
            "DrugB": DrugProfile(
                name="DrugB",
                potency=0.7,
                targeting_precision=0.85,
                side_effect_risk=0.15,
                primary_effects=["broad_stabilization", "system_balance"]
            ),
            "DrugC": DrugProfile(
                name="DrugC",
                potency=0.9,
                targeting_precision=0.7,
                side_effect_risk=0.2,
                primary_effects=["strong_activation", "rapid_response"]
            ),
            "DrugD": DrugProfile(
                name="DrugD",
                potency=0.6,
                targeting_precision=0.95,
                side_effect_risk=0.05,
                primary_effects=["gentle_modulation", "fine_tuning"]
            ),
            "DrugE": DrugProfile(
                name="DrugE",
                potency=0.85,
                targeting_precision=0.8,
                side_effect_risk=0.12,
                primary_effects=["enhanced_synergy", "amplified_effects"]
            )
        }
    
    def _calculate_synergy_matrix(self) -> np.ndarray:
        """Calculate plant-drug synergy matrix"""
        n_plants = len(self.plants)
        n_drugs = len(self.drugs)
        matrix = np.zeros((n_plants, n_drugs))
        
        plant_names = list(self.plants.keys())
        drug_names = list(self.drugs.keys())
        
        for i, plant_name in enumerate(plant_names):
            for j, drug_name in enumerate(drug_names):
                plant = self.plants[plant_name]
                drug = self.drugs[drug_name]
                
                # Calculate synergy based on complementary properties
                base_synergy = (plant.synergy_potential + drug.potency) / 2
                
                # Modulate by targeting precision and side effect risk
                precision_bonus = drug.targeting_precision * 0.2
                risk_penalty = drug.side_effect_risk * 0.3
                
                # Add some biological compatibility factors
                compatibility = self._calculate_compatibility(plant, drug)
                
                matrix[i, j] = base_synergy + precision_bonus - risk_penalty + compatibility
                
        return np.clip(matrix, 0.0, 1.0)
    
    def _calculate_compatibility(self, plant: PlantProfile, drug: DrugProfile) -> float:
        """Calculate biological compatibility between plant and drug"""
        # Simplified compatibility calculation
        if "stress_reduction" in plant.primary_effects and "broad_stabilization" in drug.primary_effects:
            return 0.2
        elif "energy_boost" in plant.primary_effects and "strong_activation" in drug.primary_effects:
            return 0.15
        elif "anti_inflammatory" in plant.primary_effects and "precision_modulation" in drug.primary_effects:
            return 0.1
        else:
            return 0.05
    
    def calculate_effect(self, plant_name: str, drug_name: str, synergy_level: float = 0.5) -> BioCoreEffect:
        """Calculate BioCore effect for plant-drug combination"""
        
        if plant_name not in self.plants:
            raise ValueError(f"Plant '{plant_name}' not found in database")
        if drug_name not in self.drugs:
            raise ValueError(f"Drug '{drug_name}' not found in database")
        
        plant = self.plants[plant_name]
        drug = self.drugs[drug_name]
        
        # Get base synergy from matrix
        plant_idx = list(self.plants.keys()).index(plant_name)
        drug_idx = list(self.drugs.keys()).index(drug_name)
        base_synergy = self.synergy_matrix[plant_idx, drug_idx]
        
        # Apply user-specified synergy level
        adjusted_synergy = base_synergy * synergy_level
        
        # Calculate effect magnitude
        calming_effect = plant.calming_factor * drug.potency * adjusted_synergy
        activation_effect = plant.activation_factor * drug.potency * adjusted_synergy
        
        # Overall magnitude (can be positive for activation, negative for calming)
        magnitude = (activation_effect - calming_effect) * 0.5
        
        # Generate effect descriptions
        effects = []
        if magnitude < -0.1:
            effects.append("calming")
            effects.extend([e for e in plant.primary_effects if "stress" in e or "calm" in e])
        elif magnitude > 0.1:
            effects.append("activating")
            effects.extend([e for e in plant.primary_effects if "energy" in e or "boost" in e])
        else:
            effects.append("balancing")
            effects.extend([e for e in plant.primary_effects if "balance" in e or "modulation" in e])
        
        # Add drug effects
        effects.extend(drug.primary_effects[:2])  # Add top 2 drug effects
        
        # Calculate confidence based on targeting precision and synergy
        confidence = (drug.targeting_precision * 0.6 + adjusted_synergy * 0.4)
        
        # Duration based on potency and synergy
        duration = int(60 * (1 + drug.potency * adjusted_synergy))  # 60-120 seconds
        
        # Determine target zones (simplified - could be more sophisticated)
        if magnitude < -0.2:
            target_zones = [1, 3]  # Overstimulated zones
        elif magnitude > 0.2:
            target_zones = [0, 2, 4]  # Calm zones
        else:
            target_zones = list(range(5))  # All zones
        
        return BioCoreEffect(
            magnitude=magnitude,
            effects=effects,
            confidence=confidence,
            duration=duration,
            target_zones=target_zones
        )
    
    def get_recommendations(self, zone_states: List[str]) -> List[Tuple[str, str, float]]:
        """Get plant-drug recommendations based on zone states"""
        recommendations = []
        
        # Count zone states
        state_counts = {}
        for state in zone_states:
            state_counts[state] = state_counts.get(state, 0) + 1
        
        # If many overstimulated zones, recommend calming combinations
        if state_counts.get("OVERSTIMULATED", 0) >= 2:
            for plant_name in self.plants:
                if self.plants[plant_name].calming_factor > 0.6:
                    for drug_name in self.drugs:
                        if self.drugs[drug_name].targeting_precision > 0.8:
                            plant_idx = list(self.plants.keys()).index(plant_name)
                            drug_idx = list(self.drugs.keys()).index(drug_name)
                            synergy = self.synergy_matrix[plant_idx, drug_idx]
                            if synergy > 0.7:
                                recommendations.append((plant_name, drug_name, synergy))
        
        # If many calm zones, recommend activating combinations
        elif state_counts.get("CALM", 0) >= 3:
            for plant_name in self.plants:
                if self.plants[plant_name].activation_factor > 0.6:
                    for drug_name in self.drugs:
                        if self.drugs[drug_name].potency > 0.7:
                            plant_idx = list(self.plants.keys()).index(plant_name)
                            drug_idx = list(self.drugs.keys()).index(drug_name)
                            synergy = self.synergy_matrix[plant_idx, drug_idx]
                            if synergy > 0.7:
                                recommendations.append((plant_name, drug_name, synergy))
        
        # Sort by synergy and return top 5
        recommendations.sort(key=lambda x: x[2], reverse=True)
        return recommendations[:5]
    
    def get_plant_info(self, plant_name: str) -> Optional[PlantProfile]:
        """Get plant profile information"""
        return self.plants.get(plant_name)
    
    def get_drug_info(self, drug_name: str) -> Optional[DrugProfile]:
        """Get drug profile information"""
        return self.drugs.get(drug_name)
    
    def export_database(self) -> Dict:
        """Export BioCore database as JSON"""
        return {
            "plants": {name: {
                "calming_factor": plant.calming_factor,
                "activation_factor": plant.activation_factor,
                "synergy_potential": plant.synergy_potential,
                "primary_effects": plant.primary_effects
            } for name, plant in self.plants.items()},
            "drugs": {name: {
                "potency": drug.potency,
                "targeting_precision": drug.targeting_precision,
                "side_effect_risk": drug.side_effect_risk,
                "primary_effects": drug.primary_effects
            } for name, drug in self.drugs.items()},
            "synergy_matrix": self.synergy_matrix.tolist()
        }
