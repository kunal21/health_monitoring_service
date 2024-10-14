# Aidar Health

Aidar Health is a web-based application that provides healthcare professionals with real-time alerts and the ability to manage patient health metrics and thresholds. The system consists of two main parts: a frontend built with React and a backend built using Flask.

## Project Structure

aidar_health/  
├── aidar_health_frontend/  # React frontend for managing health metrics and alerts  
├── aidar_health_backend/  # Flask backend providing APIs and WebSocket functionality  
└── README.md  # This file

## Requirements

### Global Requirements

- Node.js (for frontend)
- Python 3.x (for backend)
- Git for version control

## Frontend (`aidar_health_frontend`)

The frontend of the application is built with React and manages the UI for setting thresholds and displaying alerts in real-time.

### Key Features

- **Threshold Management**: Physicians can set custom health metrics thresholds for patients.
- **Alert Management**: Alerts are displayed in real-time when patients' health data falls outside of the defined thresholds.

### Getting Started (Frontend)

1. Navigate to the frontend directory: `cd aidar_health_frontend/`
2. Install the dependencies: `npm install`
3. Start the development server: `npm start`

This will run the React app locally at `http://localhost:3000`. For more detailed information, refer to the frontend's README inside the `aidar_health_frontend/` folder.

## Backend (`aidar_health_backend`)

The backend is a Flask-based API that provides the necessary routes for managing thresholds, alerts, and patients. It also handles WebSocket connections to push real-time alerts to the frontend.

### Key Features

- **RESTful API**: Provides endpoints for managing patients, thresholds, and alerts.
- **WebSocket Integration**: Pushes real-time alerts to the frontend using Flask-SocketIO.
- **Session Management**: Handles authentication and session management for physicians.

### Getting Started (Backend)

1. Navigate to the backend directory: `cd aidar_health_backend/`
2. Set up a Python virtual environment: `python3 -m venv venv`
3. Activate the virtual environment:
    - On macOS/Linux: `source venv/bin/activate`
    - On Windows: `venv\Scripts\activate`
4. Install the dependencies: `pip install -r requirements.txt`
5. Start the backend server: `python run.py`

The backend will run at `http://localhost:5000`. For more detailed information, refer to the backend's README inside the `aidar_health_backend/` folder.

## Running the `generate_patient_data.py` Script

The `generate_patient_data.py` script generates mock patient data and sends it to the backend to simulate real-time patient health data.

### Steps to Run the Script

1. Make sure the backend server is running (`http://localhost:5000`).
2. In a separate terminal, navigate to the `aidar_health_backend/` directory.
3. Run the script to start generating mock data: `python generate_patient_data.py`

This script will continuously send random health metric values for the patients to the backend, triggering real-time alerts when values exceed or fall below the thresholds set by physicians.

The backend listens for incoming data and will generate alerts when necessary, which will be pushed to the frontend via WebSocket.

