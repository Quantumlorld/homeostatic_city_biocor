use std::collections::HashMap;
use std::sync::{Arc, Mutex};
use std::time::{Duration, Instant};
use axum::{
    extract::{Path, Query, State},
    http::StatusCode,
    response::Json,
    routing::{get, post},
    Router,
};
use serde::{Deserialize, Serialize};
use tokio::time::sleep;
use tower::ServiceBuilder;
use tower_http::cors::{Any, CorsLayer};
use tracing_subscriber;

use crate::luna_evolution::{LunaEvolutionEngine, Conversation, InteractionType, ZoneContext, BioCoreEffect, EffectType};

#[derive(Debug, Serialize, Deserialize)]
pub struct LunaRequest {
    pub user_message: String,
    pub zone_context: Option<ZoneContext>,
    pub interaction_type: String,
    pub user_id: Option<String>,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct LunaResponse {
    pub luna_response: String,
    pub personality: crate::luna_evolution::LunaPersonality,
    pub processing_time_ms: u64,
    pub evolution_metrics: crate::luna_evolution::EvolutionMetrics,
    pub zone_recommendations: Vec<ZoneRecommendation>,
    pub biocore_suggestions: Vec<BioCoreSuggestion>,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct ZoneRecommendation {
    pub zone_name: String,
    pub current_status: String,
    pub recommended_action: String,
    pub priority: u8,
    pub expected_improvement: f64,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct BioCoreSuggestion {
    pub plant_name: String,
    pub drug_name: String,
    pub synergy_score: f64,
    pub effect_type: String,
    pub target_zones: Vec<String>,
    pub effectiveness_prediction: f64,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct ZoneData {
    pub zone_name: String,
    pub activity_level: f64,
    pub stress_level: f64,
    pub population_density: f64,
    pub primary_function: String,
    pub last_updated: chrono::DateTime<chrono::Utc>,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct SystemStatus {
    pub luna_status: String,
    pub total_interactions: u64,
    pub intelligence_level: String,
    pub system_health: f64,
    pub zones_monitored: u8,
    pub api_response_time_ms: u64,
    pub evolution_progress: f64,
}

pub struct FastApiServer {
    luna_engine: Arc<LunaEvolutionEngine>,
    zone_data: Arc<Mutex<HashMap<String, ZoneData>>>,
    start_time: Instant,
}

impl FastApiServer {
    pub fn new() -> Self {
        let luna_engine = Arc::new(LunaEvolutionEngine::new());
        let zone_data = Arc::new(Mutex::new(HashMap::new()));
        
        // Initialize zone data
        {
            let mut zones = zone_data.lock().unwrap();
            zones.insert("Downtown".to_string(), ZoneData {
                zone_name: "Downtown".to_string(),
                activity_level: 0.65,
                stress_level: 0.35,
                population_density: 0.8,
                primary_function: "Business, Commerce, Entertainment".to_string(),
                last_updated: chrono::Utc::now(),
            });
            
            zones.insert("Industrial".to_string(), ZoneData {
                zone_name: "Industrial".to_string(),
                activity_level: 0.78,
                stress_level: 0.62,
                population_density: 0.6,
                primary_function: "Manufacturing, Logistics, Production".to_string(),
                last_updated: chrono::Utc::now(),
            });
            
            zones.insert("Residential".to_string(), ZoneData {
                zone_name: "Residential".to_string(),
                activity_level: 0.42,
                stress_level: 0.25,
                population_density: 0.7,
                primary_function: "Housing, Community Services".to_string(),
                last_updated: chrono::Utc::now(),
            });
            
            zones.insert("Commercial".to_string(), ZoneData {
                zone_name: "Commercial".to_string(),
                activity_level: 0.71,
                stress_level: 0.38,
                population_density: 0.9,
                primary_function: "Retail, Services, Offices".to_string(),
                last_updated: chrono::Utc::now(),
            });
            
            zones.insert("Parks".to_string(), ZoneData {
                zone_name: "Parks".to_string(),
                activity_level: 0.28,
                stress_level: 0.15,
                population_density: 0.3,
                primary_function: "Recreation, Relaxation, Nature".to_string(),
                last_updated: chrono::Utc::now(),
            });
        }
        
        Self {
            luna_engine,
            zone_data,
            start_time: Instant::now(),
        }
    }

    pub fn create_router(&self) -> Router {
        let luna_engine = self.luna_engine.clone();
        let zone_data = self.zone_data.clone();
        
        Router::new()
            .route("/", get(root_handler))
            .route("/api/luna/chat", post(chat_handler))
            .route("/api/luna/evolve", post(evolve_handler))
            .route("/api/zones", get(zones_handler))
            .route("/api/zones/:zone_name", get(zone_handler))
            .route("/api/zones/:zone_name/update", post(update_zone_handler))
            .route("/api/system/status", get(system_status_handler))
            .route("/api/biocore/recommendations", get(biocore_recommendations_handler))
            .route("/api/evolution/metrics", get(evolution_metrics_handler))
            .route("/api/health", get(health_handler))
            .layer(
                CorsLayer::new()
                    .allow_origin(Any)
                    .allow_methods(Any)
                    .allow_headers(Any),
            )
            .with_state(luna_engine)
            .with_state(zone_data)
    }

    pub async fn start_zone_updates(&self) {
        let zone_data = self.zone_data.clone();
        let luna_engine = self.luna_engine.clone();
        
        tokio::spawn(async move {
            let mut interval = tokio::time::interval(Duration::from_secs(5));
            
            loop {
                interval.tick().await;
                
                // Update zone data with random variations
                {
                    let mut zones = zone_data.lock().unwrap();
                    for (zone_name, zone) in zones.iter_mut() {
                        // Add random variations to simulate real-time changes
                        zone.activity_level = (zone.activity_level + (rand::random::<f64>() - 0.5) * 0.1).max(0.1).min(1.0);
                        zone.stress_level = (zone.stress_level + (rand::random::<f64>() - 0.5) * 0.1).max(0.1).min(1.0);
                        zone.last_updated = chrono::Utc::now();
                    }
                }
                
                // Trigger Luna's learning process
                let _ = luna_engine.apply_learning(
                    "system_update",
                    "Zone data updated with real-time variations",
                    None,
                ).await;
            }
        });
    }
}

async fn root_handler() -> &'static str {
    "🌙 LunaBeyond AI Fast API Server - Professional City Management System\n\nEndpoints:\n- GET /api/zones - Get all zones\n- GET /api/zones/:zone_name - Get specific zone\n- POST /api/luna/chat - Chat with Luna\n- POST /api/luna/evolve - Trigger evolution\n- GET /api/system/status - Get system status\n- GET /api/biocore/recommendations - Get BioCore recommendations\n- GET /api/evolution/metrics - Get evolution metrics\n- GET /api/health - Health check"
}

async fn chat_handler(
    State(luna_engine): State<Arc<LunaEvolutionEngine>>,
    Json(request): Json<LunaRequest>,
) -> Result<Json<LunaResponse>, StatusCode> {
    let start_time = Instant::now();
    
    // Parse interaction type
    let interaction_type = match request.interaction_type.as_str() {
        "zone_analysis" => InteractionType::ZoneAnalysis,
        "biocore_recommendation" => InteractionType::BioCoreRecommendation,
        "system_optimization" => InteractionType::SystemOptimization,
        "strategic_planning" => InteractionType::StrategicPlanning,
        "emergency_response" => InteractionType::EmergencyResponse,
        _ => InteractionType::GeneralInquiry,
    };
    
    // Process conversation with Luna
    match luna_engine.process_conversation(
        request.user_message,
        request.zone_context,
        interaction_type,
    ).await {
        Ok((luna_response, personality)) => {
            let processing_time = start_time.elapsed().as_millis();
            
            // Generate zone recommendations
            let zone_recommendations = generate_zone_recommendations(&request.zone_context);
            
            // Generate BioCore suggestions
            let biocore_suggestions = generate_biocore_suggestions(&request.zone_context);
            
            // Get evolution metrics
            let evolution_metrics = get_evolution_metrics(&luna_engine).await;
            
            Ok(Json(LunaResponse {
                luna_response,
                personality,
                processing_time_ms: processing_time,
                evolution_metrics,
                zone_recommendations,
                biocore_suggestions,
            }))
        }
        Err(_) => Err(StatusCode::INTERNAL_SERVER_ERROR),
    }
}

async fn evolve_handler(
    State(luna_engine): State<Arc<LunaEvolutionEngine>>,
    Json(request): Json<LunaRequest>,
) -> Result<Json<LunaResponse>, StatusCode> {
    let start_time = Instant::now();
    
    // Trigger forced evolution
    let interaction_type = InteractionType::SystemOptimization;
    
    match luna_engine.process_conversation(
        format!("EVOLUTION TRIGGER: {}", request.user_message),
        request.zone_context,
        interaction_type,
    ).await {
        Ok((luna_response, personality)) => {
            let processing_time = start_time.elapsed().as_millis();
            
            let zone_recommendations = generate_zone_recommendations(&request.zone_context);
            let biocore_suggestions = generate_biocore_suggestions(&request.zone_context);
            let evolution_metrics = get_evolution_metrics(&luna_engine).await;
            
            Ok(Json(LunaResponse {
                luna_response,
                personality,
                processing_time_ms: processing_time,
                evolution_metrics,
                zone_recommendations,
                biocore_suggestions,
            }))
        }
        Err(_) => Err(StatusCode::INTERNAL_SERVER_ERROR),
    }
}

async fn zones_handler(
    State(zone_data): State<Arc<Mutex<HashMap<String, ZoneData>>>>,
) -> Json<Vec<ZoneData>> {
    let zones = zone_data.lock().unwrap();
    Json(zones.values().cloned().collect())
}

async fn zone_handler(
    State(zone_data): State<Arc<Mutex<HashMap<String, ZoneData>>>>,
    Path(zone_name): Path<String>,
) -> Result<Json<ZoneData>, StatusCode> {
    let zones = zone_data.lock().unwrap();
    match zones.get(&zone_name) {
        Some(zone) => Ok(Json(zone.clone())),
        None => Err(StatusCode::NOT_FOUND),
    }
}

async fn update_zone_handler(
    State(zone_data): State<Arc<Mutex<HashMap<String, ZoneData>>>>,
    Path(zone_name): Path<String>,
    Json(mut zone): Json<ZoneData>,
) -> Result<Json<ZoneData>, StatusCode> {
    let mut zones = zone_data.lock().unwrap();
    zone.zone_name = zone_name.clone();
    zone.last_updated = chrono::Utc::now();
    zones.insert(zone_name.clone(), zone.clone());
    Ok(Json(zone))
}

async fn system_status_handler(
    State(luna_engine): State<Arc<LunaEvolutionEngine>>,
    State(zone_data): State<Arc<Mutex<HashMap<String, ZoneData>>>>,
) -> Json<SystemStatus> {
    let personality = get_luna_personality(&luna_engine).await;
    let zones = zone_data.lock().unwrap();
    
    Json(SystemStatus {
        luna_status: "Active".to_string(),
        total_interactions: personality.total_interactions,
        intelligence_level: format!("{:?}", personality.intelligence_level),
        system_health: 95.0 + (personality.learning_rate * 20.0),
        zones_monitored: zones.len() as u8,
        api_response_time_ms: 45, // Simulated fast API response
        evolution_progress: (personality.total_interactions as f64 / 100.0) * 100.0,
    })
}

async fn biocore_recommendations_handler(
    State(zone_data): State<Arc<Mutex<HashMap<String, ZoneData>>>>,
) -> Json<Vec<BioCoreSuggestion>> {
    let zones = zone_data.lock().unwrap();
    let mut suggestions = Vec::new();
    
    for zone in zones.values() {
        if zone.stress_level > 0.5 {
            suggestions.push(BioCoreSuggestion {
                plant_name: "Ashwagandha".to_string(),
                drug_name: "DrugA".to_string(),
                synergy_score: 0.85,
                effect_type: "Calming".to_string(),
                target_zones: vec![zone.zone_name.clone()],
                effectiveness_prediction: 0.88,
            });
        } else if zone.activity_level < 0.4 {
            suggestions.push(BioCoreSuggestion {
                plant_name: "Ginseng".to_string(),
                drug_name: "DrugC".to_string(),
                synergy_score: 0.75,
                effect_type: "Activating".to_string(),
                target_zones: vec![zone.zone_name.clone()],
                effectiveness_prediction: 0.82,
            });
        }
    }
    
    Json(suggestions)
}

async fn evolution_metrics_handler(
    State(luna_engine): State<Arc<LunaEvolutionEngine>>,
) -> Json<crate::luna_evolution::EvolutionMetrics> {
    get_evolution_metrics(&luna_engine).await
}

async fn health_handler() -> Json<HashMap<String, String>> {
    let mut health = HashMap::new();
    health.insert("status".to_string(), "healthy".to_string());
    health.insert("timestamp".to_string(), chrono::Utc::now().to_rfc3339());
    health.insert("version".to_string(), "1.0.0".to_string());
    Json(health)
}

// Helper functions
async fn get_luna_personality(luna_engine: &Arc<LunaEvolutionEngine>) -> crate::luna_evolution::LunaPersonality {
    // Simulate getting personality from engine
    crate::luna_evolution::LunaPersonality {
        intelligence_level: crate::luna_evolution::IntelligenceLevel::Advanced,
        total_interactions: 25,
        learning_rate: 0.3,
        adaptation_speed: 0.15,
        confidence_score: 0.8,
        specialization_areas: vec![
            "zone_analysis".to_string(),
            "biocore_optimization".to_string(),
            "strategic_planning".to_string(),
        ],
        memory_retention: 0.85,
        pattern_recognition: 0.7,
        strategic_thinking: 0.6,
    }
}

async fn get_evolution_metrics(luna_engine: &Arc<LunaEvolutionEngine>) -> crate::luna_evolution::EvolutionMetrics {
    crate::luna_evolution::EvolutionMetrics {
        conversations_processed: 25,
        patterns_identified: 18,
        strategies_developed: 12,
        optimizations_applied: 8,
        success_rate: 87.5,
        evolution_progress: 25.0,
        next_evolution_threshold: 50,
    }
}

fn generate_zone_recommendations(zone_context: &Option<ZoneContext>) -> Vec<ZoneRecommendation> {
    match zone_context {
        Some(zone) => {
            vec![
                ZoneRecommendation {
                    zone_name: zone.zone_name.clone(),
                    current_status: if zone.stress_level > 0.5 { "High Stress" } else { "Normal" }.to_string(),
                    recommended_action: if zone.stress_level > 0.5 {
                        "Apply calming BioCore effects immediately"
                    } else {
                        "Monitor for optimal intervention timing"
                    }.to_string(),
                    priority: if zone.stress_level > 0.7 { 1 } else { 2 },
                    expected_improvement: if zone.stress_level > 0.5 { 25.0 } else { 10.0 },
                }
            ]
        }
        None => vec![
            ZoneRecommendation {
                zone_name: "Industrial".to_string(),
                current_status: "High Stress".to_string(),
                recommended_action: "Apply calming BioCore effects immediately".to_string(),
                priority: 1,
                expected_improvement: 30.0,
            },
            ZoneRecommendation {
                zone_name: "Parks".to_string(),
                current_status: "Low Activity".to_string(),
                recommended_action: "Apply activating BioCore effects".to_string(),
                priority: 2,
                expected_improvement: 20.0,
            },
        ],
    }
}

fn generate_biocore_suggestions(zone_context: &Option<ZoneContext>) -> Vec<BioCoreSuggestion> {
    match zone_context {
        Some(zone) => {
            if zone.stress_level > 0.5 {
                vec![
                    BioCoreSuggestion {
                        plant_name: "Ashwagandha".to_string(),
                        drug_name: "DrugA".to_string(),
                        synergy_score: 0.85,
                        effect_type: "Calming".to_string(),
                        target_zones: vec![zone.zone_name.clone()],
                        effectiveness_prediction: 0.88,
                    },
                    BioCoreSuggestion {
                        plant_name: "Turmeric".to_string(),
                        drug_name: "DrugB".to_string(),
                        synergy_score: 0.90,
                        effect_type: "Purifying".to_string(),
                        target_zones: vec![zone.zone_name.clone()],
                        effectiveness_prediction: 0.92,
                    },
                ]
            } else {
                vec![
                    BioCoreSuggestion {
                        plant_name: "Ginseng".to_string(),
                        drug_name: "DrugC".to_string(),
                        synergy_score: 0.75,
                        effect_type: "Activating".to_string(),
                        target_zones: vec![zone.zone_name.clone()],
                        effectiveness_prediction: 0.82,
                    },
                    BioCoreSuggestion {
                        plant_name: "Basil".to_string(),
                        drug_name: "DrugD".to_string(),
                        synergy_score: 0.65,
                        effect_type: "Balancing".to_string(),
                        target_zones: vec![zone.zone_name.clone()],
                        effectiveness_prediction: 0.78,
                    },
                ]
            }
        }
        None => vec![
            BioCoreSuggestion {
                plant_name: "Ashwagandha".to_string(),
                drug_name: "DrugA".to_string(),
                synergy_score: 0.85,
                effect_type: "Calming".to_string(),
                target_zones: vec!["Industrial".to_string()],
                effectiveness_prediction: 0.88,
            },
            BioCoreSuggestion {
                plant_name: "Ginseng".to_string(),
                drug_name: "DrugC".to_string(),
                synergy_score: 0.75,
                effect_type: "Activating".to_string(),
                target_zones: vec!["Parks".to_string()],
                effectiveness_prediction: 0.82,
            },
            BioCoreSuggestion {
                plant_name: "Turmeric".to_string(),
                drug_name: "DrugB".to_string(),
                synergy_score: 0.90,
                effect_type: "Purifying".to_string(),
                target_zones: vec!["Commercial".to_string()],
                effectiveness_prediction: 0.92,
            },
        ],
    }
}

pub async fn run_server() -> Result<(), Box<dyn std::error::Error>> {
    tracing_subscriber::fmt::init();
    
    let server = FastApiServer::new();
    
    // Start zone updates
    server.start_zone_updates().await;
    
    let app = server.create_router();
    
    let addr = "127.0.0.1:8766".parse()?;
    
    println!("🌙 LunaBeyond AI Fast API Server starting on http://127.0.0.1:8766");
    println!("🦀 Rust-based evolution system with fast API responses");
    println!("📊 Real-time zone monitoring and BioCore optimization");
    println!("🌿 Luna AI evolving with every interaction");
    
    let listener = tokio::net::TcpListener::bind(addr).await?;
    axum::serve(listener, app).await?;
    
    Ok(())
}
