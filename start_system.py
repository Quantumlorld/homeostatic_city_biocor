"""
System startup script for Homeostatic City + BioCore
Starts all components in the correct order
"""

import subprocess
import time
import sys
import os
from pathlib import Path


def check_rust_installation():
    """Check if Rust is installed and available."""
    try:
        result = subprocess.run(['rustc', '--version'], 
                              capture_output=True, text=True, timeout=5)
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def start_rust_engine():
    """Start the Rust homeostatic engine."""
    print("🦀 Starting Rust homeostatic engine...")
    
    if not check_rust_installation():
        print("❌ Rust not found. Please install Rust from https://rustup.rs/")
        return None
    
    try:
        # Change to city_core directory
        city_core_path = Path("city_core")
        if not city_core_path.exists():
            print("❌ city_core directory not found")
            return None
        
        # Start Rust engine
        process = subprocess.Popen(
            ['cargo', 'run'],
            cwd=city_core_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait a bit for startup
        time.sleep(3)
        
        if process.poll() is None:
            print("✅ Rust engine started successfully")
            return process
        else:
            stdout, stderr = process.communicate()
            print(f"❌ Rust engine failed to start:")
            print(f"STDOUT: {stdout}")
            print(f"STDERR: {stderr}")
            return None
            
    except Exception as e:
        print(f"❌ Failed to start Rust engine: {e}")
        return None


def open_dashboard():
    """Open the TypeScript dashboard in browser."""
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


def run_python_integration():
    """Run the Python integration simulation."""
    print("🧠 Starting Python integration...")
    
    try:
        result = subprocess.run([sys.executable, 'main_integrated.py'], 
                              timeout=60)
        return result.returncode == 0
        
    except subprocess.TimeoutExpired:
        print("⏰ Python integration timed out")
        return False
    except Exception as e:
        print(f"❌ Python integration failed: {e}")
        return False


def main():
    """Main startup sequence."""
    print("🌍 Homeostatic City + BioCore - System Startup")
    print("=" * 50)
    
    # Step 1: Start Rust engine
    rust_process = start_rust_engine()
    if rust_process is None:
        print("❌ Cannot proceed without Rust engine")
        return 1
    
    # Step 2: Open dashboard
    dashboard_opened = open_dashboard()
    
    # Step 3: Wait for user input or auto-run Python
    try:
        print("\n🚀 System ready!")
        print("Press Enter to start Python integration, or Ctrl+C to exit...")
        input()
        
        # Run Python integration
        success = run_python_integration()
        if success:
            print("✅ Python integration completed successfully")
        else:
            print("❌ Python integration failed")
            
    except KeyboardInterrupt:
        print("\n👋 Shutting down...")
    
    finally:
        # Clean up Rust process
        if rust_process:
            print("🛑 Stopping Rust engine...")
            rust_process.terminate()
            try:
                rust_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                rust_process.kill()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
