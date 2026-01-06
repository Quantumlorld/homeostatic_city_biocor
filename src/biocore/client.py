"""
BioCore HTTP Client for communicating with Rust homeostatic engine.
"""

import requests
import json
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class BioCoreClient:
    """
    HTTP client for sending BioCore effects to Rust homeostatic engine.
    """
    
    def __init__(self, base_url: str = "http://localhost:3030"):
        """
        Initialize BioCore client.
        
        Args:
            base_url: Base URL of the Rust homeostatic engine
        """
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'BioCore-Python-Client/1.0'
        })
    
    def health_check(self) -> bool:
        """
        Check if the Rust engine is healthy.
        
        Returns:
            True if healthy, False otherwise
        """
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=5)
            return response.status_code == 200
        except requests.RequestException as e:
            logger.error(f"Health check failed: {e}")
            return False
    
    def get_city_state(self) -> Optional[Dict[str, Any]]:
        """
        Get current city state from Rust engine.
        
        Returns:
            City state data or None if failed
        """
        try:
            response = self.session.get(f"{self.base_url}/state", timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Failed to get city state: {e}")
            return None
    
    def apply_biocore_effect(self, zone: int, plant: str, drug: str, synergy: float) -> bool:
        """
        Apply BioCore effect to a specific zone.
        
        Args:
            zone: Zone ID (0-based)
            plant: Plant name
            drug: Drug name
            synergy: Synergy score (0-1)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            payload = {
                "zone": zone,
                "plant": plant,
                "drug": drug,
                "synergy": synergy
            }
            
            response = self.session.post(
                f"{self.base_url}/biocore",
                json=payload,
                timeout=5
            )
            response.raise_for_status()
            
            logger.info(f"Applied BioCore effect: {plant} + {drug} -> Zone {zone} (synergy: {synergy})")
            return True
            
        except requests.RequestException as e:
            logger.error(f"Failed to apply BioCore effect: {e}")
            return False
    
    def batch_apply_effects(self, effects: list) -> Dict[str, int]:
        """
        Apply multiple BioCore effects in batch.
        
        Args:
            effects: List of effect dictionaries with keys: zone, plant, drug, synergy
            
        Returns:
            Dictionary with success and failure counts
        """
        results = {"success": 0, "failed": 0}
        
        for effect in effects:
            if self.apply_biocore_effect(**effect):
                results["success"] += 1
            else:
                results["failed"] += 1
        
        return results
    
    def close(self):
        """Close the HTTP session."""
        self.session.close()


# Example usage and testing
if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    
    # Initialize client
    client = BioCoreClient()
    
    # Test health check
    if client.health_check():
        print("✅ Rust engine is healthy")
        
        # Get current state
        state = client.get_city_state()
        if state:
            print(f"📊 Current city state: {json.dumps(state, indent=2)}")
        
        # Apply BioCore effect
        success = client.apply_biocore_effect(
            zone=0,
            plant="Turmeric",
            drug="DrugB",
            synergy=0.81
        )
        
        if success:
            print("🌿 BioCore effect applied successfully")
        else:
            print("❌ Failed to apply BioCore effect")
    else:
        print("❌ Rust engine is not responding")
    
    client.close()
