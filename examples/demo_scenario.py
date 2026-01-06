"""
Homeostatic City + BioCore - Integrated Entry Point
Python BioCore + Rust Engine + TypeScript Dashboard
"""

from src.simulation.integrated_runner import IntegratedSimulationRunner


def main():
    """Main entry point for integrated simulation."""
    print("🌍 Homeostatic City + BioCore - Integrated Architecture")
    print("=" * 60)
    print("🦀 Rust Engine: http://localhost:3030")
    print("🌐 Dashboard: dashboard/index.html")
    print("🧪 Python BioCore: Integrated")
    print("=" * 60)
    
    # Initialize integrated simulation
    runner = IntegratedSimulationRunner()
    
    # Run simulation with Rust engine
    runner.run_integrated_simulation(
        iterations=30,
        delay=1.0
    )


if __name__ == "__main__":
    main()
