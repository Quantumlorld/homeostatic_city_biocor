"""
BHCS Python BioCore Module

Abstract biological and environmental signal modeling for BHCS.
Simulation and recommendation only - no real-world treatment or execution.
"""

from .data import PlantDatabase, DrugDatabase
from .pathways import PathwaySimulator
from .model import BioCoreModel
from .engine import BioCoreEngine
from .interface import BioCoreInterface

__version__ = "0.1.0"
__author__ = "BHCS Team"
__email__ = "team@bhcs.org"

__all__ = [
    "PlantDatabase",
    "DrugDatabase", 
    "PathwaySimulator",
    "BioCoreModel",
    "BioCoreEngine",
    "BioCoreInterface",
]
