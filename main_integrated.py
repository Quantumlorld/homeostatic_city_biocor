#!/usr/bin/env python3
"""
🚀 Homeostatic City + BioCore - Integrated System
Multi-language simulation with Rust, Python, and TypeScript
"""

import subprocess
import time
import threading
import requests
import json
import sys
import os
from pathlib import Path

class IntegratedBHCSSystem:
    def __init__(self):
        self.rust_url = "http://localhost:3030"
        self.rust_process = None
        self.running = True
        
    def start_rust_engine(self):
        """Start Rust homeostatic engine"""
        print("🦀 Starting Rust homeostatic engine...")
        
        try:
            # Check if Rust is installed
            result = subprocess.run(['rustc', '--version'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode != 0:
                print("❌ Rust not found. Please install Rust from https://rustup.rs/")
                return False
        except:
            print("❌ Rust not found. Please install Rust from https://rustup.rs/")
            return False
        
        try:
            # Start Rust engine
            city_core_path = Path("city_core")
            if not city_core_path.exists():
                print("❌ city_core directory not found")
                return False
            
            self.rust_process = subprocess.Popen(
                ['cargo', 'run'],
                cwd=city_core_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Wait for startup
            time.sleep(3)
            
            if self.rust_process.poll() is None:
                print("✅ Rust engine started successfully")
                return True
            else:
                stdout, stderr = self.rust_process.communicate()
                print(f"❌ Rust engine failed to start:")
                print(f"STDOUT: {stdout}")
                print(f"STDERR: {stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Failed to start Rust engine: {e}")
            return False
    
    def check_rust_engine(self):
        """Check if Rust engine is running"""
        try:
            response = requests.get(f"{self.rust_url}/health", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def get_city_state(self):
        """Get current city state from Rust engine"""
        try:
            response = requests.get(f"{self.rust_url}/state", timeout=5)
            if response.status_code == 200:
                return response.json()
            return None
        except:
            return None
    
    def open_dashboard(self):
        """Open TypeScript dashboard"""
        print("🌐 Opening dashboard...")
        
        dashboard_path = Path("dashboard/index.html")
        if not dashboard_path.exists():
            print("❌ Dashboard file not found")
            return False
        
        try:
            # Open in default browser
            if sys.platform == "win32":
                os.startfile(dashboard_path)
            elif sys.platform == "darwin":
                subprocess.run(['open', dashboard_path])
            else:
                subprocess.run(['xdg-open', dashboard_path])
            
            print("✅ Dashboard opened in browser")
            return True
            
        except Exception as e:
            print(f"❌ Failed to open dashboard: {e}")
            return False
    
    def test_system_integration(self):
        """Test full system integration"""
        print("🧪 Testing System Integration...")
        
        # Test Rust API
        if not self.check_rust_engine():
            print("❌ Rust engine not responding")
            return False
        
        print("✅ Rust engine responding")
        
        # Test state endpoint
        state = self.get_city_state()
        if state:
            print(f"✅ State endpoint working - {len(state['zones'])} zones")
            for zone in state['zones']:
                print(f"   Zone {zone['id']} ({zone['name']}): {zone['state']} ({zone['activity']:.3f})")
        else:
            print("❌ State endpoint failed")
            return False
        
        # Test BioCore effect
        try:
            effect_data = {
                "zone_id": 2,
                "magnitude": -0.1,
                "effects": ["Test Effect"]
            }
            response = requests.post(f"{self.rust_url}/biocore", 
                                  json=effect_data, timeout=5)
            if response.status_code == 200:
                print("✅ BioCore effect application successful")
            else:
                print(f"⚠️ BioCore effect status: {response.status_code}")
        except Exception as e:
            print(f"❌ BioCore effect failed: {e}")
            return False
        
        return True
    
    def run_integrated_simulation(self):
        """Run integrated simulation"""
        print("🚀 Starting Integrated BHCS Simulation...")
        
        # Start Rust engine
        if not self.start_rust_engine():
            print("❌ Cannot proceed without Rust engine")
            return
        
        # Open dashboard
        self.open_dashboard()
        
        # Wait for user input
        try:
            print("\n🎯 System Ready!")
            print("📊 Rust Engine: http://localhost:3030")
            print("🌐 Dashboard: Open in browser")
            print("\nPress Enter to start simulation, or Ctrl+C to exit...")
            input()
            
            # Test integration
            if self.test_system_integration():
                print("✅ System integration successful!")
            else:
                print("❌ System integration failed")
            
            # Run simulation loop
            print("\n🔄 Running simulation...")
            while self.running:
                state = self.get_city_state()
                if state:
                    print(f"\n📊 System Health: {state['system_health']:.3f}")
                    zones_by_state = {}
                    for zone in state['zones']:
                        state_name = zone['state']
                        if state_name not in zones_by_state:
                            zones_by_state[state_name] = []
                        zones_by_state[state_name].append(zone['name'])
                    
                    for state_name, zones in zones_by_state.items():
                        emoji = {'CALM': '🟢', 'OVERSTIMULATED': '🟡', 'EMERGENT': '🔴'}.get(state_name, '⚪')
                        print(f"  {emoji} {state_name}: {', '.join(zones)}")
                
                time.sleep(5)
                
        except KeyboardInterrupt:
            print("\n🛑 Shutting down...")
            self.running = False
        
        finally:
            # Clean up Rust process
            if self.rust_process:
                print("🛑 Stopping Rust engine...")
                self.rust_process.terminate()
                try:
                    self.rust_process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    self.rust_process.kill()

def main():
    """Main entry point"""
    print("🌍 Homeostatic City + BioCore - Integrated System")
    print("=" * 60)
    print("🦀 Rust Engine + 🧠 Python BioCore + 🌐 TypeScript Dashboard")
    print("=" * 60)
    
    system = IntegratedBHCSSystem()
    system.run_integrated_simulation()
    
    print("👋 Integrated system shutdown complete")

if __name__ == "__main__":
    main()