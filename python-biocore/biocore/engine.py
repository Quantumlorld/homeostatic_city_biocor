"""
BioCore Engine

Abstract biological signal processing engine for BHCS simulation.
No real-world biological processing or medical claims.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import time
import threading
from .model import BioCoreModel, BioCoreEffect, BioCoreRecommendation
from .data import PlantDatabase, DrugDatabase


@dataclass
class EngineConfig:
    """BioCore engine configuration"""
    update_interval: float = 1.0
    decay_rate: float = 0.05
    max_active_effects: int = 100
    enable_learning: bool = True


class BioCoreEngine:
    """Abstract BioCore processing engine for BHCS"""
    
    def __init__(self, config: Optional[EngineConfig] = None):
        self.config = config or EngineConfig()
        self.model = BioCoreModel()
        self.is_running = False
        self.update_thread: Optional[threading.Thread] = None
        self.last_update = time.time()
        
    def start(self) -> None:
        """Start the BioCore engine"""
        if self.is_running:
            return
        
        self.is_running = True
        self.update_thread = threading.Thread(target=self._update_loop, daemon=True)
        self.update_thread.start()
    
    def stop(self) -> None:
        """Stop the BioCore engine"""
        self.is_running = False
        if self.update_thread:
            self.update_thread.join(timeout=2.0)
    
    def _update_loop(self) -> None:
        """Main update loop"""
        while self.is_running:
            try:
                self._update()
                time.sleep(self.config.update_interval)
            except Exception as e:
                print(f"BioCore engine update error: {e}")
    
    def _update(self) -> None:
        """Internal update method"""
        # Decay active effects
        self.model.decay_effects(self.config.decay_rate)
        
        # Limit active effects
        if len(self.model.get_active_effects()) > self.config.max_active_effects:
            self._cleanup_old_effects()
        
        self.last_update = time.time()
    
    def _cleanup_old_effects(self) -> None:
        """Clean up oldest effects"""
        active_effects = self.model.get_active_effects()
        
        # Sort by timestamp and keep only the most recent
        active_effects.sort(key=lambda x: x.timestamp, reverse=True)
        
        # Keep only the newest effects
        recent_effects = active_effects[:self.config.max_active_effects]
        
        # Update active effects
        self.model.active_effects.clear()
        for effect in recent_effects:
            self.model.active_effects[effect.id] = effect
    
    def calculate_effect(
        self, 
        plant_name: str, 
        drug_name: str, 
        synergy: float
    ) -> BioCoreEffect:
        """Calculate BioCore effect"""
        return self.model.calculate_effect(plant_name, drug_name, synergy)
    
    def apply_effect(
        self, 
        zone_id: int, 
        plant_name: str, 
        drug_name: str, 
        synergy: float
    ) -> bool:
        """Apply BioCore effect to zone"""
        try:
            effect = self.calculate_effect(plant_name, drug_name, synergy)
            self.model.apply_effect(zone_id, effect)
            return True
        except Exception as e:
            print(f"Failed to apply effect: {e}")
            return False
    
    def get_recommendation(
        self, 
        zone_id: int, 
        zone_activity: float, 
        zone_state: str
    ) -> Optional[BioCoreRecommendation]:
        """Get BioCore recommendation for zone"""
        recommendation = self.model.get_optimal_for_zone(zone_activity, zone_state)
        
        if recommendation:
            recommendation.zone_id = zone_id
        
        return recommendation
    
    def get_active_effects(self) -> List[BioCoreEffect]:
        """Get currently active effects"""
        return self.model.get_active_effects()
    
    def get_effect_history(self) -> List[BioCoreEffect]:
        """Get effect history"""
        return self.model.get_effect_history()
    
    def get_analytics(self) -> Dict[str, Any]:
        """Get engine analytics"""
        analytics = self.model.get_analytics()
        analytics.update({
            'is_running': self.is_running,
            'last_update': self.last_update,
            'update_interval': self.config.update_interval,
            'decay_rate': self.config.decay_rate,
            'max_active_effects': self.config.max_active_effects
        })
        return analytics
    
    def get_status(self) -> Dict[str, Any]:
        """Get engine status"""
        return {
            'running': self.is_running,
            'last_update': self.last_update,
            'active_effects': len(self.model.get_active_effects()),
            'total_effects': len(self.model.get_effect_history()),
            'uptime': time.time() - (self.last_update - self.config.update_interval) if self.is_running else 0
        }
    
    def reset(self) -> None:
        """Reset engine state"""
        self.model.reset()
        self.last_update = time.time()
    
    def get_available_plants(self) -> List[str]:
        """Get list of available plants"""
        return self.model.plant_db.list_plant_names()
    
    def get_available_drugs(self) -> List[str]:
        """Get list of available drugs"""
        return self.model.drug_db.list_drug_names()
    
    def validate_combination(
        self, 
        plant_name: str, 
        drug_name: str, 
        synergy: float
    ) -> bool:
        """Validate plant-drug combination"""
        # Check if plant exists
        if not self.model.plant_db.get_plant(plant_name):
            return False
        
        # Check if drug exists
        if not self.model.drug_db.get_drug(drug_name):
            return False
        
        # Check synergy range
        if not (0.0 <= synergy <= 1.0):
            return False
        
        return True
