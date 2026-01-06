//! Homeostatic Engine Implementation
//! 
//! Core regulation logic for BHCS deterministic control

use serde::{Deserialize, Serialize};
use crate::zone::Zone;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct HomeostaticConfig {
    pub target_calmness: f64,
    pub learning_rate: f64,
    pub zones: usize,
}

impl Default for HomeostaticConfig {
    fn default() -> Self {
        Self {
            target_calmness: 0.5,
            learning_rate: 0.02,
            zones: 5,
        }
    }
}

#[derive(Debug, Clone)]
pub struct HomeostaticEngine {
    zones: Vec<Zone>,
    config: HomeostaticConfig,
}

impl HomeostaticEngine {
    pub fn new(config: HomeostaticConfig) -> Self {
        let mut zones = Vec::new();
        for i in 0..config.zones {
            zones.push(Zone::new(i));
        }
        
        Self { zones, config }
    }

    pub fn update(&mut self) {
        for zone in &mut self.zones {
            // Apply homeostatic update equation
            let error = self.config.target_calmness - zone.activity();
            let adjustment = self.config.learning_rate * error;
            zone.apply_adjustment(adjustment);
        }
    }

    pub fn apply_influence(&mut self, zone_id: usize, influence: f64) {
        if let Some(zone) = self.zones.get_mut(zone_id) {
            zone.apply_influence(influence);
        }
    }

    pub fn get_zones(&self) -> &[Zone] {
        &self.zones
    }

    pub fn get_zone(&self, zone_id: usize) -> Option<&Zone> {
        self.zones.get(zone_id)
    }

    pub fn get_system_metrics(&self) -> SystemMetrics {
        let avg_activity = self.zones.iter()
            .map(|z| z.activity())
            .sum::<f64>() / self.zones.len() as f64;

        let homeostatic_balance = (avg_activity - self.config.target_calmness).abs();

        SystemMetrics {
            average_activity: avg_activity,
            total_zones: self.zones.len(),
            homeostatic_balance,
            timestamp: chrono::Utc::now().timestamp(),
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SystemMetrics {
    pub average_activity: f64,
    pub total_zones: usize,
    pub homeostatic_balance: f64,
    pub timestamp: i64,
}
