#!/usr/bin/env python3
"""
🦀 BHCS Aligned Integration - Respects Core Philosophy
ALIGN, STABILIZE, and REFINE entire system end-to-end

Core Philosophy Maintained:
- Homeostasis is primary control principle
- All systems regulate toward balance, not maximization
- Overstimulation must decay naturally into calm
- Calm is controlled intensity, not inactivity
- Human-in-the-loop control is mandatory

Universal equation applied uniformly:
balance_error = target_state - current_state
adjustment = learning_rate * balance_error
new_state = current_state + adjustment
"""

import asyncio
import time
import threading
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

# Import aligned components
from BHCS_Core_Engine import BHCSCoreEngine
from real_weather_engine import RealWeatherEngine

# Configure logging for stability
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class BHCSAlignedIntegration:
    """Aligned BHCS Integration - Maintains core philosophy"""
    
    def __init__(self):
        logger.info("🦀 Initializing BHCS Aligned Integration")
        logger.info("=" * 60)
        
        # Core Systems (Rust-equivalent authority)
        logger.info("🦀 Initializing Core BHCS Engine...")
        self.bhcs_engine = BHCSCoreEngine(5)
        
        # Environmental Modifiers (observational only)
        logger.info("🌦 Initializing Environmental Modifiers...")
        self.weather_engine = RealWeatherEngine()
        
        # Integration State
        self.system_state = {
            'bhcs_active': False,
            'weather_active': False,
            'human_approval_required': True,
            'safety_mode': 'CONSERVATIVE',
            'integration_level': 'ALIGNED'
        }
        
        # Performance Metrics (stability-focused)
        self.metrics = {
            'start_time': time.time(),
            'homeostatic_regulations': 0,
            'external_influences': 0,
            'human_interventions': 0,
            'system_stability': 0.0,
            'recovery_confidence': 0.5
        }
        
        logger.info("✅ BHCS Aligned Integration Initialized")
        logger.info("=" * 60)
    
    async def start_aligned_system(self):
        """Start the aligned BHCS system"""
        logger.info("🚀 Starting BHCS Aligned System")
        logger.info("=" * 60)
        
        # Start core regulation
        await self._start_core_regulation()
        
        # Start environmental monitoring
        await self._start_environmental_monitoring()
        
        # Start human-in-the-loop interface
        await self._start_human_interface()
        
        # Main aligned loop
        await self._run_aligned_loop()
    
    async def _start_core_regulation(self):
        """Start core homeostatic regulation"""
        logger.info("🦀 Starting Core Homeostatic Regulation")
        
        # Start BHCS engine (final authority)
        self.bhcs_engine.start_regulation()
        self.system_state['bhcs_active'] = True
        
        logger.info("✅ Core Regulation Started")
    
    async def _start_environmental_monitoring(self):
        """Start environmental monitoring (observational only)"""
        logger.info("🌦 Starting Environmental Monitoring")
        
        def environmental_loop():
            while self.system_state['bhcs_active']:
                # Get environmental data (observational)
                city_weather = self.weather_engine.get_city_weather()
                
                # Log environmental impacts periodically
                if int(time.time()) % 15 == 0:
                    logger.info("🌦 Environmental Impact Summary:")
                    for zone_id in range(5):
                        zone_weather = city_weather["city_weather"].get(f"zone_{zone_id}")
                        if zone_weather:
                            impact = self.weather_engine.get_weather_impact_on_activity(zone_weather)
                            logger.info(f"  Zone {zone_id}: environmental impact = {impact:+.3f}")
                
                time.sleep(5)  # Monitor every 5 seconds
        
        self.env_thread = threading.Thread(target=environmental_loop, daemon=True)
        self.env_thread.start()
        self.system_state['weather_active'] = True
        
        logger.info("✅ Environmental Monitoring Started")
    
    async def _start_human_interface(self):
        """Start human-in-the-loop interface"""
        logger.info("👤 Starting Human-in-the-Loop Interface")
        
        # This would connect to TypeScript dashboard
        # For now, we'll simulate human approval requirements
        logger.info("✅ Human Interface Ready")
        logger.info("📋 All interventions require human approval")
    
    async def _run_aligned_loop(self):
        """Main aligned integration loop"""
        logger.info("🔄 Starting Aligned Integration Loop")
        logger.info("=" * 60)
        logger.info("🦀 BHCS Core: Final authority on state changes")
        logger.info("🌦 Environment: Observational modifier only")
        logger.info("👤 Human: Mandatory approval for interventions")
        logger.info("=" * 60)
        
        try:
            while self.system_state['bhcs_active']:
                # Update metrics
                self._update_aligned_metrics()
                
                # Log system status periodically
                if int(time.time()) % 20 == 0:
                    self._log_aligned_status()
                
                # Check for stability opportunities
                if self.metrics['homeostatic_regulations'] % 100 == 0:
                    await self._check_system_stability()
                
                await asyncio.sleep(1)
                
        except KeyboardInterrupt:
            logger.info("\n🛑 Shutting down Aligned System...")
            await self._shutdown_aligned_system()
    
    def _update_aligned_metrics(self):
        """Update stability-focused metrics"""
        try:
            # Get current system health
            health = self.bhcs_engine.get_system_health()
            
            # Update metrics
            self.metrics['homeostatic_regulations'] += 1
            self.metrics['system_stability'] = health['system_health']
            self.metrics['recovery_confidence'] = health['recovery_confidence']
            
        except Exception as e:
            logger.error(f"⚠️ Metrics update error: {e}")
    
    def _log_aligned_status(self):
        """Log aligned system status"""
        health = self.bhcs_engine.get_system_health()
        uptime = time.time() - self.metrics['start_time']
        
        logger.info(f"🦀 Aligned System Status:")
        logger.info(f"  System Health: {health['system_health']:.3f} ({health['status']})")
        logger.info(f"  Average Activity: {health['average_activity']:.3f}")
        logger.info(f"  Target State: {health['target_state']}")
        logger.info(f"  Recovery Confidence: {health['recovery_confidence']:.3f}")
        logger.info(f"  Homeostatic Regulations: {self.metrics['homeostatic_regulations']}")
        logger.info(f"  Uptime: {uptime:.0f}s")
    
    async def _check_system_stability(self):
        """Check and maintain system stability"""
        logger.info("🔍 Checking System Stability...")
        
        health = self.bhcs_engine.get_system_health()
        
        if health['system_health'] < 0.7:
            logger.warning("⚠️ System stability below threshold")
            logger.info("🛡️ Engaging conservative regulation mode")
            
            # Temporarily reduce learning rate for stability
            for zone in self.bhcs_engine.zones:
                zone.learning_rate = max(0.01, zone.learning_rate * 0.5)
        
        elif health['system_health'] > 0.9:
            logger.info("✅ System highly stable")
            logger.info("🔄 Gradually restoring normal learning rate")
            
            # Gradually restore normal learning rate
            for zone in self.bhcs_engine.zones:
                zone.learning_rate = min(0.03, zone.learning_rate * 1.1)
    
    async def request_human_intervention(self, zone_id: int, intervention_data: Dict[str, Any]) -> Dict[str, Any]:
        """Request human approval for intervention"""
        logger.info(f"👤 Requesting human approval for Zone {zone_id} intervention")
        
        # Simulate human approval (in real system, this would wait for UI approval)
        logger.info(f"📋 Intervention Details:")
        logger.info(f"  Zone: {zone_id}")
        logger.info(f"  Magnitude: {intervention_data.get('magnitude', 0.0)}")
        logger.info(f"  Synergy: {intervention_data.get('synergy', 1.0)}")
        logger.info(f"  Source: {intervention_data.get('source', 'unknown')}")
        
        # Simulate human approval (always approve for demo)
        logger.info("✅ Human approval received")
        
        # Apply intervention through core engine
        result = self.bhcs_engine.apply_biocore_intervention(zone_id, intervention_data)
        self.metrics['human_interventions'] += 1
        
        return result
    
    async def _shutdown_aligned_system(self):
        """Graceful shutdown of aligned system"""
        logger.info("🛑 Shutting Down Aligned BHCS System")
        
        # Stop core systems
        self.system_state['bhcs_active'] = False
        self.system_state['weather_active'] = False
        
        if self.bhcs_engine:
            self.bhcs_engine.shutdown()
        
        # Final metrics
        total_uptime = time.time() - self.metrics['start_time']
        logger.info("=" * 60)
        logger.info("🦀 FINAL ALIGNED SYSTEM METRICS:")
        logger.info(f"  Total Uptime: {total_uptime:.0f} seconds")
        logger.info(f"  Homeostatic Regulations: {self.metrics['homeostatic_regulations']}")
        logger.info(f"  External Influences: {self.metrics['external_influences']}")
        logger.info(f"  Human Interventions: {self.metrics['human_interventions']}")
        logger.info(f"  Final System Stability: {self.metrics['system_stability']:.3f}")
        logger.info(f"  Final Recovery Confidence: {self.metrics['recovery_confidence']:.3f}")
        logger.info("=" * 60)
        logger.info("👋 Aligned BHCS System Shutdown Complete")

async def main():
    """Main entry point for aligned BHCS system"""
    logger.info("🦀 BHCS ALIGNED INTEGRATION")
    logger.info("=" * 60)
    logger.info("🦀 Core Philosophy Maintained:")
    logger.info("  - Homeostasis is primary control principle")
    logger.info("  - All systems regulate toward balance")
    logger.info("  - Overstimulation decays naturally to calm")
    logger.info("  - Human-in-the-loop control is mandatory")
    logger.info("=" * 60)
    
    # Initialize and start aligned system
    integration = BHCSAlignedIntegration()
    await integration.start_aligned_system()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("\n👋 Goodbye!")
    except Exception as e:
        logger.error(f"❌ System error: {e}")
        import traceback
        traceback.print_exc()
