from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_socketio import SocketIO
from flask_session import Session
import os

# Initialize the database
db = SQLAlchemy()
socketio = SocketIO(cors_allowed_origins="http://localhost:3000", manage_session=True, async_mode='eventlet')


def create_app():
    app = Flask(__name__)

    app.secret_key = os.getenv('SECRET_KEY', os.urandom(24))

    CORS(app, supports_credentials=True, resources={r"/*": {"origins": os.getenv('FRONTEND_URL', "http://localhost:3000")}})
    
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///aidar_health.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Session configuration: store sessions on the filesystem
    app.config['SESSION_TYPE'] = 'filesystem'   
    app.config['SESSION_PERMANENT'] = False     
    app.config['SESSION_USE_SIGNER'] = True     
    app.config['SESSION_COOKIE_HTTPONLY'] = True 
    app.config['SESSION_COOKIE_SECURE'] = False   # set to true for production (HTTPS)
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

    # Initialize session management
    Session(app)

    # Bind db and socketio to app
    db.init_app(app)
    socketio.init_app(app)

    # Import and register routes after app is created to avoid circular imports
    from routes.threshold import set_threshold_routes
    from routes.alerts import set_alert_routes
    from routes.login import set_auth_routes
    from routes.patient_data import set_patient_routes
    set_threshold_routes(app)
    set_alert_routes(app)
    set_auth_routes(app)
    set_patient_routes(app)

    return app