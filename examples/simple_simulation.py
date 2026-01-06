"""
Homeostatic City + BioCore - Main Entry Point
Optimized for Codeium/Windsurf
Author: Lunar Lab

Description:
- Simulates city zones with calm, overstimulated, and emergent behavior
- Integrates BioCore plant-drug simulation (placeholder ML model)
- Uses homeostatic slow learning to maintain balance
- Fully modular and annotated for easy expansion
"""

from src.simulation.runner import SimulationRunner


def main():
    """
    Main entry point for the Homeostatic City + BioCore simulation.
    """
    # Initialize simulation with custom parameters
    runner = SimulationRunner(
        zones=5,              # Number of city zones
        target_calmness=0.5,  # Target activity level
        learning_rate=0.02    # Homeostatic learning rate
    )
    
    # Run the simulation
    runner.run_simulation(
        iterations=15,    # Number of time steps
        delay=0.5,        # Delay between steps (seconds)
        show_summary=True # Show final summary
    )


if __name__ == "__main__":
    main()
