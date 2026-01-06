/**
 * BHCS Controller - Central Coordination Logic
 * 
 * Coordinates between Homeostatic Engine, BioCore Simulator,
 * and Dashboard UI. Maintains system-wide state.
 */

import { HomeostaticEngine, ZoneState } from './engine';
import { BioCoreSimulator, BioCoreEffect } from '../biocore/simulator';

export interface ControllerConfig {
    apiEndpoint: string;
    updateInterval: number;
    enableLogging: boolean;
}

export interface SystemState {
    zones: ZoneState[];
    bioCoreEffects: BioCoreEffect[];
    systemHealth: number;
    lastUpdate: number;
}

export class BHCSController {
    private engine: HomeostaticEngine;
    private biocore: BioCoreSimulator;
    private config: ControllerConfig;
    private systemState: SystemState;

    constructor(engine: HomeostaticEngine, biocore: BioCoreSimulator, config?: Partial<ControllerConfig>) {
        this.engine = engine;
        this.biocore = biocore;
        this.config = {
            apiEndpoint: 'http://localhost:3030',
            updateInterval: 1000,
            enableLogging: true,
            ...config
        };

        this.systemState = {
            zones: [],
            bioCoreEffects: [],
            systemHealth: 1.0,
            lastUpdate: Date.now()
        };
    }

    /**
     * Initialize the controller
     */
    public async initialize(): Promise<void> {
        if (this.config.enableLogging) {
            console.log('🎛️ BHCS Controller: Initializing...');
        }

        // Start system monitoring
        this.startSystemMonitoring();
    }

    /**
     * Main update loop
     */
    public async update(): Promise<void> {
        try {
            // 1. Get current zone states from engine
            const zones = this.engine.getZoneStates();
            
            // 2. Update BioCore simulations
            await this.biocore.update(zones);
            
            // 3. Calculate system health
            const systemHealth = this.calculateSystemHealth(zones);
            
            // 4. Update system state
            this.systemState = {
                zones,
                bioCoreEffects: this.biocore.getActiveEffects(),
                systemHealth,
                lastUpdate: Date.now()
            };

            if (this.config.enableLogging) {
                console.log('🔄 BHCS Controller updated', {
                    zones: zones.length,
                    health: systemHealth.toFixed(3),
                    effects: this.systemState.bioCoreEffects.length
                });
            }

        } catch (error) {
            console.error('❌ Controller update failed:', error);
        }
    }

    /**
     * Apply BioCore effect to specific zone
     */
    public async applyBioCoreEffect(zoneId: number, plant: string, drug: string, synergy: number): Promise<boolean> {
        try {
            if (this.config.enableLogging) {
                console.log(`🌿 Applying BioCore effect: Zone ${zoneId}, ${plant} + ${drug}, synergy ${synergy}`);
            }

            // 1. Calculate effect magnitude
            const effect = this.biocore.calculateEffect(plant, drug, synergy);
            
            // 2. Apply to homeostatic engine
            this.engine.applyInfluence(zoneId, effect.magnitude);
            
            // 3. Record effect
            this.biocore.recordEffect(zoneId, plant, drug, synergy, effect);
            
            return true;

        } catch (error) {
            console.error('❌ Failed to apply BioCore effect:', error);
            return false;
        }
    }

    /**
     * Get optimal BioCore recommendation for zone
     */
    public getOptimalBioCore(zoneId: number): BioCoreEffect | null {
        const zone = this.engine.getZoneState(zoneId);
        if (!zone) return null;

        return this.biocore.getOptimalForZone(zone);
    }

    /**
     * Calculate overall system health
     */
    private calculateSystemHealth(zones: ZoneState[]): number {
        if (zones.length === 0) return 0;

        // Factor in activity balance, state distribution, and stability
        const avgActivity = zones.reduce((sum, zone) => sum + zone.activity, 0) / zones.length;
        const targetActivity = 0.5; // Homeostatic target
        
        // Activity balance score (closer to target = higher score)
        const balanceScore = 1.0 - Math.abs(avgActivity - targetActivity);
        
        // State distribution score (prefer calm zones)
        const calmZones = zones.filter(z => z.state === 'CALM').length;
        const distributionScore = calmZones / zones.length;
        
        // Stability score (less variation = higher score)
        const activities = zones.map(z => z.activity);
        const variance = activities.reduce((sum, activity) => {
            return sum + Math.pow(activity - avgActivity, 2);
        }, 0) / zones.length;
        const stabilityScore = 1.0 - Math.min(variance, 1.0);
        
        // Weighted combination
        return (balanceScore * 0.4) + (distributionScore * 0.3) + (stabilityScore * 0.3);
    }

    /**
     * Get current system state
     */
    public getSystemState(): SystemState {
        return { ...this.systemState };
    }

    /**
     * Get zone-specific recommendations
     */
    public getZoneRecommendations(zoneId: number): any {
        const zone = this.engine.getZoneState(zoneId);
        if (!zone) return null;

        const bioCoreRec = this.getOptimalBioCore(zoneId);
        const systemMetrics = this.engine.getSystemMetrics();

        return {
            zoneId,
            currentState: zone.state,
            activity: zone.activity,
            bioCoreRecommendation: bioCoreRec,
            systemBalance: systemMetrics.homeostaticBalance,
            suggestedAction: this.suggestAction(zone)
        };
    }

    /**
     * Suggest action based on zone state
     */
    private suggestAction(zone: ZoneState): string {
        switch (zone.state) {
            case 'CALM':
                return 'Maintain current state - optimal balance achieved';
            case 'OVERSTIMULATED':
                return 'Apply calming BioCore effect or reduce stimulation';
            case 'EMERGENT':
                return 'Monitor closely - prepare regulation if needed';
            case 'CRITICAL':
                return 'Apply strong regulation immediately';
            default:
                return 'Monitor zone activity';
        }
    }

    /**
     * Start system health monitoring
     */
    private startSystemMonitoring(): void {
        setInterval(() => {
            const health = this.systemState.systemHealth;
            
            if (health < 0.3) {
                console.warn('⚠️ BHCS System Health Critical:', health);
            } else if (health < 0.6) {
                console.warn('⚠️ BHCS System Health Warning:', health);
            }
        }, 5000); // Check every 5 seconds
    }

    /**
     * Reset controller state
     */
    public reset(): void {
        this.engine.reset();
        this.biocore.reset();
        this.systemState = {
            zones: [],
            bioCoreEffects: [],
            systemHealth: 1.0,
            lastUpdate: Date.now()
        };
        
        console.log('🔄 BHCS Controller reset');
    }
}
