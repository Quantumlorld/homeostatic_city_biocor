//! API Implementation
//! 
//! HTTP API for BHCS Rust Core

use serde_json::{json, Value};
use warp::{Filter, Rejection, Reply};
use crate::{HomeostaticEngine, HomeostaticConfig};

pub fn start_server(engine: std::sync::Arc<std::sync::Mutex<HomeostaticEngine>>) {
    let engine = warp::any()
        .map(move || engine.clone());

    // GET /state - Get current zone states
    let state_route = warp::path("state")
        .and(warp::get())
        .and(engine.clone())
        .and_then(get_state);

    // GET /health - System health check
    let health_route = warp::path("health")
        .and(warp::get())
        .and(engine.clone())
        .and_then(health_check);

    // POST /influence - Apply influence to zone
    let influence_route = warp::path("influence")
        .and(warp::post())
        .and(warp::body::json())
        .and(engine.clone())
        .and_then(apply_influence);

    let routes = state_route.or(health_route).or(influence_route);

    warp::serve(routes)
        .run(([127, 0, 0, 1], 3030))
        .await;
}

async fn get_state(
    engine: std::sync::Arc<std::sync::Mutex<HomeostaticEngine>>,
) -> Result<impl Reply, Rejection> {
    let engine = engine.lock().unwrap();
    let zones: Vec<Value> = engine.get_zones()
        .iter()
        .map(|zone| {
            json!({
                "id": zone.id(),
                "activity": zone.activity(),
                "state": format!("{:?}", zone.state()),
                "target": zone.target()
            })
        })
        .collect();

    let response = json!({
        "zones": zones,
        "metrics": engine.get_system_metrics()
    });

    Ok(warp::reply::json(&response))
}

async fn health_check(
    engine: std::sync::Arc<std::sync::Mutex<HomeostaticEngine>>,
) -> Result<impl Reply, Rejection> {
    let engine = engine.lock().unwrap();
    let metrics = engine.get_system_metrics();
    
    let response = json!({
        "status": "healthy",
        "metrics": metrics
    });

    Ok(warp::reply::json(&response))
}

async fn apply_influence(
    body: Value,
    engine: std::sync::Arc<std::sync::Mutex<HomeostaticEngine>>,
) -> Result<impl Reply, Rejection> {
    let zone_id = body["zone_id"].as_u64().unwrap_or(0) as usize;
    let influence = body["influence"].as_f64().unwrap_or(0.0);

    {
        let mut engine = engine.lock().unwrap();
        engine.apply_influence(zone_id, influence);
    }

    let response = json!({
        "success": true,
        "zone_id": zone_id,
        "influence": influence
    });

    Ok(warp::reply::json(&response))
}
