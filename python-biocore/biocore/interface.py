"""
BioCore Interface

Abstract interface for BHCS BioCore communication.
No real-world API endpoints or medical device interfaces.
"""

from typing import Dict, List, Any, Optional
import requests
import json
from .engine import BioCoreEngine, EngineConfig
from .model import BioCoreEffect, BioCoreRecommendation


class BioCoreInterface:
    """Abstract interface for BHCS BioCore communication"""
    
    def __init__(self, engine: Optional[BioCoreEngine] = None, rust_api_url: str = "http://localhost:3030"):
        self.engine = engine or BioCoreEngine()
        self.rust_api_url = rust_api_url
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'BHCS-BioCore/0.1.0'
        })
    
    def start_engine(self) -> bool:
        """Start BioCore engine"""
        try:
            self.engine.start()
            return True
        except Exception as e:
            print(f"Failed to start BioCore engine: {e}")
            return False
    
    def stop_engine(self) -> bool:
        """Stop BioCore engine"""
        try:
            self.engine.stop()
            return True
        except Exception as e:
            print(f"Failed to stop BioCore engine: {e}")
            return False
    
    def get_rust_state(self) -> Optional[Dict[str, Any]]:
        """Get current state from Rust engine"""
        try:
            response = self.session.get(f"{self.rust_api_url}/state", timeout=5.0)
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"Failed to get Rust state: {e}")
            return None
    
    def apply_rust_influence(self, zone_id: int, influence: float) -> bool:
        """Apply influence to Rust engine"""
        try:
            data = {
                "zone_id": zone_id,
                "influence": influence
            }
            response = self.session.post(
                f"{self.rust_api_url}/influence", 
                json=data, 
                timeout=5.0
            )
            return response.status_code == 200
        except Exception as e:
            print(f"Failed to apply Rust influence: {e}")
            return False
    
    def get_rust_health(self) -> Optional[Dict[str, Any]]:
        """Get health status from Rust engine"""
        try:
            response = self.session.get(f"{self.rust_api_url}/health", timeout=5.0)
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"Failed to get Rust health: {e}")
            return None
    
    def calculate_biocore_effect(
        self, 
        plant_name: str, 
        drug_name: str, 
        synergy: float
    ) -> Optional[BioCoreEffect]:
        """Calculate BioCore effect"""
        try:
            return self.engine.calculate_effect(plant_name, drug_name, synergy)
        except Exception as e:
            print(f"Failed to calculate BioCore effect: {e}")
            return None
    
    def apply_biocore_effect(
        self, 
        zone_id: int, 
        plant_name: str, 
        drug_name: str, 
        synergy: float
    ) -> bool:
        """Apply BioCore effect to zone"""
        # Apply to local engine
        if not self.engine.apply_effect(zone_id, plant_name, drug_name, synergy):
            return False
        
        # Apply influence to Rust engine
        effect = self.engine.calculate_effect(plant_name, drug_name, synergy)
        if effect:
            return self.apply_rust_influence(zone_id, effect.magnitude)
        
        return False
    
    def get_zone_recommendation(
        self, 
        zone_id: int
    ) -> Optional[BioCoreRecommendation]:
        """Get BioCore recommendation for zone"""
        # Get zone state from Rust
        rust_state = self.get_rust_state()
        if not rust_state or 'zones' not in rust_state:
            return None
        
        # Find the zone
        zone_data = None
        for zone in rust_state['zones']:
            if zone.get('id') == zone_id:
                zone_data = zone
                break
        
        if not zone_data:
            return None
        
        # Get recommendation
        return self.engine.get_recommendation(
            zone_id, 
            zone_data.get('activity', 0.5), 
            zone_data.get('state', 'CALM')
        )
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        status = {
            'biocore_engine': self.engine.get_status(),
            'rust_connection': self._test_rust_connection(),
            'active_effects': len(self.engine.get_active_effects()),
            'total_effects': len(self.engine.get_effect_history())
        }
        
        # Add Rust state if available
        rust_state = self.get_rust_state()
        if rust_state:
            status['rust_state'] = rust_state
        
        return status
    
    def _test_rust_connection(self) -> bool:
        """Test connection to Rust engine"""
        try:
            response = self.session.get(f"{self.rust_api_url}/health", timeout=2.0)
            return response.status_code == 200
        except:
            return False
    
    def get_analytics(self) -> Dict[str, Any]:
        """Get system analytics"""
        analytics = self.engine.get_analytics()
        
        # Add Rust metrics if available
        rust_state = self.get_rust_state()
        if rust_state and 'metrics' in rust_state:
            analytics['rust_metrics'] = rust_state['metrics']
        
        return analytics
    
    def get_available_options(self) -> Dict[str, List[str]]:
        """Get available plants and drugs"""
        return {
            'plants': self.engine.get_available_plants(),
            'drugs': self.engine.get_available_drugs()
        }
    
    def validate_combination(
        self, 
        plant_name: str, 
        drug_name: str, 
        synergy: float
    ) -> Dict[str, Any]:
        """Validate plant-drug combination"""
        is_valid = self.engine.validate_combination(plant_name, drug_name, synergy)
        
        result = {
            'valid': is_valid,
            'plant_exists': plant_name in self.engine.get_available_plants(),
            'drug_exists': drug_name in self.engine.get_available_drugs(),
            'synergy_valid': 0.0 <= synergy <= 1.0
        }
        
        if is_valid:
            # Calculate expected effect
            effect = self.engine.calculate_effect(plant_name, drug_name, synergy)
            if effect:
                result['expected_magnitude'] = effect.magnitude
                result['expected_effects'] = effect.effects
                result['confidence'] = effect.confidence
        
        return result
    
    def reset_system(self) -> bool:
        """Reset entire system"""
        try:
            # Reset BioCore engine
            self.engine.reset()
            
            # Reset Rust engine (if available)
            rust_state = self.get_rust_state()
            if rust_state:
                for zone in rust_state.get('zones', []):
                    zone_id = zone.get('id')
                    if zone_id is not None:
                        # Apply reset influence (negative of current activity)
                        current_activity = zone.get('activity', 0.5)
                        reset_influence = 0.5 - current_activity
                        self.apply_rust_influence(zone_id, reset_influence)
            
            return True
        except Exception as e:
            print(f"Failed to reset system: {e}")
            return False
