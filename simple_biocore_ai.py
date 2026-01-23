#!/usr/bin/env python3
"""
🧬 Simple BioCore AI Predictor (Rule-based)
No ML dependencies - uses intelligent rules for predictions
"""

class SimpleBioCoreAI:
    def __init__(self):
        self.plants = {
            'Turmeric': {'anti-inflammatory': 0.9, 'antioxidant': 0.8, 'neuroprotective': 0.7},
            'Ginseng': {'energy': 0.9, 'cognitive': 0.8, 'adaptogenic': 0.9},
            'Ashwagandha': {'stress-relief': 0.9, 'anxiety': 0.8, 'sleep': 0.7},
            'Brahmi': {'memory': 0.9, 'cognitive': 0.8, 'focus': 0.9},
            'Tulsi': {'immune': 0.8, 'respiratory': 0.7, 'stress-relief': 0.8}
        }
        
        self.drugs = {
            'NeuroBoost': {'cognitive': 0.9, 'focus': 0.8, 'memory': 0.9, 'energy': 0.7},
            'CellRegen': {'regeneration': 0.9, 'anti-aging': 0.8, 'cellular': 0.9},
            'BioSynth': {'synthesis': 0.9, 'metabolism': 0.8, 'energy': 0.8},
            'MetaCore': {'metabolic': 0.9, 'mitochondrial': 0.8, 'energy': 0.9},
            'QuantumHeal': {'healing': 0.9, 'cellular': 0.8, 'quantum': 0.9},
            'Synaptic': {'neural': 0.9, 'cognitive': 0.9, 'synaptic': 0.8},
            'DermalFix': {'skin': 0.9, 'regeneration': 0.8, 'healing': 0.7},
            'VitaCore': {'vitality': 0.9, 'energy': 0.8, 'immune': 0.8}
        }
        
        self.zone_priorities = {
            'downtown': {'stress-relief': 0.9, 'cognitive': 0.7, 'energy': 0.6},
            'industrial': {'regeneration': 0.8, 'stress-relief': 0.7, 'immune': 0.6},
            'residential': {'stress-relief': 0.8, 'sleep': 0.7, 'immune': 0.6},
            'tech': {'cognitive': 0.9, 'focus': 0.8, 'energy': 0.7},
            'medical': {'healing': 0.9, 'regeneration': 0.8, 'immune': 0.7}
        }
    
    def calculate_effectiveness(self, plant, drug, zone_type, synergy):
        """Calculate effectiveness using rule-based scoring"""
        plant_props = self.plants[plant]
        drug_props = self.drugs[drug]
        zone_prio = self.zone_priorities[zone_type]
        
        # Find matching properties
        score = 0
        matches = 0
        
        for prop in plant_props:
            if prop in drug_props:
                # Plant-drug synergy
                combined_effect = (plant_props[prop] + drug_props[prop]) / 2
                # Zone priority multiplier
                priority_multiplier = zone_prio.get(prop, 0.5)
                # Calculate score
                score += combined_effect * priority_multiplier
                matches += 1
        
        if matches == 0:
            return 0.3  # Base effectiveness for non-matching combos
        
        # Average score and apply synergy
        base_score = score / matches
        final_score = base_score * synergy
        
        # Add some randomness for realism
        import random
        final_score *= random.uniform(0.9, 1.1)
        
        return min(0.95, max(0.1, final_score))
    
    def predict_optimal_combination(self, zone_type):
        """Find optimal combination for a zone"""
        best_combo = None
        best_score = 0
        
        for plant in self.plants:
            for drug in self.drugs:
                for synergy in [0.7, 0.8, 0.9, 1.0]:
                    score = self.calculate_effectiveness(plant, drug, zone_type, synergy)
                    
                    if score > best_score:
                        best_score = score
                        best_combo = {
                            'plant': plant,
                            'drug': drug,
                            'synergy': synergy,
                            'predicted_effectiveness': score,
                            'confidence': min(score * 1.2, 1.0)
                        }
        
        return best_combo
    
    def get_top_combinations(self, zone_type, n=5):
        """Get top N combinations for a zone"""
        combinations = []
        
        for plant in self.plants:
            for drug in self.drugs:
                for synergy in [0.6, 0.7, 0.8, 0.9, 1.0]:
                    score = self.calculate_effectiveness(plant, drug, zone_type, synergy)
                    
                    combinations.append({
                        'plant': plant,
                        'drug': drug,
                        'synergy': synergy,
                        'predicted_effectiveness': score,
                        'ranking_score': score * synergy
                    })
        
        # Sort by ranking score
        combinations.sort(key=lambda x: x['ranking_score'], reverse=True)
        return combinations[:n]
    
    def train_models(self):
        """Mock training for compatibility"""
        print("🧬 Simple AI system ready (rule-based)")
        return True
    
    def save_models(self, filepath='biocore_ai_models.pkl'):
        """Mock save for compatibility"""
        print("💾 Simple AI system doesn't need saving")
        return True
    
    def load_models(self, filepath='biocore_ai_models.pkl'):
        """Mock load for compatibility"""
        print("📂 Simple AI system loaded")
        return True

# Global instance
simple_ai = SimpleBioCoreAI()
