#!/usr/bin/env python3
"""
🦀 BHCS Core Engine - Homeostatic Regulation System
Implements core philosophy: balance_error = target - current
adjustment = learning_rate * balance_error
new_state = current + adjustment

Core Principles:
- Homeostasis is primary control principle
- All systems regulate toward balance, not maximization
- Overstimulation must decay naturally into calm
- Calm is controlled intensity, not inactivity
- Human-in-the-loop control is mandatory
"""

import time
import threading
import logging
from datetime import datetime
from typing import Dict, List, Any
from enum import Enum

# Configure logging for stability
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ZoneState(Enum):
    CALM = "CALM"
    OVERSTIMULATED = "OVERSTIMULATED"
    EMERGENT = "EMERGENT"
    CRITICAL = "CRITICAL"

class BHCSZone:
    """Single zone with homeostatic regulation"""
    
    def __init__(self, zone_id: int, name: str, target_state: float = 0.5):
        self.id = zone_id
        self.name = name
        self.target_state = target_state  # Homeostatic target
        self.current_state = target_state  # Current activity level
        self.learning_rate = 0.03  # Conservative learning rate
        self.max_activity = 1.0  # Safety cap
        self.min_activity = 0.0  # Safety floor
        self.decay_rate = 0.01  # Natural decay to calm
        self.last_update = time.time()
        
        # Recovery tracking
        self.recovery_confidence = 0.5  # Confidence in recovery
        self.stimulation_history = []  # Track stimulation events
        self.state_transitions = []  # Track state changes
        
        logger.info(f"Zone {name} initialized with target {target_state}")
    
    def calculate_balance_error(self) -> float:
        """Core homeostatic equation: balance_error = target - current"""
        return self.target_state - self.current_state
    
    def calculate_adjustment(self) -> float:
        """Core adjustment equation: adjustment = learning_rate * balance_error"""
        balance_error = self.calculate_balance_error()
        return self.learning_rate * balance_error
    
    def apply_homeostatic_regulation(self) -> Dict[str, Any]:
        """Apply core homeostatic regulation with safety bounds"""
        old_state = self.current_state
        old_zone_state = self.determine_zone_state()
        
        # Calculate adjustment
        adjustment = self.calculate_adjustment()
        
        # Apply natural decay (overstimulation decays to calm)
        decay = -self.decay_rate if self.current_state > self.target_state else 0
        
        # Core equation: new_state = current + adjustment + decay
        new_state = self.current_state + adjustment + decay
        
        # Safety bounds (never exceed limits)
        new_state = max(self.min_activity, min(self.max_activity, new_state))
        
        # Update state
        self.current_state = new_state
        self.last_update = time.time()
        
        # Track stimulation
        if abs(adjustment) > 0.001:
            self.stimulation_history.append({
                'timestamp': time.time(),
                'adjustment': adjustment,
                'old_state': old_state,
                'new_state': new_state
            })
        
        # Track state transitions
        new_zone_state = self.determine_zone_state()
        if old_zone_state != new_zone_state:
            self.state_transitions.append({
                'timestamp': time.time(),
                'from_state': old_zone_state.value,
                'to_state': new_zone_state.value,
                'activity': new_state
            })
            logger.info(f"Zone {self.name}: {old_zone_state.value} → {new_zone_state.value}")
        
        # Update recovery confidence
        if abs(self.calculate_balance_error()) < 0.05:
            self.recovery_confidence = min(1.0, self.recovery_confidence + 0.01)
        else:
            self.recovery_confidence = max(0.1, self.recovery_confidence - 0.005)
        
        return {
            'zone_id': self.id,
            'zone_name': self.name,
            'old_activity': old_state,
            'new_activity': new_state,
            'adjustment': adjustment,
            'decay': decay,
            'balance_error': self.calculate_balance_error(),
            'zone_state': new_zone_state.value,
            'recovery_confidence': self.recovery_confidence,
            'timestamp': datetime.now().isoformat()
        }
    
    def apply_external_influence(self, influence: float, source: str = "external") -> Dict[str, Any]:
        """Apply external influence (BioCore, weather, human) with safety"""
        logger.info(f"Zone {self.name}: applying {influence:+.3f} influence from {source}")
        
        old_state = self.current_state
        
        # External influences are bounded and temporary
        max_influence = 0.2  # Safety cap on external influences
        bounded_influence = max(-max_influence, min(max_influence, influence))
        
        # Apply influence with decay
        new_state = old_state + bounded_influence
        new_state = max(self.min_activity, min(self.max_activity, new_state))
        
        self.current_state = new_state
        self.last_update = time.time()
        
        return {
            'zone_id': self.id,
            'zone_name': self.name,
            'influence_source': source,
            'requested_influence': influence,
            'applied_influence': bounded_influence,
            'old_activity': old_state,
            'new_activity': new_state,
            'timestamp': datetime.now().isoformat()
        }
    
    def determine_zone_state(self) -> ZoneState:
        """Determine zone state based on activity level"""
        if self.current_state < 0.3:
            return ZoneState.CALM
        elif self.current_state < 0.6:
            return ZoneState.OVERSTIMULATED
        elif self.current_state < 0.8:
            return ZoneState.EMERGENT
        else:
            return ZoneState.CRITICAL
    
    def get_zone_status(self) -> Dict[str, Any]:
        """Get comprehensive zone status"""
        return {
            'id': self.id,
            'name': self.name,
            'activity': self.current_state,
            'target': self.target_state,
            'balance_error': self.calculate_balance_error(),
            'state': self.determine_zone_state().value,
            'recovery_confidence': self.recovery_confidence,
            'learning_rate': self.learning_rate,
            'last_update': self.last_update,
            'stimulation_events': len(self.stimulation_history),
            'state_transitions': len(self.state_transitions)
        }

class BHCSCoreEngine:
    """Core BHCS Engine - Final authority on state changes"""
    
    def __init__(self, num_zones: int = 5):
        self.num_zones = num_zones
        self.target_state = 0.5  # Universal homeostatic target
        self.global_learning_rate = 0.03  # Conservative learning
        self.running = False
        self.regulation_interval = 1.0  # seconds
        
        # Initialize zones with conservative starting states
        zone_configs = [
            (0, "Downtown", 0.5),
            (1, "Industrial", 0.6),
            (2, "Residential", 0.4),
            (3, "Commercial", 0.5),
            (4, "Tech Park", 0.3)
        ]
        
        self.zones = []
        for zone_id, name, initial_state in zone_configs:
            zone = BHCSZone(zone_id, name, self.target_state)
            zone.current_state = initial_state
            self.zones.append(zone)
        
        logger.info(f"BHCS Core Engine initialized with {len(self.zones)} zones")
        logger.info(f"Target state: {self.target_state}, Learning rate: {self.global_learning_rate}")
    
    def start_regulation(self):
        """Start homeostatic regulation loop"""
        if self.running:
            logger.warning("Regulation already running")
            return
        
        self.running = True
        logger.info("Starting homeostatic regulation loop")
        
        def regulation_loop():
            while self.running:
                regulation_results = []
                
                # Apply homeostatic regulation to all zones
                for zone in self.zones:
                    result = zone.apply_homeostatic_regulation()
                    regulation_results.append(result)
                
                # Log system status periodically
                if int(time.time()) % 10 == 0:
                    self._log_system_status()
                
                time.sleep(self.regulation_interval)
        
        self.regulation_thread = threading.Thread(target=regulation_loop, daemon=True)
        self.regulation_thread.start()
        logger.info("Homeostatic regulation loop started")
    
    def apply_biocore_intervention(self, zone_id: int, intervention_data: Dict[str, Any]) -> Dict[str, Any]:
        """Apply BioCore intervention with human-in-the-loop safety"""
        if zone_id >= len(self.zones):
            return {
                'success': False,
                'error': f'Zone {zone_id} not found',
                'timestamp': datetime.now().isoformat()
            }
        
        zone = self.zones[zone_id]
        
        # Extract intervention parameters with safety bounds
        magnitude = intervention_data.get('magnitude', 0.0)
        synergy = intervention_data.get('synergy', 1.0)
        
        # Safety: interventions are modifiers, not drivers
        max_magnitude = 0.15  # Conservative intervention cap
        bounded_magnitude = max(-max_magnitude, min(max_magnitude, magnitude))
        
        # Apply synergy as modifier (not multiplier)
        final_magnitude = bounded_magnitude * (0.5 + 0.5 * synergy)
        
        # Apply intervention
        result = zone.apply_external_influence(final_magnitude, "biocore_intervention")
        
        logger.info(f"BioCore intervention applied to Zone {zone.name}: {final_magnitude:+.3f}")
        
        return {
            'success': True,
            'zone_id': zone_id,
            'zone_name': zone.name,
            'intervention_applied': final_magnitude,
            'requested_magnitude': magnitude,
            'synergy_modifier': synergy,
            'result': result,
            'timestamp': datetime.now().isoformat()
        }
    
    def get_system_health(self) -> Dict[str, Any]:
        """Get comprehensive system health status"""
        if not self.zones:
            return {'health': 0.0, 'status': 'no_zones'}
        
        # Calculate system metrics
        activities = [zone.current_state for zone in self.zones]
        balance_errors = [abs(zone.calculate_balance_error()) for zone in self.zones]
        recovery_confidences = [zone.recovery_confidence for zone in self.zones]
        
        system_health = 1.0 - (sum(balance_errors) / len(balance_errors))
        avg_activity = sum(activities) / len(activities)
        avg_recovery_confidence = sum(recovery_confidences) / len(recovery_confidences)
        
        # Determine system state
        if system_health > 0.8:
            status = "STABLE"
        elif system_health > 0.6:
            status = "REGULATING"
        else:
            status = "IMBALANCED"
        
        return {
            'system_health': system_health,
            'status': status,
            'average_activity': avg_activity,
            'target_state': self.target_state,
            'average_balance_error': sum(balance_errors) / len(balance_errors),
            'recovery_confidence': avg_recovery_confidence,
            'zone_count': len(self.zones),
            'running': self.running,
            'timestamp': datetime.now().isoformat()
        }
    
    def get_zones_status(self) -> List[Dict[str, Any]]:
        """Get status of all zones"""
        return [zone.get_zone_status() for zone in self.zones]
    
    def _log_system_status(self):
        """Log periodic system status"""
        health = self.get_system_health()
        logger.info(f"System Health: {health['system_health']:.3f} ({health['status']})")
        logger.info(f"Avg Activity: {health['average_activity']:.3f}, Target: {health['target_state']}")
    
    def shutdown(self):
        """Graceful shutdown"""
        logger.info("Shutting down BHCS Core Engine")
        self.running = False
        if hasattr(self, 'regulation_thread'):
            self.regulation_thread.join(timeout=3)
        logger.info("BHCS Core Engine shutdown complete")

# Test the core engine
if __name__ == "__main__":
    print("🦀 BHCS Core Engine Test")
    print("=" * 50)
    
    engine = BHCSCoreEngine(5)
    
    # Test initial state
    health = engine.get_system_health()
    print(f"Initial Health: {health}")
    
    # Start regulation
    engine.start_regulation()
    
    # Test intervention
    print("\nTesting BioCore intervention...")
    result = engine.apply_biocore_intervention(0, {
        'magnitude': -0.1,
        'synergy': 0.8,
        'description': 'Calming intervention'
    })
    print(f"Intervention Result: {result}")
    
    # Run for a few seconds
    print("Running regulation for 5 seconds...")
    time.sleep(5)
    
    # Final status
    final_health = engine.get_system_health()
    zones_status = engine.get_zones_status()
    print(f"Final Health: {final_health}")
    print(f"Zones Status: {zones_status}")
    
    engine.shutdown()
    print("✅ BHCS Core Engine test complete")
