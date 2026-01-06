//! BHCS Rust Core Library
//! 
//! Deterministic homeostatic regulation engine for BHCS
//! Enforces bounds and applies homeostatic correction

pub mod engine;
pub mod zone;
pub mod api;

pub use engine::HomeostaticEngine;
pub use zone::Zone;
pub use api::start_server;
