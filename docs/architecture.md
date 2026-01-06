# Homeostatic City + BioCore Architecture

## Overview

The Homeostatic City + BioCore simulation is a modular framework that combines urban dynamics with biological interaction modeling. The architecture follows a clean separation of concerns, making it easy to extend and maintain.

## Project Structure

```
homeostatic_city_biocore/
├── main.py                 # Entry point
├── requirements.txt        # Dependencies
├── README.md              # Project documentation
├── src/                   # Source code
│   ├── __init__.py
│   ├── city/              # City simulation module
│   │   ├── __init__.py
│   │   └── sensor.py      # CitySensor class
│   ├── homeostasis/       # Homeostatic learning module
│   │   ├── __init__.py
│   │   └── engine.py      # HomeostaticEngine class
│   ├── biocore/           # BioCore simulation module
│   │   ├── __init__.py
│   │   └── simulator.py   # BioCore class
│   ├── visualization/     # Display module
│   │   ├── __init__.py
│   │   └── display.py     # Visualization functions
│   └── simulation/        # Simulation orchestration
│       ├── __init__.py
│       └── runner.py      # SimulationRunner class
├── tests/                 # Test suite
│   └── test_simulation.py
├── config/                # Configuration
│   └── settings.py        # Default parameters
├── docs/                  # Documentation
│   └── architecture.md
└── data/                  # Data files (future use)
```

## Core Components

### 1. City Module (`src/city/`)

**CitySensor**: Simulates urban activity across multiple zones
- Tracks activity levels (0-1) for each zone
- Introduces realistic noise and fluctuations
- Provides zone naming and activity management

### 2. Homeostasis Module (`src/homeostasis/`)

**HomeostaticEngine**: Implements slow learning for system balance
- Uses Exponential Moving Average (EMA) for smoothing
- Gradually adjusts activity toward target levels
- Maintains system stability through controlled learning

### 3. BioCore Module (`src/biocore/`)

**BioCore**: Simulates plant-drug synergy interactions
- Placeholder for future ML model integration
- Caches interaction results for consistency
- Maps biological effects to city zones

### 4. Visualization Module (`src/visualization/`)

**Display Functions**: Console-based visualization
- Color-coded zone states (CALM 🟢, OVERSTIMULATED 🟡, EMERGENT 🔴)
- Summary statistics and reporting
- Real-time state updates

### 5. Simulation Module (`src/simulation/`)

**SimulationRunner**: Orchestrates the complete simulation
- Coordinates all modules in time-step loop
- Handles simulation lifecycle and state management
- Provides configurable parameters and reset functionality

## Data Flow

```
1. CitySensor.update_activity()
   ↓
2. HomeostaticEngine.update()
   ↓
3. BioCore effects application
   ↓
4. Visualization.display_city()
   ↓
5. Repeat for next time step
```

## Key Design Principles

### Modularity
- Each module has a single responsibility
- Clear interfaces between components
- Easy to test and maintain individual parts

### Extensibility
- Plugin architecture for new features
- Configuration-driven parameters
- Placeholder for ML model integration

### Type Safety
- Type hints throughout the codebase
- Clear parameter and return types
- Comprehensive error handling

### Performance
- Efficient numpy operations
- Minimal memory footprint
- Configurable simulation parameters

## Future Enhancements

### ML Integration
- Replace BioCore random scoring with trained models
- Implement reinforcement learning for homeostatic control
- Add predictive analytics for city dynamics

### Advanced Visualization
- Web-based dashboard using TypeScript/React
- Real-time data streaming
- Interactive zone management

### Performance Optimization
- Rust engine integration for heavy computations
- Parallel processing for multiple zones
- GPU acceleration for ML models

### Data Management
- Historical data storage and analysis
- Export capabilities for external tools
- Configuration file support

## Configuration

All simulation parameters are centralized in `config/settings.py`:
- Default simulation values
- Module-specific constants
- Visualization thresholds
- Easy customization without code changes

## Testing

Comprehensive test suite in `tests/test_simulation.py`:
- Unit tests for all major components
- Integration tests for simulation flow
- Edge case and error handling validation
- Automated testing with unittest framework
