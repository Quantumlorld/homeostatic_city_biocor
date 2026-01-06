"""
Biomedical Analytics Module
Advanced medical data analysis and health predictions.
"""

import numpy as np
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import statistics


class HealthRisk(Enum):
    """Health risk levels for population monitoring."""
    LOW = "LOW"
    MODERATE = "MODERATE"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


@dataclass
class HealthMetrics:
    """Health metrics for zone population."""
    population_health: float
    disease_prevalence: float
    immunity_level: float
    stress_level: float
    recovery_rate: float
    medical_resource_usage: float


class BiomedicalAnalytics:
    """
    Advanced biomedical analytics for city health monitoring.
    Integrates with BioCore effects and environmental data.
    """
    
    def __init__(self):
        """Initialize biomedical analytics engine."""
        self.health_history = []
        self.bio_effectiveness_cache = {}
        self.population_data = {}
        self.medical_resources = {}
        
        # Disease parameters
        self.disease_models = {
            'respiratory': {
                'base_rate': 0.05,
                'environmental_factor': 0.3,
                'biocore_sensitivity': 0.7
            },
            'cardiovascular': {
                'base_rate': 0.08,
                'environmental_factor': 0.2,
                'biocore_sensitivity': 0.5
            },
            'neurological': {
                'base_rate': 0.03,
                'environmental_factor': 0.4,
                'biocore_sensitivity': 0.8
            },
            'immune_disorders': {
                'base_rate': 0.04,
                'environmental_factor': 0.3,
                'biocore_sensitivity': 0.9
            }
        }
    
    def analyze_zone_health(self, zone_id: int, city_activity: float, 
                         biocore_effects: List[Dict], 
                         environmental_data: Dict) -> HealthMetrics:
        """
        Analyze health metrics for a specific zone.
        
        Args:
            zone_id: Zone identifier
            city_activity: Current city activity level
            biocore_effects: List of BioCore effects applied
            environmental_data: Environmental factors
            
        Returns:
            Health metrics for the zone
        """
        # Calculate base health impact from city activity
        activity_impact = self._calculate_activity_health_impact(city_activity)
        
        # Calculate BioCore effectiveness
        biocore_impact = self._calculate_biocore_health_impact(biocore_effects)
        
        # Calculate environmental health impact
        environmental_impact = self._calculate_environmental_health_impact(environmental_data)
        
        # Combine all factors
        population_health = max(0.0, 1.0 - activity_impact + biocore_impact - environmental_impact)
        
        # Calculate disease prevalence
        disease_prevalence = self._calculate_disease_prevalence(
            population_health, environmental_data, biocore_effects
        )
        
        # Calculate immunity level
        immunity_level = self._calculate_immunity_level(biocore_effects, population_health)
        
        # Calculate stress level
        stress_level = self._calculate_stress_level(city_activity, environmental_data)
        
        # Calculate recovery rate
        recovery_rate = self._calculate_recovery_rate(population_health, biocore_effects)
        
        # Calculate medical resource usage
        medical_resource_usage = self._calculate_medical_resource_usage(
            disease_prevalence, stress_level
        )
        
        return HealthMetrics(
            population_health=population_health,
            disease_prevalence=disease_prevalence,
            immunity_level=immunity_level,
            stress_level=stress_level,
            recovery_rate=recovery_rate,
            medical_resource_usage=medical_resource_usage
        )
    
    def _calculate_activity_health_impact(self, activity: float) -> float:
        """Calculate health impact from city activity."""
        if activity < 0.4:
            # Calm activity: positive health impact
            return -0.1 * (0.4 - activity)
        elif activity < 0.7:
            # Overstimulated: moderate negative impact
            return 0.2 * (activity - 0.4)
        else:
            # Emergent: high negative impact
            return 0.3 * (activity - 0.7) + 0.06
    
    def _calculate_biocore_health_impact(self, biocore_effects: List[Dict]) -> float:
        """Calculate health impact from BioCore effects."""
        total_impact = 0.0
        
        for effect in biocore_effects:
            plant = effect.get('plant', '')
            drug = effect.get('drug', '')
            synergy = effect.get('synergy', 0.0)
            
            # Get effectiveness from cache or calculate
            effectiveness = self._get_biocore_effectiveness(plant, drug, synergy)
            total_impact += effectiveness * synergy
        
        return min(total_impact, 0.3)  # Cap maximum positive impact
    
    def _calculate_environmental_health_impact(self, environmental_data: Dict) -> float:
        """Calculate health impact from environmental factors."""
        air_quality = environmental_data.get('air_quality', 0.5)  # 0-1, lower is better
        temperature = environmental_data.get('temperature', 20)  # Celsius
        humidity = environmental_data.get('humidity', 0.5)  # 0-1
        pollution = environmental_data.get('pollution', 0.3)  # 0-1
        
        # Calculate combined environmental impact
        air_impact = (1.0 - air_quality) * 0.3
        temp_impact = abs(temperature - 22) / 30 * 0.2  # Optimal temp is 22°C
        humidity_impact = abs(humidity - 0.5) * 0.1
        pollution_impact = pollution * 0.4
        
        return air_impact + temp_impact + humidity_impact + pollution_impact
    
    def _calculate_disease_prevalence(self, population_health: float, 
                                  environmental_data: Dict, 
                                  biocore_effects: List[Dict]) -> Dict[str, float]:
        """Calculate prevalence for different disease types."""
        prevalence = {}
        
        for disease, params in self.disease_models.items():
            base_rate = params['base_rate']
            env_factor = params['environmental_factor']
            bio_sensitivity = params['biocore_sensitivity']
            
            # Environmental contribution
            env_score = self._calculate_environmental_disease_factor(environmental_data, disease)
            env_contribution = env_factor * env_score
            
            # BioCore contribution (reduces disease)
            bio_contribution = 0.0
            for effect in biocore_effects:
                synergy = effect.get('synergy', 0.0)
                bio_contribution += bio_sensitivity * synergy * 0.1
            
            # Population health contribution
            health_contribution = (1.0 - population_health) * base_rate
            
            # Combined prevalence
            disease_prevalence = base_rate + env_contribution - bio_contribution + health_contribution
            prevalence[disease] = max(0.0, min(disease_prevalence, 1.0))
        
        return prevalence
    
    def _calculate_environmental_disease_factor(self, environmental_data: Dict, disease_type: str) -> float:
        """Calculate environmental factor for specific disease."""
        air_quality = environmental_data.get('air_quality', 0.5)
        temperature = environmental_data.get('temperature', 20)
        humidity = environmental_data.get('humidity', 0.5)
        
        if disease_type == 'respiratory':
            # Respiratory diseases affected by air quality
            return (1.0 - air_quality) * 0.8 + abs(humidity - 0.6) * 0.2
        elif disease_type == 'cardiovascular':
            # Cardiovascular affected by temperature
            return abs(temperature - 22) / 20 * 0.7 + (1.0 - air_quality) * 0.3
        elif disease_type == 'neurological':
            # Neurological affected by multiple factors
            return (1.0 - air_quality) * 0.4 + abs(temperature - 22) / 20 * 0.4 + abs(humidity - 0.5) * 0.2
        else:  # immune_disorders
            # Immune disorders affected by environmental stress
            return (1.0 - air_quality) * 0.3 + abs(temperature - 22) / 20 * 0.4 + (1.0 - air_quality) * 0.3
    
    def _calculate_immunity_level(self, biocore_effects: List[Dict], population_health: float) -> float:
        """Calculate population immunity level."""
        base_immunity = population_health * 0.7
        
        # BioCore effects on immunity
        bio_immunity = 0.0
        for effect in biocore_effects:
            plant = effect.get('plant', '')
            if plant in ['Ginseng', 'Ashwagandha', 'Turmeric']:
                # Immune-boosting plants
                bio_immunity += effect.get('synergy', 0.0) * 0.2
        
        return min(base_immunity + bio_immunity, 1.0)
    
    def _calculate_stress_level(self, city_activity: float, environmental_data: Dict) -> float:
        """Calculate population stress level."""
        # Base stress from activity
        activity_stress = max(0.0, (city_activity - 0.4) * 1.5)
        
        # Environmental stress
        air_quality = environmental_data.get('air_quality', 0.5)
        noise_level = environmental_data.get('noise_level', 0.5)
        temperature = environmental_data.get('temperature', 20)
        
        env_stress = (1.0 - air_quality) * 0.3 + noise_level * 0.2 + abs(temperature - 22) / 30 * 0.2
        
        return min(activity_stress + env_stress, 1.0)
    
    def _calculate_recovery_rate(self, population_health: float, biocore_effects: List[Dict]) -> float:
        """Calculate population recovery rate."""
        base_recovery = population_health * 0.8
        
        # BioCore effects on recovery
        bio_recovery = 0.0
        for effect in biocore_effects:
            plant = effect.get('plant', '')
            if plant in ['Aloe', 'Turmeric', 'Ginkgo']:
                # Recovery-enhancing plants
                bio_recovery += effect.get('synergy', 0.0) * 0.15
        
        return min(base_recovery + bio_recovery, 1.0)
    
    def _calculate_medical_resource_usage(self, disease_prevalence: Dict[str, float], 
                                    stress_level: float) -> float:
        """Calculate medical resource usage."""
        # Base usage from disease prevalence
        disease_load = sum(disease_prevalence.values()) / len(disease_prevalence)
        
        # Additional usage from stress
        stress_load = stress_level * 0.3
        
        return min(disease_load + stress_load, 1.0)
    
    def _get_biocore_effectiveness(self, plant: str, drug: str, synergy: float) -> float:
        """Get BioCore effectiveness for health impact."""
        cache_key = f"{plant}-{drug}"
        
        if cache_key not in self.bio_effectiveness_cache:
            # Calculate effectiveness based on plant and drug properties
            plant_effect = {
                'Ginkgo': 0.6,      # Cognitive enhancement
                'Aloe': 0.4,          # Healing properties
                'Turmeric': 0.8,        # Anti-inflammatory
                'Ginseng': 0.7,        # Energy/immune boost
                'Ashwagandha': 0.9     # Stress reduction
            }.get(plant, 0.5)
            
            drug_effect = {
                'DrugA': 0.5,  # Basic medication
                'DrugB': 0.7,  # Advanced medication
                'DrugC': 0.6,  # Targeted therapy
                'DrugD': 0.8,  # Experimental treatment
                'DrugE': 0.9   # Cutting-edge therapy
            }.get(drug, 0.5)
            
            effectiveness = (plant_effect + drug_effect) / 2.0
            self.bio_effectiveness_cache[cache_key] = effectiveness
        
        return self.bio_effectiveness_cache[cache_key]
    
    def predict_health_outcomes(self, zone_id: int, time_horizon: int = 24) -> Dict:
        """
        Predict health outcomes for a zone over time.
        
        Args:
            zone_id: Zone identifier
            time_horizon: Hours to predict ahead
            
        Returns:
            Predicted health outcomes
        """
        if zone_id not in self.health_history or len(self.health_history[zone_id]) < 5:
            return {'error': 'Insufficient historical data'}
        
        recent_data = self.health_history[zone_id][-5:]
        
        # Extract trends
        health_trend = np.polyfit(range(len(recent_data)), 
                                [h.population_health for h in recent_data], 1)
        
        # Predict future health
        future_health = []
        for hour in range(1, time_horizon + 1):
            predicted_health = health_trend[0] * hour + health_trend[1]
            predicted_health = max(0.0, min(predicted_health, 1.0))
            future_health.append(predicted_health)
        
        # Calculate risk assessment
        avg_health = np.mean(future_health)
        min_health = np.min(future_health)
        
        if avg_health > 0.8 and min_health > 0.6:
            risk_level = HealthRisk.LOW
        elif avg_health > 0.6 and min_health > 0.4:
            risk_level = HealthRisk.MODERATE
        elif avg_health > 0.4 and min_health > 0.2:
            risk_level = HealthRisk.HIGH
        else:
            risk_level = HealthRisk.CRITICAL
        
        return {
            'zone_id': zone_id,
            'time_horizon': time_horizon,
            'predicted_health': future_health,
            'average_health': avg_health,
            'minimum_health': min_health,
            'risk_level': risk_level.value,
            'trend_slope': health_trend[0]
        }
    
    def recommend_biomedical_interventions(self, zone_id: int, 
                                      current_metrics: HealthMetrics) -> List[Dict]:
        """
        Recommend biomedical interventions based on current metrics.
        
        Args:
            zone_id: Zone identifier
            current_metrics: Current health metrics
            
        Returns:
            List of recommended interventions
        """
        interventions = []
        
        # Disease-specific interventions
        if current_metrics.disease_prevalence > 0.3:
            interventions.append({
                'type': 'disease_control',
                'priority': 'HIGH',
                'action': 'Deploy targeted vaccination campaigns',
                'expected_impact': 0.2,
                'timeline': '2-4 weeks'
            })
        
        # Stress-related interventions
        if current_metrics.stress_level > 0.6:
            interventions.append({
                'type': 'stress_reduction',
                'priority': 'MEDIUM',
                'action': 'Implement mental health support programs',
                'expected_impact': 0.15,
                'timeline': '1-2 weeks'
            })
        
        # Immunity-boosting interventions
        if current_metrics.immunity_level < 0.5:
            interventions.append({
                'type': 'immunity_boost',
                'priority': 'HIGH',
                'action': 'Distribute immune-enhancing supplements',
                'expected_impact': 0.25,
                'timeline': '1 week'
            })
        
        # Recovery support interventions
        if current_metrics.recovery_rate < 0.4:
            interventions.append({
                'type': 'recovery_support',
                'priority': 'MEDIUM',
                'action': 'Increase medical facility capacity',
                'expected_impact': 0.1,
                'timeline': '3-4 weeks'
            })
        
        # Resource optimization
        if current_metrics.medical_resource_usage > 0.8:
            interventions.append({
                'type': 'resource_optimization',
                'priority': 'LOW',
                'action': 'Optimize medical resource allocation',
                'expected_impact': 0.05,
                'timeline': '1-2 weeks'
            })
        
        return sorted(interventions, key=lambda x: {'HIGH': 0, 'MEDIUM': 1, 'LOW': 2}[x['priority']])
    
    def update_health_history(self, zone_id: int, metrics: HealthMetrics) -> None:
        """Update health history for a zone."""
        if zone_id not in self.health_history:
            self.health_history[zone_id] = []
        
        self.health_history[zone_id].append(metrics)
        
        # Keep only last 100 records
        if len(self.health_history[zone_id]) > 100:
            self.health_history[zone_id] = self.health_history[zone_id][-100:]
    
    def get_biomedical_summary(self) -> Dict:
        """Get summary of biomedical analytics across all zones."""
        if not self.health_history:
            return {'status': 'No data available'}
        
        summary = {
            'total_zones': len(self.health_history),
            'avg_population_health': 0.0,
            'avg_disease_prevalence': 0.0,
            'avg_immunity_level': 0.0,
            'high_risk_zones': 0,
            'critical_interventions': 0
        }
        
        all_metrics = []
        for zone_history in self.health_history.values():
            if zone_history:
                all_metrics.extend(zone_history)
        
        if all_metrics:
            summary['avg_population_health'] = np.mean([m.population_health for m in all_metrics])
            summary['avg_disease_prevalence'] = np.mean([m.disease_prevalence for m in all_metrics])
            summary['avg_immunity_level'] = np.mean([m.immunity_level for m in all_metrics])
            
            # Count high-risk zones
            for zone_id, zone_history in self.health_history.items():
                if zone_history:
                    latest_metrics = zone_history[-1]
                    if latest_metrics.disease_prevalence > 0.5 or latest_metrics.stress_level > 0.7:
                        summary['high_risk_zones'] += 1
        
        return summary
