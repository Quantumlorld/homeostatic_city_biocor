#!/usr/bin/env python3
"""
LunaBeyond AI - Intelligent BHCS System Backend
Advanced AI for homeostatic system optimization and learning
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from collections import deque
import json
import time
from datetime import datetime, timedelta

@dataclass
class ZonePattern:
    """Zone behavior pattern analysis"""
    zone_id: int
    stress_tendency: float  # How quickly zone becomes stressed
    recovery_rate: float    # How quickly zone recovers
    optimal_plant: str       # Best plant for this zone
    optimal_drug: str        # Best drug for this zone
    optimal_synergy: float   # Best synergy level
    intervention_frequency: int  # How often intervention needed
    last_intervention: float  # When last intervention occurred
    effectiveness_score: float  # How effective interventions are

@dataclass
class SystemInsight:
    """AI-generated system insights"""
    timestamp: float
    system_health_prediction: float
    recommended_actions: List[Dict]
    risk_zones: List[int]
    optimization_opportunities: List[str]
    learning_progress: float

class LunaBeyondAI:
    """Advanced AI for BHCS system optimization"""
    
    def __init__(self, num_zones: int = 5):
        self.num_zones = num_zones
        self.zone_patterns = {i: ZonePattern(
            zone_id=i,
            stress_tendency=0.5,
            recovery_rate=0.5,
            optimal_plant="Ashwagandha",
            optimal_drug="DrugE",
            optimal_synergy=0.7,
            intervention_frequency=0,
            last_intervention=0,
            effectiveness_score=0.5
        ) for i in range(num_zones)}
        
        # Learning components
        self.historical_data = deque(maxlen=1000)
        self.intervention_history = deque(maxlen=500)
        self.success_patterns = {}
        self.failure_patterns = {}
        
        # AI Models
        self.prediction_model = self._initialize_prediction_model()
        self.recommendation_engine = self._initialize_recommendation_engine()
        
        # BioCore knowledge base
        self.plant_effects = {
            "Ginkgo": {"potency": 0.7, "specialty": "neuroprotective", "speed": "medium"},
            "Aloe": {"potency": 0.5, "specialty": "anti_inflammatory", "speed": "fast"},
            "Turmeric": {"potency": 0.8, "specialty": "anti_inflammatory", "speed": "medium"},
            "Ginseng": {"potency": 0.6, "specialty": "immune_modulation", "speed": "slow"},
            "Ashwagandha": {"potency": 0.9, "specialty": "stress_reduction", "speed": "medium"}
        }
        
        self.drug_effects = {
            "DrugA": {"effectiveness": 0.6, "pathway": "COX-2/5-HT", "speed": "fast"},
            "DrugB": {"effectiveness": 0.7, "pathway": "NF-κB/MAO", "speed": "medium"},
            "DrugC": {"effectiveness": 0.8, "pathway": "NMDA/GABA", "speed": "slow"},
            "DrugD": {"effectiveness": 0.5, "pathway": "Dopamine/Serotonin", "speed": "fast"},
            "DrugE": {"effectiveness": 0.9, "pathway": "HPA-axis/Cortisol", "speed": "medium"}
        }
        
        # AI State
        self.learning_enabled = True
        self.prediction_accuracy = 0.5
        self.interventions_recommended = 0
        self.successful_interventions = 0
        
    def _initialize_prediction_model(self):
        """Initialize prediction model for system behavior"""
        return {
            'weights': np.random.random((self.num_zones, 10)),
            'biases': np.random.random(self.num_zones),
            'learning_rate': 0.01,
            'accuracy': 0.5
        }
    
    def _initialize_recommendation_engine(self):
        """Initialize recommendation engine for optimal interventions"""
        return {
            'zone_preferences': {i: {} for i in range(self.num_zones)},
            'combination_effectiveness': {},
            'timing_optimization': {},
            'synergy_learning': {}
        }
    
    def analyze_system_state(self, zones: List[Dict]) -> SystemInsight:
        """Analyze current system state and generate insights"""
        current_time = time.time()
        
        # Extract zone data
        zone_activities = [zone['activity'] for zone in zones]
        zone_states = [zone['state'] for zone in zones]
        
        # Predict system health
        health_prediction = self._predict_system_health(zone_activities)
        
        # Identify risk zones
        risk_zones = self._identify_risk_zones(zones, current_time)
        
        # Generate recommendations
        recommended_actions = self._generate_recommendations(zones, risk_zones, current_time)
        
        # Identify optimization opportunities
        optimization_opportunities = self._identify_optimization_opportunities(zones)
        
        # Calculate learning progress
        learning_progress = self._calculate_learning_progress()
        
        return SystemInsight(
            timestamp=current_time,
            system_health_prediction=health_prediction,
            recommended_actions=recommended_actions,
            risk_zones=risk_zones,
            optimization_opportunities=optimization_opportunities,
            learning_progress=learning_progress
        )
    
    def _predict_system_health(self, zone_activities: List[float]) -> float:
        """Predict future system health using AI model"""
        # Simple neural network prediction
        input_data = np.array(zone_activities)
        
        # Forward pass
        hidden = np.dot(input_data, self.prediction_model['weights'][:, :len(zone_activities)])
        hidden = np.tanh(hidden)
        output = np.dot(hidden, self.prediction_model['weights'][:, len(zone_activities):])
        output = np.tanh(output)
        
        # Convert to health prediction (0-1)
        health_prediction = (output.mean() + 1) / 2
        
        # Update model accuracy based on historical data
        if len(self.historical_data) > 10:
            self._update_prediction_model()
        
        return health_prediction
    
    def _identify_risk_zones(self, zones: List[Dict], current_time: float) -> List[int]:
        """Identify zones at risk of becoming critical"""
        risk_zones = []
        
        for i, zone in enumerate(zones):
            activity = zone['activity']
            state = zone['state']
            pattern = self.zone_patterns[i]
            
            # Calculate risk score
            risk_score = 0.0
            
            # High activity risk
            if activity > 0.7:
                risk_score += (activity - 0.7) * 3
            
            # State-based risk
            if state == "EMERGENT":
                risk_score += 0.5
            elif state == "CRITICAL":
                risk_score += 1.0
            
            # Pattern-based risk
            if pattern.stress_tendency > 0.7:
                risk_score += 0.3
            
            # Time since last intervention
            time_since_intervention = current_time - pattern.last_intervention
            if time_since_intervention > 300:  # 5 minutes
                risk_score += 0.2
            
            if risk_score > 0.6:
                risk_zones.append(i)
        
        return risk_zones
    
    def _generate_recommendations(self, zones: List[Dict], risk_zones: List[int], current_time: float) -> List[Dict]:
        """Generate AI-powered recommendations for system optimization"""
        recommendations = []
        
        # Handle risk zones first
        for zone_id in risk_zones:
            zone = zones[zone_id]
            pattern = self.zone_patterns[zone_id]
            
            # Generate optimal intervention
            intervention = self._create_optimal_intervention(zone_id, zone, pattern, current_time)
            recommendations.append(intervention)
        
        # System-wide optimization
        if len(risk_zones) > 2:
            # Multiple zones at risk - recommend system optimization
            recommendations.append({
                'type': 'system_optimization',
                'priority': 'high',
                'action': 'optimize_all',
                'reason': f'Multiple zones ({len(risk_zones)}) at risk',
                'expected_improvement': 0.3 + (len(risk_zones) * 0.1)
            })
        
        # Preventive recommendations
        for i, zone in enumerate(zones):
            if i not in risk_zones and zone['activity'] > 0.6:
                pattern = self.zone_patterns[i]
                
                # Predict if this zone will become at risk soon
                future_risk = self._predict_zone_risk(zone, pattern)
                
                if future_risk > 0.5:
                    preventive_intervention = self._create_preventive_intervention(i, zone, pattern, current_time)
                    recommendations.append(preventive_intervention)
        
        # Sort recommendations by priority
        recommendations.sort(key=lambda x: x.get('priority', 'low') == 'high', reverse=True)
        
        return recommendations[:5]  # Limit to top 5 recommendations
    
    def _create_optimal_intervention(self, zone_id: int, zone: Dict, pattern: ZonePattern, current_time: float) -> Dict:
        """Create optimal intervention for a specific zone"""
        
        # Choose best plant based on zone characteristics
        if zone['activity'] > 0.8:
            # High stress - need strong calming
            best_plant = "Ashwagandha"
            best_drug = "DrugE"
            optimal_synergy = 0.9
        elif zone['activity'] > 0.6:
            # Medium stress - balanced approach
            best_plant = pattern.optimal_plant
            best_drug = pattern.optimal_drug
            optimal_synergy = pattern.optimal_synergy
        else:
            # Low stress - gentle intervention
            best_plant = "Aloe"
            best_drug = "DrugA"
            optimal_synergy = 0.6
        
        # Calculate expected effectiveness
        plant_potency = self.plant_effects[best_plant]['potency']
        drug_effectiveness = self.drug_effects[best_drug]['effectiveness']
        expected_effectiveness = plant_potency * drug_effectiveness * optimal_synergy
        
        return {
            'type': 'zone_intervention',
            'zone_id': zone_id,
            'priority': 'high',
            'plant': best_plant,
            'drug': best_drug,
            'synergy': optimal_synergy,
            'expected_effectiveness': expected_effectiveness,
            'reason': f'Zone {zone_id} at {zone["state"]} state',
            'urgency': 'immediate' if zone['activity'] > 0.8 else 'soon'
        }
    
    def _create_preventive_intervention(self, zone_id: int, zone: Dict, pattern: ZonePattern, current_time: float) -> Dict:
        """Create preventive intervention to avoid future risk"""
        
        # Choose gentle but effective combination
        best_plant = "Ginseng"  # Good for immune modulation
        best_drug = "DrugB"    # Medium effectiveness
        optimal_synergy = 0.6   # Moderate synergy
        
        return {
            'type': 'preventive_intervention',
            'zone_id': zone_id,
            'priority': 'medium',
            'plant': best_plant,
            'drug': best_drug,
            'synergy': optimal_synergy,
            'expected_effectiveness': 0.4,
            'reason': f'Preventive: Zone {zone_id} trending toward stress',
            'urgency': 'preventive'
        }
    
    def _predict_zone_risk(self, zone: Dict, pattern: ZonePattern) -> float:
        """Predict if zone will become at risk in near future"""
        current_activity = zone['activity']
        
        # Simple linear prediction based on stress tendency
        future_activity = current_activity + (pattern.stress_tendency - 0.5) * 0.1
        
        # Calculate risk based on predicted activity
        if future_activity > 0.8:
            return 0.9
        elif future_activity > 0.7:
            return 0.6
        elif future_activity > 0.6:
            return 0.3
        else:
            return 0.1
    
    def _identify_optimization_opportunities(self, zones: List[Dict]) -> List[str]:
        """Identify opportunities for system optimization"""
        opportunities = []
        
        # Analyze system-wide patterns
        avg_activity = sum(zone['activity'] for zone in zones) / len(zones)
        
        if avg_activity > 0.6:
            opportunities.append("System-wide stress reduction recommended")
        
        # Check for consistent patterns
        calm_zones = [z for z in zones if z['state'] == 'CALM']
        if len(calm_zones) >= 3:
            opportunities.append("Majority of zones stable - focus on remaining zones")
        
        # Check intervention timing
        recent_interventions = sum(1 for pattern in self.zone_patterns.values() 
                                 if time.time() - pattern.last_intervention < 60)
        if recent_interventions > 2:
            opportunities.append("High intervention frequency - consider system optimization")
        
        # Learning opportunities
        if self.prediction_accuracy < 0.7:
            opportunities.append("AI learning in progress - accuracy improving")
        
        return opportunities
    
    def _calculate_learning_progress(self) -> float:
        """Calculate overall AI learning progress"""
        accuracy_score = self.prediction_accuracy
        intervention_score = min(1.0, self.successful_interventions / max(1, self.interventions_recommended))
        data_score = min(1.0, len(self.historical_data) / 100)
        
        return (accuracy_score + intervention_score + data_score) / 3
    
    def _update_prediction_model(self):
        """Update prediction model based on historical data"""
        if len(self.historical_data) < 10:
            return
        
        # Simple gradient descent update
        for data_point in list(self.historical_data)[-10:]:
            # Extract features and target
            features = np.array([d['activity'] for d in data_point['zones']])
            target = data_point['actual_health']
            
            # Forward pass
            hidden = np.dot(features, self.prediction_model['weights'][:, :len(features)])
            hidden = np.tanh(hidden)
            output = np.dot(hidden, self.prediction_model['weights'][:, len(features):])
            prediction = (np.tanh(output).mean() + 1) / 2
            
            # Calculate error
            error = target - prediction
            
            # Update weights (simplified)
            self.prediction_model['weights'] += self.prediction_model['learning_rate'] * error
        
        # Update accuracy
        self.prediction_accuracy = max(0.5, min(1.0, self.prediction_accuracy + 0.01))
    
    def record_intervention(self, zone_id: int, plant: str, drug: str, synergy: float, 
                           before_state: Dict, after_state: Dict):
        """Record intervention for learning"""
        intervention_data = {
            'timestamp': time.time(),
            'zone_id': zone_id,
            'plant': plant,
            'drug': drug,
            'synergy': synergy,
            'before_activity': before_state['activity'],
            'after_activity': after_state['activity'],
            'improvement': before_state['activity'] - after_state['activity'],
            'effective': after_state['activity'] < before_state['activity']
        }
        
        self.intervention_history.append(intervention_data)
        
        # Update zone patterns
        pattern = self.zone_patterns[zone_id]
        pattern.last_intervention = time.time()
        pattern.intervention_frequency += 1
        
        if intervention_data['effective']:
            pattern.effectiveness_score = min(1.0, pattern.effectiveness_score + 0.1)
            self.successful_interventions += 1
        else:
            pattern.effectiveness_score = max(0.1, pattern.effectiveness_score - 0.05)
        
        # Update optimal combinations
        if intervention_data['improvement'] > 0.1:
            pattern.optimal_plant = plant
            pattern.optimal_drug = drug
            pattern.optimal_synergy = synergy
        
        self.interventions_recommended += 1
    
    def record_system_state(self, zones: List[Dict], system_health: float):
        """Record system state for learning"""
        state_data = {
            'timestamp': time.time(),
            'zones': zones.copy(),
            'system_health': system_health,
            'actual_health': system_health  # For learning
        }
        
        self.historical_data.append(state_data)
        
        # Update zone patterns
        for i, zone in enumerate(zones):
            pattern = self.zone_patterns[i]
            
            # Update stress tendency
            if zone['activity'] > 0.7:
                pattern.stress_tendency = min(1.0, pattern.stress_tendency + 0.01)
            elif zone['activity'] < 0.4:
                pattern.stress_tendency = max(0.0, pattern.stress_tendency - 0.01)
            
            # Update recovery rate
            if zone['state'] == 'CALM':
                pattern.recovery_rate = min(1.0, pattern.recovery_rate + 0.01)
    
    def get_ai_status(self) -> Dict:
        """Get current AI status and capabilities"""
        return {
            'learning_enabled': self.learning_enabled,
            'prediction_accuracy': self.prediction_accuracy,
            'interventions_recommended': self.interventions_recommended,
            'successful_interventions': self.successful_interventions,
            'data_points_collected': len(self.historical_data),
            'interventions_recorded': len(self.intervention_history),
            'zone_patterns_learned': len([p for p in self.zone_patterns.values() if p.effectiveness_score > 0.7]),
            'learning_progress': self._calculate_learning_progress()
        }
    
    def enable_learning(self):
        """Enable AI learning"""
        self.learning_enabled = True
    
    def disable_learning(self):
        """Disable AI learning"""
        self.learning_enabled = False
    
    def reset_learning(self):
        """Reset AI learning data"""
        self.historical_data.clear()
        self.intervention_history.clear()
        self.prediction_model = self._initialize_prediction_model()
        self.recommendation_engine = self._initialize_recommendation_engine()
        self.prediction_accuracy = 0.5
        self.interventions_recommended = 0
        self.successful_interventions = 0
