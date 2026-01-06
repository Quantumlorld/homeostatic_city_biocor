/**
 * BHCS Dashboard Application
 * 
 * Human interface for BHCS visualization and control.
 * Humans remain in control - no autonomous actions.
 */

class BHCSDashboard {
    constructor() {
        this.apiBase = 'http://localhost:3030';
        this.updateInterval = 1000;
        this.isRunning = false;
        this.chart = null;
        this.maxDataPoints = 50;
        
        this.initializeElements();
        this.setupEventListeners();
        this.start();
    }

    initializeElements() {
        // Cache DOM elements
        this.elements = {
            zonesContainer: document.getElementById('zones-container'),
            avgActivity: document.getElementById('avg-activity'),
            systemHealth: document.getElementById('system-health'),
            activeEffects: document.getElementById('active-effects'),
            balanceScore: document.getElementById('balance-score'),
            zoneSelect: document.getElementById('zone-select'),
            plantSelect: document.getElementById('plant-select'),
            drugSelect: document.getElementById('drug-select'),
            synergyInput: document.getElementById('synergy-input'),
            applyButton: document.getElementById('apply-biocore'),
            optimizeButton: document.getElementById('optimize-system'),
            resetButton: document.getElementById('reset-system'),
            statusIndicators: document.querySelectorAll('.status-dot')
        };
    }

    setupEventListeners() {
        // Apply BioCore button
        this.elements.applyButton.addEventListener('click', () => {
            this.applyBioCore();
        });

        // Optimize system button
        this.elements.optimizeButton.addEventListener('click', () => {
            this.optimizeSystem();
        });

        // Reset system button
        this.elements.resetButton.addEventListener('click', () => {
            this.resetSystem();
        });

        // Zone select change
        this.elements.zoneSelect.addEventListener('change', () => {
            this.updateZoneRecommendation();
        });
    }

    async start() {
        console.log('🌐 Starting BHCS Dashboard...');
        this.isRunning = true;
        
        // Initialize chart
        this.initializeChart();
        
        // Start update loop
        this.updateLoop();
        
        // Initial data load
        await this.updateDashboard();
        
        console.log('✅ BHCS Dashboard started');
    }

    updateLoop() {
        setInterval(async () => {
            if (this.isRunning) {
                await this.updateDashboard();
            }
        }, this.updateInterval);
    }

    async updateDashboard() {
        try {
            // Get system state
            const response = await fetch(`${this.apiBase}/state`);
            const data = await response.json();
            
            if (data.zones) {
                this.renderZones(data.zones);
                this.updateMetrics(data);
                this.updateChart(data);
                this.updateStatusIndicators(data);
            }
        } catch (error) {
            console.error('❌ Failed to update dashboard:', error);
            this.showNotification('Failed to update dashboard', 'error');
        }
    }

    renderZones(zones) {
        if (!this.elements.zonesContainer) return;

        this.elements.zonesContainer.innerHTML = '';

        zones.forEach(zone => {
            const zoneCard = document.createElement('div');
            zoneCard.className = 'zone-card';
            
            const stateClass = this.getStateClass(zone.state);
            
            zoneCard.innerHTML = `
                <div class="zone-id">Zone ${zone.id}</div>
                <div class="zone-state ${stateClass}">${zone.state}</div>
                <div class="zone-activity">${zone.activity.toFixed(3)}</div>
                <div class="activity-bar">
                    <div class="activity-fill" style="width: ${zone.activity * 100}%"></div>
                </div>
            `;

            zoneCard.addEventListener('mouseenter', () => {
                zoneCard.style.transform = 'translateY(-3px)';
            });

            zoneCard.addEventListener('mouseleave', () => {
                zoneCard.style.transform = 'translateY(0)';
            });

            this.elements.zonesContainer.appendChild(zoneCard);
        });
    }

    getStateClass(state) {
        const stateMap = {
            'CALM': 'state-calm',
            'OVERSTIMULATED': 'state-overstimulated',
            'EMERGENT': 'state-emergent',
            'CRITICAL': 'state-critical'
        };
        return stateMap[state] || 'state-calm';
    }

    updateMetrics(data) {
        // Calculate average activity
        const avgActivity = data.zones.reduce((sum, zone) => sum + zone.activity, 0) / data.zones.length;
        
        // Calculate system health (percentage of calm zones)
        const calmZones = data.zones.filter(zone => zone.state === 'CALM').length;
        const systemHealth = (calmZones / data.zones.length) * 100;
        
        // Calculate homeostatic balance
        const balanceScore = Math.abs(0.5 - avgActivity);

        // Update DOM elements
        if (this.elements.avgActivity) {
            this.elements.avgActivity.textContent = avgActivity.toFixed(3);
        }
        
        if (this.elements.systemHealth) {
            this.elements.systemHealth.textContent = `${systemHealth.toFixed(0)}%`;
        }
        
        if (this.elements.activeEffects) {
            this.elements.activeEffects.textContent = '0'; // Would come from BioCore API
        }
        
        if (this.elements.balanceScore) {
            this.elements.balanceScore.textContent = balanceScore.toFixed(3);
        }
    }

    initializeChart() {
        const canvas = document.getElementById('performance-chart');
        if (!canvas) return;

        const ctx = canvas.getContext('2d');
        
        // Simple chart implementation
        this.chartData = {
            labels: [],
            datasets: [
                {
                    label: 'System Health',
                    data: [],
                    color: '#4CAF50'
                },
                {
                    label: 'Average Activity',
                    data: [],
                    color: '#9C27B0'
                },
                {
                    label: 'Homeostatic Balance',
                    data: [],
                    color: '#FF9800'
                }
            ]
        };

        // Draw simple chart
        this.drawSimpleChart(ctx);
    }

    drawSimpleChart(ctx) {
        const canvas = ctx.canvas;
        const width = canvas.width = canvas.offsetWidth;
        const height = canvas.height = canvas.offsetHeight;
        
        // Clear canvas
        ctx.clearRect(0, 0, width, height);
        
        // Draw grid
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.1)';
        ctx.lineWidth = 1;
        
        for (let i = 0; i <= 10; i++) {
            const y = (height / 10) * i;
            ctx.beginPath();
            ctx.moveTo(0, y);
            ctx.lineTo(width, y);
            ctx.stroke();
        }
        
        // Draw data
        if (this.chartData.labels.length > 1) {
            const datasets = this.chartData.datasets;
            
            datasets.forEach(dataset => {
                ctx.strokeStyle = dataset.color;
                ctx.lineWidth = 2;
                ctx.beginPath();
                
                dataset.data.forEach((value, index) => {
                    const x = (width / this.maxDataPoints) * index;
                    const y = height - (value * height);
                    
                    if (index === 0) {
                        ctx.moveTo(x, y);
                    } else {
                        ctx.lineTo(x, y);
                    }
                });
                
                ctx.stroke();
            });
        }
    }

    updateChart(data) {
        if (!this.chartData) return;

        const avgActivity = data.zones.reduce((sum, zone) => sum + zone.activity, 0) / data.zones.length;
        const calmZones = data.zones.filter(zone => zone.state === 'CALM').length;
        const systemHealth = calmZones / data.zones.length;
        const balanceScore = Math.abs(0.5 - avgActivity);

        // Add data point
        this.chartData.labels.push(new Date().toLocaleTimeString());
        this.chartData.datasets[0].data.push(systemHealth);
        this.chartData.datasets[1].data.push(avgActivity);
        this.chartData.datasets[2].data.push(balanceScore);

        // Keep only last N points
        if (this.chartData.labels.length > this.maxDataPoints) {
            this.chartData.labels.shift();
            this.chartData.datasets.forEach(dataset => dataset.data.shift());
        }

        // Redraw chart
        const canvas = document.getElementById('performance-chart');
        if (canvas) {
            const ctx = canvas.getContext('2d');
            this.drawSimpleChart(ctx);
        }
    }

    updateStatusIndicators(data) {
        // Update status indicators based on system health
        const calmZones = data.zones.filter(zone => zone.state === 'CALM').length;
        const systemHealth = calmZones / data.zones.length;
        
        this.elements.statusIndicators.forEach(indicator => {
            if (systemHealth > 0.7) {
                indicator.classList.remove('warning', 'error');
                indicator.style.background = '#4CAF50';
            } else if (systemHealth > 0.4) {
                indicator.classList.remove('error');
                indicator.classList.add('warning');
                indicator.style.background = '#FF9800';
            } else {
                indicator.classList.remove('warning');
                indicator.classList.add('error');
                indicator.style.background = '#f44336';
            }
        });
    }

    async applyBioCore() {
        const zoneId = parseInt(this.elements.zoneSelect.value);
        const plant = this.elements.plantSelect.value;
        const drug = this.elements.drugSelect.value;
        const synergy = parseFloat(this.elements.synergyInput.value);

        try {
            const response = await fetch(`${this.apiBase}/influence`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    zone_id: zoneId,
                    influence: this.calculateInfluence(plant, drug, synergy)
                })
            });

            if (response.ok) {
                this.showNotification(`BioCore effect applied to Zone ${zoneId}`, 'success');
            } else {
                this.showNotification('Failed to apply BioCore effect', 'error');
            }
        } catch (error) {
            console.error('❌ Failed to apply BioCore:', error);
            this.showNotification('Error applying BioCore effect', 'error');
        }
    }

    calculateInfluence(plant, drug, synergy) {
        // Simple influence calculation
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

        return (plantPotency + drugEffectiveness) / 2 * synergy;
    }

    async optimizeSystem() {
        try {
            // Get current state
            const response = await fetch(`${this.apiBase}/state`);
            const data = await response.json();
            
            // Apply optimization to all zones
            for (const zone of data.zones) {
                const error = 0.5 - zone.activity;
                const adjustment = 0.02 * error;
                
                await fetch(`${this.apiBase}/influence`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        zone_id: zone.id,
                        influence: adjustment
                    })
                });
            }
            
            this.showNotification('System optimized for homeostatic balance', 'success');
        } catch (error) {
            console.error('❌ Failed to optimize system:', error);
            this.showNotification('Error optimizing system', 'error');
        }
    }

    async resetSystem() {
        if (!confirm('Are you sure you want to reset the BHCS system?')) {
            return;
        }

        try {
            // Get current state
            const response = await fetch(`${this.apiBase}/state`);
            const data = await response.json();
            
            // Reset all zones to initial state
            for (const zone of data.zones) {
                const resetInfluence = 0.5 - zone.activity;
                
                await fetch(`${this.apiBase}/influence`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        zone_id: zone.id,
                        influence: resetInfluence
                    })
                });
            }
            
            this.showNotification('BHCS system reset to initial state', 'warning');
        } catch (error) {
            console.error('❌ Failed to reset system:', error);
            this.showNotification('Error resetting system', 'error');
        }
    }

    updateZoneRecommendation() {
        // This would typically call the BioCore API for recommendations
        // For now, just log the change
        const zoneId = this.elements.zoneSelect.value;
        console.log(`🎯 Zone ${zoneId} selected - recommendation would be fetched here`);
    }

    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;

        document.body.appendChild(notification);

        // Remove after 3 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 3000);
    }

    stop() {
        this.isRunning = false;
        console.log('🛑 BHCS Dashboard stopped');
    }
}

// Initialize dashboard when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    const dashboard = new BHCSDashboard();
    
    // Make dashboard globally accessible for debugging
    window.BHCSDashboard = dashboard;
});
