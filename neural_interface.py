#!/usr/bin/env python3
"""
🧠 Neural Interface & Consciousness System
Direct brain-city connection for Homeostatic City BioCore
"""

import asyncio
import time
import random
import json
from datetime import datetime
from typing import Dict, List, Any
import logging

class NeuralInterface:
    def __init__(self):
        self.connected_minds = {}
        self.collective_consciousness = {
            'thought_patterns': [],
            'emotional_state': 'balanced',
            'cognitive_load': 0.5,
            'collective_intelligence': 0.7,
            'neural_harmony': 0.8,
            'consciousness_level': 'alpha'
        }
        
        self.neural_frequencies = {
            'delta': (0.5, 4, 'deep_sleep', 'healing'),
            'theta': (4, 8, 'meditation', 'creativity'),
            'alpha': (8, 12, 'relaxed', 'learning'),
            'beta': (12, 30, 'active', 'focus'),
            'gamma': (30, 100, 'peak_performance', 'insight')
        }
        
        self.thought_forms = {
            'calm': {'frequency': 'alpha', 'coherence': 0.9, 'city_effect': 'stabilizing'},
            'creative': {'frequency': 'theta', 'coherence': 0.8, 'city_effect': 'innovative'},
            'focused': {'frequency': 'beta', 'coherence': 0.85, 'city_effect': 'productive'},
            'stressed': {'frequency': 'high_beta', 'coherence': 0.4, 'city_effect': 'disruptive'},
            'meditative': {'frequency': 'theta', 'coherence': 0.95, 'city_effect': 'harmonizing'},
            'ecstatic': {'frequency': 'gamma', 'coherence': 0.9, 'city_effect': 'elevating'}
        }
        
        self.neural_history = []
        self.consciousness_events = []
        
    def connect_mind(self, mind_id, name, neural_signature):
        """Connect a new mind to the collective consciousness"""
        mind = {
            'id': mind_id,
            'name': name,
            'neural_signature': neural_signature,
            'current_frequency': 'alpha',
            'coherence': 0.8,
            'thought_patterns': [],
            'emotional_state': 'balanced',
            'connection_strength': 0.7,
            'contribution_to_collective': 0.5,
            'last_update': datetime.now()
        }
        
        self.connected_minds[mind_id] = mind
        return mind
    
    def update_neural_activity(self):
        """Simulate real-time neural activity of all connected minds"""
        current_time = datetime.now()
        
        for mind_id, mind in self.connected_minds.items():
            # Simulate neural frequency changes
            freq_change = random.choice([-1, 0, 1])
            frequencies = list(self.neural_frequencies.keys())
            current_index = frequencies.index(mind['current_frequency'])
            new_index = max(0, min(len(frequencies) - 1, current_index + freq_change))
            mind['current_frequency'] = frequencies[new_index]
            
            # Update coherence based on collective harmony
            mind['coherence'] = max(0.3, min(1.0, 
                mind['coherence'] + (random.random() - 0.5) * 0.1
            ))
            
            # Generate thought patterns
            thought = self.generate_thought_pattern(mind)
            mind['thought_patterns'].append(thought)
            
            # Keep only recent thoughts
            if len(mind['thought_patterns']) > 10:
                mind['thought_patterns'].pop(0)
            
            # Update emotional state
            mind['emotional_state'] = random.choice([
                'calm', 'creative', 'focused', 'stressed', 
                'meditative', 'ecstatic', 'balanced'
            ])
            
            mind['last_update'] = current_time
        
        # Update collective consciousness
        self.update_collective_consciousness()
        
        # Store in history
        self.neural_history.append({
            'timestamp': current_time.isoformat(),
            'connected_minds': len(self.connected_minds),
            'collective_state': self.collective_consciousness.copy()
        })
        
        # Keep only last 50 entries
        if len(self.neural_history) > 50:
            self.neural_history.pop(0)
    
    def generate_thought_pattern(self, mind):
        """Generate a thought pattern for a mind"""
        emotions = ['peace', 'innovation', 'focus', 'anxiety', 'harmony', 'excitement']
        concepts = ['city', 'nature', 'technology', 'community', 'future', 'balance']
        
        thought = {
            'timestamp': datetime.now().isoformat(),
            'emotion': random.choice(emotions),
            'concept': random.choice(concepts),
            'intensity': random.uniform(0.3, 1.0),
            'frequency': mind['current_frequency'],
            'coherence': mind['coherence'],
            'neural_signature': mind['neural_signature']
        }
        
        return thought
    
    def update_collective_consciousness(self):
        """Update the collective consciousness based on all connected minds"""
        if not self.connected_minds:
            return
        
        # Calculate average neural metrics
        total_coherence = sum(mind['coherence'] for mind in self.connected_minds.values())
        avg_coherence = total_coherence / len(self.connected_minds)
        
        # Count frequency distribution
        freq_counts = {}
        for mind in self.connected_minds.values():
            freq = mind['current_frequency']
            freq_counts[freq] = freq_counts.get(freq, 0) + 1
        
        # Determine dominant frequency
        dominant_freq = max(freq_counts, key=freq_counts.get)
        
        # Update collective consciousness
        self.collective_consciousness['neural_harmony'] = avg_coherence
        self.collective_consciousness['consciousness_level'] = dominant_freq
        
        # Calculate cognitive load based on active minds
        active_minds = sum(1 for mind in self.connected_minds.values() 
                         if mind['current_frequency'] in ['beta', 'gamma'])
        self.collective_consciousness['cognitive_load'] = active_minds / len(self.connected_minds)
        
        # Update collective intelligence
        self.collective_consciousness['collective_intelligence'] = min(1.0, 
            avg_coherence * (1 + len(self.connected_minds) * 0.1)
        )
        
        # Determine emotional state
        emotions = [mind['emotional_state'] for mind in self.connected_minds.values()]
        emotion_counts = {}
        for emotion in emotions:
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        
        dominant_emotion = max(emotion_counts, key=emotion_counts.get)
        self.collective_consciousness['emotional_state'] = dominant_emotion
        
        # Store thought patterns
        all_thoughts = []
        for mind in self.connected_minds.values():
            all_thoughts.extend(mind['thought_patterns'][-3:])  # Last 3 thoughts per mind
        
        self.collective_consciousness['thought_patterns'] = all_thoughts[-20:]  # Keep last 20
    
    def calculate_city_influence(self):
        """Calculate how collective consciousness influences city zones"""
        influence = {
            'downtown': 0.0,
            'industrial': 0.0,
            'residential': 0.0,
            'tech': 0.0,
            'medical': 0.0
        }
        
        harmony = self.collective_consciousness['neural_harmony']
        intelligence = self.collective_consciousness['collective_intelligence']
        emotional_state = self.collective_consciousness['emotional_state']
        
        # Base influence from collective metrics
        base_influence = harmony * intelligence
        
        # Zone-specific influences based on emotional state
        if emotional_state == 'calm':
            influence['residential'] += base_influence * 0.8
            influence['medical'] += base_influence * 0.6
        elif emotional_state == 'creative':
            influence['tech'] += base_influence * 0.9
            influence['downtown'] += base_influence * 0.7
        elif emotional_state == 'focused':
            influence['industrial'] += base_influence * 0.8
            influence['tech'] += base_influence * 0.7
        elif emotional_state == 'ecstatic':
            influence['downtown'] += base_influence * 0.9
            influence['residential'] += base_influence * 0.5
        elif emotional_state == 'meditative':
            influence['medical'] += base_influence * 0.9
            influence['residential'] += base_influence * 0.8
        
        # Frequency-based influences
        freq = self.collective_consciousness['consciousness_level']
        if freq == 'gamma':
            # Peak performance - boost all zones
            for zone in influence:
                influence[zone] += base_influence * 0.3
        elif freq == 'delta':
            # Deep sleep - calm all zones
            for zone in influence:
                influence[zone] = max(0, influence[zone] - base_influence * 0.2)
        
        return influence
    
    def generate_consciousness_event(self):
        """Generate a significant consciousness event"""
        events = [
            {
                'type': 'collective_enlightenment',
                'description': 'Collective consciousness reaches new level of awareness',
                'impact': 'harmonizing',
                'duration': random.randint(300, 900)
            },
            {
                'type': 'neural_synchronization',
                'description': 'All connected minds achieve perfect coherence',
                'impact': 'stabilizing',
                'duration': random.randint(180, 600)
            },
            {
                'type': 'consciousness_shift',
                'description': 'Mass shift in collective emotional state',
                'impact': 'transformative',
                'duration': random.randint(600, 1800)
            },
            {
                'type': 'psi_resonance',
                'description': 'Strong psychic resonance detected in city grid',
                'impact': 'amplifying',
                'duration': random.randint(120, 360)
            }
        ]
        
        event = random.choice(events)
        event['timestamp'] = datetime.now().isoformat()
        event['consciousness_level'] = self.collective_consciousness['consciousness_level']
        event['neural_harmony'] = self.collective_consciousness['neural_harmony']
        
        self.consciousness_events.append(event)
        
        # Keep only last 20 events
        if len(self.consciousness_events) > 20:
            self.consciousness_events.pop(0)
        
        return event
    
    def get_neural_metrics(self):
        """Get comprehensive neural metrics"""
        return {
            'connected_minds': len(self.connected_minds),
            'collective_consciousness': self.collective_consciousness,
            'city_influence': self.calculate_city_influence(),
            'recent_events': self.consciousness_events[-5:],
            'neural_health': self.calculate_neural_health()
        }
    
    def calculate_neural_health(self):
        """Calculate overall neural health score"""
        if not self.connected_minds:
            return 0.5
        
        harmony = self.collective_consciousness['neural_harmony']
        intelligence = self.collective_consciousness['collective_intelligence']
        cognitive_load = self.collective_consciousness['cognitive_load']
        
        # Optimal cognitive load is around 0.6
        load_score = 1.0 - abs(cognitive_load - 0.6)
        
        health_score = (harmony * 0.4 + intelligence * 0.3 + load_score * 0.3)
        return round(health_score, 2)

# Global neural interface instance
neural_interface = NeuralInterface()

# Initialize with some connected minds
neural_interface.connect_mind('mind_001', 'Alpha Consciousness', 'alpha_wave_pattern')
neural_interface.connect_mind('mind_002', 'Beta Mind', 'beta_frequency')
neural_interface.connect_mind('mind_003', 'Theta State', 'theta_rhythm')
neural_interface.connect_mind('mind_004', 'Gamma Peak', 'gamma_burst')
neural_interface.connect_mind('mind_005', 'Delta Deep', 'delta_wave')

async def start_neural_monitoring():
    """Start continuous neural monitoring"""
    while True:
        neural_interface.update_neural_activity()
        
        # Random consciousness events
        if random.random() < 0.05:  # 5% chance
            event = neural_interface.generate_consciousness_event()
            print(f"🧠 Consciousness Event: {event['type']}")
        
        await asyncio.sleep(10)  # Update every 10 seconds

if __name__ == "__main__":
    print("🧠 Neural Interface System Initialized")
    print("=" * 50)
    
    # Test neural interface
    neural_interface.update_neural_activity()
    metrics = neural_interface.get_neural_metrics()
    
    print(f"🔗 Connected Minds: {metrics['connected_minds']}")
    print(f"🌊 Collective Consciousness Level: {metrics['collective_consciousness']['consciousness_level']}")
    print(f"🎵 Neural Harmony: {metrics['collective_consciousness']['neural_harmony']:.2f}")
    print(f"🧠 Collective Intelligence: {metrics['collective_consciousness']['collective_intelligence']:.2f}")
    print(f"💚 Neural Health: {metrics['neural_health']:.2f}")
    
    print("\n🏙️ City Influence:")
    for zone, influence in metrics['city_influence'].items():
        print(f"  {zone}: {influence:.3f}")
    
    if metrics['recent_events']:
        print(f"\n⚡ Recent Consciousness Events:")
        for event in metrics['recent_events'][-3:]:
            print(f"  {event['type']}: {event['description']}")
