/**
 * BHCS Dashboard UI - TypeScript Implementation
 * 
 * Human interface for visualization and control of the BHCS system.
 * Humans remain in control - no autonomous actions.
 */

import { BHCSController, SystemState } from '../core/controller';
import { ZoneState } from '../core/engine';
import { BioCoreEffect } from '../biocore/simulator';

export interface DashboardConfig {
    updateInterval: number;
    maxDataPoints: number;
    enableAnimations: boolean;
}

export class DashboardUI {
    private controller: BHCSController;
    private config: DashboardConfig;
    private chart: any; // Chart.js instance
    private isInitialized: boolean = false;

    constructor(controller: BHCSController, config?: Partial<DashboardConfig>) {
        this.controller = controller;
        this.config = {
            updateInterval: 1000,
            maxDataPoints: 50,
            enableAnimations: true,
            ...config
        };
    }

    /**
     * Initialize dashboard
     */
    public async initialize(): Promise<void> {
        console.log('🌐 Initializing BHCS Dashboard...');
        
        // Setup DOM elements
        this.setupDOM();
        
        // Initialize charts
        this.initializeCharts();
        
        // Setup event listeners
        this.setupEventListeners();
        
        // Start update loop
        this.startUpdateLoop();
        
        this.isInitialized = true;
        console.log('✅ BHCS Dashboard initialized');
    }

    /**
     * Setup DOM elements
     */
    private setupDOM(): void {
        // Create main dashboard structure
        const dashboard = document.createElement('div');
        dashboard.className = 'bhcs-dashboard';
        dashboard.innerHTML = `
            <div class="dashboard-header">
                <h1>🧠 BHCS - BioCore Homeostatic Civilization System</h1>
                <div class="system-status">
                    <div class="status-indicator" id="system-health">
                        <div class="status-dot"></div>
                        <span>System Health</span>
                    </div>
                    <div class="status-indicator" id="controller-status">
                        <div class="status-dot"></div>
                        <span>Controller</span>
                    </div>
                    <div class="status-indicator" id="biocore-status">
                        <div class="status-dot"></div>
                        <span>BioCore</span>
                    </div>
                </div>
            </div>
            
            <div class="dashboard-main">
                <div class="zones-panel">
                    <h2>🏙️ Zone States</h2>
                    <div class="zones-grid" id="zones-grid">
                        <!-- Zone cards will be inserted here -->
                    </div>
                </div>
                
                <div class="control-panel">
                    <h2>🎛️ BHCS Controls</h2>
                    <div class="control-form">
                        <div class="form-group">
                            <label for="zone-select">Target Zone:</label>
                            <select id="zone-select">
                                <option value="0">Zone 0</option>
                                <option value="1">Zone 1</option>
                                <option value="2">Zone 2</option>
                                <option value="3">Zone 3</option>
                                <option value="4">Zone 4</option>
                            </select>
                        </div>
                        
                        <div class="form-group">
                            <label for="plant-select">Plant:</label>
                            <select id="plant-select">
                                <option value="Ginkgo">Ginkgo</option>
                                <option value="Aloe">Aloe</option>
                                <option value="Turmeric">Turmeric</option>
                                <option value="Ginseng">Ginseng</option>
                                <option value="Ashwagandha">Ashwagandha</option>
                            </select>
                        </div>
                        
                        <div class="form-group">
                            <label for="drug-select">Drug:</label>
                            <select id="drug-select">
                                <option value="DrugA">DrugA</option>
                                <option value="DrugB">DrugB</option>
                                <option value="DrugC">DrugC</option>
                                <option value="DrugD">DrugD</option>
                                <option value="DrugE">DrugE</option>
                            </select>
                        </div>
                        
                        <div class="form-group">
                            <label for="synergy-input">Synergy (0-1):</label>
                            <input type="number" id="synergy-input" min="0" max="1" step="0.1" value="0.5">
                        </div>
                        
                        <div class="control-buttons">
                            <button id="apply-biocore" class="btn btn-primary">🌿 Apply BioCore</button>
                            <button id="optimize-zone" class="btn btn-secondary">🧠 Optimize Zone</button>
                            <button id="reset-system" class="btn btn-danger">🔄 Reset System</button>
                        </div>
                    </div>
                </div>
                
                <div class="analytics-panel">
                    <h2>📊 System Analytics</h2>
                    <div class="metrics-grid">
                        <div class="metric-card">
                            <h3>System Health</h3>
                            <div class="metric-value" id="system-health-value">0.00</div>
                        </div>
                        <div class="metric-card">
                            <h3>Average Activity</h3>
                            <div class="metric-value" id="avg-activity-value">0.00</div>
                        </div>
                        <div class="metric-card">
                            <h3>Active Effects</h3>
                            <div class="metric-value" id="active-effects-value">0</div>
                        </div>
                        <div class="metric-card">
                            <h3>Homeostatic Balance</h3>
                            <div class="metric-value" id="balance-value">0.00</div>
                        </div>
                    </div>
                    
                    <div class="chart-container">
                        <canvas id="performance-chart"></canvas>
                    </div>
                </div>
            </div>
            
            <div class="dashboard-footer">
                <p>🧠 BioCore Homeostatic Civilization System</p>
                <p>Research-grade simulation framework | Humans remain in control</p>
            </div>
        `;

        // Add to page
        document.body.appendChild(dashboard);
        
        // Add CSS styles
        this.addStyles();
    }

    /**
     * Add CSS styles
     */
    private addStyles(): void {
        const style = document.createElement('style');
        style.textContent = `
            .bhcs-dashboard {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 50%, #16213e 100%);
                color: white;
                min-height: 100vh;
                padding: 20px;
            }
            
            .dashboard-header {
                text-align: center;
                margin-bottom: 30px;
            }
            
            .dashboard-header h1 {
                font-size: 2.5rem;
                margin-bottom: 10px;
                background: linear-gradient(45deg, #4CAF50, #9C27B0);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }
            
            .system-status {
                display: flex;
                justify-content: center;
                gap: 20px;
                margin-top: 20px;
            }
            
            .status-indicator {
                display: flex;
                align-items: center;
                gap: 8px;
                padding: 10px 15px;
                background: rgba(255,255,255,0.1);
                border-radius: 20px;
            }
            
            .status-dot {
                width: 12px;
                height: 12px;
                border-radius: 50%;
                background: #4CAF50;
                animation: pulse 2s infinite;
            }
            
            .dashboard-main {
                display: grid;
                grid-template-columns: 1fr 1fr 1fr;
                gap: 20px;
                max-width: 1400px;
                margin: 0 auto;
            }
            
            .zones-panel, .control-panel, .analytics-panel {
                background: rgba(255,255,255,0.05);
                backdrop-filter: blur(10px);
                border-radius: 15px;
                padding: 20px;
                border: 1px solid rgba(255,255,255,0.1);
            }
            
            .zones-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
                gap: 10px;
                margin-top: 15px;
            }
            
            .zone-card {
                background: rgba(255,255,255,0.1);
                border-radius: 10px;
                padding: 15px;
                text-align: center;
                transition: transform 0.3s ease;
            }
            
            .zone-card:hover {
                transform: translateY(-2px);
            }
            
            .zone-state {
                display: inline-block;
                padding: 4px 8px;
                border-radius: 12px;
                font-size: 0.8rem;
                font-weight: 600;
                text-transform: uppercase;
                margin-bottom: 8px;
            }
            
            .state-calm { background: #4CAF50; }
            .state-overstimulated { background: #FF9800; }
            .state-emergent { background: #f44336; }
            .state-critical { background: #9C27B0; }
            
            .activity-bar {
                width: 100%;
                height: 8px;
                background: rgba(255,255,255,0.2);
                border-radius: 4px;
                overflow: hidden;
                margin: 8px 0;
            }
            
            .activity-fill {
                height: 100%;
                background: linear-gradient(90deg, #4CAF50, #8BC34A);
                transition: width 0.5s ease;
            }
            
            .control-form {
                display: grid;
                gap: 15px;
            }
            
            .form-group {
                display: flex;
                flex-direction: column;
                gap: 5px;
            }
            
            .form-group label {
                font-weight: 600;
                opacity: 0.9;
            }
            
            .form-group select,
            .form-group input {
                padding: 8px;
                border: 1px solid rgba(255,255,255,0.3);
                border-radius: 6px;
                background: rgba(255,255,255,0.1);
                color: white;
                font-size: 0.9rem;
            }
            
            .control-buttons {
                display: flex;
                gap: 10px;
                margin-top: 20px;
            }
            
            .btn {
                padding: 10px 20px;
                border: none;
                border-radius: 8px;
                font-size: 0.9rem;
                font-weight: 600;
                cursor: pointer;
                transition: transform 0.3s ease;
            }
            
            .btn-primary {
                background: linear-gradient(135deg, #4CAF50, #45a049);
                color: white;
            }
            
            .btn-secondary {
                background: linear-gradient(135deg, #9C27B0, #673AB7);
                color: white;
            }
            
            .btn-danger {
                background: linear-gradient(135deg, #f44336, #d32f2f);
                color: white;
            }
            
            .btn:hover {
                transform: translateY(-2px);
            }
            
            .metrics-grid {
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 15px;
                margin-bottom: 20px;
            }
            
            .metric-card {
                background: rgba(255,255,255,0.1);
                border-radius: 10px;
                padding: 15px;
                text-align: center;
            }
            
            .metric-card h3 {
                font-size: 0.9rem;
                opacity: 0.8;
                margin-bottom: 8px;
            }
            
            .metric-value {
                font-size: 1.8rem;
                font-weight: bold;
                color: #FFD700;
            }
            
            .chart-container {
                background: rgba(255,255,255,0.05);
                border-radius: 10px;
                padding: 15px;
                height: 300px;
            }
            
            .dashboard-footer {
                text-align: center;
                margin-top: 30px;
                opacity: 0.7;
            }
            
            @keyframes pulse {
                0% { opacity: 1; }
                50% { opacity: 0.5; }
                100% { opacity: 1; }
            }
        `;
        
        document.head.appendChild(style);
    }

    /**
     * Initialize charts
     */
    private initializeCharts(): void {
        const canvas = document.getElementById('performance-chart') as HTMLCanvasElement;
        if (!canvas) return;

        // Simple chart implementation (would use Chart.js in production)
        this.chart = {
            data: {
                labels: [],
                datasets: [
                    { label: 'System Health', data: [], color: '#4CAF50' },
                    { label: 'Average Activity', data: [], color: '#9C27B0' },
                    { label: 'Homeostatic Balance', data: [], color: '#FF9800' }
                ]
            },
            update: (data: any) => {
                // Chart update logic would go here
                console.log('Chart updated:', data);
            }
        };
    }

    /**
     * Setup event listeners
     */
    private setupEventListeners(): void {
        // Apply BioCore button
        const applyButton = document.getElementById('apply-biocore');
        if (applyButton) {
            applyButton.addEventListener('click', () => this.handleApplyBioCore());
        }

        // Optimize zone button
        const optimizeButton = document.getElementById('optimize-zone');
        if (optimizeButton) {
            optimizeButton.addEventListener('click', () => this.handleOptimizeZone());
        }

        // Reset system button
        const resetButton = document.getElementById('reset-system');
        if (resetButton) {
            resetButton.addEventListener('click', () => this.handleResetSystem());
        }
    }

    /**
     * Handle BioCore application
     */
    private async handleApplyBioCore(): Promise<void> {
        const zoneSelect = document.getElementById('zone-select') as HTMLSelectElement;
        const plantSelect = document.getElementById('plant-select') as HTMLSelectElement;
        const drugSelect = document.getElementById('drug-select') as HTMLSelectElement;
        const synergyInput = document.getElementById('synergy-input') as HTMLInputElement;

        const zoneId = parseInt(zoneSelect.value);
        const plant = plantSelect.value;
        const drug = drugSelect.value;
        const synergy = parseFloat(synergyInput.value);

        try {
            const success = await this.controller.applyBioCoreEffect(zoneId, plant, drug, synergy);
            
            if (success) {
                this.showNotification(`BioCore effect applied to Zone ${zoneId}`, 'success');
            } else {
                this.showNotification('Failed to apply BioCore effect', 'error');
            }
        } catch (error) {
            this.showNotification('Error applying BioCore effect', 'error');
        }
    }

    /**
     * Handle zone optimization
     */
    private async handleOptimizeZone(): Promise<void> {
        const zoneSelect = document.getElementById('zone-select') as HTMLSelectElement;
        const zoneId = parseInt(zoneSelect.value);

        const recommendation = this.controller.getZoneRecommendations(zoneId);
        
        if (recommendation) {
            this.showNotification(`Optimal BioCore: ${recommendation.bioCoreRecommendation?.plant} + ${recommendation.bioCoreRecommendation?.drug}`, 'info');
        }
    }

    /**
     * Handle system reset
     */
    private handleResetSystem(): void {
        if (confirm('Are you sure you want to reset the BHCS system?')) {
            this.controller.reset();
            this.showNotification('BHCS System reset', 'warning');
        }
    }

    /**
     * Start update loop
     */
    private startUpdateLoop(): void {
        setInterval(async () => {
            await this.render();
        }, this.config.updateInterval);
    }

    /**
     * Render dashboard
     */
    public async render(): Promise<void> {
        if (!this.isInitialized) return;

        try {
            // Get current system state
            const systemState = this.controller.getSystemState();
            
            // Update zones display
            this.renderZones(systemState.zones);
            
            // Update metrics
            this.renderMetrics(systemState);
            
            // Update chart
            this.renderChart(systemState);
            
            // Update status indicators
            this.updateStatusIndicators(systemState);
            
        } catch (error) {
            console.error('❌ Dashboard render failed:', error);
        }
    }

    /**
     * Render zone cards
     */
    private renderZones(zones: ZoneState[]): void {
        const zonesGrid = document.getElementById('zones-grid');
        if (!zonesGrid) return;

        zonesGrid.innerHTML = '';

        zones.forEach(zone => {
            const zoneCard = document.createElement('div');
            zoneCard.className = 'zone-card';
            zoneCard.innerHTML = `
                <div class="zone-state state-${zone.state.toLowerCase()}">${zone.state}</div>
                <div class="activity-bar">
                    <div class="activity-fill" style="width: ${zone.activity * 100}%"></div>
                </div>
                <div style="margin-top: 8px; font-size: 0.9rem;">
                    Zone ${zone.id}: ${zone.activity.toFixed(3)}
                </div>
            `;
            zonesGrid.appendChild(zoneCard);
        });
    }

    /**
     * Render system metrics
     */
    private renderMetrics(systemState: SystemState): void {
        const systemHealthValue = document.getElementById('system-health-value');
        const avgActivityValue = document.getElementById('avg-activity-value');
        const activeEffectsValue = document.getElementById('active-effects-value');
        const balanceValue = document.getElementById('balance-value');

        if (systemHealthValue) {
            systemHealthValue.textContent = systemState.systemHealth.toFixed(3);
        }

        if (avgActivityValue) {
            const avgActivity = systemState.zones.reduce((sum, zone) => sum + zone.activity, 0) / systemState.zones.length;
            avgActivityValue.textContent = avgActivity.toFixed(3);
        }

        if (activeEffectsValue) {
            activeEffectsValue.textContent = systemState.bioCoreEffects.length.toString();
        }

        if (balanceValue) {
            const balance = Math.abs(0.5 - (systemState.zones.reduce((sum, zone) => sum + zone.activity, 0) / systemState.zones.length));
            balanceValue.textContent = balance.toFixed(3);
        }
    }

    /**
     * Render chart
     */
    private renderChart(systemState: SystemState): void {
        if (!this.chart) return;

        const avgActivity = systemState.zones.reduce((sum, zone) => sum + zone.activity, 0) / systemState.zones.length;
        
        // Add data point
        this.chart.data.labels.push(new Date().toLocaleTimeString());
        this.chart.data.datasets[0].data.push(systemState.systemHealth);
        this.chart.data.datasets[1].data.push(avgActivity);
        this.chart.data.datasets[2].data.push(Math.abs(0.5 - avgActivity));
    }

    /**
     * Update status indicators
     */
    private updateStatusIndicators(systemState: SystemState): void {
        const systemHealth = document.getElementById('system-health');
        const controllerStatus = document.getElementById('controller-status');
        const biocoreStatus = document.getElementById('biocore-status');

        if (systemHealth) {
            const dot = systemHealth.querySelector('.status-dot') as HTMLElement;
            dot.style.background = systemState.systemHealth > 0.7 ? '#4CAF50' : 
                                   systemState.systemHealth > 0.4 ? '#FF9800' : '#f44336';
        }

        // Update other indicators similarly
    }

    /**
     * Show notification
     */
    private showNotification(message: string, type: 'success' | 'error' | 'warning' | 'info'): void {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 20px;
            border-radius: 8px;
            color: white;
            font-weight: 600;
            z-index: 1000;
            animation: slideIn 0.3s ease;
        `;

        // Set background based on type
        const colors = {
            success: '#4CAF50',
            error: '#f44336',
            warning: '#FF9800',
            info: '#2196F3'
        };
        notification.style.background = colors[type];

        document.body.appendChild(notification);

        // Remove after 3 seconds
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 3000);
    }
}
