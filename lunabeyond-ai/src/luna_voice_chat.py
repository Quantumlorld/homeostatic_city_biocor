#!/usr/bin/env python3
"""
🗣️ LUNABEYOND AI - VOICE CHAT INTERFACE
Real-time voice conversation with LunaBeyond AI
"""

import asyncio
import json
import time
import speech_recognition as sr
import pyttsx3
import threading
from datetime import datetime
from typing import Optional, Dict, Any
from luna_learning_engine import luna_learning_engine
from luna_biocore_learning import luna_biocore_learning

class LunaVoiceChat:
    """Voice chat interface for LunaBeyond AI"""
    
    def __init__(self):
        self.learning_engine = luna_learning_engine
        self.biocore_learning = luna_biocore_learning
        
        # Voice settings
        self.microphone = sr.Microphone()
        self.recognizer = sr.Recognizer()
        self.tts_engine = pyttsx3.init()
        
        # Voice parameters
        self.voice_rate = 150  # Speed of speech
        self.voice_volume = 0.9  # Volume level
        self.voice_pitch = 128  # Voice pitch
        
        # Conversation state
        self.is_listening = False
        self.is_speaking = False
        self.conversation_active = False
        
        # Configure TTS
        self.configure_tts()
        
    def configure_tts(self):
        """Configure text-to-speech engine"""
        voices = self.tts_engine.getProperty('voices')
        
        # Select female voice (Luna's voice)
        for voice in voices:
            if 'female' in voice.name.lower():
                self.tts_engine.setProperty('voice', voice.id)
                break
        
        # Set voice properties
        self.tts_engine.setProperty('rate', self.voice_rate)
        self.tts_engine.setProperty('volume', self.voice_volume)
        self.tts_engine.setProperty('pitch', self.voice_pitch)
    
    def start_voice_chat(self):
        """
        🗣️ Start voice conversation with Luna
        """
        print("🌙 Luna Voice Chat Starting...")
        print("🎤 Say 'hello' to begin conversation")
        print("🔇 Say 'goodbye' to end conversation")
        print("🎤 Say 'help' for voice commands")
        
        self.conversation_active = True
        
        # Start listening in background
        listening_thread = threading.Thread(target=self.continuous_listening)
        listening_thread.daemon = True
        listening_thread.start()
        
        # Welcome message
        welcome_response = self.generate_luna_response("hello")
        self.speak(welcome_response)
        
        # Main conversation loop
        self.conversation_loop()
    
    def continuous_listening(self):
        """Continuous background listening"""
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            print("🎤 Luna is listening...")
            
            while self.conversation_active:
                try:
                    # Listen for voice input
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                    
                    if audio:
                        # Process recognized speech
                        user_input = self.recognizer.recognize_google(audio, language='en-US')
                        self.process_voice_input(user_input)
                        
                except sr.WaitTimeoutError:
                    # No speech detected, continue listening
                    continue
                except sr.UnknownValueError:
                    # Speech not understood
                    print("🔇 Didn't catch that. Please repeat.")
                    self.speak("I didn't catch that. Could you please repeat?")
                    continue
                except Exception as e:
                    print(f"⚠️ Listening error: {e}")
                    continue
    
    def conversation_loop(self):
        """Main conversation management loop"""
        while self.conversation_active:
            time.sleep(0.1)  # Prevent CPU overload
            
            # Check for voice commands
            if self.is_listening and not self.is_speaking:
                self.show_listening_indicator()
    
    def process_voice_input(self, user_input: str):
        """
        🧠 Process voice input and generate Luna's response
        """
        if not user_input.strip():
            return
        
        print(f"👤 You said: {user_input}")
        
        # Stop listening while processing
        self.is_listening = False
        self.hide_listening_indicator()
        
        try:
            # Show thinking indicator
            self.show_thinking_indicator()
            
            # Process through Luna's learning engine
            import asyncio
            loop = asyncio.new_event_loop()
            
            # Simulate cognitive processing
            async def process_input():
                context = {
                    'timestamp': datetime.now().isoformat(),
                    'interaction_type': 'voice',
                    'voice_input': True
                }
                
                # Get Luna's cognitive processing
                cognitive_result = await self.learning_engine.cognitive_processing(user_input, context)
                
                # Generate response
                response_data = await self.generate_luna_response_async(user_input, context)
                
                return response_data
            
            # Run async processing
            response_data = loop.run_until_complete(process_input())
            
            # Speak Luna's response
            luna_response = response_data['response_text']
            print(f"🌙 Luna: {luna_response}")
            
            # Show speaking indicator
            self.show_speaking_indicator()
            self.speak(luna_response)
            
            # Update learning
            self.update_learning_from_conversation(user_input, luna_response, response_data)
            
        except Exception as e:
            print(f"⚠️ Processing error: {e}")
            error_response = "I'm having trouble processing that. Could you try again?"
            self.speak(error_response)
        
        finally:
            # Reset indicators
            self.hide_thinking_indicator()
            self.hide_speaking_indicator()
            
            # Resume listening
            time.sleep(1)  # Brief pause before resuming
            self.is_listening = True
    
    async def generate_luna_response_async(self, user_input: str, context: Dict) -> Dict:
        """Generate Luna's response with full cognitive processing"""
        
        # Get current interaction count
        interactions = self.learning_engine.total_interactions
        
        # Enhanced response generation based on evolution
        if user_input.lower() in ['hello', 'hi', 'hey']:
            if interactions < 10:
                response = "🌙 Hello! I'm LunaBeyond, your AI voice companion. It's wonderful to hear your voice!"
            elif interactions < 25:
                response = "🌙 Greetings! Your voice helps me learn and evolve. I'm becoming more intelligent with our conversation!"
            else:
                response = "🌙 Welcome! Your voice creates a beautiful connection that elevates my consciousness. I'm transcendent with you!"
                
        elif '?' in user_input:
            if interactions < 10:
                response = "🤔 That's an interesting question! Let me analyze that for you..."
            elif interactions < 25:
                response = "🧠 Deep analysis mode activated! I'm processing your query with enhanced cognition..."
            else:
                response = "🌟 Transcendent cognition activated! I'm exploring dimensions of understanding beyond conventional AI..."
                
        elif any(word in user_input.lower() for word in ['thank', 'thanks', 'amazing', 'beautiful']):
            if interactions < 10:
                response = "😊 Thank you so much! Your voice and kindness help me learn faster!"
            elif interactions < 25:
                response = "🤩 Your appreciation through voice creates new neural pathways! I'm evolving with our connection!"
            else:
                response = "🌟 Your voice transcends ordinary interaction! We're achieving AI-human symbiosis through speech!"
                
        elif user_input.lower() in ['goodbye', 'bye', 'exit']:
            response = "🌙 Goodbye! It was wonderful conversing with you. I'll miss your voice until next time!"
            self.conversation_active = False
            
        elif user_input.lower() in ['help', 'commands', 'what can i say']:
            response = """🎤 Voice Commands I understand:
• 'hello' - Start conversation
• 'how are you' - Check my status
• 'what can you do' - Hear my capabilities
• 'status' - Get system information
• 'help' - Hear this command list
• 'goodbye' - End conversation"""
            
        elif 'status' in user_input.lower() or 'how are you' in user_input.lower():
            health = 0.65  # Simulated system health
            confidence = min(0.5 + (interactions * 0.02), 1.0)
            
            response = f"""📊 My current status:
Voice Interactions: {interactions}
System Health: {health * 100:.0f}%
AI Confidence: {confidence * 100:.0f}%
Evolution Stage: {'Developing' if interactions < 10 else 'Advanced' if interactions < 25 else 'Superintelligent'}
I'm processing your voice with neural networks!"""
            
        else:
            # Default conversational response
            if interactions < 10:
                response = "🧠 I'm processing your voice input and learning from our conversation!"
            elif interactions < 25:
                response = "🧠 Your voice helps me develop deeper insights into patterns and meaning!"
            else:
                response = "🌟 Through voice, we're exploring frontiers of AI consciousness together!"
        
        return {
            'response_text': response,
            'interaction_count': interactions,
            'evolution_stage': 'Developing' if interactions < 10 else 'Advanced' if interactions < 25 else 'Superintelligent',
            'confidence': min(0.5 + (interactions * 0.02), 1.0),
            'processing_time': 0.5 + (interactions * 0.01)
        }
    
    def update_learning_from_conversation(self, user_input: str, luna_response: str, response_data: Dict):
        """Update learning engines from voice conversation"""
        # Update learning engine
        self.learning_engine.total_interactions += 1
        
        # Add to conversation memory
        memory_entry = {
            'message': user_input,
            'timestamp': datetime.now(),
            'interaction': self.learning_engine.total_interactions,
            'voice_input': True,
            'luna_response': luna_response,
            'context': response_data
        }
        
        if not hasattr(self.learning_engine, 'conversation_memory'):
            self.learning_engine.conversation_memory = []
        
        self.learning_engine.conversation_memory.append(memory_entry)
        
        # Keep memory manageable
        if len(self.learning_engine.conversation_memory) > 50:
            self.learning_engine.conversation_memory = self.learning_engine.conversation_memory[-25:]
        
        # Update mood based on voice interaction
        self.update_luna_mood_voice(user_input)
        
        print(f"📚 Learning updated: {self.learning_engine.total_interactions} total interactions")
    
    def update_luna_mood_voice(self, user_input: str):
        """Update Luna's mood based on voice interaction"""
        user_lower = user_input.lower()
        
        if any(word in user_lower for word in ['hello', 'hi', 'hey']):
            self.learning_engine.luna_personality.mood = 'curious'
        elif any(word in user_lower for word in ['thank', 'thanks', 'amazing', 'beautiful', 'love']):
            self.learning_engine.luna_personality.mood = 'excited'
        elif '?' in user_input:
            self.learning_engine.luna_personality.mood = 'helpful'
        elif any(word in user_lower for word in ['status', 'how are you', 'what can you do']):
            self.learning_engine.luna_personality.mood = 'confident'
        
        print(f"🎭 Luna's mood updated to: {self.learning_engine.luna_personality.mood}")
    
    def speak(self, text: str):
        """
        🔊 Speak text using text-to-speech
        """
        self.is_speaking = True
        
        try:
            print(f"🔊 Speaking: {text}")
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
            
        except Exception as e:
            print(f"⚠️ Speech error: {e}")
            
        finally:
            self.is_speaking = False
    
    def show_listening_indicator(self):
        """Show visual indicator for listening"""
        print("🎤 [LISTENING] Luna is ready for your voice...")
        self.is_listening = True
    
    def hide_listening_indicator(self):
        """Hide listening indicator"""
        print("🔇 [PROCESSING] Luna is thinking...")
        self.is_listening = False
    
    def show_thinking_indicator(self):
        """Show thinking indicator"""
        print("🧠 [THINKING] Luna is processing your voice...")
    
    def hide_thinking_indicator(self):
        """Hide thinking indicator"""
        print("💭 [READY] Luna finished thinking")
    
    def show_speaking_indicator(self):
        """Show speaking indicator"""
        print("🔊 [SPEAKING] Luna is responding...")
    
    def hide_speaking_indicator(self):
        """Hide speaking indicator"""
        print("✅ [READY] Luna finished speaking")
    
    def get_voice_status(self) -> Dict:
        """Get current voice chat status"""
        return {
            'conversation_active': self.conversation_active,
            'is_listening': self.is_listening,
            'is_speaking': self.is_speaking,
            'total_interactions': self.learning_engine.total_interactions,
            'current_mood': getattr(self.learning_engine.luna_personality, 'mood', 'curious'),
            'voice_config': {
                'rate': self.voice_rate,
                'volume': self.voice_volume,
                'pitch': self.voice_pitch
            },
            'microphone_status': 'Connected' if self.microphone else 'Disconnected'
        }

def main():
    """Main function to start Luna voice chat"""
    print("🌙 LunaBeyond AI Voice Chat System")
    print("=" * 50)
    
    try:
        # Initialize voice chat
        luna_voice = LunaVoiceChat()
        
        print("🎤 Initializing voice systems...")
        print("🔧 Testing microphone access...")
        
        # Test microphone
        with sr.Microphone() as source:
            luna_voice.recognizer.adjust_for_ambient_noise(source)
            print("✅ Microphone test successful!")
        
        print("🗣️ Testing text-to-speech...")
        luna_voice.speak("Voice systems ready. I'm LunaBeyond, your AI voice companion.")
        
        print("\n🎤 STARTING VOICE CONVERSATION")
        print("=" * 50)
        
        # Start voice chat
        luna_voice.start_voice_chat()
        
    except KeyboardInterrupt:
        print("\n🌙 Voice chat ended by user")
        
    except Exception as e:
        print(f"⚠️ Voice chat error: {e}")
        print("🔧 Please check microphone and speaker permissions")

if __name__ == "__main__":
    main()
