import time
import random
from backend.speed_detection import monitor_speed

def simulate_vehicle(vehicle_id):
    while True:
        # Simulate random speed between 0 and 100 km/h
        speed = random.uniform(0, 100)
        # Simulate location as a fixed value for simplicity
        location = "28.7041,77.1025"  # Example coordinates for New Delhi
        print(f"Simulating vehicle {vehicle_id} with speed {speed} km/h at location {location}")
        monitor_speed(vehicle_id)
        time.sleep(5)  # Wait for 5 seconds before the next simulation

if __name__ == "__main__":
    vehicle_id = "ABC123"
    simulate_vehicle(vehicle_id)
