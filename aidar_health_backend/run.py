from app import create_app, socketio
from Models.models import Physician, Alert, Patient
from werkzeug.security import generate_password_hash

app = create_app()

# List all registered patients
def list_all_patients():
    try:
        patients = Patient.query.all()
        for patient in patients:
            print(f"ID: {patient.id}, Name: {patient.name}, Physician: {patient.physician_id}, Age: {patient.age}")
    except Exception as e:
        print(f"Error fetching patients: {e}")

# List all registered physicians
def list_all_physicians():
    try:
        physicians = Physician.query.all()
        for physician in physicians:
            print(f"ID: {physician.id}, Name: {physician.name}, Specialization: {physician.specialization}, email: {physician.email}")
    except Exception as e:
        print(f"Error fetching physicians: {e}")

# Register dummy physicians
def register_physicians():
    try:
        physicians = [
            Physician(name="Dr. John Doe", email="abc@test.com", password=generate_password_hash("physician1"), specialization="Cardiologist"),
            Physician(name="Dr. Jane Smith", email="jane.smith@example.com", password=generate_password_hash("physician2"), specialization="Neurologist"),
            Physician(name="Dr. Alice Johnson", email="alice.johnson@example.com", password=generate_password_hash("physician3"), specialization="Pediatrician")
        ]
        db.session.bulk_save_objects(physicians)
        db.session.commit()
        print("3 physicians registered with passwords: physician1, physician2, physician3")
    except Exception as e:
        db.session.rollback()
        print(f"Error registering physicians: {e}")

# Register dummy patients
def register_patients():
    try:
        physicians = Physician.query.all()
        if not physicians:
            print("No physicians found. Please register physicians first.")
            return

        patients = [
            {"name": "Alice Green", "age": 30, "physician_id": physicians[0].id},  
            {"name": "Bob Brown", "age": 45, "physician_id": physicians[1].id},    
            {"name": "Charlie White", "age": 60, "physician_id": physicians[2].id}, 
            {"name": "David Black", "age": 25, "physician_id": physicians[0].id},  
            {"name": "Eva Blue", "age": 50, "physician_id": physicians[1].id}    
        ]

        for patient_data in patients:
            new_patient = Patient(
                name=patient_data['name'],
                age=patient_data['age'],
                physician_id=patient_data['physician_id']
            )
            db.session.add(new_patient)
        db.session.commit()
        print("Dummy patients added successfully!")
    except Exception as e:
        db.session.rollback()
        print(f"Error registering patients: {e}")


if __name__ == '__main__':
    with app.app_context():
        try:
            from app import db
    
            db.create_all()
            register_physicians()
            register_patients()

            list_all_physicians()
            list_all_patients()

            # Start the socket server
            socketio.run(app, host='0.0.0.0', port=5000, debug=True)
        except Exception as e:
            print(f"Error during setup or startup: {e}")