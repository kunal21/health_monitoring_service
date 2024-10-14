import collections
from datetime import datetime
from flask import request, jsonify, session
from Models.models import Threshold, Physician, Alert, Patient
from app import db, socketio
from flask_socketio import join_room


def set_patient_routes(app):

    @app.route('/api/patient-data', methods=['POST'])
    def receive_patient_data():
        try:
            # Parse and validate incoming data
            data = request.get_json()
            if not data or 'patient_id' not in data or 'health_data' not in data:
                return jsonify({"error": "Invalid request. Missing 'patient_id' or 'health_data'"}), 400

            patient_id = data.get('patient_id')
            patient_health_data = data.get('health_data')
            
            # Validate required fields
            if not isinstance(patient_id, int) or not isinstance(patient_health_data, dict):
                return jsonify({"error": "Invalid data format"}), 400
            
            # Find the patient
            patient = Patient.query.get(patient_id)
            if not patient:
                return jsonify({"error": "Patient not found"}), 404
            
            # Patient's physician
            physician_id = patient.physician_id
            
            out_of_range_metrics = collections.defaultdict(dict)
            for metric_name, value in patient_health_data.items():
                # Ensure value is numeric
                if not isinstance(value, (int, float)):
                    return jsonify({"error": f"Invalid value for {metric_name}. Must be a number."}), 400

                # Query for thresholds where the patient's health data is out of range
                thresholds = Threshold.query.filter(
                    Threshold.physician_id == physician_id,
                    Threshold.metric_name == metric_name,
                    db.or_(
                        value > Threshold.max_value,  # Check if value is above the max threshold
                        value < Threshold.min_value   # Check if value is below the min threshold
                    )
                ).all()

                # If any out-of-range thresholds are found, store them in the result
                for threshold in thresholds:
                    if value > threshold.max_value:
                        out_of_range_metrics[metric_name]["value"] = value
                        out_of_range_metrics[metric_name]["status"] = 'above'
                    elif value < threshold.min_value:
                        out_of_range_metrics[metric_name]["value"] = value
                        out_of_range_metrics[metric_name]["status"] = 'below'

                    
            # If any value is out of range, generate alerts
            alerts = []
            if out_of_range_metrics:
                for out_of_range_metric, out_of_range_metric_values in out_of_range_metrics.items():
                    new_alert = Alert(
                        physician_id=physician_id,
                        patient_id=patient.id,
                        metric_name=out_of_range_metric,
                        value=out_of_range_metric_values["value"],
                        status=out_of_range_metric_values["status"],
                        timestamp=datetime.now(),
                        acknowledged=False
                    )
                    db.session.add(new_alert)
                    alerts.append(new_alert)
                db.session.commit()

            # Notify the physician in real-time using WebSockets
            for alert in alerts:
                socketio.emit('new_alert', {
                    "alert": alert.to_dict(),
                    "patient_age": patient.age,
                    "patient_name": patient.name,
                }, room=f'physician_{physician_id}')

            # Return the alerts accordingly
            if alerts:
                return jsonify({"message": f"{len(alerts)} alert(s) generated", "alerts": [alert.to_dict() for alert in alerts]}), 201
            else:
                return jsonify({"message": "No alert generated, values within range"}), 200
        
        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"}), 500
        

@socketio.on('join')
def on_join():
    try:
        physician_id = session.get('physician_id')
        if physician_id:
            room = f'physician_{physician_id}'
            join_room(room)
            print(f'Physician {physician_id} has joined room {room}')
        else:
            print("Unauthorized: No physician_id in session")
    except Exception as e:
        print(f"Error during WebSocket room join: {str(e)}")
    
    