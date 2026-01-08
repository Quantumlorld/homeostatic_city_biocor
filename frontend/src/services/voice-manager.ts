import '../types/voice';

// LunaBeyond AI Voice Manager
// TypeScript voice recognition and synthesis service

interface VoiceSettings {
    enabled: boolean;
    language: string;
    rate: number;
    volume: number;
    pitch: number;
}

export class VoiceManager {
    private eventBus: any;
    private settings: VoiceSettings;
    private recognition: any = null;
    private synthesis: SpeechSynthesis;
    private isListening: boolean = false;
    private isSpeaking: boolean = false;
    private femaleVoice: SpeechSynthesisVoice | null = null;

    constructor(eventBus: any, enabled: boolean = true) {
        this.eventBus = eventBus;
        this.synthesis = window.speechSynthesis;
        
        this.settings = {
            enabled: enabled,
            language: 'en-US',
            rate: 1.0,
            volume: 0.9,
            pitch: 1.0
        };

        this.initializeVoiceRecognition();
        this.loadFemaleVoice();
    }

    private async loadFemaleVoice(): Promise<void> {
        // Wait for voices to be loaded
        if (this.synthesis.getVoices().length === 0) {
            this.synthesis.onvoiceschanged = () => {
                this.setFemaleVoice();
            };
        } else {
            this.setFemaleVoice();
        }
    }

    private setFemaleVoice(): void {
        const voices = this.synthesis.getVoices();
        
        // Try to find a female voice
        const femaleVoice = voices.find(voice => 
            voice.name.toLowerCase().includes('female') ||
            voice.name.toLowerCase().includes('woman') ||
            voice.name.toLowerCase().includes('samantha') ||
            voice.name.toLowerCase().includes('karen') ||
            voice.name.toLowerCase().includes('siri') ||
            voice.lang.includes('en') && voice.name.includes('Google')
        );
        
        if (femaleVoice) {
            this.femaleVoice = femaleVoice;
            console.log('Female voice selected:', femaleVoice.name);
        } else {
            // Fallback to any English voice
            const englishVoice = voices.find(voice => voice.lang.includes('en'));
            if (englishVoice) {
                this.femaleVoice = englishVoice;
                console.log('English voice selected:', englishVoice.name);
            }
        }
    }

    private initializeVoiceRecognition(): void {
        if (!this.settings.enabled) {
            console.log('Voice recognition disabled');
            return;
        }

        if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
            console.warn('Speech recognition not supported in this browser');
            return;
        }

        const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
        this.recognition = new SpeechRecognition();
        
        this.recognition.continuous = true;
        this.recognition.interimResults = true;
        this.recognition.lang = this.settings.language;

        this.recognition.onstart = () => {
            this.isListening = true;
            this.eventBus.emit('voice-started');
            console.log('Voice recognition started');
        };

        this.recognition.onresult = (event: any) => {
            const last = event.results.length - 1;
            const transcript = event.results[last][0].transcript;
            
            if (event.results[last].isFinal) {
                this.processVoiceCommand(transcript);
            }
        };

        this.recognition.onerror = (event: any) => {
            console.error('Voice recognition error:', event.error);
            this.eventBus.emit('voice-error', { error: event.error });
        };

        this.recognition.onend = () => {
            this.isListening = false;
            this.eventBus.emit('voice-stopped');
            console.log('Voice recognition stopped');
        };
    }

    public async initialize(): Promise<void> {
        try {
            // Load available voices
            await this.loadVoices();
            
            // Set default voice
            this.setFemaleVoice();
            
            console.log('Voice manager initialized successfully');
            
        } catch (error) {
            console.error('Failed to initialize voice manager:', error);
            throw error;
        }
    }

    private async loadVoices(): Promise<void> {
        return new Promise((resolve) => {
            const voices = this.synthesis.getVoices();
            
            if (voices.length > 0) {
                resolve();
            } else {
                this.synthesis.onvoiceschanged = () => {
                    resolve();
                };
            }
        });
    }

    public startListening(): void {
        if (!this.recognition) {
            console.warn('Voice recognition not available');
            return;
        }

        if (this.isListening) {
            console.warn('Voice recognition already active');
            return;
        }

        try {
            this.recognition.start();
        } catch (error) {
            console.error('Failed to start voice recognition:', error);
        }
    }

    public stopListening(): void {
        if (!this.recognition) {
            return;
        }

        if (!this.isListening) {
            return;
        }

        try {
            this.recognition.stop();
        } catch (error) {
            console.error('Failed to stop voice recognition:', error);
        }
    }

    private processVoiceCommand(command: string): void {
        console.log('Voice command received:', command);
        
        // Emit voice command event
        this.eventBus.emit('voice-command', command);
        
        // Also emit specific command type events
        const lowerCommand = command.toLowerCase();
        
        if (lowerCommand.includes('hello') || lowerCommand.includes('hi')) {
            this.eventBus.emit('voice-greeting', command);
        } else if (lowerCommand.includes('status')) {
            this.eventBus.emit('voice-status', command);
        } else if (lowerCommand.includes('biocore')) {
            this.eventBus.emit('voice-biocore', command);
        } else if (lowerCommand.includes('optimize')) {
            this.eventBus.emit('voice-optimize', command);
        } else if (lowerCommand.includes('predict')) {
            this.eventBus.emit('voice-predict', command);
        } else if (lowerCommand.includes('emergency')) {
            this.eventBus.emit('voice-emergency', command);
        } else if (lowerCommand.includes('goodbye') || lowerCommand.includes('bye')) {
            this.eventBus.emit('voice-goodbye', command);
        }
    }

    public speak(text: string, options?: Partial<VoiceSettings>): void {
        if (!this.settings.enabled) {
            console.log('Voice synthesis disabled');
            return;
        }

        if (this.isSpeaking) {
            console.warn('Already speaking, queuing message');
            return;
        }

        try {
            const utterance = new SpeechSynthesisUtterance(text);
            
            // Apply settings
            utterance.rate = options?.rate || this.settings.rate;
            utterance.volume = options?.volume || this.settings.volume;
            utterance.pitch = options?.pitch || this.settings.pitch;
            utterance.lang = options?.language || this.settings.language;
            
            // Set female voice
            if (this.femaleVoice) {
                utterance.voice = this.femaleVoice;
            }

            utterance.onstart = () => {
                this.isSpeaking = true;
                this.eventBus.emit('voice-speaking-start', { text });
            };

            utterance.onend = () => {
                this.isSpeaking = false;
                this.eventBus.emit('voice-speaking-end', { text });
            };

            utterance.onerror = (event: any) => {
                this.isSpeaking = false;
                console.error('Speech synthesis error:', event);
                this.eventBus.emit('voice-synthesis-error', { error: event });
            };

            this.synthesis.speak(utterance);
            
        } catch (error) {
            console.error('Failed to speak text:', error);
        }
    }

    public stopSpeaking(): void {
        if (this.synthesis.speaking) {
            this.synthesis.cancel();
            this.isSpeaking = false;
            this.eventBus.emit('voice-speaking-stop');
        }
    }

    public updateSettings(newSettings: Partial<VoiceSettings>): void {
        this.settings = { ...this.settings, ...newSettings };
        
        if (this.recognition && newSettings.language) {
            this.recognition.lang = newSettings.language;
        }
        
        console.log('Voice settings updated:', this.settings);
    }

    public getSettings(): VoiceSettings {
        return { ...this.settings };
    }

    public isVoiceEnabled(): boolean {
        return this.settings.enabled;
    }

    public isCurrentlyListening(): boolean {
        return this.isListening;
    }

    public isCurrentlySpeaking(): boolean {
        return this.isSpeaking;
    }

    public getAvailableVoices(): SpeechSynthesisVoice[] {
        return this.synthesis.getVoices();
    }

    public testVoice(): void {
        const testMessage = "Voice test successful! I'm Luna, your female AI assistant. I can speak clearly and naturally.";
        this.speak(testMessage);
    }

    public async shutdown(): Promise<void> {
        try {
            // Stop recognition
            if (this.recognition) {
                this.stopListening();
            }
            
            // Stop synthesis
            this.stopSpeaking();
            
            console.log('Voice manager shutdown complete');
            
        } catch (error) {
            console.error('Error during voice manager shutdown:', error);
        }
    }
}
