#!/usr/bin/env python3
"""
LunaBeyond AI Interface - Integration with BHCS System
Connects AI intelligence with the homeostatic regulation system
"""

import asyncio
import json
import time
from typing import Dict, List, Optional
from dataclasses import asdict
import requests
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

from ai_core import LunaBeyondAI, SystemInsight, ZonePattern

class LunaBeyondInterface:
    """Interface between LunaBeyond AI and BHCS system"""
    
    def __init__(self, bhcs_api_url: str = "http://localhost:3030"):
        self.ai = LunaBeyondAI()
        self.bhcs_api_url = bhcs_api_url
        self.running = False
        self.last_analysis = None
        self.ai_recommendations = []
        
    async def start_ai_monitoring(self):
        """Start AI monitoring and analysis"""
        print("🧠 LunaBeyond AI Starting...")
        print("🔗 Connecting to BHCS System...")
        print("📊 Beginning intelligent analysis...")
        
        self.running = True
        
        while self.running:
            try:
                # Get current system state
                system_state = await self.get_bhcs_state()
                
                if system_state:
                    # Analyze with AI
                    insights = self.ai.analyze_system_state(system_state['zones'])
                    
                    # Record state for learning
                    system_health = self.calculate_system_health(system_state['zones'])
                    self.ai.record_system_state(system_state['zones'], system_health)
                    
                    # Process recommendations
                    await self.process_ai_recommendations(insights)
                    
                    # Display AI insights
                    self.display_ai_insights(insights)
                    
                    self.last_analysis = insights
                
                await asyncio.sleep(2)  # Analyze every 2 seconds
                
            except Exception as e:
                print(f"❌ AI Analysis Error: {e}")
                await asyncio.sleep(5)
    
    async def get_bhcs_state(self) -> Optional[Dict]:
        """Get current BHCS system state"""
        try:
            response = requests.get(f"{self.bhcs_api_url}/state", timeout=3)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"⚠️ BHCS API Connection Issue: {e}")
        return None
    
    def calculate_system_health(self, zones: List[Dict]) -> float:
        """Calculate system health percentage"""
        if not zones:
            return 0.0
        
        calm_zones = sum(1 for zone in zones if zone['state'] == 'CALM')
        return calm_zones / len(zones)
    
    async def process_ai_recommendations(self, insights: SystemInsight):
        """Process and optionally execute AI recommendations"""
        recommendations = insights.recommended_actions
        
        for recommendation in recommendations:
            print(f"\n🧠 AI Recommendation: {recommendation.get('type', 'unknown')}")
            print(f"   Priority: {recommendation.get('priority', 'low')}")
            print(f"   Reason: {recommendation.get('reason', 'N/A')}")
            
            # Execute high-priority recommendations automatically
            if recommendation.get('priority') == 'high' and recommendation.get('urgency') == 'immediate':
                await self.execute_recommendation(recommendation)
            
            # Store for user review
            self.ai_recommendations.append(recommendation)
    
    async def execute_recommendation(self, recommendation: Dict):
        """Execute AI recommendation on BHCS system"""
        try:
            if recommendation['type'] == 'zone_intervention':
                # Apply BioCore intervention
                await self.apply_biocore_intervention(
                    recommendation['zone_id'],
                    recommendation['plant'],
                    recommendation['drug'],
                    recommendation['synergy']
                )
            elif recommendation['type'] == 'system_optimization':
                # Apply system optimization
                await self.apply_system_optimization()
            
            print(f"✅ Executed AI recommendation: {recommendation['type']}")
            
        except Exception as e:
            print(f"❌ Failed to execute recommendation: {e}")
    
    async def apply_biocore_intervention(self, zone_id: int, plant: str, drug: str, synergy: float):
        """Apply BioCore intervention based on AI recommendation"""
        try:
            # Get current zone state
            system_state = await self.get_bhcs_state()
            if not system_state or zone_id >= len(system_state['zones']):
                return
            
            before_state = system_state['zones'][zone_id]
            
            # Apply influence to zone
            influence_data = {
                "zone_id": zone_id,
                "influence": -0.3  # Calming influence
            }
            
            response = requests.post(
                f"{self.bhcs_api_url}/influence",
                json=influence_data,
                timeout=3
            )
            
            if response.status_code == 200:
                # Wait a moment for effect
                await asyncio.sleep(1)
                
                # Get after state
                after_state_response = await self.get_bhcs_state()
                if after_state_response:
                    after_state = after_state_response['zones'][zone_id]
                    
                    # Record intervention for AI learning
                    self.ai.record_intervention(
                        zone_id, plant, drug, synergy,
                        before_state, after_state
                    )
                    
                    print(f"🌿 Applied BioCore: {plant} + {drug} to Zone {zone_id}")
                    print(f"   Before: {before_state['activity']:.3f} ({before_state['state']})")
                    print(f"   After: {after_state['activity']:.3f} ({after_state['state']})")
        
        except Exception as e:
            print(f"❌ BioCore intervention failed: {e}")
    
    async def apply_system_optimization(self):
        """Apply system-wide optimization"""
        try:
            # This would call the BHCS system optimization endpoint
            print("🧠 Applying AI-driven system optimization...")
            
            # For now, apply calming influence to all stressed zones
            system_state = await self.get_bhcs_state()
            if not system_state:
                return
            
            for i, zone in enumerate(system_state['zones']):
                if zone['activity'] > 0.6:
                    influence_data = {
                        "zone_id": i,
                        "influence": -0.2
                    }
                    
                    requests.post(
                        f"{self.bhcs_api_url}/influence",
                        json=influence_data,
                        timeout=3
                    )
            
            print("✅ System optimization applied")
            
        except Exception as e:
            print(f"❌ System optimization failed: {e}")
    
    def display_ai_insights(self, insights: SystemInsight):
        """Display AI insights in a user-friendly format"""
        print(f"\n🧠 LunaBeyond AI Insights - {time.strftime('%H:%M:%S')}")
        print("=" * 60)
        
        # System health prediction
        health_pct = insights.system_health_prediction * 100
        print(f"📊 Predicted System Health: {health_pct:.1f}%")
        
        # Risk zones
        if insights.risk_zones:
            print(f"⚠️  Risk Zones: {', '.join(map(str, insights.risk_zones))}")
        else:
            print("✅ No immediate risk zones detected")
        
        # Top recommendations
        if insights.recommended_actions:
            print(f"\n🎯 Top {len(insights.recommended_actions)} Recommendations:")
            for i, rec in enumerate(insights.recommended_actions[:3], 1):
                priority_emoji = "🔴" if rec.get('priority') == 'high' else "🟡"
                print(f"   {i}. {priority_emoji} {rec.get('type', 'Unknown')}")
                print(f"      {rec.get('reason', 'No reason provided')}")
        
        # Optimization opportunities
        if insights.optimization_opportunities:
            print(f"\n💡 Optimization Opportunities:")
            for opp in insights.optimization_opportunities[:3]:
                print(f"   • {opp}")
        
        # Learning progress
        learning_pct = insights.learning_progress * 100
        print(f"\n📚 AI Learning Progress: {learning_pct:.1f}%")
        
        print("=" * 60)
    
    def get_ai_dashboard_data(self) -> Dict:
        """Get data for AI dashboard display"""
        ai_status = self.ai.get_ai_status()
        
        return {
            'ai_status': ai_status,
            'last_analysis': asdict(self.last_analysis) if self.last_analysis else None,
            'recommendations_count': len(self.ai_recommendations),
            'recent_recommendations': self.ai_recommendations[-5:],
            'zone_patterns': {i: asdict(pattern) for i, pattern in self.ai.zone_patterns.items()},
            'learning_enabled': self.ai.learning_enabled
        }
    
    async def start_ai_dashboard(self):
        """Start AI dashboard for monitoring"""
        print("🌐 Starting LunaBeyond AI Dashboard...")
        
        # This would start a web dashboard for AI monitoring
        # For now, we'll print periodic status updates
        
        dashboard_task = asyncio.create_task(self.ai_dashboard_loop())
        return dashboard_task
    
    async def ai_dashboard_loop(self):
        """AI dashboard update loop"""
        while self.running:
            try:
                dashboard_data = self.get_ai_dashboard_data()
                
                print(f"\n🌐 AI Dashboard Status:")
                print(f"   Learning: {'✅ Enabled' if dashboard_data['learning_enabled'] else '❌ Disabled'}")
                print(f"   Accuracy: {dashboard_data['ai_status']['prediction_accuracy']:.1%}")
                print(f"   Interventions: {dashboard_data['ai_status']['successful_interventions']}/{dashboard_data['ai_status']['interventions_recommended']}")
                print(f"   Data Points: {dashboard_data['ai_status']['data_points_collected']}")
                
                await asyncio.sleep(10)  # Update dashboard every 10 seconds
                
            except Exception as e:
                print(f"❌ Dashboard Error: {e}")
                await asyncio.sleep(5)
    
    def stop_ai_monitoring(self):
        """Stop AI monitoring"""
        print("🛑 Stopping LunaBeyond AI...")
        self.running = False
    
    def get_zone_analysis(self, zone_id: int) -> Dict:
        """Get detailed analysis for a specific zone"""
        if zone_id >= len(self.ai.zone_patterns):
            return {}
        
        pattern = self.ai.zone_patterns[zone_id]
        
        return {
            'zone_id': zone_id,
            'stress_tendency': pattern.stress_tendency,
            'recovery_rate': pattern.recovery_rate,
            'optimal_plant': pattern.optimal_plant,
            'optimal_drug': pattern.optimal_drug,
            'optimal_synergy': pattern.optimal_synergy,
            'effectiveness_score': pattern.effectiveness_score,
            'intervention_frequency': pattern.intervention_frequency,
            'recommendations': self.get_zone_recommendations(zone_id)
        }
    
    def get_zone_recommendations(self, zone_id: int) -> List[str]:
        """Get specific recommendations for a zone"""
        pattern = self.ai.zone_patterns[zone_id]
        recommendations = []
        
        if pattern.stress_tendency > 0.7:
            recommendations.append("High stress tendency - monitor closely")
        
        if pattern.recovery_rate < 0.3:
            recommendations.append("Slow recovery - consider stronger interventions")
        
        if pattern.effectiveness_score < 0.5:
            recommendations.append("Low intervention effectiveness - try different combinations")
        
        if pattern.intervention_frequency > 10:
            recommendations.append("Frequent interventions - consider system optimization")
        
        return recommendations

# Main execution
async def main():
    """Main LunaBeyond AI execution"""
    print("🌙 LunaBeyond AI - Intelligent BHCS Backend")
    print("🧠 Advanced AI for Homeostatic System Optimization")
    print("=" * 60)
    
    # Initialize AI interface
    ai_interface = LunaBeyondInterface()
    
    try:
        # Start AI monitoring
        monitoring_task = asyncio.create_task(ai_interface.start_ai_monitoring())
        
        # Start AI dashboard
        dashboard_task = await ai_interface.start_ai_dashboard()
        
        print("\n🚀 LunaBeyond AI is now active!")
        print("📊 Monitoring BHCS system and providing intelligent recommendations")
        print("🧠 Learning from system behavior and improving predictions")
        print("🌐 AI Dashboard running with real-time updates")
        print("\nPress Ctrl+C to stop AI monitoring")
        
        # Keep running
        await asyncio.gather(monitoring_task, dashboard_task)
        
    except KeyboardInterrupt:
        print("\n🛑 Shutting down LunaBeyond AI...")
        ai_interface.stop_ai_monitoring()
        print("✅ AI monitoring stopped")

if __name__ == "__main__":
    asyncio.run(main())
