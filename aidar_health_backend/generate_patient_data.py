import random
import time
import requests

# Backend API URLs
LOGIN_URL = "http://localhost:5000/login"
API_URL = "http://localhost:5000/api/patient-data"

patients = [
    {"patient_id": 1},
    {"patient_id": 2},
    {"patient_id": 3},
    {"patient_id": 4},
    {"patient_id": 5},
    {"patient_id": 6},
    {"patient_id": 7}
]

METRIC_RANGES = {
    "heart_rate": {"min": 60, "max": 100},
    "blood_pressure_systolic": {"min": 90, "max": 120},
    "blood_pressure_diastolic": {"min": 60, "max": 80},
    "respiratory_rate": {"min": 12, "max": 20},
    "oxygen_saturation": {"min": 95, "max": 100},
    "body_temperature": {"min": 36.1, "max": 37.2},
    "blood_glucose": {"min": 70, "max": 140}
}


# Function to log in and obtain session cookie
def login(session, username, password):
    payload = {"email": username, "password": password}
    try:
        response = session.post(LOGIN_URL, json=payload)
        if response.status_code == 200:
            print("Login successful")
        else:
            print(f"Login failed - Status Code: {response.status_code}, {response.json()}")
            return False
    except Exception as e:
        print(f"Error during login: {str(e)}")
        return False
    return True

# Function to generate random health metric values (with occasional out-of-range values)
def generate_health_data():
    health_data = {}
    
    for metric, range_ in METRIC_RANGES.items():
        out_of_range = random.choice([True, False, False, False]) 

        if out_of_range:
            if random.choice([True, False]):
                value = range_["max"] + random.uniform(1, 20) 
            else:
                value = range_["min"] - random.uniform(1, 20) 
        else:
            value = random.uniform(range_["min"], range_["max"])
        
        health_data[metric] = round(value, 2) 
    
    return health_data

def send_patient_data(session, patient, health_data):
    payload = {
        "patient_id": patient["patient_id"],
        "health_data": health_data
    }
    
    try:
        response = session.post(API_URL, json=payload)
        if response.status_code == 200:
            print(f"Data sent successfully for patient {patient['name']}: {health_data}")
        else:
            print(f"Failed to send data for {patient['name']} - Status Code: {response.status_code}, {response.__dict__}")
    except Exception as e:
        print(f"Error sending data for {patient['name']}: {str(e)}")

def simulate_patient_data(session, interval=5):
    while True:
        for patient in patients:
            health_data = generate_health_data()
            send_patient_data(session, patient, health_data)
        time.sleep(interval)

if __name__ == "__main__":
    session = requests.Session()

    if login(session, username="abc@test.com", password="physician1"):
        simulate_patient_data(session, interval=5)
