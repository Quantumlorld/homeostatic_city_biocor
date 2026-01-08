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

mod luna_evolution;
mod fast_api_server;

use luna_evolution::LunaEvolutionEngine;
use fast_api_server::{FastApiServer, run_server};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    tracing_subscriber::fmt::init();
    
    println!("🌙 LUNABEYOND AI - RUST-BASED EVOLUTION SYSTEM");
    println!("🦀 Fast API Server with PyTorch + JAX Integration");
    println!("🌿 BioCore Optimization with Real-time Learning");
    println!("🚀 Starting combined simulation system...");
    
    // Start the Fast API server
    run_server().await
}
