"""
Test suite for Homeostatic City + BioCore simulation.
"""

import unittest
import numpy as np
from src.city.sensor import CitySensor
from src.homeostasis.engine import HomeostaticEngine
from src.biocore.simulator import BioCore
from src.simulation.runner import SimulationRunner


class TestCitySensor(unittest.TestCase):
    """Test cases for CitySensor class."""
    
    def setUp(self):
        self.sensor = CitySensor(zones=3)
    
    def test_initialization(self):
        """Test sensor initialization."""
        self.assertEqual(self.sensor.zones, 3)
        self.assertEqual(len(self.sensor.activity), 3)
        self.assertEqual(len(self.sensor.zone_names), 3)
        self.assertTrue(all(0 <= a <= 1 for a in self.sensor.activity))
    
    def test_update_activity(self):
        """Test activity update."""
        initial_activity = self.sensor.activity.copy()
        updated_activity = self.sensor.update_activity()
        
        self.assertEqual(len(updated_activity), 3)
        self.assertTrue(all(0 <= a <= 1 for a in updated_activity))
        # Activity should change due to noise
        self.assertFalse(np.array_equal(initial_activity, updated_activity))


class TestHomeostaticEngine(unittest.TestCase):
    """Test cases for HomeostaticEngine class."""
    
    def setUp(self):
        self.engine = HomeostaticEngine(target=0.5, eta=0.01)
    
    def test_initialization(self):
        """Test engine initialization."""
        self.assertEqual(self.engine.target, 0.5)
        self.assertEqual(self.engine.eta, 0.01)
        self.assertIsNone(self.engine.ema)
    
    def test_update_first_time(self):
        """Test first update (EMA initialization)."""
        activity = np.array([0.3, 0.7, 0.5])
        result = self.engine.update(activity)
        
        self.assertIsNotNone(self.engine.ema)
        self.assertTrue(all(0 <= a <= 1 for a in result))
    
    def test_update_subsequent(self):
        """Test subsequent updates with EMA."""
        activity1 = np.array([0.3, 0.7, 0.5])
        activity2 = np.array([0.4, 0.6, 0.5])
        
        self.engine.update(activity1)
        result = self.engine.update(activity2)
        
        self.assertTrue(all(0 <= a <= 1 for a in result))


class TestBioCore(unittest.TestCase):
    """Test cases for BioCore class."""
    
    def setUp(self):
        self.biocore = BioCore(
            plants=["Ginkgo", "Aloe"],
            drugs=["DrugA", "DrugB"]
        )
    
    def test_initialization(self):
        """Test BioCore initialization."""
        self.assertEqual(len(self.biocore.plants), 2)
        self.assertEqual(len(self.biocore.drugs), 2)
        self.assertEqual(len(self.biocore._interaction_cache), 0)
    
    def test_simulate_interaction_valid(self):
        """Test valid plant-drug interaction."""
        score = self.biocore.simulate_interaction("Ginkgo", "DrugA")
        self.assertTrue(0 <= score <= 1)
    
    def test_simulate_interaction_invalid(self):
        """Test invalid plant-drug interaction."""
        with self.assertRaises(ValueError):
            self.biocore.simulate_interaction("Invalid", "DrugA")
    
    def test_zone_effect(self):
        """Test zone effect calculation."""
        effect = self.biocore.zone_effect(0.5)
        self.assertTrue(0 <= effect <= 1)
    
    def test_caching(self):
        """Test interaction result caching."""
        score1 = self.biocore.simulate_interaction("Ginkgo", "DrugA")
        score2 = self.biocore.simulate_interaction("Ginkgo", "DrugA")
        self.assertEqual(score1, score2)


class TestSimulationRunner(unittest.TestCase):
    """Test cases for SimulationRunner class."""
    
    def setUp(self):
        self.runner = SimulationRunner(zones=3, target_calmness=0.5, learning_rate=0.01)
    
    def test_initialization(self):
        """Test runner initialization."""
        self.assertEqual(self.runner.zones, 3)
        self.assertIsNotNone(self.runner.city)
        self.assertIsNotNone(self.runner.homeostasis)
        self.assertIsNotNone(self.runner.biocore)
    
    def test_run_step(self):
        """Test single simulation step."""
        result = self.runner.run_step(1)
        self.assertEqual(len(result), 3)
        self.assertTrue(all(0 <= a <= 1 for a in result))
    
    def test_reset(self):
        """Test simulation reset."""
        self.runner.run_step(1)
        self.runner.reset()
        self.assertIsNone(self.runner.homeostasis.ema)
        self.assertEqual(len(self.runner.biocore._interaction_cache), 0)


if __name__ == "__main__":
    unittest.main()
