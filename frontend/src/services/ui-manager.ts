// 🎨 LunaBeyond AI UI Manager
// TypeScript service for UI management and updates

interface ChatMessage {
    id: string;
    text: string;
    sender: 'user' | 'luna';
    timestamp: string;
    mood?: string;
}

interface LunaStatus {
    mood: string;
    confidence: number;
    interactions: number;
    expertise: string;
    evolutionStage: string;
}

export class UIManager {
    private eventBus: any;
    private chatMessages: ChatMessage[];
    private lunaStatus: LunaStatus;
    private connectionStatus: 'connected' | 'disconnected' | 'connecting' = 'disconnected';
    private voiceStatus: 'active' | 'inactive' | 'listening' | 'speaking' = 'inactive';

    constructor(eventBus: any) {
        this.eventBus = eventBus;
        this.chatMessages = [];
        
        this.lunaStatus = {
            mood: 'curious',
            confidence: 0.5,
            interactions: 0,
            expertise: 'developing',
            evolutionStage: 'developing'
        };
        
        this.initializeUI();
        this.setupEventHandlers();
    }

    private initializeUI(): void {
        // Create chat container if it doesn't exist
        this.createChatContainer();
        this.createStatusContainer();
        this.createVoiceControls();
        
        // Add welcome message
        this.addMessageToChat('🌙 Hello! I\'m LunaBeyond AI, ready to chat and help you manage the BHCS system!', 'luna');
    }

    private createChatContainer(): void {
        let chatContainer = document.getElementById('luna-chat-container');
        
        if (!chatContainer) {
            chatContainer = document.createElement('div');
            chatContainer.id = 'luna-chat-container';
            chatContainer.className = 'luna-chat-container';
            
            chatContainer.innerHTML = `
                <div class="luna-chat-header">
                    <h3>🌙 LunaBeyond AI Chat</h3>
                    <div class="connection-indicator" id="connection-indicator">
                        <span class="indicator-dot disconnected"></span>
                        <span class="indicator-text">Disconnected</span>
                    </div>
                </div>
                <div class="luna-chat-messages" id="luna-chat-messages"></div>
                <div class="luna-chat-input">
                    <input type="text" id="luna-chat-input" placeholder="Type your message..." />
                    <button id="luna-chat-send">Send</button>
                </div>
            `;
            
            document.body.appendChild(chatContainer);
        }
        
        // Setup chat input handlers
        const input = document.getElementById('luna-chat-input') as HTMLInputElement;
        const sendButton = document.getElementById('luna-chat-send') as HTMLButtonElement;
        
        if (input && sendButton) {
            sendButton.addEventListener('click', () => this.handleChatInput());
            input.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    this.handleChatInput();
                }
            });
        }
    }

    private createStatusContainer(): void {
        let statusContainer = document.getElementById('luna-status-container');
        
        if (!statusContainer) {
            statusContainer = document.createElement('div');
            statusContainer.id = 'luna-status-container';
            statusContainer.className = 'luna-status-container';
            
            statusContainer.innerHTML = `
                <div class="luna-status-header">
                    <h3>🧠 Luna Status</h3>
                </div>
                <div class="luna-status-grid">
                    <div class="status-item">
                        <span class="status-label">Mood:</span>
                        <span class="status-value" id="luna-mood">curious</span>
                    </div>
                    <div class="status-item">
                        <span class="status-label">Confidence:</span>
                        <span class="status-value" id="luna-confidence">50%</span>
                    </div>
                    <div class="status-item">
                        <span class="status-label">Interactions:</span>
                        <span class="status-value" id="luna-interactions">0</span>
                    </div>
                    <div class="status-item">
                        <span class="status-label">Expertise:</span>
                        <span class="status-value" id="luna-expertise">developing</span>
                    </div>
                </div>
            `;
            
            document.body.appendChild(statusContainer);
        }
    }

    private createVoiceControls(): void {
        let voiceContainer = document.getElementById('luna-voice-container');
        
        if (!voiceContainer) {
            voiceContainer = document.createElement('div');
            voiceContainer.id = 'luna-voice-container';
            voiceContainer.className = 'luna-voice-container';
            
            voiceContainer.innerHTML = `
                <div class="luna-voice-header">
                    <h3>🎤 Voice Controls</h3>
                    <div class="voice-indicator" id="voice-indicator">
                        <span class="voice-dot inactive"></span>
                        <span class="voice-text">Inactive</span>
                    </div>
                </div>
                <div class="luna-voice-controls">
                    <button id="voice-start" class="voice-btn">🎤 Start Voice</button>
                    <button id="voice-stop" class="voice-btn">🔇 Stop Voice</button>
                    <button id="voice-test" class="voice-btn">🧪 Test Voice</button>
                </div>
                <div class="luna-voice-commands">
                    <h4>Quick Commands:</h4>
                    <div class="voice-command-grid">
                        <button class="voice-cmd-btn" data-cmd="Hello Luna">👋 Hello</button>
                        <button class="voice-cmd-btn" data-cmd="System status">📊 Status</button>
                        <button class="voice-cmd-btn" data-cmd="Apply BioCore">🧬 BioCore</button>
                        <button class="voice-cmd-btn" data-cmd="Optimize system">⚡ Optimize</button>
                    </div>
                </div>
            `;
            
            document.body.appendChild(voiceContainer);
            
            // Setup voice control handlers
            this.setupVoiceControlHandlers();
        }
    }

    private setupVoiceControlHandlers(): void {
        const startBtn = document.getElementById('voice-start');
        const stopBtn = document.getElementById('voice-stop');
        const testBtn = document.getElementById('voice-test');
        
        if (startBtn) {
            startBtn.addEventListener('click', () => {
                this.eventBus.emit('voice-start-request');
            });
        }
        
        if (stopBtn) {
            stopBtn.addEventListener('click', () => {
                this.eventBus.emit('voice-stop-request');
            });
        }
        
        if (testBtn) {
            testBtn.addEventListener('click', () => {
                this.eventBus.emit('voice-test-request');
            });
        }
        
        // Setup voice command buttons
        const cmdButtons = document.querySelectorAll('.voice-cmd-btn');
        cmdButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                const command = (e.target as HTMLElement).getAttribute('data-cmd');
                if (command) {
                    this.eventBus.emit('voice-command', command);
                }
            });
        });
    }

    private setupEventHandlers(): void {
        // Connection events
        this.eventBus.on('connected', () => {
            this.showConnectionStatus('connected');
        });

        this.eventBus.on('disconnected', () => {
            this.showConnectionStatus('disconnected');
        });

        // Voice events
        this.eventBus.on('voice-started', () => {
            this.showVoiceStatus('listening');
        });

        this.eventBus.on('voice-stopped', () => {
            this.showVoiceStatus('inactive');
        });

        this.eventBus.on('voice-speaking-start', () => {
            this.showVoiceStatus('speaking');
        });

        this.eventBus.on('voice-speaking-end', () => {
            this.showVoiceStatus('listening');
        });

        // BHCS events
        this.eventBus.on('bhcs-update', (data: any) => {
            this.updateBHCSStatus(data);
        });

        this.eventBus.on('bhcs-alert', (alert: any) => {
            this.showBHCSAlert(alert);
        });
    }

    private handleChatInput(): void {
        const input = document.getElementById('luna-chat-input') as HTMLInputElement;
        const message = input.value.trim();
        
        if (message) {
            this.addMessageToChat(message, 'user');
            this.eventBus.emit('chat-message-sent', message);
            input.value = '';
        }
    }

    public addMessageToChat(text: string, sender: 'user' | 'luna'): void {
        const messagesContainer = document.getElementById('luna-chat-messages');
        if (!messagesContainer) return;

        const message: ChatMessage = {
            id: Date.now().toString(),
            text,
            sender,
            timestamp: new Date().toISOString()
        };

        this.chatMessages.push(message);

        const messageElement = document.createElement('div');
        messageElement.className = `chat-message ${sender}`;
        
        const senderIcon = sender === 'user' ? '👤' : '🌙';
        const moodEmoji = sender === 'luna' && this.lunaStatus.mood ? 
            this.getMoodEmoji(this.lunaStatus.mood) : '';
        
        messageElement.innerHTML = `
            <div class="message-header">
                <span class="message-sender">${senderIcon} ${sender === 'user' ? 'You' : 'Luna'}</span>
                <span class="message-time">${new Date().toLocaleTimeString()}</span>
                ${moodEmoji ? `<span class="message-mood">${moodEmoji}</span>` : ''}
            </div>
            <div class="message-content">${text}</div>
        `;

        messagesContainer.appendChild(messageElement);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;

        // Keep only last 100 messages in UI
        if (messagesContainer.firstChild) {
            messagesContainer.removeChild(messagesContainer.firstChild);
        }
    }

    private getMoodEmoji(mood: string): string {
        const moodEmojis: { [key: string]: string } = {
            'curious': '🤔',
            'excited': '🤩',
            'confident': '😊',
            'helpful': '💫',
            'concerned': '😟',
            'grateful': '🙏'
        };
        return moodEmojis[mood] || '🌙';
    }

    public updateLunaStatus(status: any): void {
        if (status.response_data) {
            const data = status.response_data;
            
            this.lunaStatus.mood = data.processing_details?.emotional_tone || 'curious';
            this.lunaStatus.confidence = data.confidence || 0.5;
            this.lunaStatus.interactions = data.processing_details?.interactions || 0;
            this.lunaStatus.expertise = data.evolution_stage || 'developing';
        }
        
        this.updateStatusDisplay();
    }

    private updateStatusDisplay(): void {
        const moodElement = document.getElementById('luna-mood');
        const confidenceElement = document.getElementById('luna-confidence');
        const interactionsElement = document.getElementById('luna-interactions');
        const expertiseElement = document.getElementById('luna-expertise');
        
        if (moodElement) {
            moodElement.textContent = `${this.lunaStatus.mood} ${this.getMoodEmoji(this.lunaStatus.mood)}`;
        }
        
        if (confidenceElement) {
            confidenceElement.textContent = `${Math.round(this.lunaStatus.confidence * 100)}%`;
        }
        
        if (interactionsElement) {
            interactionsElement.textContent = this.lunaStatus.interactions.toString();
        }
        
        if (expertiseElement) {
            expertiseElement.textContent = this.lunaStatus.expertise;
        }
    }

    public showConnectionStatus(status: 'connected' | 'disconnected' | 'connecting'): void {
        this.connectionStatus = status;
        
        const indicator = document.getElementById('connection-indicator');
        if (!indicator) return;

        const dot = indicator.querySelector('.indicator-dot') as HTMLElement;
        const text = indicator.querySelector('.indicator-text') as HTMLElement;
        
        if (dot && text) {
            dot.className = `indicator-dot ${status}`;
            text.textContent = status.charAt(0).toUpperCase() + status.slice(1);
        }
    }

    public showVoiceStatus(status: 'active' | 'inactive' | 'listening' | 'speaking'): void {
        this.voiceStatus = status;
        
        const indicator = document.getElementById('voice-indicator');
        if (!indicator) return;

        const dot = indicator.querySelector('.voice-dot') as HTMLElement;
        const text = indicator.querySelector('.voice-text') as HTMLElement;
        
        if (dot && text) {
            dot.className = `voice-dot ${status}`;
            text.textContent = status.charAt(0).toUpperCase() + status.slice(1);
        }
    }

    public updateBHCSStatus(data: any): void {
        // Update BHCS status display
        const healthElement = document.getElementById('bhcs-health');
        const zonesElement = document.getElementById('bhcs-zones');
        
        if (healthElement) {
            healthElement.textContent = `${Math.round(data.system_health * 100)}%`;
        }
        
        if (zonesElement && data.zones) {
            const activeZones = data.zones.filter((zone: any) => zone.activity > 0.2).length;
            zonesElement.textContent = `${activeZones}/${data.zones.length}`;
        }
    }

    public showBHCSAlert(alert: any): void {
        // Create alert notification
        const alertElement = document.createElement('div');
        alertElement.className = `bhcs-alert ${alert.type}`;
        alertElement.innerHTML = `
            <div class="alert-content">
                <span class="alert-icon">${alert.type === 'critical' ? '🚨' : '⚠️'}</span>
                <span class="alert-message">${alert.message}</span>
                <button class="alert-close">×</button>
            </div>
        `;
        
        document.body.appendChild(alertElement);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (alertElement.parentNode) {
                alertElement.parentNode.removeChild(alertElement);
            }
        }, 5000);
        
        // Setup close button
        const closeBtn = alertElement.querySelector('.alert-close');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => {
                if (alertElement.parentNode) {
                    alertElement.parentNode.removeChild(alertElement);
                }
            });
        }
    }

    public showError(message: string): void {
        this.showBHCSAlert({
            type: 'critical',
            message,
            timestamp: new Date().toISOString()
        });
    }

    public async initialize(): Promise<void> {
        // UI is already initialized in constructor
        console.log('UI Manager initialized');
    }

    public async cleanup(): Promise<void> {
        // Remove UI elements
        const containers = [
            'luna-chat-container',
            'luna-status-container',
            'luna-voice-container'
        ];
        
        containers.forEach(id => {
            const element = document.getElementById(id);
            if (element && element.parentNode) {
                element.parentNode.removeChild(element);
            }
        });
        
        console.log('UI Manager cleanup complete');
    }
}
