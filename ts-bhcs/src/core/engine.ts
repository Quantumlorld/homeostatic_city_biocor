/**
 * Homeostatic Engine - Core Regulation Logic
 * 
 * Implements the fundamental homeostatic equation:
 * error = target - current
 * adjustment = learning_rate * error
 * new_state = current + adjustment
 */

export interface ZoneState {
    id: number;
    activity: number;
    target: number;
    state: 'CALM' | 'OVERSTIMULATED' | 'EMERGENT' | 'CRITICAL';
    lastUpdate: number;
}

export interface HomeostaticConfig {
    targetCalmness: number;
    learningRate: number;
    zones: number;
    updateInterval: number;
}

export class HomeostaticEngine {
    private zones: Map<number, ZoneState>;
    private config: HomeostaticConfig;
    private isRunning: boolean = false;

    constructor(config?: Partial<HomeostaticConfig>) {
        this.config = {
            targetCalmness: 0.5,
            learningRate: 0.02,
            zones: 5,
            updateInterval: 1000,
            ...config
        };

        this.zones = new Map();
        this.initializeZones();
    }

    /**
     * Initialize all zones with default states
     */
    private initializeZones(): void {
        for (let i = 0; i < this.config.zones; i++) {
            const zone: ZoneState = {
                id: i,
                activity: Math.random() * 0.6 + 0.2, // Random initial activity
                target: this.config.targetCalmness,
                state: this.calculateState(0.5),
                lastUpdate: Date.now()
            };
            this.zones.set(i, zone);
        }
    }

    /**
     * Initialize the engine
     */
    public async initialize(): Promise<void> {
        console.log('🦀 Homeostatic Engine: Zones initialized');
        this.isRunning = true;
    }

    /**
     * Main update loop - applies homeostatic regulation
     */
    public async update(): Promise<void> {
        if (!this.isRunning) return;

        const now = Date.now();
        
        for (const [id, zone] of this.zones) {
            // Apply homeostatic update equation
            const error = zone.target - zone.activity;
            const adjustment = this.config.learningRate * error;
            const newActivity = Math.max(0, Math.min(1, zone.activity + adjustment));
            
            // Update zone state
            zone.activity = newActivity;
            zone.state = this.calculateState(newActivity);
            zone.lastUpdate = now;
            
            this.zones.set(id, zone);
        }
    }

    /**
     * Calculate zone state based on activity level
     */
    private calculateState(activity: number): ZoneState['state'] {
        if (activity < 0.4) return 'CALM';
        if (activity < 0.7) return 'OVERSTIMULATED';
        if (activity < 0.9) return 'EMERGENT';
        return 'CRITICAL';
    }

    /**
     * Apply external influence to a zone
     */
    public applyInfluence(zoneId: number, influence: number): void {
        const zone = this.zones.get(zoneId);
        if (!zone) return;

        zone.activity = Math.max(0, Math.min(1, zone.activity + influence));
        zone.state = this.calculateState(zone.activity);
        zone.lastUpdate = Date.now();
        
        this.zones.set(zoneId, zone);
        console.log(`🎛️ Applied influence ${influence.toFixed(3)} to Zone ${zoneId}`);
    }

    /**
     * Get current state of all zones
     */
    public getZoneStates(): ZoneState[] {
        return Array.from(this.zones.values());
    }

    /**
     * Get specific zone state
     */
    public getZoneState(zoneId: number): ZoneState | undefined {
        return this.zones.get(zoneId);
    }

    /**
     * Get system-wide metrics
     */
    public getSystemMetrics() {
        const zones = Array.from(this.zones.values());
        const avgActivity = zones.reduce((sum, zone) => sum + zone.activity, 0) / zones.length;
        const stateDistribution = zones.reduce((acc, zone) => {
            acc[zone.state] = (acc[zone.state] || 0) + 1;
            return acc;
        }, {} as Record<string, number>);

        return {
            averageActivity: avgActivity,
            totalZones: zones.length,
            stateDistribution,
            homeostaticBalance: Math.abs(avgActivity - this.config.targetCalmness),
            timestamp: Date.now()
        };
    }

    /**
     * Reset engine to initial state
     */
    public reset(): void {
        this.zones.clear();
        this.initializeZones();
        console.log('🔄 Homeostatic Engine reset to initial state');
    }

    /**
     * Stop the engine
     */
    public stop(): void {
        this.isRunning = false;
        console.log('🛑 Homeostatic Engine stopped');
    }
}
