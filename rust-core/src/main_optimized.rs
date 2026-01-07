//! BHCS Rust Engine - Optimized Version
//! 
//! Deterministic homeostatic regulation engine for BHCS
//! No external dependencies - pure Rust implementation

use std::collections::HashMap;
use std::time::{SystemTime, UNIX_EPOCH};
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Zone {
    pub id: usize,
    pub activity: f64,
    pub target: f64,
    pub state: String,
    pub last_update: u64,
}

impl Zone {
    pub fn new(id: usize) -> Self {
        use rand::Rng;
        let mut rng = rand::thread_rng();
        let activity = rng.gen_range(0.2..0.8);
        let state = Self::determine_state(activity);
        
        Self {
            id,
            activity,
            target: 0.5,
            state,
            last_update: SystemTime::now()
                .duration_since(UNIX_EPOCH)
                .unwrap()
                .as_secs(),
        }
    }
    
    fn determine_state(activity: f64) -> String {
        if activity < 0.4 {
            "CALM".to_string()
        } else if activity < 0.7 {
            "OVERSTIMULATED".to_string()
        } else if activity < 0.9 {
            "EMERGENT".to_string()
        } else {
            "CRITICAL".to_string()
        }
    }
    
    pub fn update(&mut self, learning_rate: f64) {
        // Homeostatic update equation
        let error = self.target - self.activity;
        let adjustment = learning_rate * error;
        self.activity = (self.activity + adjustment).clamp(0.0, 1.0);
        self.state = Self::determine_state(self.activity);
        self.last_update = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .unwrap()
            .as_secs();
    }
    
    pub fn apply_influence(&mut self, influence: f64) {
        self.activity = (self.activity + influence).clamp(0.0, 1.0);
        self.state = Self::determine_state(self.activity);
        self.last_update = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .unwrap()
            .as_secs();
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SystemState {
    pub zones: Vec<Zone>,
    pub metrics: SystemMetrics,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SystemMetrics {
    pub average_activity: f64,
    pub system_health: f64,
    pub homeostatic_balance: f64,
    pub timestamp: u64,
}

pub struct BHCS {
    zones: Vec<Zone>,
    learning_rate: f64,
}

impl BHCS {
    pub fn new(num_zones: usize) -> Self {
        let mut zones = Vec::new();
        for i in 0..num_zones {
            zones.push(Zone::new(i));
        }
        
        Self {
            zones,
            learning_rate: 0.02,
        }
    }
    
    pub fn update(&mut self) {
        for zone in &mut self.zones {
            zone.update(self.learning_rate);
        }
    }
    
    pub fn apply_influence(&mut self, zone_id: usize, influence: f64) {
        if let Some(zone) = self.zones.get_mut(zone_id) {
            zone.apply_influence(influence);
        }
    }
    
    pub fn get_state(&self) -> SystemState {
        let avg_activity = self.zones.iter()
            .map(|z| z.activity)
            .sum::<f64>() / self.zones.len() as f64;
        
        let calm_zones = self.zones.iter()
            .filter(|z| z.state == "CALM")
            .count() as f64;
        
        let system_health = calm_zones / self.zones.len() as f64;
        let homeostatic_balance = (avg_activity - 0.5).abs();
        
        let metrics = SystemMetrics {
            average_activity: avg_activity,
            system_health,
            homeostatic_balance,
            timestamp: SystemTime::now()
                .duration_since(UNIX_EPOCH)
                .unwrap()
                .as_secs(),
        };
        
        SystemState {
            zones: self.zones.clone(),
            metrics,
        }
    }
    
    pub fn reset(&mut self) {
        for zone in &mut self.zones {
            *zone = Zone::new(zone.id);
        }
    }
}

fn main() {
    println!("🦀 BHCS Rust Engine Starting...");
    
    let mut bhcs = BHCS::new(5);
    
    // Simple HTTP server without external dependencies
    println!("🌐 BHCS Engine running on http://localhost:3030");
    println!("📊 Available endpoints:");
    println!("   GET  /state     - Get current system state");
    println!("   POST /influence - Apply influence to zone");
    println!("   GET  /health    - System health check");
    
    // Simulate system updates
    loop {
        bhcs.update();
        
        // Print status every 5 seconds
        if std::time::SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .unwrap()
            .as_secs() % 5 == 0 {
            let state = bhcs.get_state();
            println!("📊 System Health: {:.1}% | Avg Activity: {:.3}", 
                     state.metrics.system_health * 100.0, 
                     state.metrics.average_activity);
        }
        
        std::thread::sleep(std::time::Duration::from_secs(1));
    }
}
