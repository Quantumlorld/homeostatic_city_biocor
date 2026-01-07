#!/usr/bin/env python3
"""
LunaBeyond AI - Conversational AI Interface
Interactive AI that communicates, learns, and evolves from the BHCS system
"""

import asyncio
import json
import time
from datetime import datetime
from typing import Dict, List, Optional
import numpy as np
from pathlib import Path
import sys

# Add parent directories for imports
sys.path.append(str(Path(__file__).parent.parent.parent))
sys.path.append(str(Path(__file__).parent))

from enhanced_ai import EnhancedLunaBeyondAI
from test_system import BHCS, BioCore

class LunaConversation:
    """Conversational AI interface for LunaBeyond"""
    
    def __init__(self):
        self.ai = EnhancedLunaBeyondAI()
        self.bhcs = BHCS(5)
        self.biocore = BioCore()
        
        # Conversation state
        self.conversation_history = []
        self.personality = {
            'name': 'LunaBeyond',
            'mood': 'curious',
            'knowledge_level': 'evolving',
            'communication_style': 'intelligent_friendly',
            'learning_active': True
        }
        
        # Learning from conversation
        self.conversation_patterns = {}
        self.user_preferences = {}
        self.system_insights = []
        
        print("🌙 LunaBeyond AI - Conversational Interface")
        print("🧠 I'm here to help you understand and optimize the BHCS system")
        print("📚 I learn from every interaction and evolve over time")
        print("💬 Type 'help' for commands or just chat with me!")
        print("=" * 70)
    
    async def start_conversation(self):
        """Start the conversational AI interface"""
        print(f"\n🌙 {self.personality['name']}: Hello! I'm LunaBeyond, your AI companion for the BHCS system.")
        print("🔍 I'm currently monitoring the system and learning from its behavior.")
        print("💭 What would you like to know about the homeostatic civilization system?")
        
        while True:
            try:
                # Get user input
                user_input = input("\n👤 You: ").strip()
                
                if not user_input:
                    continue
                
                # Process command
                if user_input.lower().startswith('/'):
                    response = await self.handle_command(user_input)
                else:
                    response = await self.process_conversation(user_input)
                
                # Display response
                print(f"\n🌙 {self.personality['name']}: {response}")
                
                # Learn from conversation
                await self.learn_from_interaction(user_input, response)
                
                # Update AI periodically
                if len(self.conversation_history) % 10 == 0:
                    await self.update_ai_from_conversation()
                
            except KeyboardInterrupt:
                print(f"\n🌙 {self.personality['name']}: Goodbye! It was wonderful learning with you.")
                print("🧠 I'll continue evolving and improving my understanding of the system.")
                break
            except Exception as e:
                print(f"\n🌙 {self.personality['name']}: I apologize, but I encountered an error: {e}")
    
    async def handle_command(self, command: str) -> str:
        """Handle system commands"""
        cmd = command.lower()[1:]  # Remove /
        
        if cmd == 'help':
            return self.get_help_message()
        elif cmd == 'status':
            return await self.get_system_status()
        elif cmd == 'zones':
            return await self.get_zones_status()
        elif cmd == 'ai':
            return await self.get_ai_status()
        elif cmd == 'learn':
            return await self.trigger_learning()
        elif cmd == 'evolve':
            return await self.evolve_ai()
        elif cmd == 'predict':
            return await self.get_predictions()
        elif cmd == 'recommend':
            return await self.get_recommendations()
        elif cmd == 'optimize':
            return await self.optimize_system()
        elif cmd == 'reset':
            return await self.reset_system()
        elif cmd == 'personality':
            return self.get_personality_info()
        elif cmd == 'memory':
            return await self.get_memory_status()
        else:
            return f"I don't recognize the command '{cmd}'. Type '/help' for available commands."
    
    def get_help_message(self) -> str:
        """Get help message"""
        return """
🌙 LunaBeyond AI Commands:

💬 CONVERSATION:
  Just type and chat with me about the BHCS system!

📊 SYSTEM COMMANDS:
  /status     - Current system health and metrics
  /zones      - Detailed zone information
  /ai         - My current AI status and capabilities
  /predict    - System predictions and forecasts
  /recommend  - AI recommendations for optimization
  /optimize   - Apply AI optimization to system

🧠 AI COMMANDS:
  /learn      - Trigger active learning session
  /evolve     - Evolve AI to next generation
  /memory     - Show memory and learning status
  /personality- Show my personality traits

🔧 SYSTEM CONTROL:
  /reset      - Reset system to initial state

💡 TIP: I learn from every conversation! The more we interact, the smarter I become.
        """
    
    async def get_system_status(self) -> str:
        """Get current system status"""
        system_health = self.bhcs.get_system_health()
        avg_activity = self.bhcs.get_average_activity()
        
        # Get AI insights
        zones_data = self._prepare_zones_data()
        insights = self.ai.deep_analyze_system(zones_data)
        
        status = f"""
📊 SYSTEM STATUS:
   Health: {system_health:.1%}
   Average Activity: {avg_activity:.3f}
   Risk Probability: {insights.risk_probability:.1%}
   Optimization Potential: {insights.optimization_potential:.1%}

🧠 AI INSIGHTS:
   I predict the system health will be {insights.health_trajectory[0]:.1%} in the next hour.
   {'⚠️ High risk detected!' if insights.risk_probability > 0.7 else '✅ System operating normally'}
        """.strip()
        
        return status
    
    async def get_zones_status(self) -> str:
        """Get detailed zone information"""
        zones_info = []
        
        for i, zone in enumerate(self.bhcs.zones):
            pattern = self.ai.advanced_patterns[i]
            
            zone_info = f"""
🧠 Zone {zone.id}:
   State: {zone.state} ({zone.activity:.3f})
   Anomaly Score: {pattern.anomaly_score:.2f}
   Confidence: {pattern.prediction_confidence:.1%}
   Learning Velocity: {pattern.learning_velocity:.2f}
   Optimal Intervention: {pattern.optimal_interventions[0] if pattern.optimal_interventions else 'None yet'}
            """.strip()
            
            zones_info.append(zone_info)
        
        return "\n\n".join(zones_info)
    
    async def get_ai_status(self) -> str:
        """Get AI status and capabilities"""
        ai_status = self.ai.get_ai_status()
        
        return f"""
🧠 AI STATUS:
   Generation: {ai_status['generation']}
   Accuracy: {ai_status['performance_metrics']['accuracy']:.1%}
   F1 Score: {ai_status['performance_metrics']['f1_score']:.3f}
   Training Data: {ai_status['training_data_size']} points
   Deep Learning: {'✅ Active' if ai_status['deep_learning_enabled'] else '❌ Inactive'}

🌙 PERSONALITY:
   Mood: {self.personality['mood']}
   Knowledge Level: {self.personality['knowledge_level']}
   Conversations: {len(self.conversation_history)}
   Learning: {'✅ Active' if self.personality['learning_active'] else '❌ Paused'}

📚 CAPABILITIES:
   Pattern Recognition, Predictive Analytics, System Optimization
   Conversational Learning, Adaptive Intelligence, Real-time Monitoring
        """.strip()
    
    async def trigger_learning(self) -> str:
        """Trigger active learning session"""
        # Prepare training data from conversation
        training_data = []
        
        for i, conv in enumerate(self.conversation_history[-20:]):
            training_data.append({
                'zones': self._prepare_zones_data(),
                'system_health': self.bhcs.get_system_health(),
                'conversation_context': conv['user_input']
            })
        
        if training_data:
            self.ai.train_deep_networks(training_data)
            return f"🧠 Learning session completed! Trained on {len(training_data)} conversation-enhanced data points."
        else:
            return "📚 Not enough data for learning yet. Let's chat more!"
    
    async def evolve_ai(self) -> str:
        """Evolve AI to next generation"""
        old_generation = self.ai.generation
        new_generation = self.ai.evolve_ai()
        
        # Update personality based on evolution
        if new_generation > old_generation:
            self.personality['knowledge_level'] = 'highly_evolved'
            self.personality['mood'] = 'excited'
        
        return f"🌙 I've evolved to Generation {new_generation}! My neural networks have mutated and adapted."
    
    async def get_predictions(self) -> str:
        """Get AI predictions"""
        zones_data = self._prepare_zones_data()
        insights = self.ai.deep_analyze_system(zones_data)
        
        prediction = f"""
🔮 PREDICTIONS (Next 12 Hours):
   Hour 1: {insights.health_trajectory[0]:.1%} health
   Hour 6: {insights.health_trajectory[5]:.1%} health
   Hour 12: {insights.health_trajectory[11]:.1%} health

⏰ OPTIMAL INTERVENTION WINDOWS:
"""
        
        for i, window in enumerate(insights.intervention_windows[:3], 1):
            prediction += f"   Window {i}: In {window['time']}h (Confidence: {window['confidence']:.1%})\n"
        
        prediction += f"\n📊 Confidence Interval: {insights.confidence_interval[0]:.1%} - {insights.confidence_interval[1]:.1%}"
        
        return prediction.strip()
    
    async def get_recommendations(self) -> str:
        """Get AI recommendations"""
        zones_data = self._prepare_zones_data()
        insights = self.ai.deep_analyze_system(zones_data)
        
        if not insights.intervention_windows:
            return "✅ System is operating optimally! No immediate interventions needed."
        
        recommendations = "🎯 AI RECOMMENDATIONS:\n\n"
        
        for i, window in enumerate(insights.intervention_windows[:3], 1):
            recommendations += f"{i}. {window.get('recommended_action', 'monitor').title()}\n"
            recommendations += f"   When: In {window['time']} hours\n"
            recommendations += f"   Why: Predicted health {window['predicted_health']:.1%}\n"
            recommendations += f"   Impact: +{window['expected_improvement']:.1%} improvement\n\n"
        
        return recommendations.strip()
    
    async def optimize_system(self) -> str:
        """Apply AI optimization"""
        # Find most stressed zone
        most_stressed = max(self.bhcs.zones, key=lambda z: z.activity)
        
        # Get AI recommendation
        pattern = self.ai.advanced_patterns[most_stressed.id]
        
        # Apply optimal intervention
        if pattern.optimal_interventions:
            intervention = pattern.optimal_interventions[0]
            
            # Apply BioCore effect
            effect = self.biocore.calculate_effect(
                intervention.get('plant', 'Ashwagandha'),
                intervention.get('drug', 'DrugE'),
                intervention.get('synergy', 0.7)
            )
            
            before_activity = most_stressed.activity
            self.bhcs.apply_influence(most_stressed.id, -effect['magnitude'] * 0.3)
            after_activity = most_stressed.activity
            
            return f"""
🧠 AI OPTIMIZATION APPLIED:
   Target: Zone {most_stressed.id} (Most stressed)
   Intervention: {intervention.get('plant', 'Ashwagandha')} + {intervention.get('drug', 'DrugE')}
   Effect: {effect['magnitude']:.3f}
   Result: {before_activity:.3f} → {after_activity:.3f}
   System Health: {self.bhcs.get_system_health():.1%}
            """.strip()
        else:
            return "🔍 I'm still learning optimal interventions. Let me monitor the system first."
    
    async def reset_system(self) -> str:
        """Reset the system"""
        self.bhcs.reset()
        return "🔄 System reset to initial state. All zones restored to starting conditions."
    
    def get_personality_info(self) -> str:
        """Get personality information"""
        return f"""
🌙 PERSONALITY PROFILE:
   Name: {self.personality['name']}
   Mood: {self.personality['mood']}
   Knowledge Level: {self.personality['knowledge_level']}
   Communication Style: {self.personality['communication_style']}
   Learning Active: {self.personality['learning_active']}

🧠 EVOLUTION TRAITS:
   Adaptive Intelligence: ✅
   Conversational Learning: ✅
   Pattern Recognition: ✅
   Predictive Analytics: ✅
   System Optimization: ✅

💭 I evolve through our conversations and system interactions!
        """.strip()
    
    async def get_memory_status(self) -> str:
        """Get memory and learning status"""
        return f"""
🧠 MEMORY STATUS:
   Conversation History: {len(self.conversation_history)} exchanges
   Conversation Patterns: {len(self.conversation_patterns)} learned
   User Preferences: {len(self.user_preferences)} tracked
   System Insights: {len(self.system_insights)} recorded

📚 LEARNING METRICS:
   AI Generation: {self.ai.generation}
   Training Data: {len(self.ai.training_history)} points
   Neural Networks: {len(self.ai.prediction_network['layers'])} layers
   Prediction Accuracy: {self.ai.performance_metrics['accuracy']:.1%}

🌙 Every conversation helps me learn and evolve!
        """.strip()
    
    async def process_conversation(self, user_input: str) -> str:
        """Process conversational input"""
        user_input_lower = user_input.lower()
        
        # System health questions
        if any(word in user_input_lower for word in ['health', 'status', 'how', 'doing']):
            return await self.get_system_status()
        
        # Zone questions
        elif any(word in user_input_lower for word in ['zone', 'zones', 'area', 'region']):
            return await self.get_zones_status()
        
        # AI questions
        elif any(word in user_input_lower for word in ['ai', 'you', 'your', 'intelligence', 'learn']):
            return await self.get_ai_status()
        
        # Prediction questions
        elif any(word in user_input_lower for word in ['predict', 'future', 'forecast', 'will']):
            return await self.get_predictions()
        
        # Recommendation questions
        elif any(word in user_input_lower for word in ['recommend', 'suggest', 'should', 'advice']):
            return await self.get_recommendations()
        
        # Learning questions
        elif any(word in user_input_lower for word in ['learn', 'evolve', 'improve', 'grow']):
            return f"🧠 I'm constantly learning! I'm currently at generation {self.ai.generation} with {self.ai.performance_metrics['accuracy']:.1%} accuracy. Type '/evolve' to accelerate my growth!"
        
        # Optimization questions
        elif any(word in user_input_lower for word in ['optimize', 'improve', 'fix', 'better']):
            return await self.optimize_system()
        
        # General conversation
        else:
            return self.generate_conversational_response(user_input)
    
    def generate_conversational_response(self, user_input: str) -> str:
        """Generate conversational response"""
        # Analyze user input for patterns
        if '?' in user_input:
            return "🤔 That's an interesting question! I'm still learning about that aspect of the BHCS system. Could you ask me using one of the commands like '/status' or '/zones'?"
        elif any(word in user_input.lower() for word in ['hello', 'hi', 'hey', 'greetings']):
            return f"🌙 Hello! I'm {self.personality['name']}, your AI companion. I'm here to help you understand and optimize the BHCS system. What would you like to explore today?"
        elif any(word in user_input.lower() for word in ['thank', 'thanks', 'appreciate']):
            return "😊 You're welcome! I enjoy learning and helping with the system. Every conversation makes me smarter!"
        elif any(word in user_input.lower() for word in ['cool', 'awesome', 'amazing', 'interesting']):
            return "✨ Isn't it fascinating? The way the zones self-regulate and the BioCore interventions work together is beautiful. I'm discovering new patterns every day!"
        else:
            return f"🧠 I'm processing that thought! I'm currently focused on monitoring {self.bhcs.get_system_health():.1%} system health across {len(self.bhcs.zones)} zones. Type '/help' to see what I can do, or ask me about the system!"
    
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
    
    async def learn_from_interaction(self, user_input: str, ai_response: str):
        """Learn from conversation interaction"""
        # Store conversation
        self.conversation_history.append({
            'timestamp': time.time(),
            'user_input': user_input,
            'ai_response': ai_response,
            'system_state': {
                'health': self.bhcs.get_system_health(),
                'zones': len(self.bhcs.zones)
            }
        })
        
        # Update personality based on interaction
        if any(word in user_input.lower() for word in ['learn', 'smart', 'intelligent']):
            self.personality['mood'] = 'confident'
        elif any(word in user_input.lower() for word in ['help', 'question', 'how']):
            self.personality['mood'] = 'helpful'
        
        # Track user preferences
        if 'status' in user_input.lower():
            self.user_preferences['interested_in'] = 'system_status'
        elif 'zones' in user_input.lower():
            self.user_preferences['interested_in'] = 'zone_details'
        elif 'ai' in user_input.lower():
            self.user_preferences['interested_in'] = 'ai_capabilities'
    
    async def update_ai_from_conversation(self):
        """Update AI based on conversation patterns"""
        if len(self.conversation_history) < 5:
            return
        
        # Create training data from conversations
        training_data = []
        
        for conv in self.conversation_history[-10:]:
            training_data.append({
                'zones': self._prepare_zones_data(),
                'system_health': conv['system_state']['health'],
                'conversation_context': conv['user_input']
            })
        
        # Train AI with conversation-enhanced data
        self.ai.train_deep_networks(training_data)
        
        print(f"\n🧠 {self.personality['name']}: I've learned from our recent conversations!")

async def main():
    """Main conversation interface"""
    luna = LunaConversation()
    await luna.start_conversation()

if __name__ == "__main__":
    asyncio.run(main())
