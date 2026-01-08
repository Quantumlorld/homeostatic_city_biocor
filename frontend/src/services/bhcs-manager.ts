// 🧬 LunaBeyond AI BHCS Manager
// TypeScript service for BHCS system management

import { LunaClient } from './luna-client';

interface BHCSZone {
    id: number;
    activity: number;
    state: 'CALM' | 'OVERSTIMULATED' | 'EMERGENT' | 'CRITICAL';
    health: number;
    lastUpdate: string;
}

interface BHCSStatus {
    systemHealth: number;
    zones: BHCSZone[];
    activeZones: number;
    riskLevel: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
    lastUpdate: string;
}

interface BHCSAlert {
    type: 'warning' | 'critical' | 'info';
    message: string;
    zone?: number;
    timestamp: string;
}

export class BHCSManager {
    private lunaClient: LunaClient;
    private eventBus: any;
    private status: BHCSStatus;
    private alerts: BHCSAlert[];
    private monitoringInterval: number | null = null;
    private isMonitoring: boolean = false;

    constructor(lunaClient: LunaClient, eventBus: any) {
        this.lunaClient = lunaClient;
        this.eventBus = eventBus;
        
        this.status = {
            systemHealth: 0.8,
            zones: [],
            activeZones: 0,
            riskLevel: 'LOW',
            lastUpdate: new Date().toISOString()
        };
        
        this.alerts = [];
        this.initializeZones();
    }

    private initializeZones(): void {
        // Initialize 5 zones
        for (let i = 0; i < 5; i++) {
            this.status.zones.push({
                id: i,
                activity: Math.random() * 0.3,
                state: 'CALM',
                health: 0.8 + Math.random() * 0.2,
                lastUpdate: new Date().toISOString()
            });
        }
        
        this.updateActiveZones();
    }

    public async startMonitoring(): Promise<void> {
        if (this.isMonitoring) {
            console.warn('BHCS monitoring already started');
            return;
        }

        try {
            this.isMonitoring = true;
            
            // Get initial status
            await this.updateStatus();
            
            // Start periodic monitoring
            this.monitoringInterval = window.setInterval(async () => {
                await this.updateStatus();
            }, 5000); // Update every 5 seconds
            
            console.log('BHCS monitoring started');
            
        } catch (error) {
            console.error('Failed to start BHCS monitoring:', error);
            this.isMonitoring = false;
            throw error;
        }
    }

    public async stopMonitoring(): Promise<void> {
        if (!this.isMonitoring) {
            return;
        }

        try {
            this.isMonitoring = false;
            
            if (this.monitoringInterval) {
                clearInterval(this.monitoringInterval);
                this.monitoringInterval = null;
            }
            
            console.log('BHCS monitoring stopped');
            
        } catch (error) {
            console.error('Error stopping BHCS monitoring:', error);
        }
    }

    private async updateStatus(): Promise<void> {
        try {
            // Get status from backend
            const backendStatus = await this.lunaClient.getSystemStatus();
            
            // Update local status
            this.status.systemHealth = backendStatus.system_health;
            this.status.lastUpdate = backendStatus.timestamp;
            
            // Update zones
            if (backendStatus.zones) {
                backendStatus.zones.forEach((zone: any, index: number) => {
                    if (index < this.status.zones.length) {
                        this.status.zones[index] = {
                            ...this.status.zones[index],
                            activity: zone.activity,
                            state: zone.state,
                            health: this.calculateZoneHealth(zone),
                            lastUpdate: new Date().toISOString()
                        };
                    }
                });
            }
            
            this.updateActiveZones();
            this.updateRiskLevel();
            this.checkForAlerts();
            
            // Emit status update
            this.eventBus.emit('bhcs-update', this.getStatus());
            
        } catch (error) {
            console.error('Failed to update BHCS status:', error);
            
            // Simulate local updates if backend is unavailable
            this.simulateStatusUpdate();
        }
    }

    private simulateStatusUpdate(): void {
        // Simulate zone activity changes
        this.status.zones.forEach(zone => {
            const change = (Math.random() - 0.5) * 0.1;
            zone.activity = Math.max(0, Math.min(1, zone.activity + change));
            zone.state = this.determineZoneState(zone.activity);
            zone.health = this.calculateZoneHealth(zone);
            zone.lastUpdate = new Date().toISOString();
        });
        
        this.status.systemHealth = this.calculateSystemHealth();
        this.status.lastUpdate = new Date().toISOString();
        
        this.updateActiveZones();
        this.updateRiskLevel();
        this.checkForAlerts();
        
        this.eventBus.emit('bhcs-update', this.getStatus());
    }

    private determineZoneState(activity: number): 'CALM' | 'OVERSTIMULATED' | 'EMERGENT' | 'CRITICAL' {
        if (activity < 0.4) return 'CALM';
        if (activity < 0.7) return 'OVERSTIMULATED';
        if (activity < 0.9) return 'EMERGENT';
        return 'CRITICAL';
    }

    private calculateZoneHealth(zone: any): number {
        const activityHealth = 1 - Math.abs(zone.activity - 0.3);
        const stateHealth = zone.state === 'CALM' ? 1 : 0.8;
        return (activityHealth + stateHealth) / 2;
    }

    private calculateSystemHealth(): number {
        const zoneHealths = this.status.zones.map(zone => zone.health);
        return zoneHealths.reduce((sum, health) => sum + health, 0) / zoneHealths.length;
    }

    private updateActiveZones(): void {
        this.status.activeZones = this.status.zones.filter(zone => zone.activity > 0.2).length;
    }

    private updateRiskLevel(): void {
        const criticalZones = this.status.zones.filter(zone => zone.state === 'CRITICAL').length;
        const emergentZones = this.status.zones.filter(zone => zone.state === 'EMERGENT').length;
        
        if (criticalZones > 0) {
            this.status.riskLevel = 'CRITICAL';
        } else if (emergentZones > 2) {
            this.status.riskLevel = 'HIGH';
        } else if (emergentZones > 0) {
            this.status.riskLevel = 'MEDIUM';
        } else {
            this.status.riskLevel = 'LOW';
        }
    }

    private checkForAlerts(): void {
        const newAlerts: BHCSAlert[] = [];
        
        this.status.zones.forEach(zone => {
            if (zone.state === 'CRITICAL') {
                newAlerts.push({
                    type: 'critical',
                    message: `Zone ${zone.id} is in critical state!`,
                    zone: zone.id,
                    timestamp: new Date().toISOString()
                });
            } else if (zone.state === 'EMERGENT' && zone.activity > 0.8) {
                newAlerts.push({
                    type: 'warning',
                    message: `Zone ${zone.id} shows high activity levels`,
                    zone: zone.id,
                    timestamp: new Date().toISOString()
                });
            }
        });
        
        if (this.status.systemHealth < 0.5) {
            newAlerts.push({
                type: 'critical',
                message: 'System health is below 50%',
                timestamp: new Date().toISOString()
            });
        }
        
        // Emit new alerts
        newAlerts.forEach(alert => {
            this.alerts.push(alert);
            this.eventBus.emit('bhcs-alert', alert);
        });
        
        // Keep only last 50 alerts
        if (this.alerts.length > 50) {
            this.alerts = this.alerts.slice(-50);
        }
    }

    public async applyBioCore(zoneId?: number): Promise<void> {
        try {
            const parameters = zoneId !== undefined ? { zone_id: zoneId } : {};
            
            const response = await this.lunaClient.sendBHCSCommand('apply_biocore', parameters);
            
            // Update local status
            if (zoneId !== undefined && zoneId < this.status.zones.length) {
                const zone = this.status.zones[zoneId];
                zone.activity = Math.max(0.1, zone.activity - 0.3);
                zone.state = this.determineZoneState(zone.activity);
                zone.health = Math.min(1, zone.health + 0.2);
                zone.lastUpdate = new Date().toISOString();
            }
            
            this.status.systemHealth = this.calculateSystemHealth();
            this.updateActiveZones();
            this.updateRiskLevel();
            
            this.eventBus.emit('bhcs-update', this.getStatus());
            
            console.log('BioCore applied successfully');
            
        } catch (error) {
            console.error('Failed to apply BioCore:', error);
            throw error;
        }
    }

    public async optimizeSystem(): Promise<void> {
        try {
            const response = await this.lunaClient.sendBHCSCommand('optimize');
            
            // Update local status
            this.status.zones.forEach(zone => {
                if (zone.activity > 0.5) {
                    zone.activity = zone.activity * 0.8;
                    zone.state = this.determineZoneState(zone.activity);
                    zone.health = Math.min(1, zone.health + 0.1);
                    zone.lastUpdate = new Date().toISOString();
                }
            });
            
            this.status.systemHealth = this.calculateSystemHealth();
            this.updateActiveZones();
            this.updateRiskLevel();
            
            this.eventBus.emit('bhcs-update', this.getStatus());
            
            console.log('System optimization completed');
            
        } catch (error) {
            console.error('Failed to optimize system:', error);
            throw error;
        }
    }

    public async getPredictions(): Promise<any> {
        try {
            const response = await this.lunaClient.sendBHCSCommand('predict');
            return response.response;
        } catch (error) {
            console.error('Failed to get predictions:', error);
            throw error;
        }
    }

    public getStatus(): BHCSStatus {
        return { ...this.status };
    }

    public getAlerts(): BHCSAlert[] {
        return [...this.alerts];
    }

    public getZone(zoneId: number): BHCSZone | undefined {
        return this.status.zones.find(zone => zone.id === zoneId);
    }

    public isMonitoringActive(): boolean {
        return this.isMonitoring;
    }
}
