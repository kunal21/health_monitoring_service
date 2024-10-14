from flask import request, jsonify, session
from Models.models import Threshold, Physician
from app import db

# Define routes for thresholds
def set_threshold_routes(app):
    
    @app.route('/api/threshold', methods=['POST'])
    def set_threshold():
        try:
            # Check session for logged-in physician
            physician_id = session.get('physician_id')
            if not physician_id:
                return jsonify({"error": "Unauthorized"}), 401

            # Parse and validate input
            data = request.get_json()
            if not data:
                return jsonify({"error": "Invalid input"}), 400
            
            metric_name = data.get('metric_name')
            min_value = data.get('min_value')
            max_value = data.get('max_value')

            if not metric_name or not isinstance(min_value, (int, float)) or not isinstance(max_value, (int, float)):
                return jsonify({"error": "Invalid input: metric_name, min_value, and max_value are required"}), 400

            if min_value >= max_value:
                return jsonify({"error": "Min value must be less than Max value"}), 400

            # Check if physician exists
            physician = Physician.query.get(physician_id)
            if not physician:
                print(f"Physician ID {physician_id} not found in the database")
                return jsonify({"error": "Physician not found in the Database"}), 404

            # Check if a threshold already exists for this physician and metric
            existing_threshold = Threshold.query.filter_by(physician_id=physician_id, metric_name=metric_name).first()

            if existing_threshold:
                # Update the existing threshold
                existing_threshold.min_value = min_value
                existing_threshold.max_value = max_value
                db.session.commit()
                return jsonify({"message": "Threshold updated successfully!"}), 200
            else:
                # Create a new threshold
                new_threshold = Threshold(physician_id, metric_name, min_value, max_value)
                db.session.add(new_threshold)
                db.session.commit()
                return jsonify({"message": "Threshold set successfully!"}), 201
        except Exception as e:
            return jsonify({"error": "An unexpected error occurred"}), 500

    @app.route('/api/threshold/', methods=['GET'])
    def get_thresholds():
        try:
            # Check session for logged-in physician
            physician_id = session.get('physician_id')
            if not physician_id:
                return jsonify({"error": "Unauthorized"}), 401
        
            # Check if physician exists
            physician = Physician.query.get(physician_id)
            if not physician:
                return jsonify({"error": "Physician not found in the Database"}), 404

            # Fetch and return all thresholds for this physician
            thresholds = Threshold.query.filter_by(physician_id=physician_id).all()
            return jsonify([t.to_dict() for t in thresholds]), 200
        
        except Exception as e:
            return jsonify({"error": "An unexpected error occurred"}), 500
        
    