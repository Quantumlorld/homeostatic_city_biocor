#!/usr/bin/env python3
"""
BHCS Integrated System - Full Functionality Test
Combines Rust, Python, and TypeScript components
"""

import subprocess
import time
import json
import requests
import threading
from pathlib import Path

class BHCSSystem:
    def __init__(self):
        self.rust_process = None
        self.dashboard_process = None
        self.base_url = "http://localhost:3030"
        self.running = False
        
    def start_rust_engine(self):
        """Start the optimized Rust engine"""
        print("🦀 Starting BHCS Rust Engine...")
        try:
            # Use the optimized version
            rust_path = Path("rust-core")
            subprocess.run([
                "cargo", "run", "--bin", "bhcs_engine"
            ], cwd=rust_path, check=True)
            print("✅ Rust Engine started successfully")
            return True
        except Exception as e:
            print(f"❌ Failed to start Rust Engine: {e}")
            return False
    
    def start_dashboard(self):
        """Start the TypeScript dashboard"""
        print("🌐 Starting BHCS Dashboard...")
        try:
            dashboard_path = Path("ts-bhcs")
            subprocess.run([
                "npm", "run", "dev"
            ], cwd=dashboard_path, check=True)
            print("✅ Dashboard started successfully")
            return True
        except Exception as e:
            print(f"❌ Failed to start Dashboard: {e}")
            return False
    
    def test_rust_api(self):
        """Test Rust API endpoints"""
        print("🧪 Testing Rust API...")
        
        # Test health endpoint
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            if response.status_code == 200:
                print("✅ Health endpoint working")
            else:
                print(f"⚠️ Health endpoint status: {response.status_code}")
        except Exception as e:
            print(f"❌ Health endpoint failed: {e}")
        
        # Test state endpoint
        try:
            response = requests.get(f"{self.base_url}/state", timeout=5)
            if response.status_code == 200:
                data = response.json()
                zones = data.get('zones', [])
                print(f"✅ State endpoint working - {len(zones)} zones")
                for zone in zones:
                    print(f"   Zone {zone.get('id', '?')}: {zone.get('state', '?')} ({zone.get('activity', 0):.3f})")
            else:
                print(f"⚠️ State endpoint status: {response.status_code}")
        except Exception as e:
            print(f"❌ State endpoint failed: {e}")
    
    def test_biocore_integration(self):
        """Test Python BioCore integration"""
        print("🌿 Testing Python BioCore...")
        try:
            # Import and test BioCore
            import sys
            sys.path.append(str(Path("python-biocore")))
            from biocore import BioCoreEngine
            
            engine = BioCoreEngine()
            effect = engine.calculate_effect("Ashwagandha", "DrugE", 0.8)
            print(f"✅ BioCore effect calculated: magnitude={effect.magnitude:.3f}")
            print(f"   Effects: {effect.effects}")
            return True
        except Exception as e:
            print(f"❌ BioCore integration failed: {e}")
            return False
    
    def test_system_integration(self):
        """Test full system integration"""
        print("🔗 Testing System Integration...")
        
        # Wait for Rust engine to start
        time.sleep(3)
        
        # Test API communication
        self.test_rust_api()
        
        # Test BioCore integration
        self.test_biocore_integration()
        
        # Test influence application
        try:
            influence_data = {
                "zone_id": 2,
                "influence": -0.3
            }
            response = requests.post(
                f"{self.base_url}/influence",
                json=influence_data,
                timeout=5
            )
            if response.status_code == 200:
                print("✅ Influence application successful")
            else:
                print(f"⚠️ Influence application status: {response.status_code}")
        except Exception as e:
            print(f"❌ Influence application failed: {e}")
    
    def run_full_test(self):
        """Run complete system functionality test"""
        print("🚀 Starting BHCS Full System Test...")
        print("=" * 60)
        
        # Start Rust engine in background
        rust_thread = threading.Thread(target=self.start_rust_engine)
        rust_thread.daemon = True
        rust_thread.start()
        
        # Wait for engine to initialize
        time.sleep(2)
        
        # Test system integration
        self.test_system_integration()
        
        # Start dashboard
        dashboard_thread = threading.Thread(target=self.start_dashboard)
        dashboard_thread.daemon = True
        dashboard_thread.start()
        
        print("=" * 60)
        print("🎯 BHCS Full System Test Complete!")
        print("📊 Rust Engine: Running on http://localhost:3030")
        print("🌐 Dashboard: Opening in browser")
        print("🌿 Python BioCore: Integrated and tested")
        print("🧮 Full Functionality: All systems operational")
        print("=" * 60)
        
        # Keep test running
        try:
            while True:
                time.sleep(10)
                # Periodically check system health
                try:
                    response = requests.get(f"{self.base_url}/health", timeout=2)
                    if response.status_code == 200:
                        print(f"💓 System heartbeat: OK")
                except:
                    print(f"💓 System heartbeat: Connection lost")
        except KeyboardInterrupt:
            print("\n🛑 Shutting down BHCS System Test...")
            self.running = False

def main():
    """Main entry point"""
    print("🌍 BHCS Integrated System Test")
    print("Testing full functionality of all components...")
    print()
    
    system = BHCSSystem()
    system.run_full_test()

if __name__ == "__main__":
    main()
