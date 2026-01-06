//! Zone Implementation
//! 
//! Individual zone management for BHCS

use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum ZoneState {
    Calm,
    Overstimulated,
    Emergent,
    Critical,
}

impl ZoneState {
    pub fn from_activity(activity: f64) -> Self {
        if activity < 0.4 {
            ZoneState::Calm
        } else if activity < 0.7 {
            ZoneState::Overstimulated
        } else if activity < 0.9 {
            ZoneState::Emergent
        } else {
            ZoneState::Critical
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Zone {
    id: usize,
    activity: f64,
    target: f64,
    state: ZoneState,
    last_update: i64,
}

impl Zone {
    pub fn new(id: usize) -> Self {
        let activity = rand::random::<f64>() * 0.6 + 0.2; // Random initial activity
        let state = ZoneState::from_activity(activity);
        
        Self {
            id,
            activity,
            target: 0.5, // Homeostatic target
            state,
            last_update: chrono::Utc::now().timestamp(),
        }
    }

    pub fn id(&self) -> usize {
        self.id
    }

    pub fn activity(&self) -> f64 {
        self.activity
    }

    pub fn state(&self) -> &ZoneState {
        &self.state
    }

    pub fn target(&self) -> f64 {
        self.target
    }

    pub fn apply_adjustment(&mut self, adjustment: f64) {
        self.activity = (self.activity + adjustment).clamp(0.0, 1.0);
        self.state = ZoneState::from_activity(self.activity);
        self.last_update = chrono::Utc::now().timestamp();
    }

    pub fn apply_influence(&mut self, influence: f64) {
        self.activity = (self.activity + influence).clamp(0.0, 1.0);
        self.state = ZoneState::from_activity(self.activity);
        self.last_update = chrono::Utc::now().timestamp();
    }

    pub fn reset(&mut self) {
        self.activity = rand::random::<f64>() * 0.6 + 0.2;
        self.state = ZoneState::from_activity(self.activity);
        self.last_update = chrono::Utc::now().timestamp();
    }
}
