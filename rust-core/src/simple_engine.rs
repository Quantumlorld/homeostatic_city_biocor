//! BHCS Simple Engine - No External Dependencies
//! Pure Rust implementation for guaranteed execution

use std::time::{SystemTime, UNIX_EPOCH};

#[derive(Debug, Clone)]
pub struct Zone {
    pub id: usize,
    pub activity: f64,
    pub target: f64,
    pub state: String,
}

impl Zone {
    pub fn new(id: usize) -> Self {
        let activity = (id as f64 * 0.1 + 0.3).min(0.9);
        let state = Self::determine_state(activity);
        
        Self {
            id,
            activity,
            target: 0.5,
            state,
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
        let error = self.target - self.activity;
        let adjustment = learning_rate * error;
        self.activity = (self.activity + adjustment).clamp(0.0, 1.0);
        self.state = Self::determine_state(self.activity);
    }
    
    pub fn apply_influence(&mut self, influence: f64) {
        self.activity = (self.activity + influence).clamp(0.0, 1.0);
        self.state = Self::determine_state(self.activity);
    }
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
    
    pub fn get_system_health(&self) -> f64 {
        let calm_zones = self.zones.iter()
            .filter(|z| z.state == "CALM")
            .count() as f64;
        calm_zones / self.zones.len() as f64
    }
    
    pub fn get_average_activity(&self) -> f64 {
        self.zones.iter()
            .map(|z| z.activity)
            .sum::<f64>() / self.zones.len() as f64
    }
    
    pub fn print_status(&self) {
        println!("\n📊 BHCS System Status:");
        println!("─" * 50);
        
        for zone in &self.zones {
            let emoji = match zone.state.as_str() {
                "CALM" => "🟢",
                "OVERSTIMULATED" => "🟡",
                "EMERGENT" => "🔴",
                "CRITICAL" => "🟣",
                _ => "⚪",
            };
            
            println!("Zone {}: {} {:.3} - {}", 
                     zone.id, emoji, zone.activity, zone.state);
        }
        
        println!("─" * 50);
        println!("System Health: {:.1}%", self.get_system_health() * 100.0);
        println!("Avg Activity: {:.3}", self.get_average_activity());
        println!("Timestamp: {}", SystemTime::now()
                .duration_since(UNIX_EPOCH)
                .unwrap()
                .as_secs());
    }
    
    pub fn reset(&mut self) {
        for zone in &mut self.zones {
            *zone = Zone::new(zone.id);
        }
    }
}

fn main() {
    println!("🦀 BHCS Simple Engine Starting...");
    println!("🎯 Pure Rust Implementation - No External Dependencies");
    println!("📊 Real-time Homeostatic Regulation System");
    println!();
    
    let mut bhcs = BHCS::new(5);
    let mut update_counter = 0;
    
    println!("🚀 System Initialized - Starting Homeostatic Regulation");
    println!("💓 Heartbeat: Every 5 seconds");
    println!("🌿 BioCore Integration: Ready");
    println!("🎛️ Interactive Controls: Available");
    println!();
    
    loop {
        // Update system
        bhcs.update();
        update_counter += 1;
        
        // Print status every 5 seconds
        if update_counter % 5 == 0 {
            bhcs.print_status();
            
            // Simulate BioCore influence
            if bhcs.get_system_health() < 0.6 {
                println!("🌿 Applying BioCore influence to improve system health...");
                bhcs.apply_influence(2, -0.2); // Calm zone 2
            }
            
            // Random fluctuations
            use std::collections::hash_map::DefaultHasher;
            use std::hash::{Hash, Hasher};
            let mut hasher = DefaultHasher::new();
            SystemTime::now().duration_since(UNIX_EPOCH).unwrap().as_secs().hash(&mut hasher);
            let random = (hasher.finish() % 100) as f64 / 100.0;
            
            if random < 0.3 {
                let zone_id = (random * 5.0) as usize;
                let influence = (random - 0.5) * 0.3;
                bhcs.apply_influence(zone_id, influence);
                println!("🎲 Random influence: Zone {} -> {:.3}", zone_id, influence);
            }
        }
        
        // Reset every 30 seconds
        if update_counter % 30 == 0 {
            println!("🔄 System Reset - Starting Fresh Cycle");
            bhcs.reset();
        }
        
        std::thread::sleep(std::time::Duration::from_secs(1));
    }
}
