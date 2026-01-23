#!/usr/bin/env python3
"""
🏙️ Smart City IoT Sensor Network
Real-time environmental monitoring for Homeostatic City BioCore
"""

import asyncio
import random
import time
import json
from datetime import datetime
from typing import Dict, List, Any
import logging

class IoTsensorNetwork:
    def __init__(self):
        self.sensors = {
            'air_quality': {
                'downtown': {'pm25': 0, 'pm10': 0, 'no2': 0, 'o3': 0, 'co': 0},
                'industrial': {'pm25': 0, 'pm10': 0, 'no2': 0, 'o3': 0, 'co': 0},
                'residential': {'pm25': 0, 'pm10': 0, 'no2': 0, 'o3': 0, 'co': 0},
                'tech': {'pm25': 0, 'pm10': 0, 'no2': 0, 'o3': 0, 'co': 0},
                'medical': {'pm25': 0, 'pm10': 0, 'no2': 0, 'o3': 0, 'co': 0}
            },
            'noise_pollution': {
                'downtown': {'decibels': 0, 'frequency': 0},
                'industrial': {'decibels': 0, 'frequency': 0},
                'residential': {'decibels': 0, 'frequency': 0},
                'tech': {'decibels': 0, 'frequency': 0},
                'medical': {'decibels': 0, 'frequency': 0}
            },
            'traffic_flow': {
                'downtown': {'vehicle_count': 0, 'avg_speed': 0, 'congestion': 0},
                'industrial': {'vehicle_count': 0, 'avg_speed': 0, 'congestion': 0},
                'residential': {'vehicle_count': 0, 'avg_speed': 0, 'congestion': 0},
                'tech': {'vehicle_count': 0, 'avg_speed': 0, 'congestion': 0},
                'medical': {'vehicle_count': 0, 'avg_speed': 0, 'congestion': 0}
            },
            'environmental': {
                'downtown': {'temperature': 0, 'humidity': 0, 'uv_index': 0, 'light_level': 0},
                'industrial': {'temperature': 0, 'humidity': 0, 'uv_index': 0, 'light_level': 0},
                'residential': {'temperature': 0, 'humidity': 0, 'uv_index': 0, 'light_level': 0},
                'tech': {'temperature': 0, 'humidity': 0, 'uv_index': 0, 'light_level': 0},
                'medical': {'temperature': 0, 'humidity': 0, 'uv_index': 0, 'light_level': 0}
            },
            'biometric': {
                'downtown': {'heart_rate_avg': 0, 'stress_level': 0, 'cortisol': 0},
                'industrial': {'heart_rate_avg': 0, 'stress_level': 0, 'cortisol': 0},
                'residential': {'heart_rate_avg': 0, 'stress_level': 0, 'cortisol': 0},
                'tech': {'heart_rate_avg': 0, 'stress_level': 0, 'cortisol': 0},
                'medical': {'heart_rate_avg': 0, 'stress_level': 0, 'cortisol': 0}
            }
        }
        
        # Zone-specific baseline values
        self.baselines = {
            'downtown': {
                'air_quality': {'pm25': 35, 'pm10': 50, 'no2': 40, 'o3': 60, 'co': 10},
                'noise_pollution': {'decibels': 75, 'frequency': 1000},
                'traffic_flow': {'vehicle_count': 1000, 'avg_speed': 25, 'congestion': 0.7},
                'environmental': {'temperature': 22, 'humidity': 45, 'uv_index': 5, 'light_level': 800},
                'biometric': {'heart_rate_avg': 75, 'stress_level': 0.6, 'cortisol': 15}
            },
            'industrial': {
                'air_quality': {'pm25': 45, 'pm10': 70, 'no2': 60, 'o3': 40, 'co': 15},
                'noise_pollution': {'decibels': 85, 'frequency': 200},
                'traffic_flow': {'vehicle_count': 500, 'avg_speed': 35, 'congestion': 0.4},
                'environmental': {'temperature': 24, 'humidity': 40, 'uv_index': 3, 'light_level': 600},
                'biometric': {'heart_rate_avg': 80, 'stress_level': 0.7, 'cortisol': 18}
            },
            'residential': {
                'air_quality': {'pm25': 20, 'pm10': 30, 'no2': 20, 'o3': 50, 'co': 5},
                'noise_pollution': {'decibels': 55, 'frequency': 500},
                'traffic_flow': {'vehicle_count': 200, 'avg_speed': 30, 'congestion': 0.2},
                'environmental': {'temperature': 21, 'humidity': 50, 'uv_index': 4, 'light_level': 700},
                'biometric': {'heart_rate_avg': 70, 'stress_level': 0.3, 'cortisol': 10}
            },
            'tech': {
                'air_quality': {'pm25': 25, 'pm10': 35, 'no2': 25, 'o3': 55, 'co': 8},
                'noise_pollution': {'decibels': 65, 'frequency': 1500},
                'traffic_flow': {'vehicle_count': 800, 'avg_speed': 20, 'congestion': 0.8},
                'environmental': {'temperature': 23, 'humidity': 42, 'uv_index': 6, 'light_level': 900},
                'biometric': {'heart_rate_avg': 72, 'stress_level': 0.5, 'cortisol': 12}
            },
            'medical': {
                'air_quality': {'pm25': 15, 'pm10': 25, 'no2': 15, 'o3': 45, 'co': 3},
                'noise_pollution': {'decibels': 50, 'frequency': 800},
                'traffic_flow': {'vehicle_count': 300, 'avg_speed': 40, 'congestion': 0.3},
                'environmental': {'temperature': 20, 'humidity': 55, 'uv_index': 2, 'light_level': 500},
                'biometric': {'heart_rate_avg': 68, 'stress_level': 0.2, 'cortisol': 8}
            }
        }
        
        self.sensor_history = []
        self.alerts = []
        
    def update_sensor_readings(self):
        """Update all sensor readings with realistic variations"""
        current_time = datetime.now()
        
        for zone_type in self.baselines.keys():
            for sensor_type, zone_data in self.sensors.items():
                baseline = self.baselines[zone_type][sensor_type]
                
                for metric, baseline_value in baseline.items():
                    # Add realistic variations
                    variation = random.uniform(-0.2, 0.2)  # ±20% variation
                    time_factor = self._get_time_factor(sensor_type, current_time)
                    event_factor = self._get_event_factor(zone_type, current_time)
                    
                    new_value = baseline_value * (1 + variation) * time_factor * event_factor
                    
                    # Ensure values stay within realistic bounds
                    new_value = max(0, new_value)
                    
                    self.sensors[sensor_type][zone_type][metric] = round(new_value, 2)
        
        # Store in history
        self.sensor_history.append({
            'timestamp': current_time.isoformat(),
            'readings': self.get_all_readings()
        })
        
        # Keep only last 100 readings
        if len(self.sensor_history) > 100:
            self.sensor_history.pop(0)
        
        # Check for alerts
        self._check_alerts()
    
    def _get_time_factor(self, sensor_type, current_time):
        """Get time-based adjustment factors"""
        hour = current_time.hour
        
        if sensor_type == 'traffic_flow':
            # Rush hour patterns
            if 7 <= hour <= 9 or 17 <= hour <= 19:
                return random.uniform(1.5, 2.0)
            elif 22 <= hour or hour <= 6:
                return random.uniform(0.3, 0.5)
            else:
                return 1.0
        
        elif sensor_type == 'environmental':
            # Temperature and light variations
            if 6 <= hour <= 18:
                temp_factor = 1.0 + (hour - 12) * 0.05
                light_factor = 1.0 + (hour - 12) * 0.1
                return max(0.8, min(1.2, temp_factor * light_factor))
            else:
                return 0.8
        
        elif sensor_type == 'biometric':
            # Human activity patterns
            if 8 <= hour <= 18:
                return 1.1
            elif 22 <= hour or hour <= 6:
                return 0.9
            else:
                return 1.0
        
        return 1.0
    
    def _get_event_factor(self, zone_type, current_time):
        """Simulate random events"""
        # Random events that affect sensor readings
        if random.random() < 0.05:  # 5% chance of event
            events = {
                'downtown': {
                    'concert': 1.3,  # Increased noise and traffic
                    'protest': 1.5,  # High stress and congestion
                    'festival': 1.4,  # High activity
                    'emergency': 1.2  # Slight stress increase
                },
                'industrial': {
                    'accident': 1.6,  # High pollution and stress
                    'maintenance': 1.2,  # Moderate noise
                    'inspection': 1.1,  # Slight increase
                    'shutdown': 0.5   # Reduced activity
                },
                'residential': {
                    'party': 1.3,  # Noise increase
                    'construction': 1.4,  # Noise and dust
                    'event': 1.2,  # Moderate increase
                    'quiet_hours': 0.7  # Reduced activity
                },
                'tech': {
                    'product_launch': 1.5,  # High activity
                    'conference': 1.3,  # Moderate increase
                    'hackathon': 1.4,  # High stress
                    'maintenance': 0.8  # Reduced activity
                },
                'medical': {
                    'emergency': 1.6,  # High stress
                    'surgery': 1.2,  # Moderate stress
                    'outbreak': 1.8,  # High biometric stress
                    'quiet_period': 0.8  # Reduced activity
                }
            }
            
            zone_events = events.get(zone_type, {})
            if zone_events:
                event = random.choice(list(zone_events.keys()))
                factor = zone_events[event]
                
                # Log the event
                self.alerts.append({
                    'timestamp': current_time.isoformat(),
                    'zone': zone_type,
                    'event': event,
                    'severity': 'high' if factor > 1.4 else 'medium' if factor > 1.2 else 'low',
                    'factor': factor
                })
                
                return factor
        
        return 1.0
    
    def _check_alerts(self):
        """Check for threshold violations and generate alerts"""
        thresholds = {
            'air_quality': {'pm25': 50, 'pm10': 75, 'no2': 50, 'o3': 70, 'co': 12},
            'noise_pollution': {'decibels': 85},
            'traffic_flow': {'congestion': 0.8},
            'biometric': {'stress_level': 0.8, 'cortisol': 20}
        }
        
        for sensor_type, zones in self.sensors.items():
            if sensor_type in thresholds:
                for zone, readings in zones.items():
                    for metric, value in readings.items():
                        if metric in thresholds[sensor_type]:
                            if value > thresholds[sensor_type][metric]:
                                self.alerts.append({
                                    'timestamp': datetime.now().isoformat(),
                                    'zone': zone,
                                    'sensor': sensor_type,
                                    'metric': metric,
                                    'value': value,
                                    'threshold': thresholds[sensor_type][metric],
                                    'severity': 'critical' if value > thresholds[sensor_type][metric] * 1.5 else 'warning',
                                    'type': 'threshold_violation'
                                })
        
        # Keep only last 50 alerts
        if len(self.alerts) > 50:
            self.alerts = self.alerts[-50:]
    
    def get_all_readings(self):
        """Get current sensor readings for all zones"""
        return self.sensors
    
    def get_zone_readings(self, zone_type):
        """Get sensor readings for a specific zone"""
        readings = {}
        for sensor_type in self.sensors:
            readings[sensor_type] = self.sensors[sensor_type].get(zone_type, {})
        return readings
    
    def get_zone_health_score(self, zone_type):
        """Calculate overall health score for a zone"""
        readings = self.get_zone_readings(zone_type)
        score = 100
        
        # Air quality impact (30% weight)
        air_quality = readings.get('air_quality', {})
        pm25_score = max(0, 100 - (air_quality.get('pm25', 0) / 50) * 100)
        no2_score = max(0, 100 - (air_quality.get('no2', 0) / 50) * 100)
        air_score = (pm25_score + no2_score) / 2
        
        # Noise pollution impact (20% weight)
        noise = readings.get('noise_pollution', {})
        noise_score = max(0, 100 - ((noise.get('decibels', 50) - 50) / 35) * 100)
        
        # Traffic flow impact (20% weight)
        traffic = readings.get('traffic_flow', {})
        traffic_score = max(0, 100 - traffic.get('congestion', 0) * 100)
        
        # Biometric impact (30% weight)
        biometric = readings.get('biometric', {})
        stress_score = max(0, 100 - biometric.get('stress_level', 0) * 100)
        cortisol_score = max(0, 100 - (biometric.get('cortisol', 10) / 20) * 100)
        bio_score = (stress_score + cortisol_score) / 2
        
        # Calculate weighted score
        final_score = (
            air_score * 0.3 +
            noise_score * 0.2 +
            traffic_score * 0.2 +
            bio_score * 0.3
        )
        
        return round(final_score, 1)
    
    def get_recent_alerts(self, limit=10):
        """Get recent alerts"""
        return self.alerts[-limit:]
    
    def get_sensor_trends(self, zone_type, hours=24):
        """Get sensor trends for the last N hours"""
        cutoff_time = datetime.now().timestamp() - (hours * 3600)
        recent_data = []
        
        for entry in self.sensor_history:
            entry_time = datetime.fromisoformat(entry['timestamp']).timestamp()
            if entry_time >= cutoff_time:
                recent_data.append(entry)
        
        return recent_data

# Global sensor network instance
sensor_network = IoTsensorNetwork()

async def start_sensor_monitoring():
    """Start continuous sensor monitoring"""
    while True:
        sensor_network.update_sensor_readings()
        await asyncio.sleep(30)  # Update every 30 seconds

if __name__ == "__main__":
    # Test the sensor network
    print("🏙️ Testing Smart City IoT Sensor Network")
    print("=" * 50)
    
    # Update readings
    sensor_network.update_sensor_readings()
    
    # Display readings for each zone
    for zone in ['downtown', 'industrial', 'residential', 'tech', 'medical']:
        print(f"\n📍 {zone.upper()} ZONE:")
        readings = sensor_network.get_zone_readings(zone)
        health_score = sensor_network.get_zone_health_score(zone)
        
        print(f"🏥 Health Score: {health_score}/100")
        print(f"🌬️ Air Quality - PM2.5: {readings['air_quality']['pm25']}, NO2: {readings['air_quality']['no2']}")
        print(f"🔊 Noise Level: {readings['noise_pollution']['decibels']} dB")
        print(f"🚗 Traffic Congestion: {readings['traffic_flow']['congestion']*100:.1f}%")
        print(f"💓 Stress Level: {readings['biometric']['stress_level']*100:.1f}%")
    
    # Show recent alerts
    alerts = sensor_network.get_recent_alerts(5)
    if alerts:
        print(f"\n🚨 Recent Alerts:")
        for alert in alerts:
            print(f"  {alert['zone']}: {alert.get('event', alert.get('metric', 'Unknown'))} - {alert['severity']}")
