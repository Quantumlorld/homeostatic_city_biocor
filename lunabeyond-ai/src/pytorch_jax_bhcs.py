#!/usr/bin/env python3
"""
BHCS Combined PyTorch + JAX Simulation System
Integrating PyTorch for core processing and JAX for advanced numerical simulation
"""

import torch
import jax
import jax.numpy as jnp
import time
import requests
import json
import numpy as np
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bhcs_pytorch_jax.log'),
        logging.StreamHandler()
    ]
)

class BHCSCombinedSimulator:
    """
    Combined PyTorch + JAX simulation system for BHCS
    """
    
    def __init__(self):
        # PyTorch configuration
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"🔥 PyTorch using device: {self.device}")
        
        # JAX configuration
        jax.config.update('jax_platform_name', 'cpu')  # Can be changed to 'gpu'
        print(f"⚡ JAX platform configured")
        
        # BHCS API endpoints
        self.bhcs_api_base = "http://localhost:8766"
        self.luna_api_base = "http://localhost:8000"
        
        # Zone configuration
        self.zones = {
            1: {"name": "Downtown", "activity": 0.65, "stress": 0.35},
            2: {"name": "Industrial", "activity": 0.78, "stress": 0.62},
            3: {"name": "Residential", "activity": 0.42, "stress": 0.25},
            4: {"name": "Commercial", "activity": 0.71, "stress": 0.38},
            5: {"name": "Parks", "activity": 0.28, "stress": 0.15}
        }
        
        # Simulation parameters
        self.simulation_log = []
        self.luna_confidence_history = []
        
    def send_activity_to_bhcs(self, zone_id: int, activity_value: float) -> bool:
        """Send activity update to BHCS Rust engine"""
        try:
            response = requests.post(
                f"{self.bhcs_api_base}/api/zones/{zone_id}/update",
                json={
                    "activity_level": activity_value,
                    "timestamp": datetime.now().isoformat(),
                    "source": "pytorch_jax_simulator"
                },
                timeout=5.0
            )
            if response.status_code == 200:
                logging.info(f"✅ BHCS Update: Zone {zone_id} activity set to {activity_value}")
                return True
            else:
                logging.error(f"❌ BHCS Update Failed: {response.status_code}")
                return False
        except Exception as e:
            logging.error(f"❌ BHCS Connection Error: {e}")
            return False
    
    def send_to_luna(self, message: str, zone_context: Optional[Dict] = None) -> Optional[Dict]:
        """Send message to Luna AI for analysis"""
        try:
            response = requests.post(
                f"{self.luna_api_base}/api/luna/chat",
                json={
                    "user_message": message,
                    "zone_context": zone_context,
                    "interaction_type": "zone_analysis"
                },
                timeout=10.0
            )
            if response.status_code == 200:
                luna_response = response.json()
                logging.info(f"🌙 Luna Response: {luna_response.get('luna_response', 'No response')[:100]}...")
                return luna_response
            else:
                logging.error(f"❌ Luna API Failed: {response.status_code}")
                return None
        except Exception as e:
            logging.error(f"❌ Luna Connection Error: {e}")
            return None
    
    def get_bhcs_state(self, zone_id: int) -> Optional[Dict]:
        """Get current state from BHCS"""
        try:
            response = requests.get(f"{self.bhcs_api_base}/api/zones/{zone_id}", timeout=5.0)
            if response.status_code == 200:
                return response.json()
            else:
                logging.error(f"❌ BHCS State Failed: {response.status_code}")
                return None
        except Exception as e:
            logging.error(f"❌ BHCS State Error: {e}")
            return None
    
    def pytorch_overstimulation(self, zone_id: int, target_activity: float) -> torch.Tensor:
        """Use PyTorch for overstimulation simulation"""
        print(f"\n🔥 PYTORCH OVERSIMULATION - Zone {zone_id}")
        
        # Create PyTorch tensor for the zone
        initial_activity = self.zones[zone_id]["activity"]
        activity_tensor = torch.tensor([initial_activity], dtype=torch.float32, device=self.device)
        
        # Apply overstimulation using PyTorch operations
        overstimulation_factor = torch.tensor([target_activity / initial_activity], device=self.device)
        activity_tensor_pt = activity_tensor * overstimulation_factor
        
        # Apply non-linear activation (simulating stress response)
        stress_response = torch.relu(activity_tensor_pt - 0.7) * 1.5
        activity_tensor_pt = activity_tensor_pt + stress_response
        
        final_activity = torch.clamp(activity_tensor_pt, 0.0, 1.0)
        
        print(f"🔥 PyTorch Calculation:")
        print(f"   Initial: {initial_activity:.3f}")
        print(f"   Target: {target_activity:.3f}")
        print(f"   Factor: {overstimulation_factor.item():.3f}")
        print(f"   Final: {final_activity.item():.3f}")
        
        # Send to BHCS
        success = self.send_activity_to_bhcs(zone_id, final_activity.item())
        
        if success:
            # Log simulation step
            self.simulation_log.append({
                "timestamp": datetime.now().isoformat(),
                "framework": "PyTorch",
                "zone_id": zone_id,
                "initial_activity": initial_activity,
                "target_activity": target_activity,
                "final_activity": final_activity.item(),
                "stress_response": stress_response.item(),
                "success": True
            })
            
            # Update local zone data
            self.zones[zone_id]["activity"] = final_activity.item()
        
        return final_activity
    
    def jax_pulse_simulation(self, zone_id: int, pulse_values: jnp.ndarray) -> List[float]:
        """Use JAX for advanced pulse simulation"""
        print(f"\n⚡ JAX PULSE SIMULATION - Zone {zone_id}")
        
        # Create JAX arrays for simulation
        current_activity = self.zones[zone_id]["activity"]
        activity_array = jnp.array([current_activity])
        
        # Apply JAX pulses with advanced mathematical operations
        pulse_results = []
        for i, pulse_value in enumerate(pulse_values):
            # JAX operations for pulse application
            pulse_tensor = jnp.array([pulse_value])
            
            # Advanced JAX mathematical operations
            decay_factor = jnp.exp(-i * 0.1)  # Exponential decay
            resonance = jnp.sin(pulse_value * jnp.pi * 2)  # Resonance effect
            combined_pulse = pulse_tensor * decay_factor + resonance * 0.1
            
            # Apply to activity
            new_activity = activity_array + combined_pulse
            new_activity = jnp.clip(new_activity, 0.0, 1.0)  # Clamp to valid range
            
            pulse_result = float(new_activity[0])
            pulse_results.append(pulse_result)
            
            print(f"⚡ JAX Pulse {i+1}:")
            print(f"   Pulse Value: {pulse_value:.3f}")
            print(f"   Decay Factor: {decay_factor:.3f}")
            print(f"   Resonance: {resonance:.3f}")
            print(f"   Result Activity: {pulse_result:.3f}")
            
            # Send to BHCS
            self.send_activity_to_bhcs(zone_id, pulse_result)
            time.sleep(2)  # Wait between pulses
        
        # Calculate JAX optimization metrics
        avg_activity = jnp.mean(jnp.array(pulse_results))
        variance = jnp.var(jnp.array(pulse_results))
        
        print(f"⚡ JAX Analysis:")
        print(f"   Average Activity: {avg_activity:.3f}")
        print(f"   Variance: {variance:.3f}")
        print(f"   Stability: {1.0 - variance:.3f}")
        
        # Update zone with final value
        final_activity = float(avg_activity)
        self.zones[zone_id]["activity"] = final_activity
        
        return pulse_results
    
    def luna_analysis(self, zone_id: int, context: str) -> Optional[float]:
        """Get Luna AI analysis and confidence"""
        print(f"\n🌙 LUNA AI ANALYSIS - Zone {zone_id}")
        
        zone_info = self.zones[zone_id]
        zone_context = {
            "zone_name": zone_info["name"],
            "activity_level": zone_info["activity"],
            "stress_level": zone_info["stress"],
            "population_density": 0.7,
            "primary_function": "Simulation Testing"
        }
        
        luna_response = self.send_to_luna(
            f"Analyze {context} for {zone_info['name']} zone. Current activity: {zone_info['activity']:.3f}, stress: {zone_info['stress']:.3f}",
            zone_context
        )
        
        if luna_response:
            # Extract confidence from Luna's response
            luna_text = luna_response.get('luna_response', '')
            confidence = self.extract_confidence(luna_text)
            
            print(f"🌙 Luna Analysis:")
            print(f"   Response: {luna_text[:100]}...")
            print(f"   Confidence: {confidence:.3f}")
            print(f"   Intelligence Level: {luna_response.get('personality', {}).get('intelligence_level', 'Unknown')}")
            
            # Store confidence history
            self.luna_confidence_history.append(confidence)
            
            return confidence
        return None
    
    def extract_confidence(self, luna_response: str) -> float:
        """Extract confidence score from Luna's response"""
        confidence_keywords = [
            "confidence", "certain", "sure", "accurate", "precise",
            "predict", "forecast", "analyze", "assessment"
        ]
        
        response_lower = luna_response.lower()
        confidence_score = 0.5  # Base confidence
        
        for keyword in confidence_keywords:
            if keyword in response_lower:
                confidence_score += 0.1
        
        # Look for percentage mentions
        import re
        percentages = re.findall(r'(\d+(?:\.\d+)?)%?', response_lower)
        if percentages:
            confidence_score += min(float(percentages[0]) / 100, 0.5)
        
        return min(confidence_score, 1.0)
    
    def run_combined_simulation(self, zone_id: int = 2):
        """Run complete PyTorch + JAX simulation"""
        print(f"\n🚀 STARTING COMBINED PYTORCH + JAX SIMULATION")
        print(f"🎯 Target Zone: {self.zones[zone_id]['name']} (ID: {zone_id})")
        print(f"📊 Initial Activity: {self.zones[zone_id]['activity']:.3f}")
        print(f"😰 Initial Stress: {self.zones[zone_id]['stress']:.3f}")
        
        # Step 1: PyTorch Overstimulation
        print(f"\n" + "="*60)
        print(f"STEP 1: PYTORCH OVERSIMULATION")
        print(f"="*60)
        
        initial_activity = self.zones[zone_id]["activity"]
        overstimulated_activity = 0.9  # Target overstimulation
        
        final_pt_activity = self.pytorch_overstimulation(zone_id, overstimulated_activity)
        
        # Wait for BHCS regulation
        print(f"\n⏱️ Waiting 5 seconds for BHCS regulation...")
        time.sleep(5)
        
        # Get BHCS state after PyTorch step
        bhcs_state = self.get_bhcs_state(zone_id)
        if bhcs_state:
            print(f"📊 BHCS State after PyTorch:")
            print(f"   Activity: {bhcs_state.get('activity_level', 'N/A')}")
            print(f"   Stress: {bhcs_state.get('stress_level', 'N/A')}")
            print(f"   Last Updated: {bhcs_state.get('last_updated', 'N/A')}")
        
        # Step 2: Luna Analysis
        print(f"\n" + "="*60)
        print(f"STEP 2: LUNA AI ANALYSIS")
        print(f"="*60)
        
        luna_confidence = self.luna_analysis(zone_id, "PyTorch overstimulation effects")
        
        # Step 3: JAX Pulse Simulation
        print(f"\n" + "="*60)
        print(f"STEP 3: JAX PULSE SIMULATION")
        print(f"="*60)
        
        # Create JAX pulse sequence
        pulse_values = jnp.linspace(0.6, 0.85, num=3)
        pulse_results = self.jax_pulse_simulation(zone_id, pulse_values)
        
        # Wait for final stabilization
        print(f"\n⏱️ Waiting 3 seconds for final stabilization...")
        time.sleep(3)
        
        # Step 4: Final Analysis
        print(f"\n" + "="*60)
        print(f"STEP 4: FINAL ANALYSIS")
        print(f"="*60)
        
        final_bhcs_state = self.get_bhcs_state(zone_id)
        if final_bhcs_state:
            print(f"📊 Final BHCS State:")
            print(f"   Activity: {final_bhcs_state.get('activity_level', 'N/A')}")
            print(f"   Stress: {final_bhcs_state.get('stress_level', 'N/A')}")
            print(f"   Last Updated: {final_bhcs_state.get('last_updated', 'N/A')}")
        
        # Final Luna analysis
        final_luna_confidence = self.luna_analysis(zone_id, "JAX pulse simulation results")
        
        # Simulation Summary
        print(f"\n" + "="*60)
        print(f"SIMULATION SUMMARY")
        print(f"="*60)
        print(f"🎯 Zone: {self.zones[zone_id]['name']}")
        print(f"📊 Initial Activity: {initial_activity:.3f}")
        print(f"🔥 PyTorch Final: {final_pt_activity.item():.3f}")
        print(f"⚡ JAX Average: {np.mean(pulse_results):.3f}")
        print(f"📊 Final Activity: {final_bhcs_state.get('activity_level', 'N/A') if final_bhcs_state else 'N/A'}")
        print(f"🌙 Luna Confidence (Initial): {luna_confidence:.3f}" if luna_confidence else "🌙 Luna Confidence (Initial): N/A")
        print(f"🌙 Luna Confidence (Final): {final_luna_confidence:.3f}" if final_luna_confidence else "🌙 Luna Confidence (Final): N/A")
        
        # Calculate simulation metrics
        if luna_confidence and final_luna_confidence:
            confidence_improvement = final_luna_confidence - luna_confidence
            print(f"📈 Confidence Improvement: {confidence_improvement:+.3f}")
        
        # Log final results
        self.simulation_log.append({
            "timestamp": datetime.now().isoformat(),
            "framework": "Combined",
            "zone_id": zone_id,
            "initial_activity": initial_activity,
            "pytorch_result": final_pt_activity.item(),
            "jax_average": np.mean(pulse_results),
            "final_activity": final_bhcs_state.get('activity_level') if final_bhcs_state else None,
            "initial_luna_confidence": luna_confidence,
            "final_luna_confidence": final_luna_confidence,
            "success": True
        })
        
        return {
            "zone_id": zone_id,
            "zone_name": self.zones[zone_id]["name"],
            "initial_activity": initial_activity,
            "pytorch_result": final_pt_activity.item(),
            "jax_results": pulse_results,
            "final_activity": final_bhcs_state.get('activity_level') if final_bhcs_state else None,
            "luna_confidence_improvement": (final_luna_confidence - luna_confidence) if (luna_confidence and final_luna_confidence) else None
        }
    
    def save_simulation_log(self):
        """Save simulation log to file"""
        try:
            with open('bhcs_pytorch_jax_simulation_log.json', 'w') as f:
                json.dump(self.simulation_log, f, indent=2)
            print(f"💾 Simulation log saved to bhcs_pytorch_jax_simulation_log.json")
        except Exception as e:
            print(f"❌ Failed to save simulation log: {e}")
    
    def print_system_info(self):
        """Print system information"""
        print(f"\n🚀 BHCS COMBINED PYTORCH + JAX SIMULATION SYSTEM")
        print(f"="*50)
        print(f"🔥 PyTorch Version: {torch.__version__}")
        print(f"🔥 PyTorch Device: {self.device}")
        print(f"⚡ JAX Version: {jax.__version__}")
        print(f"⚡ JAX Platform: {jax.config.jax_platform_name}")
        print(f"🌐 BHCS API: {self.bhcs_api_base}")
        print(f"🌙 Luna API: {self.luna_api_base}")
        print(f"📊 Zones Configured: {len(self.zones)}")
        print(f"📝 Log Level: {logging.getLogger().level}")

def main():
    """Main simulation function"""
    simulator = BHCSCombinedSimulator()
    simulator.print_system_info()
    
    # Get target zone from user input or use default
    try:
        zone_input = input("\n🎯 Enter zone ID (1-5) or press Enter for default (2): ").strip()
        zone_id = int(zone_input) if zone_input else 2
        if zone_id not in simulator.zones:
            print(f"❌ Invalid zone ID. Using default zone 2.")
            zone_id = 2
    except ValueError:
        print(f"❌ Invalid input. Using default zone 2.")
        zone_id = 2
    
    print(f"\n🎯 Starting simulation for Zone {zone_id}: {simulator.zones[zone_id]['name']}")
    
    # Run the combined simulation
    try:
        results = simulator.run_combined_simulation(zone_id)
        
        # Save results
        simulator.save_simulation_log()
        
        print(f"\n🎉 SIMULATION COMPLETED SUCCESSFULLY!")
        print(f"📊 Results saved to simulation log")
        
    except KeyboardInterrupt:
        print(f"\n⏹️ Simulation interrupted by user")
        simulator.save_simulation_log()
    except Exception as e:
        print(f"\n❌ Simulation error: {e}")
        simulator.save_simulation_log()

if __name__ == "__main__":
    main()
