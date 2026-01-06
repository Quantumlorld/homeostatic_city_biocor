use serde::{Deserialize, Serialize};
use std::sync::{Arc, Mutex};
use warp::Filter;

#[derive(Serialize, Deserialize, Clone, Debug)]
struct Zone {
    id: usize,
    activity: f32, // 0.0 calm -> 1.0 emergent
}

#[derive(Serialize, Deserialize, Clone, Debug)]
struct BioCoreInput {
    zone: usize,
    plant: String,
    drug: String,
    synergy: f32,
}

#[derive(Clone)]
struct CityState {
    zones: Vec<Zone>,
    target: f32,
    eta: f32,
    ema: Vec<f32>,
}

impl CityState {
    fn new(zones_count: usize, target: f32, eta: f32) -> Self {
        let zones: Vec<Zone> = (0..zones_count)
            .map(|i| Zone { 
                id: i, 
                activity: rand::random::<f32>() 
            })
            .collect();
        
        let ema = zones.iter().map(|z| z.activity).collect();
        
        Self {
            zones,
            target,
            eta,
            ema,
        }
    }
    
    fn homeostatic_update(&mut self) {
        for (i, zone) in self.zones.iter_mut().enumerate() {
            // Update EMA with current activity
            self.ema[i] = 0.97 * self.ema[i] + 0.03 * zone.activity;
            
            // Compute error and adjustment
            let error = self.target - self.ema[i];
            let adjustment = self.eta * error;
            
            // Apply adjustment with bounds checking
            zone.activity += adjustment;
            zone.activity = zone.activity.clamp(0.0, 1.0);
        }
    }
    
    fn apply_biocore_effect(&mut self, input: BioCoreInput) {
        if let Some(zone) = self.zones.get_mut(input.zone) {
            // Apply BioCore synergy effect
            // High synergy reduces overstimulation
            let effect = if zone.activity > 0.7 {
                // Dampen overstimulated zones
                -0.05 * input.synergy
            } else if zone.activity < 0.4 {
                // Slightly activate calm zones
                0.03 * input.synergy
            } else {
                // Minimal effect on balanced zones
                0.01 * (input.synergy - 0.5)
            };
            
            zone.activity += effect;
            zone.activity = zone.activity.clamp(0.0, 1.0);
        }
    }
    
    fn get_zone_state(&self, activity: f32) -> &'static str {
        if activity < 0.4 {
            "CALM"
        } else if activity < 0.7 {
            "OVERSTIMULATED"
        } else {
            "EMERGENT"
        }
    }
}

#[tokio::main]
async fn main() {
    // Initialize city state with 5 zones
    let state = Arc::new(Mutex::new(CityState::new(5, 0.5, 0.02)));

    let state_filter = warp::any().map(move || state.clone());

    // GET /state - Get current city state and update homeostasis
    let state_route = warp::path("state")
        .and(warp::get())
        .and(state_filter.clone())
        .map(|state: Arc<Mutex<CityState>>| {
            let mut s = state.lock().unwrap();
            s.homeostatic_update();
            
            let response: Vec<_> = s.zones.iter().map(|z| {
                serde_json::json!({
                    "id": z.id,
                    "activity": z.activity,
                    "state": s.get_zone_state(z.activity)
                })
            }).collect();
            
            warp::reply::json(&response)
        });

    // POST /biocore - Apply BioCore effects
    let biocore_route = warp::path("biocore")
        .and(warp::post())
        .and(warp::body::json())
        .and(state_filter.clone())
        .map(|input: BioCoreInput, state: Arc<Mutex<CityState>>| {
            let mut s = state.lock().unwrap();
            s.apply_biocore_effect(input);
            
            warp::reply::json(&serde_json::json!({
                "status": "success",
                "message": "BioCore effect applied"
            }))
        });

    // GET /health - Health check endpoint
    let health_route = warp::path("health")
        .and(warp::get())
        .map(|| {
            warp::reply::json(&serde_json::json!({
                "status": "healthy",
                "service": "city_core",
                "version": "0.1.0"
            }))
        });

    // Combine all routes
    let routes = state_route
        .or(biocore_route)
        .or(health_route)
        .with(warp::cors().allow_any_origin().allow_methods(vec!["GET", "POST"]));

    println!("🦀 Rust city core running at http://localhost:3030");
    println!("📊 Available endpoints:");
    println!("   GET  /state   - Get city state");
    println!("   POST /biocore - Apply BioCore effects");
    println!("   GET  /health  - Health check");

    warp::serve(routes)
        .run(([127, 0, 0, 1], 3030))
        .await;
}
