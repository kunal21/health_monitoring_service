# Aidar Health Backend

This is the backend for the **Aidar Health** project, a platform designed to monitor patient health metrics, set thresholds, and generate real-time alerts using WebSockets.

## Table of Contents

1. Project Overview
2. Features
3. Technologies Used
4. Installation and Setup
5. API Endpoints
6. Database Schema
7. Running the Application
8. WebSocket Notifications
9. Security

## Project Overview

The **Aidar Health Backend** handles all server-side operations for the health monitoring system. It provides an API for managing thresholds, patients, and physicians, and generates alerts when health metrics go beyond the defined thresholds. WebSocket notifications are used for real-time alerting, and patient and physician data are stored securely in a database.

## Features

- Manage health metric thresholds for physicians.
- Monitor patient health data.
- Generate real-time alerts when thresholds are breached.
- Secure physician authentication and session management.
- WebSocket notifications for real-time updates on alerts.

## Technologies Used

- **Python**: Backend logic.
- **Flask**: Lightweight web framework.
- **Flask-SQLAlchemy**: ORM for interacting with the SQLite database.
- **Flask-SocketIO**: For WebSocket support.
- **SQLite**: Database for storing application data.
- **Flask-Session**: Manages user sessions securely.
- **CORS**: Cross-Origin Resource Sharing to allow the frontend to interact with the backend.

## Installation and Setup

To run this backend project locally, follow these steps:

1. Clone the repository.
2. Navigate to the project folder.
3. Set up a virtual environment (optional but recommended).
4. Install required dependencies from the `requirements.txt` file.
5. Run the application.

## API Endpoints

### Threshold Management

- `POST /api/threshold`: Create or update a health metric threshold for a physician.
- `GET /api/threshold/`: Get all thresholds set for the currently authenticated physician.

### Alert Management

- `GET /api/alerts`: Retrieve all unacknowledged alerts for the authenticated physician.
- `POST /api/acknowledge-alert`: Acknowledge an alert by ID.

### Patient Data

- `POST /api/patient-data`: Send patient health data and generate alerts if thresholds are breached.

### Authentication

- `POST /login`: Physician login to start a session.

## Database Schema

The application uses an SQLite database to store all relevant data. Here is an overview of the key tables used in the database:

- **Physician**:
  - `id`: Unique identifier for the physician.
  - `name`: Physician's full name.
  - `email`: Email address (used for login).
  - `password`: Hashed password for authentication.
  - `specialization`: Medical field of specialization (e.g., Cardiologist).

- **Patient**:
  - `id`: Unique identifier for the patient.
  - `name`: Patient's full name.
  - `age`: Patient's age.
  - `physician_id`: Foreign key to the `Physician` table.

- **Threshold**:
  - `id`: Unique identifier for the threshold.
  - `physician_id`: Foreign key to the `Physician` table.
  - `metric_name`: Name of the health metric (e.g., heart_rate).
  - `min_value`: Minimum value of the metric.
  - `max_value`: Maximum value of the metric.

- **Alert**:
  - `id`: Unique identifier for the alert.
  - `physician_id`: Foreign key to the `Physician` table.
  - `patient_id`: Foreign key to the `Patient` table.
  - `metric_name`: Name of the health metric.
  - `value`: The metric value that triggered the alert.
  - `status`: Whether the value is above or below the threshold.
  - `acknowledged`: Whether the alert has been acknowledged.
  - `timestamp`: Timestamp of the generated alert.

## Running the Application

1. Ensure that all dependencies are installed.
2. To start the backend, run the backend application using the appropriate command.
   `python run.py`
4. The backend should now be running on `http://localhost:5000`.

## WebSocket Notifications

The backend uses **Flask-SocketIO** to emit real-time notifications to the frontend when a patient's health metrics breach predefined thresholds. To listen for alerts on the frontend, connect to the WebSocket at `http://localhost:5000` and subscribe to `new_alert` events.

## Security

- **Session Management**: The application uses Flask-Session for secure, server-side session management.
- **CORS**: Configured to allow cross-origin requests only from the trusted frontend hosted at `http://localhost:3000`.
- **Password Hashing**: All physician passwords are stored securely using hashing algorithms.

