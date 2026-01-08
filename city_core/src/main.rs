use std::collections::HashMap;
use std::sync::{Arc, Mutex};
use tokio::time::{interval, Duration};
use warp::{Filter, Reply};
use serde::{Deserialize, Serialize};
use uuid::Uuid;
use chrono::{DateTime, Utc};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Zone {
    pub id: usize,
    pub activity: f64,
    pub state: ZoneState,
    pub name: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum ZoneState {
    CALM,
    OVERSTIMULATED,
    EMERGENT,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CityState {
    pub zones: Vec<Zone>,
    pub timestamp: DateTime<Utc>,
    pub system_health: f64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct BioCoreEffect {
    pub zone_id: usize,
    pub magnitude: f64,
    pub effects: Vec<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct InfluenceRequest {
    pub zone_id: usize,
    pub influence: f64,
}

pub struct HomeostaticEngine {
    zones: Vec<Zone>,
    ema: Vec<f64>,
    target: f64,
    eta: f64,
}

impl HomeostaticEngine {
    pub fn new() -> Self {
        let zones = vec![
            Zone { id: 0, activity: 0.3, state: ZoneState::CALM, name: "Downtown".to_string() },
            Zone { id: 1, activity: 0.6, state: ZoneState::OVERSTIMULATED, name: "Industrial".to_string() },
            Zone { id: 2, activity: 0.2, state: ZoneState::CALM, name: "Residential".to_string() },
            Zone { id: 3, activity: 0.8, state: ZoneState::EMERGENT, name: "Commercial".to_string() },
            Zone { id: 4, activity: 0.4, state: ZoneState::CALM, name: "Parks".to_string() },
        ];
        
        Self {
            ema: vec![0.5; zones.len()],
            target: 0.5,
            eta: 0.1,
            zones,
        }
    }
    
    pub fn update(&mut self) {
        for (i, zone) in self.zones.iter_mut().enumerate() {
            // EMA smoothing
            self.ema[i] = 0.97 * self.ema[i] + 0.03 * zone.activity;
            
            // Error-driven adjustment
            let error = self.target - self.ema[i];
            let adjustment = self.eta * error;
            
            zone.activity += adjustment;
            zone.activity = zone.activity.clamp(0.0, 1.0);
            
            // Update zone state
            zone.state = match zone.activity {
                x if x < 0.4 => ZoneState::CALM,
                x if x < 0.7 => ZoneState::OVERSTIMULATED,
                _ => ZoneState::EMERGENT,
            };
        }
    }
    
    pub fn apply_influence(&mut self, zone_id: usize, influence: f64) -> Result<(), String> {
        if zone_id >= self.zones.len() {
            return Err(format!("Zone {} not found", zone_id));
        }
        
        self.zones[zone_id].activity = (self.zones[zone_id].activity + influence).clamp(0.0, 1.0);
        Ok(())
    }
    
    pub fn apply_biocore_effect(&mut self, effect: BioCoreEffect) -> Result<(), String> {
        self.apply_influence(effect.zone_id, effect.magnitude)
    }
    
    pub fn get_state(&self) -> CityState {
        let system_health = self.zones.iter().map(|z| z.activity).sum::<f64>() / self.zones.len() as f64;
        
        CityState {
            zones: self.zones.clone(),
            timestamp: Utc::now(),
            system_health,
        }
    }
}

#[tokio::main]
async fn main() {
    env_logger::init();
    
    let engine = Arc::new(Mutex::new(HomeostaticEngine::new()));
    
    // Background update task
    let engine_clone = Arc::clone(&engine);
    tokio::spawn(async move {
        let mut interval = interval(Duration::from_secs(1));
        loop {
            interval.tick().await;
            let mut eng = engine_clone.lock().unwrap();
            eng.update();
        }
    });
    
    // CORS
    let cors = warp::cors()
        .allow_any_origin()
        .allow_headers(vec!["content-type"])
        .allow_methods(vec!["GET", "POST", "PUT", "DELETE"]);
    
    // GET /health
    let health = warp::path("health")
        .and(warp::get())
        .map(|| {
            warp::reply::json(&serde_json::json!({
                "status": "healthy",
                "timestamp": Utc::now(),
                "engine": "BHCS Rust Engine v0.1.0"
            }))
        });
    
    // GET /state
    let engine_state = Arc::clone(&engine);
    let state = warp::path("state")
        .and(warp::get())
        .and(warp::any().map(move || engine_state.clone()))
        .map(|engine: Arc<Mutex<HomeostaticEngine>>| {
            let eng = engine.lock().unwrap();
            let state = eng.get_state();
            warp::reply::json(&state)
        });
    
    // POST /biocore
    let engine_biocore = Arc::clone(&engine);
    let biocore = warp::path("biocore")
        .and(warp::post())
        .and(warp::body::json())
        .and(warp::any().map(move || engine_biocore.clone()))
        .map(|effect: BioCoreEffect, engine: Arc<Mutex<HomeostaticEngine>>| {
            let mut eng = engine.lock().unwrap();
            match eng.apply_biocore_effect(effect.clone()) {
                Ok(()) => warp::reply::json(&serde_json::json!({
                    "success": true,
                    "effect": effect,
                    "timestamp": Utc::now()
                })),
                Err(e) => warp::reply::json(&serde_json::json!({
                    "success": false,
                    "error": e,
                    "timestamp": Utc::now()
                }))
            }
        });
    
    // POST /influence
    let engine_influence = Arc::clone(&engine);
    let influence = warp::path("influence")
        .and(warp::post())
        .and(warp::body::json())
        .and(warp::any().map(move || engine_influence.clone()))
        .map(|req: InfluenceRequest, engine: Arc<Mutex<HomeostaticEngine>>| {
            let mut eng = engine.lock().unwrap();
            match eng.apply_influence(req.zone_id, req.influence) {
                Ok(()) => warp::reply::json(&serde_json::json!({
                    "success": true,
                    "zone_id": req.zone_id,
                    "influence": req.influence,
                    "timestamp": Utc::now()
                })),
                Err(e) => warp::reply::json(&serde_json::json!({
                    "success": false,
                    "error": e,
                    "timestamp": Utc::now()
                }))
            }
        });
    
    let routes = health
        .or(state)
        .or(biocore)
        .or(influence)
        .with(cors)
        .with(warp::log("bhcs_engine"));
    
    println!("🦀 BHCS Rust Engine starting on http://localhost:3030");
    println!("📊 Available endpoints:");
    println!("  GET  /health - Health check");
    println!("  GET  /state  - Get city state");
    println!("  POST /biocore - Apply BioCore effects");
    println!("  POST /influence - Apply direct influence");
    
    warp::serve(routes)
        .run(([127, 0, 0, 1], 3030))
        .await;
}