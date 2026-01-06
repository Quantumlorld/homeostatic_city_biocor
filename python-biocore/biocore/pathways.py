"""
BioCore Pathway Simulator

Abstract pathway modeling for BHCS simulation.
No real-world biological pathways or medical claims.
"""

from typing import Dict, List, Tuple
from dataclasses import dataclass
import numpy as np
from .data import PlantCompound, DrugTarget


@dataclass
class PathwayInteraction:
    """Abstract pathway interaction result"""
    pathway: str
    effect: float
    confidence: float


class PathwaySimulator:
    """Abstract pathway simulator for BHCS"""
    
    def __init__(self):
        self._pathway_weights = self._initialize_pathway_weights()
    
    def _initialize_pathway_weights(self) -> Dict[str, float]:
        """Initialize abstract pathway interaction weights"""
        return {
            'COX-2': 0.8,
            '5-HT': 0.7,
            'NF-κB': 0.9,
            'MAO': 0.6,
            'NMDA': 0.8,
            'GABA': 0.7,
            'Dopamine': 0.6,
            'Serotonin': 0.7,
            'HPA-axis': 0.9,
            'Cortisol': 0.8
        }
    
    def calculate_pathway_compatibility(
        self, 
        plant: PlantCompound, 
        drug: DrugTarget
    ) -> float:
        """Calculate abstract pathway compatibility between plant and drug"""
        plant_score = (
            plant.properties.get('anti_inflammatory', 0) +
            plant.properties.get('neuroprotective', 0) +
            plant.properties.get('immune_modulation', 0) +
            plant.properties.get('stress_reduction', 0)
        ) / 4.0
        
        drug_score = (drug.effectiveness + (1.0 - drug.toxicity)) / 2.0
        
        # Pathway overlap calculation
        pathway_overlap = self._calculate_pathway_overlap(plant, drug)
        
        return (plant_score + drug_score + pathway_overlap) / 3.0
    
    def _calculate_pathway_overlap(
        self, 
        plant: PlantCompound, 
        drug: DrugTarget
    ) -> float:
        """Calculate abstract pathway overlap"""
        # Simplified pathway overlap calculation
        plant_pathways = ['inflammation', 'neural', 'immune', 'stress']
        drug_pathways = drug.pathways
        
        overlap_count = 0
        for pathway in drug_pathways:
            if any(p in pathway.lower() for p in plant_pathways):
                overlap_count += 1
        
        return overlap_count / max(len(drug_pathways), 1)
    
    def simulate_interaction(
        self, 
        plant: PlantCompound, 
        drug: DrugTarget, 
        synergy: float
    ) -> List[PathwayInteraction]:
        """Simulate abstract pathway interactions"""
        interactions = []
        
        # Calculate base effect magnitude
        base_effect = (plant.potency + drug.effectiveness) / 2.0
        compatibility = self.calculate_pathway_compatibility(plant, drug)
        final_effect = base_effect * compatibility * synergy
        
        # Generate pathway-specific interactions
        for pathway in drug.pathways:
            pathway_weight = self._pathway_weights.get(pathway, 0.5)
            pathway_effect = final_effect * pathway_weight
            
            # Calculate confidence based on plant properties
            confidence = self._calculate_confidence(plant, drug, pathway)
            
            interactions.append(PathwayInteraction(
                pathway=pathway,
                effect=pathway_effect,
                confidence=confidence
            ))
        
        return interactions
    
    def _calculate_confidence(
        self, 
        plant: PlantCompound, 
        drug: DrugTarget, 
        pathway: str
    ) -> float:
        """Calculate confidence score for pathway interaction"""
        # Simplified confidence calculation
        base_confidence = 0.7
        
        # Adjust based on plant properties
        if 'inflammation' in pathway.lower():
            base_confidence += plant.properties.get('anti_inflammatory', 0) * 0.2
        elif 'neural' in pathway.lower() or '5-HT' in pathway or 'NMDA' in pathway:
            base_confidence += plant.properties.get('neuroprotective', 0) * 0.2
        elif 'immune' in pathway.lower():
            base_confidence += plant.properties.get('immune_modulation', 0) * 0.2
        elif 'stress' in pathway.lower() or 'HPA' in pathway or 'Cortisol' in pathway:
            base_confidence += plant.properties.get('stress_reduction', 0) * 0.2
        
        # Adjust based on drug effectiveness
        base_confidence += drug.effectiveness * 0.1
        
        # Adjust based on drug toxicity (lower toxicity = higher confidence)
        base_confidence += (1.0 - drug.toxicity) * 0.1
        
        return min(base_confidence, 1.0)
    
    def get_optimal_pathways(
        self, 
        interactions: List[PathwayInteraction]
    ) -> List[PathwayInteraction]:
        """Get most effective pathway interactions"""
        return sorted(interactions, key=lambda x: x.effect * x.confidence, reverse=True)
    
    def calculate_overall_effect(
        self, 
        interactions: List[PathwayInteraction]
    ) -> float:
        """Calculate overall effect from pathway interactions"""
        if not interactions:
            return 0.0
        
        total_effect = sum(interaction.effect * interaction.confidence 
                       for interaction in interactions)
        total_confidence = sum(interaction.confidence for interaction in interactions)
        
        return total_effect / max(total_confidence, 0.1)
