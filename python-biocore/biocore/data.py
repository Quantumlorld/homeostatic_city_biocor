"""
BioCore Data Module

Abstract plant and drug database for BHCS simulation.
No real-world medical or chemical data.
"""

from typing import Dict, List, Any
from dataclasses import dataclass
import json


@dataclass
class PlantCompound:
    """Abstract plant compound data structure"""
    name: str
    compounds: List[str]
    potency: float
    properties: Dict[str, float]


@dataclass
class DrugTarget:
    """Abstract drug target data structure"""
    name: str
    pathways: List[str]
    effectiveness: float
    toxicity: float


class PlantDatabase:
    """Abstract plant database for BHCS simulation"""
    
    def __init__(self):
        self._plants = self._initialize_plants()
    
    def _initialize_plants(self) -> Dict[str, PlantCompound]:
        """Initialize abstract plant data"""
        return {
            'Ginkgo': PlantCompound(
                name='Ginkgo',
                compounds=['Ginkgolides', 'Flavonoids'],
                potency=0.7,
                properties={
                    'anti_inflammatory': 0.6,
                    'neuroprotective': 0.8,
                    'immune_modulation': 0.5,
                    'stress_reduction': 0.4
                }
            ),
            'Aloe': PlantCompound(
                name='Aloe',
                compounds=['Aloin', 'Acemannan'],
                potency=0.5,
                properties={
                    'anti_inflammatory': 0.8,
                    'neuroprotective': 0.3,
                    'immune_modulation': 0.6,
                    'stress_reduction': 0.2
                }
            ),
            'Turmeric': PlantCompound(
                name='Turmeric',
                compounds=['Curcumin', 'Turmerone'],
                potency=0.8,
                properties={
                    'anti_inflammatory': 0.9,
                    'neuroprotective': 0.6,
                    'immune_modulation': 0.7,
                    'stress_reduction': 0.5
                }
            ),
            'Ginseng': PlantCompound(
                name='Ginseng',
                compounds=['Ginsenosides'],
                potency=0.6,
                properties={
                    'anti_inflammatory': 0.5,
                    'neuroprotective': 0.7,
                    'immune_modulation': 0.8,
                    'stress_reduction': 0.6
                }
            ),
            'Ashwagandha': PlantCompound(
                name='Ashwagandha',
                compounds=['Withanolides'],
                potency=0.9,
                properties={
                    'anti_inflammatory': 0.7,
                    'neuroprotective': 0.8,
                    'immune_modulation': 0.9,
                    'stress_reduction': 0.9
                }
            )
        }
    
    def get_plant(self, name: str) -> PlantCompound:
        """Get plant data by name"""
        return self._plants.get(name)
    
    def get_all_plants(self) -> List[PlantCompound]:
        """Get all plant data"""
        return list(self._plants.values())
    
    def list_plant_names(self) -> List[str]:
        """List all available plant names"""
        return list(self._plants.keys())


class DrugDatabase:
    """Abstract drug database for BHCS simulation"""
    
    def __init__(self):
        self._drugs = self._initialize_drugs()
    
    def _initialize_drugs(self) -> Dict[str, DrugTarget]:
        """Initialize abstract drug data"""
        return {
            'DrugA': DrugTarget(
                name='DrugA',
                pathways=['COX-2', '5-HT'],
                effectiveness=0.6,
                toxicity=0.1
            ),
            'DrugB': DrugTarget(
                name='DrugB',
                pathways=['NF-κB', 'MAO'],
                effectiveness=0.7,
                toxicity=0.15
            ),
            'DrugC': DrugTarget(
                name='DrugC',
                pathways=['NMDA', 'GABA'],
                effectiveness=0.8,
                toxicity=0.2
            ),
            'DrugD': DrugTarget(
                name='DrugD',
                pathways=['Dopamine', 'Serotonin'],
                effectiveness=0.5,
                toxicity=0.05
            ),
            'DrugE': DrugTarget(
                name='DrugE',
                pathways=['HPA-axis', 'Cortisol'],
                effectiveness=0.9,
                toxicity=0.25
            )
        }
    
    def get_drug(self, name: str) -> DrugTarget:
        """Get drug data by name"""
        return self._drugs.get(name)
    
    def get_all_drugs(self) -> List[DrugTarget]:
        """Get all drug data"""
        return list(self._drugs.values())
    
    def list_drug_names(self) -> List[str]:
        """List all available drug names"""
        return list(self._drugs.keys())
