/**
 * BHCS - BioCore Homeostatic Civilization System
 * TypeScript Implementation
 * 
 * A research-grade software architecture designed to maintain stability 
 * in complex systems through homeostatic regulation.
 */

import { BHCSController } from './core/controller';
import { HomeostaticEngine } from './core/engine';
import { BioCoreSimulator } from './biocore/simulator';
import { DashboardUI } from './ui/dashboard';

/**
 * Main BHCS Application Entry Point
 */
class BHCSApplication {
    private controller: BHCSController;
    private engine: HomeostaticEngine;
    private biocore: BioCoreSimulator;
    private dashboard: DashboardUI;

    constructor() {
        console.log('🧠 BHCS: BioCore Homeostatic Civilization System Initializing...');
        
        // Initialize core components
        this.engine = new HomeostaticEngine();
        this.biocore = new BioCoreSimulator();
        this.controller = new BHCSController(this.engine, this.biocore);
        this.dashboard = new DashboardUI(this.controller);
        
        this.initialize();
    }

    /**
     * Initialize the BHCS system
     */
    private async initialize(): Promise<void> {
        try {
            console.log('🔧 Initializing Homeostatic Engine...');
            await this.engine.initialize();
            
            console.log('🌿 Initializing BioCore Simulator...');
            await this.biocore.initialize();
            
            console.log('🌐 Initializing Dashboard...');
            await this.dashboard.initialize();
            
            console.log('🚀 Starting BHCS System...');
            this.start();
            
        } catch (error) {
            console.error('❌ BHCS Initialization failed:', error);
        }
    }

    /**
     * Start the main BHCS loop
     */
    private start(): void {
        // Start real-time updates
        setInterval(async () => {
            await this.update();
        }, 1000); // Update every second
        
        console.log('✅ BHCS System Running - Homeostatic Regulation Active');
    }

    /**
     * Main update loop
     */
    private async update(): Promise<void> {
        try {
            // 1. Update homeostatic engine
            await this.engine.update();
            
            // 2. Process BioCore simulations
            await this.biocore.update([]);
            
            // 3. Update controller state
            await this.controller.update();
            
            // 4. Refresh dashboard
            await this.dashboard.render();
            
        } catch (error) {
            console.error('❌ BHCS Update failed:', error);
        }
    }
}

/**
 * Application Entry Point
 */
document.addEventListener('DOMContentLoaded', () => {
    new BHCSApplication();
});

export { BHCSApplication };
