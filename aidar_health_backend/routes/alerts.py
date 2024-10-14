from flask import jsonify, request, session
from Models.models import Alert, Patient
from app import db

# Define routes for alerts
def set_alert_routes(app):
    @app.route('/api/alerts', methods=['GET'])
    def get_alerts():
        try:
            # Ensure physician is authenticated
            physician_id = session.get('physician_id')
            if not physician_id:
                return jsonify({"error": "Unauthorized"}), 401

            # Get all the alerts and corresponsing patients for the provided Physician
            alert_results = db.session.query(Alert, Patient).join(Patient, Alert.patient_id == Patient.id).filter(
                Alert.physician_id == physician_id,
                Alert.acknowledged == False
                ).all()

            # Loop over the result of the query, which is a list of tuples (Alert, Patient)
            alerts_with_patient = []
            for alert, patient in alert_results:
                alert_data = alert.to_dict()
                alert_data['patient_name'] = patient.name
                alert_data['patient_age'] = patient.age
                alerts_with_patient.append(alert_data)
        
            # Return the result as JSON
            return jsonify(alerts_with_patient), 200
        
        except Exception as e:
            return jsonify({"error": "An unexpected error occurred"}), 500

    @app.route('/api/acknowledge-alert', methods=['POST'])
    def acknowledge_alert():
        try:
            # Ensure physician is authenticated
            physician_id = session.get('physician_id')
            if not physician_id:
                return jsonify({"error": "Unauthorized"}), 401
            
            # Validate input data
            data = request.get_json()
            if not data or not isinstance(data, dict):
                return jsonify({"error": "Invalid input data"}), 400
            
            alert_id = data.get('alert_id')
            if not alert_id or not isinstance(alert_id, int):
                return jsonify({"error": "Invalid or missing alert_id"}), 400
        
            # Find the alert
            alert = Alert.query.get(alert_id)
            if not alert:
                return jsonify({'error': 'Alert not found'}), 404
            
            # Ensure the alert belongs to the physician
            if alert.physician_id != physician_id:
                return jsonify({"error": "Unauthorized action"}), 403

            # Mark the alert as acknowledged
            alert.acknowledged = True
            db.session.commit()

            return jsonify({'message': 'Alert acknowledged'}), 200
        
        except Exception as e:
            return jsonify({"error": "An unexpected error occurred"}), 500