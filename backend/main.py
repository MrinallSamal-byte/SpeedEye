from backend.speed_detection import monitor_speed
from backend.ai_service import train_model

def run_system():
    vehicle_id = "ABC123"
    monitor_speed(vehicle_id)
    train_model()

if __name__ == "__main__":
    run_system()
