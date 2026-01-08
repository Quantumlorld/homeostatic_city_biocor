#!/usr/bin/env python3
"""
Integrated BHCS + LunaBeyond AI System
Complete homeostatic system with intelligent AI backend
"""

import asyncio
import time
import json
from pathlib import Path
import sys

# Add paths for imports
sys.path.append(str(Path(__file__).parent))
sys.path.append(str(Path(__file__).parent / "lunabeyond-ai" / "src"))

from test_system import BHCS, BioCore
# from lunabeyond_ai.src.ai_interface import LunaBeyondInterface
# Mock LunaBeyond interface for now
class LunaBeyondInterface:
    def __init__(self):
        self.name = "LunaBeyond AI Mock"
        self.version = "1.0.0"
    
    def process_query(self, query: str) -> str:
        return f"LunaBeyond response to: {query}"
    
    def get_status(self) -> dict:
        return {"status": "active", "mood": "curious", "confidence": 0.85}

class IntegratedBHCSwithAI:
    """Complete BHCS system with LunaBeyond AI integration"""
    
    def __init__(self):
        print("🌙 Initializing Integrated BHCS + LunaBeyond AI System...")
        
        # Initialize BHCS system
        self.bhcs = BHCS(5)
        self.biocore = BioCore()
        
        # Initialize AI
        self.ai_interface = LunaBeyondInterface()
        
        # System state
        self.running = True
        self.update_counter = 0
        self.ai_enabled = True
        
        print("✅ BHCS System Initialized")
        print("✅ BioCore Integration Ready")
        print("✅ LunaBeyond AI Initialized")
        print("✅ Complete Integration Active")
    
    async def run_integrated_system(self):
        """Run the complete integrated system"""
        print("\n🚀 Starting Integrated BHCS + AI System...")
        print("🧠 AI will monitor, analyze, and optimize the system")
        print("🌿 BioCore will provide intelligent interventions")
        print("📊 Real-time system evolution with AI guidance")
        print("=" * 70)
        
        # Start AI monitoring
        ai_task = asyncio.create_task(self.ai_interface.start_ai_monitoring())
        
        # Run main system loop
        try:
            while self.running:
                # Update BHCS system
                self.bhcs.update()
                self.update_counter += 1
                
                # Display system status
                if self.update_counter % 5 == 0:
                    await self.display_integrated_status()
                
                # Apply AI recommendations periodically
                if self.update_counter % 10 == 0 and self.ai_enabled:
                    await self.apply_ai_recommendations()
                
                # Random fluctuations for realistic behavior
                if self.update_counter % 7 == 0:
                    import random
                    zone_id = random.randint(0, 4)
                    influence = (random.random() - 0.5) * 0.2
                    self.bhcs.apply_influence(zone_id, influence)
                
                # Reset periodically
                if self.update_counter % 60 == 0:
                    print("\n🔄 System Reset - Starting Fresh AI Learning Cycle")
                    self.bhcs.reset()
                
                await asyncio.sleep(1)
                
        except KeyboardInterrupt:
            print("\n🛑 Shutting down Integrated System...")
            self.running = False
            self.ai_interface.stop_ai_monitoring()
            print("✅ System shutdown complete")
    
    async def display_integrated_status(self):
        """Display integrated system status with AI insights"""
        print(f"\n🌙 Integrated BHCS + AI Status - {time.strftime('%H:%M:%S')}")
        print("=" * 70)
        
        # BHCS System Status
        self.bhcs.print_status()
        
        # AI Status
        ai_status = self.ai_interface.get_ai_dashboard_data()['ai_status']
        print(f"\n🧠 AI Status:")
        print(f"   Learning: {'✅ Enabled' if ai_status['learning_enabled'] else '❌ Disabled'}")
        print(f"   Prediction Accuracy: {ai_status['prediction_accuracy']:.1%}")
        print(f"   Interventions: {ai_status['successful_interventions']}/{ai_status['interventions_recommended']}")
        print(f"   Data Points: {ai_status['data_points_collected']}")
        print(f"   Learning Progress: {ai_status['learning_progress']:.1%}")
        
        # Recent AI Recommendations
        recent_recs = self.ai_interface.get_ai_dashboard_data()['recent_recommendations']
        if recent_recs:
            print(f"\n🎯 Recent AI Recommendations:")
            for i, rec in enumerate(recent_recs[-3:], 1):
                priority_emoji = "🔴" if rec.get('priority') == 'high' else "🟡"
                print(f"   {i}. {priority_emoji} {rec.get('type', 'Unknown')}")
                print(f"      {rec.get('reason', 'No reason')}")
        
        # Zone-specific AI insights
        print(f"\n📊 Zone AI Analysis:")
        for i in range(5):
            zone_analysis = self.ai_interface.get_zone_analysis(i)
            if zone_analysis:
                pattern = zone_analysis
                print(f"   Zone {i}: Effectiveness {pattern['effectiveness_score']:.1%} | "
                      f"Stress Tendency {pattern['stress_tendency']:.1%} | "
                      f"Optimal: {pattern['optimal_plant']} + {pattern['optimal_drug']}")
        
        print("=" * 70)
    
    async def apply_ai_recommendations(self):
        """Apply AI recommendations to the system"""
        try:
            # Get current system state for AI
            zones_data = []
            for i, zone in enumerate(self.bhcs.zones):
                zones_data.append({
                    'id': zone.id,
                    'activity': zone.activity,
                    'state': zone.state
                })
            
            # Simulate AI analysis
            system_health = self.bhcs.get_system_health()
            
            # Apply AI-driven interventions
            if system_health < 0.6:
                print("🧠 AI: System health low - applying intelligent intervention")
                
                # Find most stressed zone
                most_stressed_zone = max(self.bhcs.zones, key=lambda z: z.activity)
                
                # Get AI recommendation for this zone
                zone_analysis = self.ai_interface.get_zone_analysis(most_stressed_zone.id)
                
                if zone_analysis:
                    # Apply AI-recommended intervention
                    plant = zone_analysis['optimal_plant']
                    drug = zone_analysis['optimal_drug']
                    synergy = zone_analysis['optimal_synergy']
                    
                    # Apply BioCore effect
                    effect = self.biocore.calculate_effect(plant, drug, synergy)
                    influence = -effect['magnitude'] * 0.4  # Stronger AI intervention
                    
                    before_activity = most_stressed_zone.activity
                    self.bhcs.apply_influence(most_stressed_zone.id, influence)
                    after_activity = most_stressed_zone.activity
                    
                    # Record for AI learning
                    self.ai_interface.ai.record_intervention(
                        most_stressed_zone.id, plant, drug, synergy,
                        {'activity': before_activity, 'state': most_stressed_zone.state},
                        {'activity': after_activity, 'state': most_stressed_zone.state}
                    )
                    
                    print(f"🧠 AI Applied: {plant} + {drug} to Zone {most_stressed_zone.id}")
                    print(f"   Result: {before_activity:.3f} → {after_activity:.3f}")
                    print(f"   Effectiveness: {effect['magnitude']:.3f}")
            
            # Record system state for AI learning
            self.ai_interface.ai.record_system_state(zones_data, system_health)
            
        except Exception as e:
            print(f"❌ AI Recommendation Error: {e}")
    
    def toggle_ai(self):
        """Toggle AI on/off"""
        self.ai_enabled = not self.ai_enabled
        if self.ai_enabled:
            self.ai_interface.ai.enable_learning()
            print("🧠 AI Enabled - System optimization active")
        else:
            self.ai_interface.ai.disable_learning()
            print("🧠 AI Disabled - Manual control only")
    
    def get_system_performance(self):
        """Get comprehensive system performance metrics"""
        bhcs_metrics = {
            'system_health': self.bhcs.get_system_health(),
            'average_activity': self.bhcs.get_average_activity(),
            'zone_states': [zone.state for zone in self.bhcs.zones]
        }
        
        ai_metrics = self.ai_interface.get_ai_dashboard_data()['ai_status']
        
        return {
            'bhcs': bhcs_metrics,
            'ai': ai_metrics,
            'integrated_performance': {
                'overall_score': (bhcs_metrics['system_health'] + ai_metrics['learning_progress']) / 2,
                'ai_effectiveness': ai_metrics['successful_interventions'] / max(1, ai_metrics['interventions_recommended']),
                'system_stability': 1.0 - abs(bhcs_metrics['average_activity'] - 0.5)
            }
        }

async def main():
    """Main execution for integrated system"""
    print("🌙 Integrated BHCS + LunaBeyond AI System")
    print("🧠 Intelligent Homeostatic Regulation with AI Backend")
    print("🌿 Advanced BioCore Integration with Machine Learning")
    print("📊 Real-time System Optimization and Learning")
    print("=" * 70)
    
    # Initialize and run integrated system
    integrated_system = IntegratedBHCSwithAI()
    
    try:
        await integrated_system.run_integrated_system()
    except KeyboardInterrupt:
        print("\n🛑 System shutdown initiated by user")
        integrated_system.running = False
        integrated_system.ai_interface.stop_ai_monitoring()
        print("✅ Integrated system shutdown complete")

if __name__ == "__main__":
    asyncio.run(main())
