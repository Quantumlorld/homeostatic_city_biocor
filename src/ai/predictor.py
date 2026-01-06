"""
AI Predictor Module
Machine learning predictions for city dynamics and BioCore optimization.
"""

import numpy as np
from typing import List, Dict, Tuple, Optional
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import joblib
import os


class AIPredictor:
    """
    AI-powered predictor for city dynamics and BioCore effects.
    Uses ensemble methods for robust predictions.
    """
    
    def __init__(self, model_path: Optional[str] = None):
        """
        Initialize AI predictor.
        
        Args:
            model_path: Path to saved model (optional)
        """
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.is_trained = False
        self.model_path = model_path or "models/ai_predictor.joblib"
        
        # Feature names for interpretability
        self.feature_names = [
            'zone_activity', 'time_of_day', 'day_of_week', 
            'population_density', 'weather_severity', 'historical_avg',
            'biocore_synergy', 'plant_potency', 'drug_effectiveness'
        ]
    
    def extract_features(self, zone_data: Dict, biocore_data: Dict, 
                     environmental_data: Dict) -> np.ndarray:
        """
        Extract features for ML prediction.
        
        Args:
            zone_data: Current zone state
            biocore_data: BioCore effect data
            environmental_data: Environmental factors
            
        Returns:
            Feature array for prediction
        """
        features = [
            zone_data.get('activity', 0.5),
            environmental_data.get('time_of_day', 12) / 24.0,  # Normalize to 0-1
            environmental_data.get('day_of_week', 3) / 7.0,    # Normalize to 0-1
            environmental_data.get('population_density', 0.5),
            environmental_data.get('weather_severity', 0.0),
            zone_data.get('historical_avg', 0.5),
            biocore_data.get('synergy', 0.5),
            biocore_data.get('plant_potency', 0.5),
            biocore_data.get('drug_effectiveness', 0.5)
        ]
        
        return np.array(features).reshape(1, -1)
    
    def predict_zone_activity(self, zone_data: Dict, biocore_data: Dict, 
                          environmental_data: Dict) -> Tuple[float, float]:
        """
        Predict future zone activity and confidence.
        
        Args:
            zone_data: Current zone state
            biocore_data: BioCore effect data
            environmental_data: Environmental factors
            
        Returns:
            Tuple of (predicted_activity, confidence_score)
        """
        if not self.is_trained:
            return 0.5, 0.0
        
        features = self.extract_features(zone_data, biocore_data, environmental_data)
        features_scaled = self.scaler.transform(features)
        
        # Get prediction from all trees
        predictions = [tree.predict(features_scaled) for tree in self.model.estimators_]
        predicted_activity = np.mean(predictions)
        
        # Calculate confidence based on prediction variance
        confidence = 1.0 - (np.std(predictions) / (predicted_activity + 0.1))
        confidence = np.clip(confidence, 0.0, 1.0)
        
        return float(predicted_activity), float(confidence)
    
    def predict_optimal_biocore(self, zone_data: Dict, 
                              environmental_data: Dict) -> Dict:
        """
        Predict optimal BioCore configuration for a zone.
        
        Args:
            zone_data: Current zone state
            environmental_data: Environmental factors
            
        Returns:
            Optimal BioCore configuration
        """
        if not self.is_trained:
            return {'plant': 'Turmeric', 'drug': 'DrugB', 'synergy': 0.5}
        
        best_config = None
        best_score = float('inf')
        
        plants = ['Ginkgo', 'Aloe', 'Turmeric', 'Ginseng', 'Ashwagandha']
        drugs = ['DrugA', 'DrugB', 'DrugC', 'DrugD', 'DrugE']
        
        for plant in plants:
            for drug in drugs:
                for synergy in np.linspace(0.1, 1.0, 10):
                    biocore_data = {
                        'plant': plant,
                        'drug': drug,
                        'synergy': synergy,
                        'plant_potency': self._get_plant_potency(plant),
                        'drug_effectiveness': self._get_drug_effectiveness(drug)
                    }
                    
                    predicted_activity, confidence = self.predict_zone_activity(
                        zone_data, biocore_data, environmental_data
                    )
                    
                    # Score based on distance to target and confidence
                    target = 0.5
                    score = abs(predicted_activity - target) / (confidence + 0.1)
                    
                    if score < best_score:
                        best_score = score
                        best_config = {
                            'plant': plant,
                            'drug': drug,
                            'synergy': synergy,
                            'predicted_activity': predicted_activity,
                            'confidence': confidence,
                            'score': score
                        }
        
        return best_config
    
    def train(self, training_data: List[Dict]) -> None:
        """
        Train the AI model with historical data.
        
        Args:
            training_data: List of training examples
        """
        if len(training_data) < 10:
            print("⚠️  Insufficient training data (need at least 10 samples)")
            return
        
        # Extract features and targets
        X = []
        y = []
        
        for example in training_data:
            features = self.extract_features(
                example['zone_data'],
                example['biocore_data'],
                example['environmental_data']
            )
            X.append(features.flatten())
            y.append(example['target_activity'])
        
        X = np.array(X)
        y = np.array(y)
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Train model
        self.model.fit(X_scaled, y)
        self.is_trained = True
        
        # Save model
        self._save_model()
        
        print(f"✅ AI Model trained with {len(training_data)} samples")
        print(f"📊 Model R² score: {self.model.score(X_scaled, y):.3f}")
    
    def _get_plant_potency(self, plant: str) -> float:
        """Get plant potency value."""
        potency_map = {
            'Ginkgo': 0.7,
            'Aloe': 0.5,
            'Turmeric': 0.8,
            'Ginseng': 0.6,
            'Ashwagandha': 0.9
        }
        return potency_map.get(plant, 0.5)
    
    def _get_drug_effectiveness(self, drug: str) -> float:
        """Get drug effectiveness value."""
        effectiveness_map = {
            'DrugA': 0.6,
            'DrugB': 0.7,
            'DrugC': 0.8,
            'DrugD': 0.5,
            'DrugE': 0.9
        }
        return effectiveness_map.get(drug, 0.5)
    
    def _save_model(self) -> None:
        """Save trained model to disk."""
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        joblib.dump({
            'model': self.model,
            'scaler': self.scaler,
            'feature_names': self.feature_names
        }, self.model_path)
    
    def load_model(self) -> bool:
        """
        Load trained model from disk.
        
        Returns:
            True if model loaded successfully
        """
        try:
            data = joblib.load(self.model_path)
            self.model = data['model']
            self.scaler = data['scaler']
            self.feature_names = data['feature_names']
            self.is_trained = True
            print(f"✅ AI Model loaded from {self.model_path}")
            return True
        except FileNotFoundError:
            print("⚠️  No pre-trained model found")
            return False
    
    def get_feature_importance(self) -> Dict[str, float]:
        """
        Get feature importance from trained model.
        
        Returns:
            Dictionary of feature importance scores
        """
        if not self.is_trained:
            return {}
        
        importance = self.model.feature_importances_
        return dict(zip(self.feature_names, importance))
