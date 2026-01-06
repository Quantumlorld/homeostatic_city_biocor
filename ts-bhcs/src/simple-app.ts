/**
 * Simple BHCS Application - Working Version
 * BioCore Homeostatic Civilization System
 */

// Simple interfaces
interface Zone {
    id: number;
    activity: number;
    state: 'CALM' | 'OVERSTIMULATED' | 'EMERGENT' | 'CRITICAL';
}

interface BioCoreEffect {
    plant: string;
    drug: string;
    synergy: number;
    magnitude: number;
}

// Simple application class
class SimpleBHCS {
    private zones: Zone[];
    private effects: BioCoreEffect[];
    private isRunning: boolean = false;

    constructor() {
        console.log('🧠 BHCS: Simple Homeostatic System Initializing...');
        this.zones = [];
        this.effects = [];
        this.initializeZones();
    }

    private initializeZones(): void {
        for (let i = 0; i < 5; i++) {
            this.zones.push({
                id: i,
                activity: Math.random() * 0.6 + 0.2,
                state: 'CALM'
            });
        }
    }

    public start(): void {
        console.log('🚀 Starting Simple BHCS...');
        this.isRunning = true;
        this.createUI();
        this.startUpdateLoop();
    }

    private createUI(): void {
        // Create dashboard
        const dashboard = document.createElement('div');
        dashboard.innerHTML = `
            <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 50%, #16213e 100%); color: white; min-height: 100vh; padding: 20px;">
                <div style="text-align: center; margin-bottom: 30px;">
                    <h1 style="font-size: 2.5rem; margin-bottom: 10px; background: linear-gradient(45deg, #4CAF50, #9C27B0); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">🧠 BHCS - Simple Homeostatic System</h1>
                    <div style="display: flex; justify-content: center; gap: 20px; margin-top: 10px;">
                        <div style="padding: 10px 20px; background: rgba(255,255,255,0.1); border-radius: 20px;">
                            <div style="width: 12px; height: 12px; background: #4CAF50; border-radius: 50%; display: inline-block; margin-right: 8px;"></div>
                            <span>System Active</span>
                        </div>
                        <div style="padding: 10px 20px; background: rgba(255,255,255,0.1); border-radius: 20px;">
                            <div style="width: 12px; height: 12px; background: #9C27B0; border-radius: 50%; display: inline-block; margin-right: 8px;"></div>
                            <span>BioCore Ready</span>
                        </div>
                        <div style="padding: 10px 20px; background: rgba(255,255,255,0.1); border-radius: 20px;">
                            <div style="width: 12px; height: 12px; background: #FF9800; border-radius: 50%; display: inline-block; margin-right: 8px;"></div>
                            <span>Dashboard Live</span>
                        </div>
                    </div>
                </div>
                
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; max-width: 1200px; margin: 0 auto;">
                    <div style="background: rgba(255,255,255,0.05); backdrop-filter: blur(10px); border-radius: 15px; padding: 20px; border: 1px solid rgba(255,255,255,0.1);">
                        <h2 style="color: #64B5F6; margin-bottom: 15px;">🏙️ Zone States</h2>
                        <div id="zones-container" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 10px;">
                            <!-- Zones will be inserted here -->
                        </div>
                    </div>
                    
                    <div style="background: rgba(255,255,255,0.05); backdrop-filter: blur(10px); border-radius: 15px; padding: 20px; border: 1px solid rgba(255,255,255,0.1);">
                        <h2 style="color: #64B5F6; margin-bottom: 15px;">🎛️ BHCS Controls</h2>
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 15px;">
                            <div>
                                <label style="display: block; margin-bottom: 5px; font-weight: 600;">Target Zone:</label>
                                <select id="zone-select" style="width: 100%; padding: 8px; border: 1px solid rgba(255,255,255,0.3); border-radius: 6px; background: rgba(255,255,255,0.1); color: white;">
                                    <option value="0">Zone 0</option>
                                    <option value="1">Zone 1</option>
                                    <option value="2">Zone 2</option>
                                    <option value="3">Zone 3</option>
                                    <option value="4">Zone 4</option>
                                </select>
                            </div>
                            <div>
                                <label style="display: block; margin-bottom: 5px; font-weight: 600;">Plant:</label>
                                <select id="plant-select" style="width: 100%; padding: 8px; border: 1px solid rgba(255,255,255,0.3); border-radius: 6px; background: rgba(255,255,255,0.1); color: white;">
                                    <option value="Ginkgo">Ginkgo</option>
                                    <option value="Aloe">Aloe</option>
                                    <option value="Turmeric">Turmeric</option>
                                    <option value="Ginseng">Ginseng</option>
                                    <option value="Ashwagandha">Ashwagandha</option>
                                </select>
                            </div>
                        </div>
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 15px;">
                            <div>
                                <label style="display: block; margin-bottom: 5px; font-weight: 600;">Drug:</label>
                                <select id="drug-select" style="width: 100%; padding: 8px; border: 1px solid rgba(255,255,255,0.3); border-radius: 6px; background: rgba(255,255,255,0.1); color: white;">
                                    <option value="DrugA">DrugA</option>
                                    <option value="DrugB">DrugB</option>
                                    <option value="DrugC">DrugC</option>
                                    <option value="DrugD">DrugD</option>
                                    <option value="DrugE">DrugE</option>
                                </select>
                            </div>
                            <div>
                                <label style="display: block; margin-bottom: 5px; font-weight: 600;">Synergy:</label>
                                <input type="number" id="synergy-input" min="0" max="1" step="0.1" value="0.5" style="width: 100%; padding: 8px; border: 1px solid rgba(255,255,255,0.3); border-radius: 6px; background: rgba(255,255,255,0.1); color: white;">
                            </div>
                        </div>
                        <div style="display: flex; gap: 10px; margin-top: 15px;">
                            <button id="apply-biocore" style="padding: 10px 20px; border: none; border-radius: 8px; font-size: 0.9rem; font-weight: 600; cursor: pointer; background: linear-gradient(135deg, #4CAF50, #45a049); color: white;">🌿 Apply BioCore</button>
                            <button id="optimize-system" style="padding: 10px 20px; border: none; border-radius: 8px; font-size: 0.9rem; font-weight: 600; cursor: pointer; background: linear-gradient(135deg, #9C27B0, #673AB7); color: white;">🧠 Optimize All</button>
                            <button id="reset-system" style="padding: 10px 20px; border: none; border-radius: 8px; font-size: 0.9rem; font-weight: 600; cursor: pointer; background: linear-gradient(135deg, #f44336, #d32f2f); color: white;">🔄 Reset System</button>
                        </div>
                    </div>
                    
                    <div style="background: rgba(255,255,255,0.05); backdrop-filter: blur(10px); border-radius: 15px; padding: 20px; border: 1px solid rgba(255,255,255,0.1);">
                        <h2 style="color: #64B5F6; margin-bottom: 15px;">📊 System Metrics</h2>
                        <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px;">
                            <div style="background: rgba(255,255,255,0.1); border-radius: 8px; padding: 10px; text-align: center;">
                                <div style="font-size: 0.8rem; opacity: 0.8; margin-bottom: 5px;">Average Activity</div>
                                <div id="avg-activity" style="font-size: 1.5rem; font-weight: bold; color: #FFD700;">0.00</div>
                            </div>
                            <div style="background: rgba(255,255,255,0.1); border-radius: 8px; padding: 10px; text-align: center;">
                                <div style="font-size: 0.8rem; opacity: 0.8; margin-bottom: 5px;">System Health</div>
                                <div id="system-health" style="font-size: 1.5rem; font-weight: bold; color: #FFD700;">100%</div>
                            </div>
                            <div style="background: rgba(255,255,255,0.1); border-radius: 8px; padding: 10px; text-align: center;">
                                <div style="font-size: 0.8rem; opacity: 0.8; margin-bottom: 5px;">Active Effects</div>
                                <div id="active-effects" style="font-size: 1.5rem; font-weight: bold; color: #FFD700;">0</div>
                            </div>
                            <div style="background: rgba(255,255,255,0.1); border-radius: 8px; padding: 10px; text-align: center;">
                                <div style="font-size: 0.8rem; opacity: 0.8; margin-bottom: 5px;">Homeostatic Balance</div>
                                <div id="balance-score" style="font-size: 1.5rem; font-weight: bold; color: #FFD700;">0.00</div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div style="text-align: center; margin-top: 30px; opacity: 0.7;">
                    <p>🧠 BioCore Homeostatic Civilization System</p>
                    <p>Research-grade simulation framework | Humans remain in control</p>
                </div>
            </div>
        `;

        // Replace loading screen
        document.body.innerHTML = '';
        document.body.appendChild(dashboard);

        // Setup event listeners
        this.setupEventListeners();
    }

    private setupEventListeners(): void {
        const applyButton = document.getElementById('apply-biocore');
        const optimizeButton = document.getElementById('optimize-system');
        const resetButton = document.getElementById('reset-system');

        if (applyButton) {
            applyButton.addEventListener('click', () => this.applyBioCore());
        }

        if (optimizeButton) {
            optimizeButton.addEventListener('click', () => this.optimizeSystem());
        }

        if (resetButton) {
            resetButton.addEventListener('click', () => this.resetSystem());
        }
    }

    private applyBioCore(): void {
        const zoneSelect = document.getElementById('zone-select') as HTMLSelectElement;
        const plantSelect = document.getElementById('plant-select') as HTMLSelectElement;
        const drugSelect = document.getElementById('drug-select') as HTMLSelectElement;
        const synergyInput = document.getElementById('synergy-input') as HTMLInputElement;

        const zoneId = parseInt(zoneSelect.value);
        const plant = plantSelect.value;
        const drug = drugSelect.value;
        const synergy = parseFloat(synergyInput.value);

        // Apply effect
        const effect = this.calculateEffect(plant, drug, synergy);
        this.applyEffectToZone(zoneId, effect);

        console.log(`🌿 Applied BioCore: Zone ${zoneId}, ${plant} + ${drug}, synergy ${synergy}`);
        this.showNotification(`BioCore effect applied to Zone ${zoneId}`, 'success');
    }

    private optimizeSystem(): void {
        console.log('🧠 Optimizing all zones...');
        
        this.zones.forEach(zone => {
            // Optimize toward homeostatic balance (0.5)
            const error = 0.5 - zone.activity;
            const adjustment = 0.02 * error;
            zone.activity = Math.max(0, Math.min(1, zone.activity + adjustment));
            
            // Update state
            if (zone.activity < 0.4) zone.state = 'CALM';
            else if (zone.activity < 0.7) zone.state = 'OVERSTIMULATED';
            else if (zone.activity < 0.9) zone.state = 'EMERGENT';
            else zone.state = 'CRITICAL';
        });

        this.renderZones();
        this.updateMetrics();
        this.showNotification('System optimized for homeostatic balance', 'success');
    }

    private resetSystem(): void {
        console.log('🔄 Resetting BHCS system...');
        this.zones = [];
        this.effects = [];
        this.initializeZones();
        this.renderZones();
        this.updateMetrics();
        this.showNotification('BHCS system reset to initial state', 'warning');
    }

    private calculateEffect(plant: string, drug: string, synergy: number): BioCoreEffect {
        // Simple effect calculation
        const plantPotency = {
            'Ginkgo': 0.7,
            'Aloe': 0.5,
            'Turmeric': 0.8,
            'Ginseng': 0.6,
            'Ashwagandha': 0.9
        }[plant] || 0.5;

        const drugEffectiveness = {
            'DrugA': 0.6,
            'DrugB': 0.7,
            'DrugC': 0.8,
            'DrugD': 0.5,
            'DrugE': 0.9
        }[drug] || 0.5;

        const magnitude = (plantPotency + drugEffectiveness) / 2 * synergy;

        return {
            plant,
            drug,
            synergy,
            magnitude
        };
    }

    private applyEffectToZone(zoneId: number, effect: BioCoreEffect): void {
        const zone = this.zones.find(z => z.id === zoneId);
        if (!zone) return;

        // Apply effect to zone activity
        zone.activity = Math.max(0, Math.min(1, zone.activity + effect.magnitude));

        // Update zone state
        if (zone.activity < 0.4) zone.state = 'CALM';
        else if (zone.activity < 0.7) zone.state = 'OVERSTIMULATED';
        else if (zone.activity < 0.9) zone.state = 'EMERGENT';
        else zone.state = 'CRITICAL';

        // Record effect
        this.effects.push(effect);

        console.log(`🎛️ Applied effect ${effect.magnitude.toFixed(3)} to Zone ${zoneId}`);
    }

    private startUpdateLoop(): void {
        setInterval(() => {
            if (this.isRunning) {
                this.update();
            }
        }, 1000);
    }

    private update(): void {
        // Simulate natural activity changes
        this.zones.forEach(zone => {
            const change = (Math.random() - 0.5) * 0.02; // Small random changes
            zone.activity = Math.max(0, Math.min(1, zone.activity + change));
            
            // Update state
            if (zone.activity < 0.4) zone.state = 'CALM';
            else if (zone.activity < 0.7) zone.state = 'OVERSTIMULATED';
            else if (zone.activity < 0.9) zone.state = 'EMERGENT';
            else zone.state = 'CRITICAL';
        });

        // Decay effects over time
        this.effects = this.effects.filter(effect => {
            return Math.random() > 0.05; // 5% chance to decay
        });

        this.renderZones();
        this.updateMetrics();
    }

    private renderZones(): void {
        const container = document.getElementById('zones-container');
        if (!container) return;

        container.innerHTML = '';

        this.zones.forEach(zone => {
            const zoneCard = document.createElement('div');
            zoneCard.style.cssText = `
                background: rgba(255,255,255,0.1);
                border-radius: 10px;
                padding: 15px;
                text-align: center;
                transition: transform 0.3s ease;
                border: 1px solid rgba(255,255,255,0.2);
            `;

            const stateColor = {
                'CALM': '#4CAF50',
                'OVERSTIMULATED': '#FF9800',
                'EMERGENT': '#f44336',
                'CRITICAL': '#9C27B0'
            }[zone.state];

            zoneCard.innerHTML = `
                <div style="font-weight: bold; margin-bottom: 8px;">Zone ${zone.id}</div>
                <div style="padding: 4px 8px; border-radius: 12px; font-size: 0.8rem; font-weight: 600; text-transform: uppercase; margin-bottom: 8px; background: ${stateColor};">${zone.state}</div>
                <div style="font-size: 1.2rem; font-weight: bold; color: #FFD700; margin-bottom: 8px;">${zone.activity.toFixed(2)}</div>
                <div style="width: 100%; height: 8px; background: rgba(255,255,255,0.2); border-radius: 4px; overflow: hidden; margin-bottom: 8px;">
                    <div style="height: 100%; background: linear-gradient(90deg, ${stateColor}, #8BC34A); transition: width 0.5s ease; width: ${zone.activity * 100}%;"></div>
                </div>
            `;

            zoneCard.addEventListener('mouseenter', () => {
                zoneCard.style.transform = 'translateY(-2px)';
            });

            zoneCard.addEventListener('mouseleave', () => {
                zoneCard.style.transform = 'translateY(0)';
            });

            container.appendChild(zoneCard);
        });
    }

    private updateMetrics(): void {
        const avgActivity = this.zones.reduce((sum, zone) => sum + zone.activity, 0) / this.zones.length;
        const calmZones = this.zones.filter(z => z.state === 'CALM').length;
        const systemHealth = (calmZones / this.zones.length) * 100;
        const balance = Math.abs(0.5 - avgActivity);

        const avgActivityEl = document.getElementById('avg-activity');
        const systemHealthEl = document.getElementById('system-health');
        const activeEffectsEl = document.getElementById('active-effects');
        const balanceScoreEl = document.getElementById('balance-score');

        if (avgActivityEl) avgActivityEl.textContent = avgActivity.toFixed(2);
        if (systemHealthEl) systemHealthEl.textContent = `${systemHealth.toFixed(0)}%`;
        if (activeEffectsEl) activeEffectsEl.textContent = this.effects.length.toString();
        if (balanceScoreEl) balanceScoreEl.textContent = balance.toFixed(2);
    }

    private showNotification(message: string, type: 'success' | 'warning' | 'error'): void {
        const notification = document.createElement('div');
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

        const colors = {
            success: '#4CAF50',
            warning: '#FF9800',
            error: '#f44336'
        };

        notification.style.background = colors[type];
        notification.textContent = message;

        document.body.appendChild(notification);

        setTimeout(() => {
            document.body.removeChild(notification);
        }, 3000);
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    const app = new SimpleBHCS();
    app.start();
});
