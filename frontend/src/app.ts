// 🚀 LunaBeyond AI Frontend - TypeScript Application
// High-performance TypeScript frontend for LunaBeyond AI system

import { LunaClient } from './services/luna-client';
import { VoiceManager } from './services/voice-manager';
import { BHCSManager } from './services/bhcs-manager';
import { UIManager } from './services/ui-manager';
import { EventBus } from './utils/event-bus';
import { Logger } from './utils/logger';

// Configuration
interface AppConfig {
    apiUrl: string;
    wsUrl: string;
    voiceEnabled: boolean;
    debugMode: boolean;
    sessionTimeout: number;
}

// Main Application Class
class LunaBeyondApp {
    private config: AppConfig;
    private lunaClient!: LunaClient;
    private voiceManager!: VoiceManager;
    private bhcsManager!: BHCSManager;
    private uiManager!: UIManager;
    private eventBus: EventBus;
    private logger: Logger;
    private sessionId: string;
    private isConnected: boolean = false;

    constructor(config: AppConfig) {
        this.config = config;
        this.logger = new Logger('LunaBeyondApp', config.debugMode);
        this.eventBus = new EventBus();
        this.sessionId = this.generateSessionId();
        
        this.initializeServices();
        this.setupEventHandlers();
    }

    private initializeServices(): void {
        this.logger.info('Initializing LunaBeyond AI services...');

        // Initialize core services
        this.lunaClient = new LunaClient(this.config.apiUrl, this.config.wsUrl, this.sessionId);
        this.voiceManager = new VoiceManager(this.eventBus, this.config.voiceEnabled);
        this.bhcsManager = new BHCSManager(this.lunaClient, this.eventBus);
        this.uiManager = new UIManager(this.eventBus);

        this.logger.info('Services initialized successfully');
    }

    private setupEventHandlers(): void {
        // Connection events
        this.eventBus.on('connected', () => {
            this.isConnected = true;
            this.uiManager.showConnectionStatus('connected');
            this.logger.info('Connected to LunaBeyond AI backend');
        });

        this.eventBus.on('disconnected', () => {
            this.isConnected = false;
            this.uiManager.showConnectionStatus('disconnected');
            this.logger.warn('Disconnected from LunaBeyond AI backend');
        });

        this.eventBus.on('error', (error: Error) => {
            this.logger.error('Application error:', error);
            this.uiManager.showError(error.message);
        });

        // Chat events
        this.eventBus.on('message-sent', (message: string) => {
            this.logger.debug('Message sent:', message);
            this.uiManager.addMessageToChat(message, 'user');
        });

        this.eventBus.on('message-received', (response: any) => {
            this.logger.debug('Message received:', response);
            this.uiManager.addMessageToChat(response.response_text, 'luna');
            this.uiManager.updateLunaStatus(response);
        });

        // Voice events
        this.eventBus.on('voice-started', () => {
            this.uiManager.showVoiceStatus('listening');
            this.logger.info('Voice recognition started');
        });

        this.eventBus.on('voice-stopped', () => {
            this.uiManager.showVoiceStatus('inactive');
            this.logger.info('Voice recognition stopped');
        });

        this.eventBus.on('voice-command', (command: string) => {
            this.logger.info('Voice command received:', command);
            this.processCommand(command);
        });

        // BHCS events
        this.eventBus.on('bhcs-update', (data: any) => {
            this.logger.debug('BHCS update:', data);
            this.uiManager.updateBHCSStatus(data);
        });

        this.eventBus.on('bhcs-alert', (alert: any) => {
            this.logger.warn('BHCS alert:', alert);
            this.uiManager.showBHCSAlert(alert);
        });
    }

    public async start(): Promise<void> {
        try {
            this.logger.info('Starting LunaBeyond AI application...');

            // Start UI
            await this.uiManager.initialize();

            // Connect to backend
            await this.connect();

            // Start voice if enabled
            if (this.config.voiceEnabled) {
                await this.voiceManager.initialize();
            }

            // Start BHCS monitoring
            await this.bhcsManager.startMonitoring();

            // Setup periodic health checks
            this.startHealthChecks();

            this.logger.info('LunaBeyond AI application started successfully');

        } catch (error) {
            this.logger.error('Failed to start application:', error);
            throw error;
        }
    }

    private async connect(): Promise<void> {
        try {
            await this.lunaClient.connect();
            this.logger.info('Connected to backend successfully');
        } catch (error) {
            this.logger.error('Failed to connect to backend:', error);
            throw error;
        }
    }

    private async disconnect(): Promise<void> {
        try {
            await this.lunaClient.disconnect();
            this.logger.info('Disconnected from backend');
        } catch (error) {
            this.logger.error('Error during disconnect:', error);
        }
    }

    public async sendMessage(message: string): Promise<void> {
        if (!this.isConnected) {
            throw new Error('Not connected to backend');
        }

        try {
            this.eventBus.emit('message-sent', message);
            
            const response = await this.lunaClient.sendChatMessage(message);
            
            this.eventBus.emit('message-received', response);
            
        } catch (error) {
            this.logger.error('Failed to send message:', error);
            this.eventBus.emit('error', error);
        }
    }

    public async sendVoiceCommand(command: string): Promise<void> {
        if (!this.isConnected) {
            throw new Error('Not connected to backend');
        }

        try {
            const response = await this.lunaClient.sendVoiceCommand(command);
            this.eventBus.emit('message-received', response);
        } catch (error) {
            this.logger.error('Failed to send voice command:', error);
            this.eventBus.emit('error', error);
        }
    }

    public async sendBHCSCommand(command: string, parameters?: any): Promise<void> {
        if (!this.isConnected) {
            throw new Error('Not connected to backend');
        }

        try {
            const response = await this.lunaClient.sendBHCSCommand(command, parameters);
            this.eventBus.emit('bhcs-update', response);
        } catch (error) {
            this.logger.error('Failed to send BHCS command:', error);
            this.eventBus.emit('error', error);
        }
    }

    private async processCommand(command: string): Promise<void> {
        const lowerCommand = command.toLowerCase();

        try {
            if (lowerCommand.includes('hello') || lowerCommand.includes('hi')) {
                await this.sendMessage(command);
            } else if (lowerCommand.includes('system status')) {
                await this.sendBHCSCommand('status');
            } else if (lowerCommand.includes('apply biocore')) {
                await this.sendBHCSCommand('apply_biocore');
            } else if (lowerCommand.includes('optimize')) {
                await this.sendBHCSCommand('optimize');
            } else if (lowerCommand.includes('predict')) {
                await this.sendBHCSCommand('predict');
            } else if (lowerCommand.includes('emergency')) {
                await this.sendBHCSCommand('emergency_stop');
            } else {
                await this.sendMessage(command);
            }
        } catch (error) {
            this.logger.error('Failed to process command:', error);
            this.eventBus.emit('error', error);
        }
    }

    private startHealthChecks(): void {
        setInterval(async () => {
            try {
                if (this.isConnected) {
                    const status = await this.lunaClient.getSystemStatus();
                    this.eventBus.emit('bhcs-update', status);
                }
            } catch (error) {
                this.logger.error('Health check failed:', error);
            }
        }, 30000); // Check every 30 seconds
    }

    private generateSessionId(): string {
        return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }

    public getSessionId(): string {
        return this.sessionId;
    }

    public isConnectedToBackend(): boolean {
        return this.isConnected;
    }

    public async shutdown(): Promise<void> {
        this.logger.info('Shutting down LunaBeyond AI application...');

        try {
            // Stop voice
            await this.voiceManager.shutdown();

            // Stop BHCS monitoring
            await this.bhcsManager.stopMonitoring();

            // Disconnect from backend
            await this.disconnect();

            // Cleanup UI
            await this.uiManager.cleanup();

            this.logger.info('Application shutdown complete');

        } catch (error) {
            this.logger.error('Error during shutdown:', error);
        }
    }
}

// Configuration
const config: AppConfig = {
    apiUrl: process.env.API_URL || 'http://localhost:8000',
    wsUrl: process.env.WS_URL || 'ws://localhost:8000',
    voiceEnabled: process.env.VOICE_ENABLED !== 'false',
    debugMode: process.env.DEBUG_MODE === 'true',
    sessionTimeout: 3600000 // 1 hour
};

// Initialize and start application
const app = new LunaBeyondApp(config);

// Start application when DOM is ready
document.addEventListener('DOMContentLoaded', async () => {
    try {
        await app.start();
    } catch (error) {
        console.error('Failed to start LunaBeyond AI application:', error);
    }
});

// Handle page unload
window.addEventListener('beforeunload', async () => {
    await app.shutdown();
});

// Export for global access
(window as any).lunaApp = app;

export { LunaBeyondApp, AppConfig };
