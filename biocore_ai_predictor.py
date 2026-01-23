#!/usr/bin/env python3
"""
🧬 BioCore AI Synergy Prediction Engine
Advanced machine learning for plant-drug combination optimization
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
import joblib
import json
from typing import Dict, List, Tuple, Any
import logging

class BioCoreAIPredictor:
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
        
        self.models = {
            'random_forest': RandomForestRegressor(n_estimators=100, random_state=42),
            'gradient_boost': GradientBoostingRegressor(n_estimators=100, random_state=42),
            'neural_network': MLPRegressor(hidden_layer_sizes=(64, 32), max_iter=1000, random_state=42)
        }
        
        self.scaler = StandardScaler()
        self.plant_encoder = LabelEncoder()
        self.drug_encoder = LabelEncoder()
        self.trained_models = {}
        
    def generate_training_data(self, n_samples=10000):
        """Generate synthetic training data based on plant-drug properties"""
        data = []
        
        for _ in range(n_samples):
            plant = np.random.choice(list(self.plants.keys()))
            drug = np.random.choice(list(self.drugs.keys()))
            synergy = np.random.uniform(0, 1)
            
            # Calculate base effectiveness from properties
            plant_props = self.plants[plant]
            drug_props = self.drugs[drug]
            
            # Find overlapping properties
            common_effects = set(plant_props.keys()) & set(drug_props.keys())
            base_effectiveness = 0
            
            for effect in common_effects:
                base_effectiveness += (plant_props[effect] * drug_props[effect]) / len(common_effects)
            
            # Add noise and synergy multiplier
            effectiveness = base_effectiveness * synergy * np.random.uniform(0.8, 1.2)
            effectiveness = np.clip(effectiveness, 0, 1)
            
            # Zone-specific factors
            zone_type = np.random.choice(['downtown', 'residential', 'industrial', 'medical', 'tech'])
            zone_modifier = {
                'downtown': 0.8,
                'residential': 1.0,
                'industrial': 0.7,
                'medical': 1.2,
                'tech': 1.1
            }[zone_type]
            
            final_effectiveness = effectiveness * zone_modifier * np.random.uniform(0.9, 1.1)
            final_effectiveness = np.clip(final_effectiveness, 0, 1)
            
            data.append({
                'plant': plant,
                'drug': drug,
                'synergy': synergy,
                'zone_type': zone_type,
                'effectiveness': final_effectiveness,
                'base_effectiveness': effectiveness
            })
        
        return pd.DataFrame(data)
    
    def prepare_features(self, df):
        """Prepare features for machine learning"""
        # Encode categorical variables
        df['plant_encoded'] = self.plant_encoder.fit_transform(df['plant'])
        df['drug_encoded'] = self.drug_encoder.fit_transform(df['drug'])
        df['zone_encoded'] = pd.Categorical(df['zone_type']).codes
        
        # Create feature vectors
        features = []
        for _, row in df.iterrows():
            plant_props = list(self.plants[row['plant']].values())
            drug_props = list(self.drugs[row['drug']].values())
            
            # Pad shorter property list
            max_props = 5
            plant_props.extend([0] * (max_props - len(plant_props)))
            drug_props.extend([0] * (max_props - len(drug_props)))
            
            feature_vector = [
                row['plant_encoded'],
                row['drug_encoded'],
                row['zone_encoded'],
                row['synergy'],
                *plant_props,
                *drug_props
            ]
            features.append(feature_vector)
        
        return np.array(features)
    
    def train_models(self):
        """Train all ML models"""
        print("🧬 Training BioCore AI Prediction Models...")
        
        # Generate training data
        df = self.generate_training_data()
        X = self.prepare_features(df)
        y = df['effectiveness'].values
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train each model
        for name, model in self.models.items():
            print(f"📊 Training {name.replace('_', ' ').title()}...")
            model.fit(X_train_scaled, y_train)
            
            # Evaluate
            score = model.score(X_test_scaled, y_test)
            print(f"✅ {name.replace('_', ' ').title()} R² Score: {score:.4f}")
            
            # Cross-validation
            cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=5)
            print(f"🎯 Cross-Validation Score: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
            
            self.trained_models[name] = model
        
        print("🎉 All models trained successfully!")
        return self.trained_models
    
    def predict_optimal_combination(self, zone_type, target_effectiveness=0.8):
        """Predict optimal plant-drug combination for a specific zone"""
        best_combination = None
        best_score = 0
        
        print(f"🔍 Finding optimal combination for {zone_type} zone...")
        
        for plant in self.plants.keys():
            for drug in self.drugs.keys():
                for synergy in np.linspace(0.3, 1.0, 8):
                    # Prepare features
                    df_test = pd.DataFrame([{
                        'plant': plant,
                        'drug': drug,
                        'synergy': synergy,
                        'zone_type': zone_type
                    }])
                    
                    X_test = self.prepare_features(df_test)
                    X_test_scaled = self.scaler.transform(X_test)
                    
                    # Get predictions from all models
                    predictions = []
                    for model in self.trained_models.values():
                        pred = model.predict(X_test_scaled)[0]
                        predictions.append(pred)
                    
                    # Ensemble prediction
                    ensemble_pred = np.mean(predictions)
                    
                    if ensemble_pred > best_score:
                        best_score = ensemble_pred
                        best_combination = {
                            'plant': plant,
                            'drug': drug,
                            'synergy': synergy,
                            'predicted_effectiveness': ensemble_pred,
                            'confidence': min(ensemble_pred / target_effectiveness, 1.0)
                        }
        
        return best_combination
    
    def get_top_combinations(self, zone_type, n=5):
        """Get top N combinations for a zone"""
        combinations = []
        
        for plant in self.plants.keys():
            for drug in self.drugs.keys():
                for synergy in np.linspace(0.3, 1.0, 5):
                    df_test = pd.DataFrame([{
                        'plant': plant,
                        'drug': drug,
                        'synergy': synergy,
                        'zone_type': zone_type
                    }])
                    
                    X_test = self.prepare_features(df_test)
                    X_test_scaled = self.scaler.transform(X_test)
                    
                    predictions = []
                    for model in self.trained_models.values():
                        pred = model.predict(X_test_scaled)[0]
                        predictions.append(pred)
                    
                    ensemble_pred = np.mean(predictions)
                    
                    combinations.append({
                        'plant': plant,
                        'drug': drug,
                        'synergy': synergy,
                        'predicted_effectiveness': ensemble_pred,
                        'ranking_score': ensemble_pred * synergy
                    })
        
        # Sort by ranking score
        combinations.sort(key=lambda x: x['ranking_score'], reverse=True)
        return combinations[:n]
    
    def save_models(self, filepath='biocore_ai_models.pkl'):
        """Save trained models"""
        model_data = {
            'models': self.trained_models,
            'scaler': self.scaler,
            'plant_encoder': self.plant_encoder,
            'drug_encoder': self.drug_encoder
        }
        joblib.dump(model_data, filepath)
        print(f"💾 Models saved to {filepath}")
    
    def load_models(self, filepath='biocore_ai_models.pkl'):
        """Load trained models"""
        try:
            model_data = joblib.load(filepath)
            self.trained_models = model_data['models']
            self.scaler = model_data['scaler']
            self.plant_encoder = model_data['plant_encoder']
            self.drug_encoder = model_data['drug_encoder']
            print(f"📂 Models loaded from {filepath}")
            return True
        except FileNotFoundError:
            print("❌ No saved models found. Training new models...")
            return False

# Initialize and train the AI predictor
if __name__ == "__main__":
    predictor = BioCoreAIPredictor()
    
    # Try to load existing models
    if not predictor.load_models():
        # Train new models
        predictor.train_models()
        predictor.save_models()
    
    # Test predictions
    print("\n🧪 Testing AI Predictions:")
    print("=" * 50)
    
    zones = ['downtown', 'residential', 'industrial', 'medical', 'tech']
    
    for zone in zones:
        print(f"\n🏙️ {zone.upper()} ZONE:")
        optimal = predictor.predict_optimal_combination(zone)
        print(f"🎯 Optimal: {optimal['plant']} + {optimal['drug']} (synergy: {optimal['synergy']:.2f})")
        print(f"📈 Predicted Effectiveness: {optimal['predicted_effectiveness']:.3f}")
        print(f"🔋 Confidence: {optimal['confidence']:.2%}")
        
        print("🏆 Top 3 Combinations:")
        top_combinations = predictor.get_top_combinations(zone, 3)
        for i, combo in enumerate(top_combinations, 1):
            print(f"  {i}. {combo['plant']} + {combo['drug']} (synergy: {combo['synergy']:.2f}) - {combo['predicted_effectiveness']:.3f}")
