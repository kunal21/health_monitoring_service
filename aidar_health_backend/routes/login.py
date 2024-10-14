from flask import request, jsonify, session
from Models.models import Physician
from werkzeug.security import check_password_hash  

def set_auth_routes(app):

    @app.route('/login', methods=['POST', 'OPTIONS'])
    def login():
        if request.method == "OPTIONS":
            return build_cors_preflight_response()

        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid input, please provide JSON"}), 400
        
        email = data.get('email')
        password = data.get('password')
        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400

        # Find physician by email
        try:
            physician = Physician.query.filter_by(email=email).first()
        except Exception as e:
            return jsonify({"error": "Database error"}), 500

        if not physician or not check_password_hash(physician.password, password):
            return jsonify({"error": "Invalid email or password"}), 401

        # Store physician_id in the session
        session['physician_id'] = physician.id

        return jsonify({"message": "Login successful", "physician_id": physician.id}), 200

    @app.route('/logout', methods=['POST'])
    def logout():
        session.clear()
        return jsonify({"message": "Logout successful"}), 200
    
    def build_cors_preflight_response():
        response = jsonify({"message": "CORS preflight successful"})
        response.headers.add("Access-Control-Allow-Origin", "http://localhost:3000")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        response.headers.add("Access-Control-Allow-Credentials", "true")
        return response
