import random
import time
import requests

# Backend API URLs
API_URL = "http://localhost:5000/api/patient-data"

METRIC_RANGES = {
    "heart_rate": {"min": 60, "max": 100},
    "blood_pressure_systolic": {"min": 90, "max": 120},
    "blood_pressure_diastolic": {"min": 60, "max": 80},
    "respiratory_rate": {"min": 12, "max": 20},
    "oxygen_saturation": {"min": 95, "max": 100},
    "body_temperature": {"min": 36.1, "max": 37.2},
    "blood_glucose": {"min": 70, "max": 140}
}

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

def send_patient_data(patient_id, health_data):
    payload = {
        "patient_id": patient_id,
        "health_data": health_data
    }
    
    try:
        response = requests.post(API_URL, json=payload)
        if response.status_code == 200:
            print(f"Data sent successfully for patient {patient_id}: {health_data}")
        else:
            print(f"Failed to send data for {patient_id} - Status Code: {response.status_code}, {response.__dict__}")
    except Exception as e:
        print(f"Error sending data for {patient_id}: {str(e)}")

def simulate_patient_data(interval=5):
    while True:
        for patient_id in range(1, 8):
            health_data = generate_health_data()
            send_patient_data(patient_id, health_data)
        time.sleep(interval)

if __name__ == "__main__":
    simulate_patient_data(interval=5)
