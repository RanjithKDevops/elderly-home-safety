#!/usr/bin/env python3
"""
Elderly Home Safety - Sensor Simulator (EC2 Version)
Runs on EC2 and sends data to local fog node
"""

import random
import time
import requests
from datetime import datetime

class ElderlyHomeSensor:
    def __init__(self, home_id="HOME-001", patient_id="P001"):
        self.home_id = home_id
        self.patient_id = patient_id
        self.base_heart_rate = random.randint(65, 85)
        self.motion_timer = 0
        
    def generate_readings(self):
        fall = 1 if random.random() < 0.05 else 0
        if fall:
            print(f"⚠️ FALL DETECTED in {self.home_id}!")
        
        heart_rate = random.randint(120, 155) if fall else self.base_heart_rate + random.randint(-8, 8)
        temperature = round(21.0 + random.uniform(-2, 3), 1)
        
        self.motion_timer += 1
        if self.motion_timer > 20:
            motion = 0
        else:
            motion = 1 if random.random() < 0.7 else 0
        if motion:
            self.motion_timer = 0
        
        gas_leak = 1 if random.random() < 0.02 else 0
        
        return [
            {"home_id": self.home_id, "patient_id": self.patient_id, "sensor_id": f"{self.home_id}-fall", "type": "fall_detection", "value": fall, "unit": "boolean", "timestamp": datetime.utcnow().isoformat()},
            {"home_id": self.home_id, "patient_id": self.patient_id, "sensor_id": f"{self.home_id}-heart", "type": "heart_rate", "value": heart_rate, "unit": "bpm", "timestamp": datetime.utcnow().isoformat()},
            {"home_id": self.home_id, "patient_id": self.patient_id, "sensor_id": f"{self.home_id}-temp", "type": "temperature", "value": temperature, "unit": "°C", "timestamp": datetime.utcnow().isoformat()},
            {"home_id": self.home_id, "patient_id": self.patient_id, "sensor_id": f"{self.home_id}-motion", "type": "activity", "value": motion, "unit": "boolean", "timestamp": datetime.utcnow().isoformat()},
            {"home_id": self.home_id, "patient_id": self.patient_id, "sensor_id": f"{self.home_id}-gas", "type": "gas_leak", "value": gas_leak, "unit": "boolean", "timestamp": datetime.utcnow().isoformat()}
        ]

homes = [
    ElderlyHomeSensor("HOME-001", "P001"),
    ElderlyHomeSensor("HOME-002", "P002"),
    ElderlyHomeSensor("HOME-003", "P003")
]

FOG_NODE_URL = "http://localhost:5000/data"  # EC2 localhost

print("🏥 Starting Elderly Home Safety Monitoring System on EC2")
print(f"📡 Monitoring {len(homes)} homes")
print("=" * 50)

while True:
    for home in homes:
        readings = home.generate_readings()
        try:
            response = requests.post(FOG_NODE_URL, json=readings, timeout=3)
            if response.status_code == 200:
                result = response.json()
                if result.get('emergency'):
                    print(f"🚨 EMERGENCY in {home.home_id}!")
        except:
            print(f"❌ Fog node not available")
    time.sleep(3)
# Updated sensor frequency to 3 seconds
