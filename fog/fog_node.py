#!/usr/bin/env python3
"""
Elderly Home Safety - Fog Node
Processes sensor data locally and triggers emergency alerts
"""

from flask import Flask, request, jsonify
import boto3
import json
from datetime import datetime

app = Flask(__name__)

# ⚠️ UPDATE THIS WITH YOUR SQS URL FROM AWS CONSOLE ⚠️
SQS_QUEUE_URL = "https://sqs.us-east-1.amazonaws.com/306727604573/elderly-safety-queue"

sqs = boto3.client('sqs', region_name='us-east-1')
FOG_NODE_ID = "fog-dublin-01"

# Safety rules for elderly
RULES = {
    "heart_rate": {"min": 40, "max": 130, "critical_min": 30, "critical_max": 150},
    "temperature": {"min": 10, "max": 35, "critical_min": 5, "critical_max": 40},
    "fall_detection": {"critical": 1},
    "gas_leak": {"critical": 1}
}

# Track inactivity
last_activity = {}

@app.route('/data', methods=['POST'])
def process_data():
    """Fog processing with emergency detection"""
    readings = request.json
    if not readings:
        return jsonify({"error": "No data"}), 400
    
    home_id = readings[0].get('home_id', 'unknown')
    alerts = []
    emergency = False
    
    # Check activity
    has_activity = any(r['type'] == 'activity' and r['value'] == 1 for r in readings)
    if has_activity:
        last_activity[home_id] = datetime.utcnow()
    
    # Inactivity check (30 minutes = 1800 seconds)
    if home_id in last_activity:
        inactivity = (datetime.utcnow() - last_activity[home_id]).total_seconds()
        if inactivity > 1800:
            alerts.append(f"🚨 No activity in {home_id} for 30 minutes!")
            emergency = True
    
    processed = []
    for reading in readings:
        sensor_type = reading['type']
        value = reading['value']
        
        # Apply rules
        if sensor_type == 'fall_detection' and value == 1:
            alerts.append(f"🚨 FALL in {home_id}!")
            emergency = True
            reading['emergency'] = True
            
        elif sensor_type == 'gas_leak' and value == 1:
            alerts.append(f"☠️ GAS LEAK in {home_id}!")
            emergency = True
            reading['emergency'] = True
            
        elif sensor_type == 'heart_rate':
            if value <= 30 or value >= 150:
                alerts.append(f"🚨 CRITICAL HR in {home_id}: {value} BPM")
                emergency = True
                reading['emergency'] = True
            elif value <= 40 or value >= 130:
                alerts.append(f"⚠️ Abnormal HR in {home_id}: {value} BPM")
                reading['warning'] = True
                
        elif sensor_type == 'temperature':
            if value <= 5 or value >= 40:
                alerts.append(f"🚨 EXTREME TEMP in {home_id}: {value}°C")
                emergency = True
                reading['emergency'] = True
            elif value <= 10 or value >= 35:
                alerts.append(f"⚠️ Temp alert in {home_id}: {value}°C")
                reading['warning'] = True
        
        # Add fog metadata
        reading['fog_node'] = FOG_NODE_ID
        reading['processed_at'] = datetime.utcnow().isoformat()
        reading['emergency'] = reading.get('emergency', emergency)
        processed.append(reading)
    
    # Send to SQS
    try:
        for reading in processed:
            sqs.send_message(
                QueueUrl=SQS_QUEUE_URL,
                MessageBody=json.dumps(reading)
            )
    except Exception as e:
        print(f"Error sending to SQS: {e}")
        return jsonify({"error": str(e)}), 500
    
    return jsonify({
        "status": "success",
        "processed": len(processed),
        "alerts": len(alerts),
        "emergency": emergency,
        "alert_messages": alerts[:3]
    })

if __name__ == "__main__":
    print(f"🏥 Fog Node: {FOG_NODE_ID}")
    print("📡 Listening on port 5000")
    app.run(host='0.0.0.0', port=5000, debug=False)
# Added inactivity detection rule (30 minutes threshold)
# SQS Queue URL: https://sqs.us-east-1.amazonaws.com/306727604573/elderly-safety-queue
# Lambda function: elderly_safety_processor
