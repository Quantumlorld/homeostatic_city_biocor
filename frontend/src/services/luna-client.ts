// 🌙 LunaBeyond AI Client Service
// TypeScript client for LunaBeyond AI backend communication

interface LunaResponse {
    success: boolean;
    session_id: string;
    response: any;
    processing_time: number;
    timestamp: string;
}

interface SystemStatus {
    system_health: number;
    zones: Array<{
        id: number;
        activity: number;
        state: string;
    }>;
    learning_engine: any;
    biocore_learning: any;
    conversation_manager: any;
    fast_response: any;
    active_sessions: number;
    performance_stats: any;
    timestamp: string;
}

export class LunaClient {
    private apiUrl: string;
    private wsUrl: string;
    private sessionId: string;
    private websocket: WebSocket | null = null;
    private reconnectAttempts: number = 0;
    private maxReconnectAttempts: number = 5;
    private reconnectDelay: number = 1000;

    constructor(apiUrl: string, wsUrl: string, sessionId: string) {
        this.apiUrl = apiUrl;
        this.wsUrl = wsUrl;
        this.sessionId = sessionId;
    }

    public async connect(): Promise<void> {
        try {
            // Connect WebSocket
            await this.connectWebSocket();
            
            // Test API connection
            await this.testConnection();
            
        } catch (error) {
            console.error('Failed to connect to LunaBeyond AI backend:', error);
            throw error;
        }
    }

    public async disconnect(): Promise<void> {
        if (this.websocket) {
            this.websocket.close();
            this.websocket = null;
        }
    }

    private async connectWebSocket(): Promise<void> {
        return new Promise((resolve, reject) => {
            const wsUrl = `${this.wsUrl}/ws/${this.sessionId}`;
            
            this.websocket = new WebSocket(wsUrl);
            
            this.websocket.onopen = () => {
                console.log('WebSocket connected to LunaBeyond AI backend');
                this.reconnectAttempts = 0;
                resolve();
            };
            
            this.websocket.onmessage = (event) => {
                try {
                    const data = JSON.parse(event.data);
                    this.handleWebSocketMessage(data);
                } catch (error) {
                    console.error('Failed to parse WebSocket message:', error);
                }
            };
            
            this.websocket.onclose = () => {
                console.log('WebSocket disconnected');
                this.handleWebSocketClose();
            };
            
            this.websocket.onerror = (error) => {
                console.error('WebSocket error:', error);
                reject(error);
            };
            
            // Connection timeout
            setTimeout(() => {
                if (this.websocket?.readyState !== WebSocket.OPEN) {
                    reject(new Error('WebSocket connection timeout'));
                }
            }, 10000);
        });
    }

    private handleWebSocketMessage(data: any): void {
        // Emit events based on message type
        const event = new CustomEvent(`luna-${data.type}`, {
            detail: data
        });
        document.dispatchEvent(event);
    }

    private async handleWebSocketClose(): Promise<void> {
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
            this.reconnectAttempts++;
            console.log(`Attempting to reconnect (${this.reconnectAttempts}/${this.maxReconnectAttempts})`);
            
            setTimeout(async () => {
                try {
                    await this.connectWebSocket();
                } catch (error) {
                    console.error('Reconnection failed:', error);
                }
            }, this.reconnectDelay * this.reconnectAttempts);
        } else {
            console.error('Max reconnection attempts reached');
        }
    }

    private async testConnection(): Promise<void> {
        try {
            const response = await fetch(`${this.apiUrl}/health`);
            if (!response.ok) {
                throw new Error(`Health check failed: ${response.status}`);
            }
            
            const data = await response.json();
            console.log('Backend health check passed:', data);
            
        } catch (error) {
            console.error('Backend health check failed:', error);
            throw error;
        }
    }

    public async sendChatMessage(message: string): Promise<LunaResponse> {
        try {
            const response = await fetch(`${this.apiUrl}/api/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                    session_id: this.sessionId,
                    context: {
                        timestamp: new Date().toISOString(),
                        interaction_type: 'chat'
                    }
                })
            });

            if (!response.ok) {
                throw new Error(`Chat request failed: ${response.status}`);
            }

            const data = await response.json();
            return data;

        } catch (error) {
            console.error('Failed to send chat message:', error);
            throw error;
        }
    }

    public async sendVoiceCommand(command: string, voiceData?: any): Promise<LunaResponse> {
        try {
            const response = await fetch(`${this.apiUrl}/api/voice`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    command: command,
                    session_id: this.sessionId,
                    voice_data: voiceData || {}
                })
            });

            if (!response.ok) {
                throw new Error(`Voice request failed: ${response.status}`);
            }

            const data = await response.json();
            return data;

        } catch (error) {
            console.error('Failed to send voice command:', error);
            throw error;
        }
    }

    public async sendBHCSCommand(command: string, parameters?: any): Promise<LunaResponse> {
        try {
            const response = await fetch(`${this.apiUrl}/api/bhcs`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    command: command,
                    parameters: parameters || {},
                    session_id: this.sessionId
                })
            });

            if (!response.ok) {
                throw new Error(`BHCS request failed: ${response.status}`);
            }

            const data = await response.json();
            return data;

        } catch (error) {
            console.error('Failed to send BHCS command:', error);
            throw error;
        }
    }

    public async sendLearningRequest(query: string, context?: any): Promise<LunaResponse> {
        try {
            const response = await fetch(`${this.apiUrl}/api/learn`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    query: query,
                    context: context || {},
                    session_id: this.sessionId
                })
            });

            if (!response.ok) {
                throw new Error(`Learning request failed: ${response.status}`);
            }

            const data = await response.json();
            return data;

        } catch (error) {
            console.error('Failed to send learning request:', error);
            throw error;
        }
    }

    public async getSystemStatus(): Promise<SystemStatus> {
        try {
            const response = await fetch(`${this.apiUrl}/api/status`);
            
            if (!response.ok) {
                throw new Error(`Status request failed: ${response.status}`);
            }

            const data = await response.json();
            return data;

        } catch (error) {
            console.error('Failed to get system status:', error);
            throw error;
        }
    }

    public sendWebSocketMessage(type: string, data: any): void {
        if (this.websocket && this.websocket.readyState === WebSocket.OPEN) {
            const message = {
                type: type,
                ...data,
                timestamp: new Date().toISOString()
            };
            
            this.websocket.send(JSON.stringify(message));
        } else {
            console.warn('WebSocket not connected, cannot send message');
        }
    }

    public getSessionId(): string {
        return this.sessionId;
    }

    public isConnected(): boolean {
        return this.websocket?.readyState === WebSocket.OPEN;
    }

    public getConnectionState(): string {
        if (!this.websocket) return 'disconnected';
        
        switch (this.websocket.readyState) {
            case WebSocket.CONNECTING: return 'connecting';
            case WebSocket.OPEN: return 'connected';
            case WebSocket.CLOSING: return 'closing';
            case WebSocket.CLOSED: return 'disconnected';
            default: return 'unknown';
        }
    }
}
