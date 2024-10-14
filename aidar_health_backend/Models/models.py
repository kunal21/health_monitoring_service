from app import db
from datetime import datetime

# Physician Table
class Physician(db.Model):
    __tablename__ = 'physicians'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    specialization = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __init__(self, name, specialization, email, password):
        self.name = name
        self.specialization = specialization
        self.email = email
        self.password = password

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "specialization": self.specialization
        }

# Patient Table
class Patient(db.Model):
    __tablename__ = 'patients'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)
    physician_id = db.Column(db.Integer, db.ForeignKey('physicians.id'), nullable=False)

    physician = db.relationship('Physician', backref=db.backref('patients', lazy=True))
    
    def __init__(self, name, age, physician_id):
        self.name = name
        self.age = age
        self.physician_id = physician_id

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "physician_id": self.physician_id
        }

# Threshold Table (depends on Physician)
class Threshold(db.Model):
    __tablename__ = 'thresholds'
    id = db.Column(db.Integer, primary_key=True)
    physician_id = db.Column(db.Integer, db.ForeignKey('physicians.id'), nullable=False)
    metric_name = db.Column(db.String(50), nullable=False)
    min_value = db.Column(db.Float, nullable=False)
    max_value = db.Column(db.Float, nullable=False)

    physician = db.relationship('Physician', backref=db.backref('thresholds', lazy=True))

    def __init__(self, physician_id, metric_name, min_value, max_value):
        self.physician_id = physician_id
        self.metric_name = metric_name
        self.min_value = min_value
        self.max_value = max_value

    def to_dict(self):
        return {
            "id": self.id,
            "physician_id": self.physician_id,
            "metric_name": self.metric_name,
            "min_value": self.min_value,
            "max_value": self.max_value
        }

# Alert Table (depends on Physician and Patient)
class Alert(db.Model):
    __tablename__ = 'alerts'
    id = db.Column(db.Integer, primary_key=True)
    physician_id = db.Column(db.Integer, db.ForeignKey('physicians.id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    metric_name = db.Column(db.String(50), nullable=False)
    value = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(10), nullable=False)  # 'above' or 'below'
    timestamp = db.Column(db.DateTime, default=datetime.now)
    acknowledged = db.Column(db.Boolean, default=False)

    physician = db.relationship('Physician', backref=db.backref('alerts', lazy=True))
    patient = db.relationship('Patient', backref=db.backref('alerts', lazy=True))

    def __init__(self, physician_id, patient_id, metric_name, value, status, timestamp, acknowledged):
        self.physician_id = physician_id
        self.patient_id = patient_id
        self.metric_name = metric_name
        self.value = value
        self.status = status
        self.timestamp = timestamp
        self.acknowledged = acknowledged

    def to_dict(self):
        return {
            "id": self.id,
            "physician_id": self.physician_id,
            "patient_id": self.patient_id,
            "metric_name": self.metric_name,
            "value": self.value,
            "status": self.status,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'acknowledged': self.acknowledged
        }
