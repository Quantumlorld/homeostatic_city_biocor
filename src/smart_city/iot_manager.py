"""
IoT Manager Module
Intelligent IoT device management and data collection for smart city applications.
"""

import numpy as np
from typing import List, Dict, Optional, Callable
from dataclasses import dataclass
from enum import Enum
import time
import json


class DeviceType(Enum):
    """Types of IoT devices in the smart city."""
    TRAFFIC_SENSOR = "TRAFFIC_SENSOR"
    AIR_QUALITY_SENSOR = "AIR_QUALITY_SENSOR"
    NOISE_SENSOR = "NOISE_SENSOR"
    WEATHER_STATION = "WEATHER_STATION"
    ENERGY_METER = "ENERGY_METER"
    WATER_METER = "WATER_METER"
    SECURITY_CAMERA = "SECURITY_CAMERA"
    STREET_LIGHT = "STREET_LIGHT"
    EMERGENCY_BEACON = "EMERGENCY_BEACON"


class DeviceStatus(Enum):
    """Status of IoT devices."""
    ONLINE = "ONLINE"
    OFFLINE = "OFFLINE"
    MAINTENANCE = "MAINTENANCE"
    ERROR = "ERROR"


@dataclass
class IoTDevice:
    """IoT device representation."""
    device_id: str
    device_type: DeviceType
    zone_id: int
    location: Dict[str, float]  # lat, lon
    status: DeviceStatus
    last_update: float
    data: Dict
    battery_level: float
    signal_strength: float


class IoTManager:
    """
    Advanced IoT device management for smart city applications.
    Handles device registration, data collection, and automated responses.
    """
    
    def __init__(self, zones: int = 5):
        """
        Initialize IoT manager.
        
        Args:
            zones: Number of city zones to manage
        """
        self.zones = zones
        self.devices = {}  # device_id -> IoTDevice
        self.zone_devices = {i: [] for i in range(zones)}  # zone_id -> [device_ids]
        self.data_streams = {}  # device_type -> [data_points]
        self.alert_thresholds = {}
        self.automation_rules = []
        
        # Initialize default devices
        self._initialize_default_devices()
        
        # Data processing callbacks
        self.data_callbacks = {}
    
    def _initialize_default_devices(self) -> None:
        """Initialize default IoT devices for each zone."""
        for zone in range(self.zones):
            # Traffic sensors
            traffic_device = IoTDevice(
                device_id=f"traffic_{zone}",
                device_type=DeviceType.TRAFFIC_SENSOR,
                zone_id=zone,
                location={"lat": 40.7128 + zone * 0.01, "lon": -74.0060 + zone * 0.01},
                status=DeviceStatus.ONLINE,
                last_update=time.time(),
                data={"vehicle_count": 0, "average_speed": 0, "congestion_level": 0},
                battery_level=0.8,
                signal_strength=0.9
            )
            
            # Air quality sensors
            air_device = IoTDevice(
                device_id=f"air_{zone}",
                device_type=DeviceType.AIR_QUALITY_SENSOR,
                zone_id=zone,
                location={"lat": 40.7128 + zone * 0.01, "lon": -74.0060 + zone * 0.01},
                status=DeviceStatus.ONLINE,
                last_update=time.time(),
                data={"pm25": 0, "pm10": 0, "o2": 21.0, "co2": 400, "aqi": 0},
                battery_level=0.9,
                signal_strength=0.8
            )
            
            # Noise sensors
            noise_device = IoTDevice(
                device_id=f"noise_{zone}",
                device_type=DeviceType.NOISE_SENSOR,
                zone_id=zone,
                location={"lat": 40.7128 + zone * 0.01, "lon": -74.0060 + zone * 0.01},
                status=DeviceStatus.ONLINE,
                last_update=time.time(),
                data={"decibels": 0, "frequency_spectrum": {}},
                battery_level=0.85,
                signal_strength=0.95
            )
            
            # Energy meters
            energy_device = IoTDevice(
                device_id=f"energy_{zone}",
                device_type=DeviceType.ENERGY_METER,
                zone_id=zone,
                location={"lat": 40.7128 + zone * 0.01, "lon": -74.0060 + zone * 0.01},
                status=DeviceStatus.ONLINE,
                last_update=time.time(),
                data={"consumption_kw": 0, "peak_demand": 0, "efficiency": 1.0},
                battery_level=1.0,  # Mains powered
                signal_strength=0.7
            )
            
            # Register devices
            self.register_device(traffic_device)
            self.register_device(air_device)
            self.register_device(noise_device)
            self.register_device(energy_device)
    
    def register_device(self, device: IoTDevice) -> None:
        """
        Register a new IoT device.
        
        Args:
            device: IoT device to register
        """
        self.devices[device.device_id] = device
        self.zone_devices[device.zone_id].append(device.device_id)
        
        # Initialize data stream for device type
        if device.device_type not in self.data_streams:
            self.data_streams[device.device_type] = []
        
        print(f"📱 Device registered: {device.device_id} ({device.device_type.value}) in Zone {device.zone_id}")
    
    def update_device_data(self, device_id: str, new_data: Dict) -> bool:
        """
        Update data for a specific device.
        
        Args:
            device_id: Device identifier
            new_data: New sensor data
            
        Returns:
            True if update successful
        """
        if device_id not in self.devices:
            print(f"❌ Device {device_id} not found")
            return False
        
        device = self.devices[device_id]
        device.data.update(new_data)
        device.last_update = time.time()
        
        # Add to data stream
        self.data_streams[device.device_type].append({
            'device_id': device_id,
            'timestamp': device.last_update,
            'data': new_data.copy(),
            'zone_id': device.zone_id
        })
        
        # Keep data stream size manageable
        if len(self.data_streams[device.device_type]) > 1000:
            self.data_streams[device.device_type] = self.data_streams[device.device_type][-500:]
        
        # Check for alerts
        self._check_device_alerts(device)
        
        # Trigger automation rules
        self._evaluate_automation_rules(device)
        
        # Call data callbacks
        if device.device_type in self.data_callbacks:
            for callback in self.data_callbacks[device.device_type]:
                callback(device, new_data)
        
        return True
    
    def _check_device_alerts(self, device: IoTDevice) -> None:
        """Check if device data triggers any alerts."""
        device_key = f"{device.device_type.value}_{device.zone_id}"
        
        if device_key not in self.alert_thresholds:
            return
        
        thresholds = self.alert_thresholds[device_key]
        alerts = []
        
        # Check specific thresholds based on device type
        if device.device_type == DeviceType.AIR_QUALITY_SENSOR:
            aqi = device.data.get('aqi', 0)
            if aqi > thresholds.get('aqi', 100):
                alerts.append({
                    'type': 'air_quality',
                    'severity': 'HIGH' if aqi > 150 else 'MODERATE',
                    'message': f'AQI level {aqi} exceeds threshold',
                    'timestamp': time.time()
                })
        
        elif device.device_type == DeviceType.TRAFFIC_SENSOR:
            congestion = device.data.get('congestion_level', 0)
            if congestion > thresholds.get('congestion', 0.8):
                alerts.append({
                    'type': 'traffic_congestion',
                    'severity': 'HIGH' if congestion > 0.9 else 'MODERATE',
                    'message': f'Traffic congestion {congestion:.1%} detected',
                    'timestamp': time.time()
                })
        
        elif device.device_type == DeviceType.NOISE_SENSOR:
            decibels = device.data.get('decibels', 0)
            if decibels > thresholds.get('decibels', 85):
                alerts.append({
                    'type': 'noise_pollution',
                    'severity': 'HIGH' if decibels > 95 else 'MODERATE',
                    'message': f'Noise level {decibels} dB exceeds threshold',
                    'timestamp': time.time()
                })
        
        elif device.device_type == DeviceType.ENERGY_METER:
            consumption = device.data.get('consumption_kw', 0)
            if consumption > thresholds.get('consumption', 1000):
                alerts.append({
                    'type': 'energy_overload',
                    'severity': 'HIGH' if consumption > 1200 else 'MODERATE',
                    'message': f'Energy consumption {consumption} kW exceeds threshold',
                    'timestamp': time.time()
                })
        
        # Process alerts
        for alert in alerts:
            self._handle_alert(alert, device)
    
    def _evaluate_automation_rules(self, device: IoTDevice) -> None:
        """Evaluate automation rules based on device data."""
        for rule in self.automation_rules:
            if self._rule_matches(rule, device):
                self._execute_automation_rule(rule, device)
    
    def _rule_matches(self, rule: Dict, device: IoTDevice) -> bool:
        """Check if an automation rule matches the current device state."""
        conditions = rule.get('conditions', {})
        
        for key, expected_value in conditions.items():
            if key not in device.data:
                return False
            
            actual_value = device.data[key]
            
            # Support different comparison operators
            if isinstance(expected_value, dict):
                operator = expected_value.get('operator', 'eq')
                threshold = expected_value.get('value', 0)
                
                if operator == 'gt' and actual_value <= threshold:
                    return False
                elif operator == 'lt' and actual_value >= threshold:
                    return False
                elif operator == 'eq' and actual_value != threshold:
                    return False
            elif actual_value != expected_value:
                return False
        
        return True
    
    def _execute_automation_rule(self, rule: Dict, device: IoTDevice) -> None:
        """Execute an automation rule."""
        actions = rule.get('actions', [])
        
        for action in actions:
            action_type = action.get('type')
            
            if action_type == 'adjust_bio_core':
                # Trigger BioCore effect
                print(f"🤖 Automation: Triggering BioCore effect - {action}")
                # This would integrate with the BioCore system
                
            elif action_type == 'alert_authorities':
                # Send alert to emergency services
                print(f"🚨 Automation: Alerting authorities - {action}")
                
            elif action_type == 'adjust_infrastructure':
                # Adjust city infrastructure
                print(f"🏗️ Automation: Adjusting infrastructure - {action}")
                
            elif action_type == 'notify_citizens':
                # Send public notification
                print(f"📢 Automation: Notifying citizens - {action}")
    
    def _handle_alert(self, alert: Dict, device: IoTDevice) -> None:
        """Handle device alert."""
        print(f"🚨 ALERT: {alert['message']} in Zone {device.zone_id}")
        
        # Store alert for historical analysis
        alert['device_id'] = device.device_id
        alert['zone_id'] = device.zone_id
        
        # This could integrate with emergency systems
        # or trigger automated responses
    
    def set_alert_thresholds(self, device_type: DeviceType, zone_id: int, 
                           thresholds: Dict) -> None:
        """
        Set alert thresholds for a device type in a specific zone.
        
        Args:
            device_type: Type of IoT device
            zone_id: Zone identifier
            thresholds: Threshold values
        """
        key = f"{device_type.value}_{zone_id}"
        self.alert_thresholds[key] = thresholds
        print(f"⚙️ Alert thresholds set for {key}: {thresholds}")
    
    def add_automation_rule(self, rule: Dict) -> None:
        """
        Add an automation rule.
        
        Args:
            rule: Automation rule definition
        """
        rule_id = rule.get('id', f"rule_{len(self.automation_rules)}")
        rule['id'] = rule_id
        self.automation_rules.append(rule)
        print(f"🤖 Automation rule added: {rule_id}")
    
    def get_zone_summary(self, zone_id: int) -> Dict:
        """
        Get summary of IoT data for a specific zone.
        
        Args:
            zone_id: Zone identifier
            
        Returns:
            Zone IoT summary
        """
        if zone_id >= self.zones:
            return {'error': 'Invalid zone ID'}
        
        zone_device_ids = self.zone_devices[zone_id]
        summary = {
            'zone_id': zone_id,
            'total_devices': len(zone_device_ids),
            'online_devices': 0,
            'device_types': {},
            'latest_data': {},
            'alerts_count': 0
        }
        
        # Count online devices and collect data
        for device_id in zone_device_ids:
            device = self.devices[device_id]
            if device.status == DeviceStatus.ONLINE:
                summary['online_devices'] += 1
            
            # Count device types
            device_type = device.device_type.value
            summary['device_types'][device_type] = summary['device_types'].get(device_type, 0) + 1
            
            # Get latest data
            summary['latest_data'][device_id] = device.data.copy()
        
        return summary
    
    def get_city_wide_summary(self) -> Dict:
        """
        Get city-wide IoT summary.
        
        Returns:
            City-wide IoT statistics
        """
        summary = {
            'total_devices': len(self.devices),
            'online_devices': 0,
            'offline_devices': 0,
            'maintenance_devices': 0,
            'error_devices': 0,
            'device_types': {},
            'zones': {},
            'data_points_collected': sum(len(stream) for stream in self.data_streams.values()),
            'automation_rules': len(self.automation_rules)
        }
        
        # Count device statuses and types
        for device in self.devices.values():
            if device.status == DeviceStatus.ONLINE:
                summary['online_devices'] += 1
            elif device.status == DeviceStatus.OFFLINE:
                summary['offline_devices'] += 1
            elif device.status == DeviceStatus.MAINTENANCE:
                summary['maintenance_devices'] += 1
            elif device.status == DeviceStatus.ERROR:
                summary['error_devices'] += 1
            
            device_type = device.device_type.value
            summary['device_types'][device_type] = summary['device_types'].get(device_type, 0) + 1
        
        # Zone summaries
        for zone_id in range(self.zones):
            summary['zones'][zone_id] = self.get_zone_summary(zone_id)
        
        return summary
    
    def register_data_callback(self, device_type: DeviceType, callback: Callable) -> None:
        """
        Register a callback for specific device type data.
        
        Args:
            device_type: Device type to monitor
            callback: Function to call when data is received
        """
        if device_type not in self.data_callbacks:
            self.data_callbacks[device_type] = []
        
        self.data_callbacks[device_type].append(callback)
        print(f"📞 Data callback registered for {device_type.value}")
    
    def simulate_data_updates(self, duration_minutes: int = 60) -> None:
        """
        Simulate realistic IoT data updates.
        
        Args:
            duration_minutes: How long to simulate
        """
        print(f"🔄 Starting IoT data simulation for {duration_minutes} minutes...")
        
        start_time = time.time()
        end_time = start_time + (duration_minutes * 60)
        
        while time.time() < end_time:
            for device in self.devices.values():
                if device.status != DeviceStatus.ONLINE:
                    continue
                
                # Simulate data based on device type
                if device.device_type == DeviceType.TRAFFIC_SENSOR:
                    # Simulate traffic patterns
                    hour = int(time.strftime("%H"))
                    base_traffic = 50 + 30 * np.sin(hour * np.pi / 12)  # Daily pattern
                    noise = np.random.normal(0, 10)
                    vehicle_count = max(0, base_traffic + noise)
                    
                    new_data = {
                        'vehicle_count': int(vehicle_count),
                        'average_speed': max(10, 60 - vehicle_count / 10),
                        'congestion_level': min(1.0, vehicle_count / 100)
                    }
                
                elif device.device_type == DeviceType.AIR_QUALITY_SENSOR:
                    # Simulate air quality changes
                    current_aqi = device.data.get('aqi', 50)
                    change = np.random.normal(0, 5)
                    new_aqi = max(0, min(500, current_aqi + change))
                    
                    new_data = {
                        'pm25': max(0, new_aqi * 0.4),
                        'pm10': max(0, new_aqi * 0.6),
                        'o2': max(15, 21 - new_aqi * 0.01),
                        'co2': max(300, 400 + new_aqi * 2),
                        'aqi': new_aqi
                    }
                
                elif device.device_type == DeviceType.NOISE_SENSOR:
                    # Simulate noise levels
                    hour = int(time.strftime("%H"))
                    base_noise = 60 + 20 * np.sin(hour * np.pi / 12)
                    noise = np.random.normal(0, 5)
                    decibels = max(30, base_noise + noise)
                    
                    new_data = {
                        'decibels': decibels,
                        'frequency_spectrum': {
                            'low': decibels * 0.8,
                            'mid': decibels * 0.6,
                            'high': decibels * 0.4
                        }
                    }
                
                elif device.device_type == DeviceType.ENERGY_METER:
                    # Simulate energy consumption
                    hour = int(time.strftime("%H"))
                    base_consumption = 500 + 300 * np.sin(hour * np.pi / 12)
                    noise = np.random.normal(0, 50)
                    consumption = max(100, base_consumption + noise)
                    
                    new_data = {
                        'consumption_kw': consumption,
                        'peak_demand': consumption * 1.2,
                        'efficiency': max(0.7, 1.0 - consumption / 2000)
                    }
                
                else:
                    continue
                
                # Update device data
                self.update_device_data(device.device_id, new_data)
                
                # Simulate battery drain for battery-powered devices
                if device.battery_level < 1.0:
                    device.battery_level = max(0, device.battery_level - 0.001)
                    if device.battery_level < 0.1:
                        device.status = DeviceStatus.OFFLINE
                        print(f"🔋 Device {device.device_id} battery depleted")
            
            time.sleep(1)  # Update every second
        
        print(f"✅ IoT data simulation completed")
