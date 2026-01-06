"""
Configuration settings for Homeostatic City + BioCore simulation.
"""

# Simulation defaults
DEFAULT_ZONES = 5
DEFAULT_ITERATIONS = 20
DEFAULT_TARGET_CALMNESS = 0.5
DEFAULT_LEARNING_RATE = 0.02
DEFAULT_DELAY = 0.5

# City simulation parameters
ACTIVITY_NOISE_MEAN = 0.0
ACTIVITY_NOISE_STD = 0.05
ACTIVITY_MIN = 0.0
ACTIVITY_MAX = 1.0

# Homeostatic engine parameters
EMA_ALPHA = 0.97  # EMA smoothing factor
EMA_BETA = 0.03   # New data weight

# BioCore parameters
DEFAULT_PLANTS = ["Ginkgo", "Aloe", "Turmeric", "Ginseng", "Ashwagandha"]
DEFAULT_DRUGS = ["DrugA", "DrugB", "DrugC", "DrugD", "DrugE"]
BIO_EFFECT_WEIGHT = 0.05
ZONE_EFFECT_WEIGHT = 0.03

# Visualization parameters
ZONE_THRESHOLDS = {
    "calm": 0.4,
    "overstimulated": 0.7
}

ZONE_STATES = {
    "calm": ("CALM", "🟢"),
    "overstimulated": ("OVERSTIMULATED", "🟡"),
    "emergent": ("EMERGENT", "🔴")
}
