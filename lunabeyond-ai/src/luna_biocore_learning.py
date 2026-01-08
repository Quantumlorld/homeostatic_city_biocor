#!/usr/bin/env python3
"""
🧬 LUNABEYOND AI - BIOCORE LEARNING INTEGRATION
Direct learning from Homeostatic City BioCore system data and patterns
"""

import asyncio
import json
import time
import numpy as np
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass

@dataclass
class BioCorePattern:
    """BioCore system pattern learned by Luna"""
    pattern_type: str
    zone_id: str
    activity_level: float
    state_transition: str
    intervention_effectiveness: float
    timestamp: datetime
    confidence: float
    prediction_accuracy: float

@dataclass
class SystemLearning:
    """Learning from BHCS system interactions"""
    interaction_type: str
    system_state: Dict
    user_action: str
    system_response: Dict
    learning_outcome: str
    timestamp: datetime
    effectiveness_score: float

class LunaBioCoreLearning:
    """Advanced BioCore learning integration for LunaBeyond AI"""
    
    def __init__(self):
        self.biocore_patterns = []
        self.system_learning = []
        self.zone_behaviors = {}
        self.intervention_effectiveness = {}
        self.prediction_models = {}
        
        # Learning parameters
        self.learning_rate = 0.05
        self.pattern_recognition_threshold = 0.7
        self.prediction_confidence_threshold = 0.8
        
        # BioCore knowledge base
        self.biocore_knowledge = {
            'zone_states': {
                'CALM': {'optimal_range': (0.0, 0.4), 'description': 'System in balanced state'},
                'OVERSTIMULATED': {'optimal_range': (0.4, 0.7), 'description': 'System experiencing stress'},
                'EMERGENT': {'optimal_range': (0.7, 0.9), 'description': 'System showing critical patterns'},
                'CRITICAL': {'optimal_range': (0.9, 1.0), 'description': 'System requires immediate intervention'}
            },
            'interventions': {
                'BioCore': {'effectiveness': 0.8, 'duration': 300, 'optimal_zones': ['OVERSTIMULATED', 'EMERGENT']},
                'Optimization': {'effectiveness': 0.6, 'duration': 180, 'optimal_zones': ['CALM', 'OVERSTIMULATED']},
                'Reset': {'effectiveness': 0.9, 'duration': 60, 'optimal_zones': ['CRITICAL', 'EMERGENT']}
            },
            'system_dynamics': {
                'equilibrium_point': 0.3,
                'stability_threshold': 0.6,
                'oscillation_frequency': 0.1,
                'damping_factor': 0.8
            }
        }
        
        # Neural network for BioCore pattern recognition
        self.biocore_neural_network = self.initialize_biocore_network()
        
    def initialize_biocore_network(self) -> Dict:
        """Initialize neural network for BioCore pattern recognition"""
        return {
            'input_size': 25,  # 5 zones × 5 features (activity, state, trend, history, interventions)
            'hidden_layers': [64, 32, 16],
            'output_size': 10,  # Predictions for next states
            'weights': {
                'input_hidden': np.random.rand(25, 64) * 0.1,
                'hidden_1': np.random.rand(64, 32) * 0.1,
                'hidden_2': np.random.rand(32, 16) * 0.1,
                'hidden_output': np.random.rand(16, 10) * 0.1
            },
            'biases': {
                'hidden_1': np.random.rand(64) * 0.1,
                'hidden_2': np.random.rand(32) * 0.1,
                'hidden_3': np.random.rand(16) * 0.1,
                'output': np.random.rand(10) * 0.1
            }
        }
    
    async def learn_from_biocore_data(self, biocore_data: Dict) -> List[BioCorePattern]:
        """
        🧬 Learn directly from BioCore system data
        """
        patterns = []
        
        # Extract zone data
        zones = biocore_data.get('zones', [])
        system_health = biocore_data.get('system_health', 0.5)
        
        for zone in zones:
            zone_id = zone.get('id', 'unknown')
            activity = zone.get('activity', 0.0)
            state = zone.get('state', 'CALM')
            
            # Learn zone behavior patterns
            pattern = await self.analyze_zone_pattern(zone_id, activity, state, system_health)
            if pattern:
                patterns.append(pattern)
            
            # Update zone behavior model
            await self.update_zone_behavior(zone_id, activity, state)
        
        # Learn system-level patterns
        system_pattern = await self.analyze_system_pattern(biocore_data)
        if system_pattern:
            patterns.append(system_pattern)
        
        # Update neural network
        await self.train_biocore_network(biocore_data)
        
        # Store learned patterns
        self.biocore_patterns.extend(patterns)
        
        # Keep pattern database manageable
        if len(self.biocore_patterns) > 1000:
            self.biocore_patterns = self.biocore_patterns[-500:]
        
        return patterns
    
    async def analyze_zone_pattern(self, zone_id: str, activity: float, state: str, system_health: float) -> Optional[BioCorePattern]:
        """Analyze individual zone patterns"""
        
        # Get historical zone behavior
        zone_history = self.zone_behaviors.get(zone_id, [])
        zone_history.append({'activity': activity, 'state': state, 'timestamp': datetime.now()})
        
        # Keep only recent history
        if len(zone_history) > 50:
            zone_history = zone_history[-30:]
        
        self.zone_behaviors[zone_id] = zone_history
        
        if len(zone_history) < 3:
            return None
        
        # Detect patterns
        pattern_type = self.detect_zone_pattern_type(zone_history)
        state_transition = self.detect_state_transition(zone_history)
        intervention_effectiveness = self.calculate_intervention_effectiveness(zone_id, zone_history)
        
        # Calculate confidence based on pattern consistency
        confidence = self.calculate_pattern_confidence(zone_history)
        
        return BioCorePattern(
            pattern_type=pattern_type,
            zone_id=zone_id,
            activity_level=activity,
            state_transition=state_transition,
            intervention_effectiveness=intervention_effectiveness,
            timestamp=datetime.now(),
            confidence=confidence,
            prediction_accuracy=self.calculate_prediction_accuracy(zone_id, zone_history)
        )
    
    def detect_zone_pattern_type(self, zone_history: List[Dict]) -> str:
        """Detect type of zone behavior pattern"""
        if len(zone_history) < 3:
            return 'insufficient_data'
        
        activities = [h['activity'] for h in zone_history[-10:]]
        
        # Calculate trend
        if len(activities) >= 3:
            recent_avg = np.mean(activities[-3:])
            older_avg = np.mean(activities[-10:-3]) if len(activities) > 3 else recent_avg
            
            if recent_avg > older_avg + 0.1:
                return 'escalating_activity'
            elif recent_avg < older_avg - 0.1:
                return 'decreasing_activity'
            elif np.std(activities) < 0.05:
                return 'stable_activity'
            else:
                return 'oscillating_activity'
        
        return 'unknown_pattern'
    
    def detect_state_transition(self, zone_history: List[Dict]) -> str:
        """Detect state transitions in zone behavior"""
        if len(zone_history) < 2:
            return 'no_transition'
        
        recent_states = [h['state'] for h in zone_history[-5:]]
        unique_states = list(set(recent_states))
        
        if len(unique_states) == 1:
            return f'stable_{unique_states[0].lower()}'
        elif len(unique_states) == 2:
            return f'transition_{unique_states[0].lower()}_to_{unique_states[-1].lower()}'
        else:
            return 'multiple_transitions'
    
    def calculate_intervention_effectiveness(self, zone_id: str, zone_history: List[Dict]) -> float:
        """Calculate effectiveness of interventions for this zone"""
        if zone_id not in self.intervention_effectiveness:
            return 0.5  # Default effectiveness
        
        effectiveness_data = self.intervention_effectiveness[zone_id]
        
        if not effectiveness_data:
            return 0.5
        
        # Calculate weighted average effectiveness
        total_effectiveness = 0
        total_weight = 0
        
        for intervention in effectiveness_data:
            effectiveness = intervention['effectiveness']
            recency_weight = self.calculate_recency_weight(intervention['timestamp'])
            
            total_effectiveness += effectiveness * recency_weight
            total_weight += recency_weight
        
        return total_effectiveness / total_weight if total_weight > 0 else 0.5
    
    def calculate_recency_weight(self, timestamp: datetime) -> float:
        """Calculate weight based on recency"""
        age_hours = (datetime.now() - timestamp).total_seconds() / 3600
        return max(0.1, 1.0 - age_hours / 168)  # Decay over a week
    
    def calculate_pattern_confidence(self, zone_history: List[Dict]) -> float:
        """Calculate confidence in detected pattern"""
        if len(zone_history) < 5:
            return 0.3
        
        activities = [h['activity'] for h in zone_history[-10:]]
        
        # Calculate consistency
        if len(activities) >= 3:
            consistency = 1.0 - (np.std(activities) / np.mean(activities)) if np.mean(activities) > 0 else 0.5
            return min(max(consistency, 0.0), 1.0)
        
        return 0.5
    
    def calculate_prediction_accuracy(self, zone_id: str, zone_history: List[Dict]) -> float:
        """Calculate prediction accuracy for this zone"""
        if zone_id not in self.prediction_models:
            return 0.5
        
        prediction_model = self.prediction_models[zone_id]
        predictions = prediction_model.get('predictions', [])
        
        if not predictions:
            return 0.5
        
        # Compare predictions with actual outcomes
        correct_predictions = 0
        total_predictions = len(predictions)
        
        for prediction in predictions[-10:]:  # Last 10 predictions
            predicted_state = prediction.get('predicted_state')
            actual_state = prediction.get('actual_state')
            
            if predicted_state == actual_state:
                correct_predictions += 1
        
        return correct_predictions / total_predictions if total_predictions > 0 else 0.5
    
    async def update_zone_behavior(self, zone_id: str, activity: float, state: str):
        """Update zone behavior model"""
        if zone_id not in self.zone_behaviors:
            self.zone_behaviors[zone_id] = []
        
        self.zone_behaviors[zone_id].append({
            'activity': activity,
            'state': state,
            'timestamp': datetime.now()
        })
        
        # Keep only recent data
        if len(self.zone_behaviors[zone_id]) > 100:
            self.zone_behaviors[zone_id] = self.zone_behaviors[zone_id][-50:]
    
    async def analyze_system_pattern(self, biocore_data: Dict) -> Optional[BioCorePattern]:
        """Analyze system-level patterns"""
        zones = biocore_data.get('zones', [])
        system_health = biocore_data.get('system_health', 0.5)
        
        if not zones:
            return None
        
        # Calculate system-wide metrics
        activities = [zone.get('activity', 0.0) for zone in zones]
        states = [zone.get('state', 'CALM') for zone in zones]
        
        avg_activity = np.mean(activities)
        activity_std = np.std(activities)
        
        # Detect system pattern
        if activity_std < 0.1:
            pattern_type = 'system_stable'
        elif avg_activity > 0.7:
            pattern_type = 'system_overloaded'
        elif avg_activity < 0.2:
            pattern_type = 'system_underutilized'
        else:
            pattern_type = 'system_balanced'
        
        return BioCorePattern(
            pattern_type=pattern_type,
            zone_id='system',
            activity_level=avg_activity,
            state_transition=self.detect_system_state_transition(states),
            intervention_effectiveness=self.calculate_system_intervention_effectiveness(biocore_data),
            timestamp=datetime.now(),
            confidence=0.8,
            prediction_accuracy=0.7
        )
    
    def detect_system_state_transition(self, states: List[str]) -> str:
        """Detect system-level state transitions"""
        state_counts = {state: states.count(state) for state in set(states)}
        dominant_state = max(state_counts, key=state_counts.get)
        
        if state_counts[dominant_state] / len(states) > 0.7:
            return f'dominant_{dominant_state.lower()}'
        else:
            return 'mixed_states'
    
    def calculate_system_intervention_effectiveness(self, biocore_data: Dict) -> float:
        """Calculate overall system intervention effectiveness"""
        zones = biocore_data.get('zones', [])
        
        if not zones:
            return 0.5
        
        zone_effectiveness = []
        for zone in zones:
            zone_id = zone.get('id', 'unknown')
            effectiveness = self.calculate_intervention_effectiveness(zone_id, [])
            zone_effectiveness.append(effectiveness)
        
        return np.mean(zone_effectiveness)
    
    async def train_biocore_network(self, biocore_data: Dict):
        """Train neural network on BioCore data"""
        # Prepare training data
        zones = biocore_data.get('zones', [])
        
        if len(zones) < 5:
            return
        
        # Create input vector (5 zones × 5 features)
        input_vector = []
        for zone in zones[:5]:  # Limit to 5 zones
            zone_features = [
                zone.get('activity', 0.0),
                self.encode_state(zone.get('state', 'CALM')),
                self.calculate_activity_trend(zone),
                self.calculate_intervention_history(zone.get('id', 'unknown')),
                zone.get('health', 0.5)
            ]
            input_vector.extend(zone_features)
        
        # Pad or truncate to 25 features
        input_vector = (input_vector + [0.0] * 25)[:25]
        
        # Simple forward pass (in real implementation, this would be backpropagation)
        network = self.biocore_neural_network
        weights = network['weights']
        biases = network['biases']
        
        # Hidden layer 1
        hidden1 = self.activate(np.dot(input_vector, weights['input_hidden']) + biases['hidden_1'])
        # Hidden layer 2
        hidden2 = self.activate(np.dot(hidden1, weights['hidden_1']) + biases['hidden_2'])
        # Hidden layer 3
        hidden3 = self.activate(np.dot(hidden2, weights['hidden_2']) + biases['hidden_3'])
        # Output layer
        output = self.activate(np.dot(hidden3, weights['hidden_output']) + biases['output'])
        
        # Store for learning
        network['last_input'] = input_vector
        network['last_output'] = output
        
        # Simple weight update (in real implementation, use proper backpropagation)
        learning_rate = self.learning_rate
        weights['input_hidden'] += learning_rate * np.outer(input_vector, hidden1) * 0.01
        weights['hidden_1'] += learning_rate * np.outer(hidden1, hidden2) * 0.01
        weights['hidden_2'] += learning_rate * np.outer(hidden2, hidden3) * 0.01
        weights['hidden_output'] += learning_rate * np.outer(hidden3, output) * 0.01
    
    def encode_state(self, state: str) -> float:
        """Encode zone state as numeric value"""
        state_encoding = {
            'CALM': 0.0,
            'OVERSTIMULATED': 0.5,
            'EMERGENT': 0.75,
            'CRITICAL': 1.0
        }
        return state_encoding.get(state, 0.0)
    
    def calculate_activity_trend(self, zone: Dict) -> float:
        """Calculate activity trend for a zone"""
        zone_id = zone.get('id', 'unknown')
        
        if zone_id not in self.zone_behaviors:
            return 0.0
        
        history = self.zone_behaviors[zone_id][-5:]  # Last 5 data points
        if len(history) < 2:
            return 0.0
        
        activities = [h['activity'] for h in history]
        if len(activities) < 2:
            return 0.0
        
        # Simple linear trend
        x = np.arange(len(activities))
        trend = np.polyfit(x, activities, 1)[0]  # Slope
        
        return max(min(trend, 1.0), -1.0)
    
    def calculate_intervention_history(self, zone_id: str) -> float:
        """Calculate intervention history for a zone"""
        if zone_id not in self.intervention_effectiveness:
            return 0.0
        
        interventions = self.intervention_effectiveness[zone_id]
        if not interventions:
            return 0.0
        
        # Calculate recent intervention frequency
        recent_interventions = [inv for inv in interventions 
                             if (datetime.now() - inv['timestamp']).total_seconds() < 3600]
        
        return min(len(recent_interventions) / 10.0, 1.0)
    
    def activate(self, x: np.ndarray) -> np.ndarray:
        """Activation function for neural network"""
        return 1.0 / (1.0 + np.exp(-x))  # Sigmoid
    
    async def predict_system_evolution(self, current_data: Dict, time_horizon: int = 60) -> Dict:
        """
        🔮 Predict system evolution based on learned patterns
        """
        zones = current_data.get('zones', [])
        
        if not zones:
            return {'error': 'No zone data available'}
        
        predictions = {}
        
        for zone in zones:
            zone_id = zone.get('id', 'unknown')
            current_activity = zone.get('activity', 0.0)
            current_state = zone.get('state', 'CALM')
            
            # Use neural network for prediction
            prediction = await self.predict_zone_evolution(zone_id, current_activity, current_state, time_horizon)
            predictions[zone_id] = prediction
        
        # System-level prediction
        system_prediction = await self.predict_system_evolution_aggregate(predictions)
        
        return {
            'zone_predictions': predictions,
            'system_prediction': system_prediction,
            'confidence': self.calculate_prediction_confidence(),
            'time_horizon': time_horizon,
            'based_on_patterns': len(self.biocore_patterns)
        }
    
    async def predict_zone_evolution(self, zone_id: str, current_activity: float, current_state: str, time_horizon: int) -> Dict:
        """Predict evolution of individual zone"""
        # Get similar historical patterns
        similar_patterns = [p for p in self.biocore_patterns 
                         if p.zone_id == zone_id and p.confidence > 0.7]
        
        if not similar_patterns:
            return {
                'predicted_activity': current_activity,
                'predicted_state': current_state,
                'confidence': 0.3,
                'trend': 'stable'
            }
        
        # Analyze patterns for prediction
        activities = [p.activity_level for p in similar_patterns]
        states = [p.state_transition for p in similar_patterns]
        
        # Predict activity trend
        if len(activities) >= 3:
            activity_trend = np.polyfit(range(len(activities)), activities, 1)[0]
            predicted_activity = current_activity + (activity_trend * time_horizon / 60.0)
            predicted_activity = max(min(predicted_activity, 1.0), 0.0)
        else:
            predicted_activity = current_activity
        
        # Predict state transition
        state_transitions = [s for s in states if 'transition' in s]
        if state_transitions:
            most_common_transition = max(set(state_transitions), key=state_transitions.count)
            predicted_state = self.extract_target_state(most_common_transition)
        else:
            predicted_state = current_state
        
        # Calculate confidence
        avg_confidence = np.mean([p.confidence for p in similar_patterns])
        
        return {
            'predicted_activity': predicted_activity,
            'predicted_state': predicted_state,
            'confidence': avg_confidence,
            'trend': 'increasing' if activity_trend > 0.01 else 'decreasing' if activity_trend < -0.01 else 'stable',
            'based_on_patterns': len(similar_patterns)
        }
    
    def extract_target_state(self, transition: str) -> str:
        """Extract target state from transition string"""
        if 'to_' in transition:
            return transition.split('to_')[-1].upper()
        return 'CALM'
    
    async def predict_system_evolution_aggregate(self, zone_predictions: Dict) -> Dict:
        """Aggregate zone predictions for system-level prediction"""
        if not zone_predictions:
            return {'error': 'No zone predictions available'}
        
        # Aggregate predictions
        predicted_activities = [p['predicted_activity'] for p in zone_predictions.values()]
        predicted_states = [p['predicted_state'] for p in zone_predictions.values()]
        confidences = [p['confidence'] for p in zone_predictions.values()]
        
        # System-level metrics
        avg_predicted_activity = np.mean(predicted_activities)
        activity_std = np.std(predicted_activities)
        avg_confidence = np.mean(confidences)
        
        # Predict dominant system state
        state_counts = {state: predicted_states.count(state) for state in set(predicted_states)}
        dominant_state = max(state_counts, key=state_counts.get) if state_counts else 'CALM'
        
        return {
            'average_activity': avg_predicted_activity,
            'activity_stability': 1.0 - (activity_std / avg_predicted_activity) if avg_predicted_activity > 0 else 0.5,
            'dominant_state': dominant_state,
            'confidence': avg_confidence,
            'risk_assessment': 'high' if avg_predicted_activity > 0.7 else 'medium' if avg_predicted_activity > 0.4 else 'low'
        }
    
    def calculate_prediction_confidence(self) -> float:
        """Calculate overall prediction confidence"""
        if not self.biocore_patterns:
            return 0.3
        
        # Base confidence on pattern quality and quantity
        pattern_confidences = [p.confidence for p in self.biocore_patterns[-50:]]  # Recent patterns
        avg_confidence = np.mean(pattern_confidences) if pattern_confidences else 0.5
        
        # Boost confidence with more patterns
        pattern_count_boost = min(len(self.biocore_patterns) / 100.0, 0.3)
        
        return min(avg_confidence + pattern_count_boost, 1.0)
    
    def get_biocore_learning_status(self) -> Dict:
        """Get comprehensive BioCore learning status"""
        return {
            'total_patterns_learned': len(self.biocore_patterns),
            'zones_tracked': list(self.zone_behaviors.keys()),
            'intervention_effectiveness': {
                zone: self.calculate_intervention_effectiveness(zone, [])
                for zone in self.zone_behaviors.keys()
            },
            'prediction_confidence': self.calculate_prediction_confidence(),
            'neural_network_status': {
                'input_size': self.biocore_neural_network['input_size'],
                'hidden_layers': self.biocore_neural_network['hidden_layers'],
                'output_size': self.biocore_neural_network['output_size'],
                'learning_rate': self.learning_rate
            },
            'knowledge_base_size': len(self.biocore_knowledge),
            'last_learning_update': datetime.now().isoformat()
        }

# Global BioCore learning instance
luna_biocore_learning = LunaBioCoreLearning()
