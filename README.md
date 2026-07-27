# Elderly Home Safety Monitoring System

## Fog and Edge Computing Project - NCI 2026

### Overview
A fog-based elderly home safety monitoring system with:
- 5 sensor types (fall, heart rate, temperature, activity, gas leak)
- Fog node on AWS EC2 with real-time processing
- Scalable cloud backend (SQS → Lambda → DynamoDB)
- Responsive dashboard with emergency alerts

### Architecture
Sensors → Fog Node (EC2) → SQS → Lambda → DynamoDB → Dashboard

### Technologies
- Python 3.11
- Flask
- AWS (EC2, SQS, Lambda, DynamoDB)
- HTML/CSS/JavaScript

### Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Configure AWS: `aws configure`
3. Run fog node: `python3 fog/fog_node.py`
4. Run sensors: `python3 sensors/elderly_sensors.py`
5. Run dashboard: `python3 -m http.server 5001`

### Repository Structure


elderly-home-safety/
│
├── sensors/
│   └── elderly_sensors.py
│
├── fog/
│   └── fog_node.py
│
├── dashboard/
│   └── dashboard.html
│
├── README.md
└── .gitignore


## Cloud Architecture



## Features

- Real-time elderly home monitoring
- Fall detection
- Heart rate monitoring
- Temperature monitoring
- Activity monitoring
- Gas leak detection
- Emergency alert processing
- AWS cloud integration


## Future Improvements

- Docker container deployment
- Kubernetes deployment
- GitHub Actions CI/CD pipeline
- Prometheus and Grafana monitoring
- Machine learning based anomaly detection

