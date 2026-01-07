#!/usr/bin/env python3
"""
LunaBeyond AI Dashboard - Real-time AI Monitoring Interface
Web dashboard for visualizing AI insights and system performance
"""

import asyncio
import json
import time
from datetime import datetime
from typing import Dict, List
import numpy as np
from pathlib import Path
import sys

# Add parent directories for imports
sys.path.append(str(Path(__file__).parent.parent.parent))
sys.path.append(str(Path(__file__).parent))

from enhanced_ai import EnhancedLunaBeyondAI
from test_system import BHCS, BioCore

class AIDashboard:
    """Real-time AI dashboard for monitoring LunaBeyond AI"""
    
    def __init__(self):
        self.ai = EnhancedLunaBeyondAI()
        self.bhcs = BHCS(5)
        self.biocore = BioCore()
        self.running = True
        self.update_counter = 0
        
        # Dashboard data
        self.dashboard_data = {
            'ai_status': {},
            'system_metrics': {},
            'predictions': [],
            'recommendations': [],
            'performance_history': [],
            'alerts': []
        }
    
    async def start_dashboard(self):
        """Start the AI dashboard"""
        print("🌐 LunaBeyond AI Dashboard Starting...")
        print("📊 Real-time AI Monitoring and Analytics")
        print("🧠 Deep Learning Insights and Predictions")
        print("=" * 60)
        
        try:
            while self.running:
                # Update system
                self.bhcs.update()
                self.update_counter += 1
                
                # AI Analysis
                zones_data = self._prepare_zones_data()
                insights = self.ai.deep_analyze_system(zones_data)
                
                # Update dashboard data
                await self.update_dashboard_data(insights, zones_data)
                
                # Display dashboard
                if self.update_counter % 3 == 0:
                    self.display_dashboard()
                
                # Train AI periodically
                if self.update_counter % 20 == 0:
                    await self.train_ai()
                
                # Evolve AI periodically
                if self.update_counter % 100 == 0:
                    self.ai.evolve_ai()
                
                # Random fluctuations
                if self.update_counter % 7 == 0:
                    import random
                    zone_id = random.randint(0, 4)
                    influence = (random.random() - 0.5) * 0.2
                    self.bhcs.apply_influence(zone_id, influence)
                
                await asyncio.sleep(1)
                
        except KeyboardInterrupt:
            print("\n🛑 Dashboard shutdown")
            self.running = False
    
    def _prepare_zones_data(self) -> List[Dict]:
        """Prepare zones data for AI analysis"""
        zones_data = []
        for zone in self.bhcs.zones:
            zones_data.append({
                'id': zone.id,
                'activity': zone.activity,
                'state': zone.state
            })
        return zones_data
    
    async def update_dashboard_data(self, insights, zones_data):
        """Update dashboard data with latest insights"""
        # AI Status
        self.dashboard_data['ai_status'] = self.ai.get_ai_status()
        
        # System Metrics
        self.dashboard_data['system_metrics'] = {
            'system_health': self.bhcs.get_system_health(),
            'average_activity': self.bhcs.get_average_activity(),
            'zone_states': [zone.state for zone in self.bhcs.zones],
            'timestamp': time.time()
        }
        
        # Predictions
        self.dashboard_data['predictions'] = insights.health_trajectory[:12]  # Next 12 hours
        
        # Recommendations
        self.dashboard_data['recommendations'] = insights.intervention_windows
        
        # Performance History
        self.dashboard_data['performance_history'].append({
            'timestamp': time.time(),
            'system_health': self.bhcs.get_system_health(),
            'ai_accuracy': self.ai.performance_metrics['accuracy'],
            'risk_probability': insights.risk_probability
        })
        
        # Keep history limited
        if len(self.dashboard_data['performance_history']) > 50:
            self.dashboard_data['performance_history'] = self.dashboard_data['performance_history'][-50:]
        
        # Alerts
        await self.generate_alerts(insights)
    
    async def generate_alerts(self, insights):
        """Generate alerts based on insights"""
        alerts = []
        
        # Risk alerts
        if insights.risk_probability > 0.7:
            alerts.append({
                'type': 'HIGH_RISK',
                'message': f'High system risk: {insights.risk_probability:.1%}',
                'urgency': 'critical',
                'timestamp': time.time()
            })
        
        # Health alerts
        current_health = self.bhcs.get_system_health()
        if current_health < 0.3:
            alerts.append({
                'type': 'LOW_HEALTH',
                'message': f'System health critical: {current_health:.1%}',
                'urgency': 'high',
                'timestamp': time.time()
            })
        
        # AI performance alerts
        if self.ai.performance_metrics['accuracy'] < 0.6:
            alerts.append({
                'type': 'AI_PERFORMANCE',
                'message': f'AI accuracy low: {self.ai.performance_metrics["accuracy"]:.1%}',
                'urgency': 'medium',
                'timestamp': time.time()
            })
        
        # Optimization opportunities
        if insights.optimization_potential > 0.8:
            alerts.append({
                'type': 'OPTIMIZATION',
                'message': f'High optimization potential: {insights.optimization_potential:.1%}',
                'urgency': 'info',
                'timestamp': time.time()
            })
        
        self.dashboard_data['alerts'] = alerts[-5:]  # Keep last 5 alerts
    
    def display_dashboard(self):
        """Display the AI dashboard"""
        print(f"\n🧠 LunaBeyond AI Dashboard - {datetime.now().strftime('%H:%M:%S')}")
        print("=" * 80)
        
        # AI Status Panel
        ai_status = self.dashboard_data['ai_status']
        print(f"🤖 AI Status:")
        print(f"   Generation: {ai_status.get('generation', 1)}")
        print(f"   Accuracy: {ai_status.get('performance_metrics', {}).get('accuracy', 0):.1%}")
        print(f"   F1 Score: {ai_status.get('performance_metrics', {}).get('f1_score', 0):.3f}")
        print(f"   Training Data: {ai_status.get('training_data_size', 0)} points")
        print(f"   Deep Learning: {'✅ Active' if ai_status.get('deep_learning_enabled') else '❌ Inactive'}")
        
        # System Metrics Panel
        metrics = self.dashboard_data['system_metrics']
        print(f"\n📊 System Metrics:")
        print(f"   Health: {metrics['system_health']:.1%}")
        print(f"   Avg Activity: {metrics['average_activity']:.3f}")
        print(f"   Zone States: {metrics['zone_states'].count('CALM')} calm, {metrics['zone_states'].count('OVERSTIMULATED')} stimulated")
        
        # Predictions Panel
        predictions = self.dashboard_data['predictions']
        if predictions:
            print(f"\n🔮 12-Hour Health Forecast:")
            for i, health in enumerate(predictions[:6]):  # Show next 6 hours
                hour = i + 1
                health_emoji = "🟢" if health > 0.7 else "🟡" if health > 0.4 else "🔴"
                print(f"   Hour {hour}: {health_emoji} {health:.1%}")
        
        # Recommendations Panel
        recommendations = self.dashboard_data['recommendations']
        if recommendations:
            print(f"\n🎯 AI Recommendations:")
            for i, rec in enumerate(recommendations[:3], 1):
                urgency_emoji = "🔴" if rec.get('confidence', 0) > 0.8 else "🟡" if rec.get('confidence', 0) > 0.5 else "🟢"
                print(f"   {i}. {urgency_emoji} In {rec.get('time', 0)}h - Health: {rec.get('predicted_health', 0):.1%}")
                print(f"      Expected improvement: {rec.get('expected_improvement', 0):.1%}")
        
        # Performance Trend Panel
        history = self.dashboard_data['performance_history']
        if len(history) > 5:
            print(f"\n📈 Performance Trend (Last 5 updates):")
            recent = history[-5:]
            for i, data in enumerate(recent, 1):
                health_trend = "↗️" if data['system_health'] > 0.5 else "↘️"
                ai_trend = "↗️" if data['ai_accuracy'] > 0.6 else "↘️"
                print(f"   {i}: Health {health_trend} {data['system_health']:.1%} | AI {ai_trend} {data['ai_accuracy']:.1%}")
        
        # Alerts Panel
        alerts = self.dashboard_data['alerts']
        if alerts:
            print(f"\n⚠️ Active Alerts:")
            for alert in alerts:
                urgency_emoji = "🔴" if alert['urgency'] == 'critical' else "🟡" if alert['urgency'] == 'high' else "🟢"
                print(f"   {urgency_emoji} {alert['type']}: {alert['message']}")
        
        # Zone Analysis Panel
        print(f"\n🧬 Zone Analysis:")
        for i, zone in enumerate(self.bhcs.zones):
            pattern = self.ai.advanced_patterns[i]
            state_emoji = {"CALM": "🟢", "OVERSTIMULATED": "🟡", "EMERGENT": "🔴", "CRITICAL": "🟣"}.get(zone.state, "⚪")
            anomaly_emoji = "⚠️" if pattern.anomaly_score > 0.5 else "✅"
            
            print(f"   Zone {i}: {state_emoji} {zone.activity:.3f} | {anomaly_emoji} Anomaly: {pattern.anomaly_score:.2f}")
            print(f"      Confidence: {pattern.prediction_confidence:.1%} | Learning: {pattern.learning_velocity:.2f}")
        
        print("=" * 80)
    
    async def train_ai(self):
        """Train AI with current data"""
        # Prepare training data
        training_data = []
        
        for data_point in self.dashboard_data['performance_history'][-10:]:
            training_data.append({
                'zones': self._prepare_zones_data(),
                'system_health': data_point['system_health']
            })
        
        if training_data:
            self.ai.train_deep_networks(training_data)
            print(f"🧠 AI Training Completed - {len(training_data)} data points")
    
    def export_dashboard_data(self) -> Dict:
        """Export dashboard data for external use"""
        return {
            'export_timestamp': time.time(),
            'ai_generation': self.ai.generation,
            'performance_metrics': self.ai.performance_metrics,
            'system_dynamics': self.ai.system_dynamics,
            'current_status': self.dashboard_data,
            'advanced_patterns': {i: {
                'prediction_confidence': p.prediction_confidence,
                'anomaly_score': p.anomaly_score,
                'learning_velocity': p.learning_velocity
            } for i, p in self.ai.advanced_patterns.items()}
        }

async def main():
    """Main dashboard execution"""
    print("🌙 LunaBeyond AI Dashboard")
    print("🧠 Advanced AI Monitoring Interface")
    print("📊 Real-time Deep Learning Analytics")
    print("🔮 Predictive System Insights")
    print("=" * 60)
    
    dashboard = AIDashboard()
    
    try:
        await dashboard.start_dashboard()
    except KeyboardInterrupt:
        print("\n🛑 Dashboard shutdown initiated")
        dashboard.running = False
        
        # Export final data
        final_data = dashboard.export_dashboard_data()
        print(f"📊 Final AI Performance: {final_data['performance_metrics']['accuracy']:.1%}")
        print(f"🧠 AI Generation: {final_data['ai_generation']}")
        print("✅ Dashboard shutdown complete")

if __name__ == "__main__":
    asyncio.run(main())
