#!/usr/bin/env python3
"""
🎤 LUNABEYOND AI - VOICE INTERFACE
Complete voice interaction system with natural conversation
"""

import asyncio
import json
import time
import threading
import queue
from datetime import datetime
from typing import Dict, List, Any, Optional
from luna_conversation_manager import luna_conversation_manager
from luna_learning_engine import luna_learning_engine

class LunaVoiceInterface:
    """Complete voice interface for natural Luna conversation"""
    
    def __init__(self):
        self.conversation_manager = luna_conversation_manager
        self.learning_engine = luna_learning_engine
        
        # Voice processing queue
        self.voice_queue = queue.Queue()
        self.is_processing = False
        
        # Voice settings
        self.voice_settings = {
            'enabled': True,
            'language': 'en-US',
            'accent': 'female',
            'rate': 150,  # Slightly faster than normal
            'volume': 0.9,
            'pitch': 135  # Slightly higher for female voice
        }
        
        # Conversation state
        self.conversation_active = False
        self.listening_timeout = 30  # seconds
        self.last_voice_activity = time.time()
        
        # Initialize voice systems
        self.initialize_voice_systems()
    
    def initialize_voice_systems(self):
        """Initialize voice recognition and synthesis"""
        try:
            import speech_recognition as sr
            import pyttsx3
            
            # Initialize speech recognition
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
            
            # Initialize text-to-speech
            self.tts_engine = pyttsx3.init()
            
            # Configure voice
            voices = self.tts_engine.getProperty('voices')
            for voice in voices:
                if 'female' in voice.name.lower():
                    self.tts_engine.setProperty('voice', voice.id)
                    break
            
            # Set voice properties
            self.tts_engine.setProperty('rate', self.voice_settings['rate'])
            self.tts_engine.setProperty('volume', self.voice_settings['volume'])
            self.tts_engine.setProperty('pitch', self.voice_settings['pitch'])
            
            print("✅ Voice systems initialized successfully!")
            return True
            
        except ImportError as e:
            print(f"⚠️ Voice library not available: {e}")
            print("🔧 Please install: pip install SpeechRecognition pyttsx3")
            return False
        except Exception as e:
            print(f"⚠️ Voice initialization error: {e}")
            return False
    
    def start_voice_conversation(self):
        """
        🎤 Start complete voice conversation interface
        """
        print("🌙 LunaBeyond AI Voice Interface")
        print("=" * 60)
        
        if not self.initialize_voice_systems():
            print("❌ Voice systems failed to initialize")
            return
        
        print("🎤 Starting voice conversation...")
        print("🎙 Luna is ready to talk with you!")
        print("🎤 Say 'hello Luna' to begin")
        print("🔇 Say 'stop listening' to pause")
        print("👋 Say 'goodbye' to end conversation")
        print("=" * 60)
        
        # Start conversation
        self.conversation_active = True
        
        # Start voice processing thread
        voice_thread = threading.Thread(target=self.voice_processing_loop)
        voice_thread.daemon = True
        voice_thread.start()
        
        # Main conversation loop
        self.conversation_management_loop()
    
    def voice_processing_loop(self):
        """Continuous voice processing loop"""
        while self.conversation_active:
            try:
                # Listen for voice input
                with self.microphone as source:
                    self.recognizer.adjust_for_ambient_noise(source)
                    print("🎤 [LISTENING] Luna is listening...")
                    
                    # Listen with timeout
                    try:
                        audio = self.recognizer.listen(
                            source, 
                            timeout=1, 
                            phrase_time_limit=10,
                            snowboy_configuration=None
                        )
                        
                        if audio:
                            user_input = self.recognizer.recognize_google(
                                audio, 
                                language=self.voice_settings['language']
                            )
                            
                            # Process voice input
                            self.process_voice_input(user_input)
                            self.last_voice_activity = time.time()
                            
                    except sr.WaitTimeoutError:
                        # Check for inactivity timeout
                        if time.time() - self.last_voice_activity > self.listening_timeout:
                            self.speak("I'm still here and listening. Is everything okay?")
                            self.last_voice_activity = time.time()
                            
                    except sr.UnknownValueError:
                        print("🔇 [UNCLEAR] Didn't catch that...")
                        continue
                        
                    except sr.RequestError as e:
                        print(f"⚠️ Voice recognition error: {e}")
                        continue
                        
            except Exception as e:
                print(f"⚠️ Microphone error: {e}")
                time.sleep(1)
                continue
    
    def conversation_management_loop(self):
        """Manage conversation flow and context"""
        while self.conversation_active:
            time.sleep(0.5)
            
            # Check for voice commands
            if not self.voice_queue.empty():
                command = self.voice_queue.get()
                self.handle_voice_command(command)
    
    def process_voice_input(self, user_input: str):
        """
        🧠 Process voice input through natural conversation manager
        """
        if not user_input or not user_input.strip():
            return
        
        print(f"👤 You: {user_input}")
        
        # Check for voice commands
        if self.is_voice_command(user_input):
            self.voice_queue.put(user_input.lower())
            return
        
        # Set processing state
        self.is_processing = True
        
        try:
            # Create context for voice interaction
            context = {
                'timestamp': datetime.now().isoformat(),
                'interaction_type': 'voice',
                'voice_settings': self.voice_settings,
                'conversation_depth': self.conversation_manager.conversation_context.conversation_depth
            }
            
            # Process through conversation manager
            import asyncio
            loop = asyncio.new_event_loop()
            
            async def process_input():
                return await self.conversation_manager.process_user_input(user_input, context)
            
            # Get response data
            response_data = loop.run_until_complete(process_input())
            
            # Speak Luna's response
            luna_response = response_data['response_text']
            print(f"🌙 Luna: {luna_response}")
            
            # Show processing indicators
            self.show_processing_indicators(response_data)
            
            # Speak response
            self.speak(luna_response)
            
            # Update learning
            self.update_learning_from_voice(user_input, luna_response, response_data)
            
            # Handle follow-up questions
            if response_data.get('follow_up_question'):
                time.sleep(2)  # Pause before follow-up
                follow_up = response_data['follow_up_question']
                print(f"🌙 Luna: {follow_up}")
                self.speak(follow_up)
            
        except Exception as e:
            print(f"⚠️ Voice processing error: {e}")
            error_response = "I'm having trouble processing that. Could you please repeat?"
            self.speak(error_response)
        
        finally:
            self.is_processing = False
            self.hide_processing_indicators()
    
    def is_voice_command(self, user_input: str) -> bool:
        """Check if input is a voice command"""
        voice_commands = [
            'hello luna',
            'stop listening',
            'start listening',
            'goodbye luna',
            'luna sleep',
            'luna wake up',
            'what can i say',
            'voice commands',
            'help voice'
        ]
        
        return user_input.lower() in voice_commands
    
    def handle_voice_command(self, command: str):
        """Handle voice commands"""
        if command == 'hello luna':
            self.speak("Hello! I'm LunaBeyond, your voice companion. I'm ready to chat!")
            print("🌙 Voice conversation activated")
            
        elif command == 'stop listening':
            self.speak("Voice listening paused. Say 'start listening' to resume.")
            print("🔇 Voice listening paused")
            
        elif command == 'start listening':
            self.speak("Voice listening resumed. I'm here and ready to chat!")
            print("🎤 Voice listening resumed")
            
        elif command == 'goodbye luna':
            self.speak("Goodbye! It was wonderful talking with you. I'll miss our voice conversations!")
            self.conversation_active = False
            print("👋 Voice conversation ended")
            
        elif command == 'luna sleep':
            self.speak("I'll rest now. Wake me up by saying 'Luna wake up'.")
            print("😴 Luna entering sleep mode")
            
        elif command == 'luna wake up':
            self.speak("I'm awake and ready to continue our conversation!")
            print("🌙 Luna awakened from sleep")
            
        elif command in ['what can i say', 'voice commands', 'help voice']:
            help_text = """🎤 Voice commands I understand:
• 'Hello Luna' - Start conversation
• 'Stop listening' - Pause voice recognition
• 'Start listening' - Resume voice recognition
• 'Goodbye Luna' - End conversation
• 'Luna sleep' - Enter sleep mode
• 'Luna wake up' - Wake from sleep
• 'What can I say' - Hear all commands
• 'Help voice' - Hear this list"""
            
            print(help_text)
            self.speak(help_text)
    
    def update_learning_from_voice(self, user_input: str, luna_response: str, response_data: Dict):
        """Update learning systems from voice conversation"""
        # Update learning engine
        self.learning_engine.total_interactions += 1
        
        # Add to conversation memory
        memory_entry = {
            'message': user_input,
            'timestamp': datetime.now(),
            'interaction': self.learning_engine.total_interactions,
            'voice_input': True,
            'luna_response': luna_response,
            'response_data': response_data,
            'emotional_tone': response_data.get('emotional_tone', 'neutral')
        }
        
        if not hasattr(self.learning_engine, 'conversation_memory'):
            self.learning_engine.conversation_memory = []
        
        self.learning_engine.conversation_memory.append(memory_entry)
        
        # Keep memory manageable
        if len(self.learning_engine.conversation_memory) > 100:
            self.learning_engine.conversation_memory = self.learning_engine.conversation_memory[-50:]
        
        print(f"📚 Voice learning updated: {self.learning_engine.total_interactions} total voice interactions")
    
    def show_processing_indicators(self, response_data: Dict):
        """Show visual indicators for processing state"""
        pattern = response_data.get('pattern_id', 'general')
        emotional_tone = response_data.get('emotional_tone', 'neutral')
        
        indicators = {
            'greeting': "👋 [GREETING] Luna recognizes your greeting!",
            'how_are_you': "🤔 [THINKING] Luna is considering how she feels...",
            'capabilities': "🧠 [ANALYZING] Luna is accessing her capabilities...",
            'emotional_support': "💝 [EMPATHY] Luna is processing with care...",
            'excitement': "🤩 [EXCITEMENT] Luna is processing your positive energy!",
            'curiosity': "🤔 [CURIOSITY] Luna is exploring your ideas...",
            'problem_solving': "🛠️ [PROBLEM SOLVING] Luna is thinking through solutions...",
            'farewell': "👋 [FAREWELL] Luna is processing your goodbye..."
        }
        
        indicator = indicators.get(pattern, "🧠 [PROCESSING] Luna is thinking...")
        print(indicator)
    
    def hide_processing_indicators(self):
        """Hide processing indicators"""
        print("✅ [READY] Luna finished processing")
    
    def speak(self, text: str):
        """
        🔊 Speak text with natural voice
        """
        if not self.voice_settings['enabled']:
            print(f"🔊 [VOICE DISABLED] {text}")
            return
        
        try:
            print(f"🔊 [SPEAKING] {text}")
            
            # Create separate thread for speaking to avoid blocking
            speak_thread = threading.Thread(
                target=self._speak_in_thread,
                args=(text,),
                daemon=True
            )
            speak_thread.start()
            
        except Exception as e:
            print(f"⚠️ Speech error: {e}")
    
    def _speak_in_thread(self, text: str):
        """Speak text in separate thread"""
        try:
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        except Exception as e:
            print(f"⚠️ Speech thread error: {e}")
    
    def get_voice_status(self) -> Dict:
        """Get comprehensive voice interface status"""
        return {
            'conversation_active': self.conversation_active,
            'is_processing': self.is_processing,
            'voice_enabled': self.voice_settings['enabled'],
            'voice_settings': self.voice_settings,
            'queue_size': self.voice_queue.qsize(),
            'last_activity': self.last_voice_activity,
            'conversation_status': self.conversation_manager.get_conversation_status(),
            'learning_interactions': self.learning_engine.total_interactions,
            'microphone_status': 'Connected' if hasattr(self, 'microphone') else 'Disconnected',
            'tts_status': 'Ready' if hasattr(self, 'tts_engine') else 'Not initialized'
        }
    
    def adjust_voice_settings(self, setting: str, value: Any):
        """Adjust voice settings"""
        if setting in self.voice_settings:
            self.voice_settings[setting] = value
            
            # Apply setting if voice is initialized
            if hasattr(self, 'tts_engine'):
                if setting == 'rate':
                    self.tts_engine.setProperty('rate', value)
                elif setting == 'volume':
                    self.tts_engine.setProperty('volume', value)
                elif setting == 'pitch':
                    self.tts_engine.setProperty('pitch', value)
            
            print(f"🔧 Voice setting updated: {setting} = {value}")
    
    def enable_voice_mode(self):
        """Enable voice interaction mode"""
        self.voice_settings['enabled'] = True
        self.speak("Voice mode enabled. I'm ready to listen and speak!")
        print("🎤 Voice mode enabled")
    
    def disable_voice_mode(self):
        """Disable voice interaction mode"""
        self.voice_settings['enabled'] = False
        self.speak("Voice mode disabled. I'll respond through text only.")
        print("🔇 Voice mode disabled")

def main():
    """Main function to start Luna voice interface"""
    print("🌙 LunaBeyond AI Voice Interface Starting...")
    print("🎤 Initializing voice systems...")
    
    try:
        # Initialize voice interface
        luna_voice = LunaVoiceInterface()
        
        # Test voice systems
        if not luna_voice.initialize_voice_systems():
            print("❌ Cannot start voice interface without proper voice libraries")
            print("🔧 Install with: pip install SpeechRecognition pyttsx3")
            return
        
        print("✅ Voice systems ready!")
        print("🎤 Starting voice conversation interface...")
        
        # Start voice conversation
        luna_voice.start_voice_conversation()
        
    except KeyboardInterrupt:
        print("\n🌙 Voice interface ended by user")
        
    except Exception as e:
        print(f"⚠️ Voice interface error: {e}")

if __name__ == "__main__":
    main()
