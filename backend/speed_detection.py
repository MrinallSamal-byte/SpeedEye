from hardware.speed_sensor import get_speed
from hardware.gps_module import get_gps_location
from hardware.gsm_module import send_sms
from database.db_operations import insert_speed_data
import logging

SPEED_LIMIT = 80  # Example speed limit
SPEED_THRESHOLD = 5  # Threshold to ignore minor inaccuracies

logging.basicConfig(level=logging.INFO)

def monitor_speed(vehicle_id):
    try:
        location = get_gps_location()  # Use the GPS module to get the location
        speed = get_speed()  # Use the hardware speed sensor to get the speed
        
        # Ignore minor inaccuracies
        if speed < SPEED_THRESHOLD:
            logging.info(f"Ignoring minor speed inaccuracy for vehicle {vehicle_id}: {speed} km/h.")
            return
        
        insert_speed_data(vehicle_id, speed)
        
        if speed > SPEED_LIMIT:
            logging.warning(f"ALERT! Vehicle {vehicle_id} exceeded speed limit with {speed} km/h.")
            detect_speed(vehicle_id, speed, location)
        else:
            logging.info(f"Vehicle {vehicle_id} is within the limit: {speed} km/h.")
    except Exception as e:
        logging.error(f"Error monitoring speed for vehicle {vehicle_id}: {e}")

def detect_speed(vehicle_id, speed, location):
    # Logic to detect speed and store in the database
    from database.db_operations import insert_vehicle_speed
    insert_vehicle_speed(vehicle_id, speed)
    if speed > SPEED_LIMIT:
        generate_challan(vehicle_id, speed, location)

def generate_challan(vehicle_id, speed, location):
    # Logic to generate challan and store in the database
    from database.db_operations import insert_challan
    challan_amount = calculate_challan_amount(speed)
    insert_challan(vehicle_id, speed, location, challan_amount)
    
    # Send SMS notification
    phone_number = "1234567890"  # Replace with the actual phone number
    message = f"Challan issued to vehicle {vehicle_id} for speeding at {speed} km/h. Location: {location}. Fine: ₹{challan_amount}."
    send_sms(phone_number, message)

def calculate_challan_amount(speed):
    # Logic to calculate challan amount based on speed
    if speed <= SPEED_LIMIT + 20:
        return 1000  # Fine for exceeding speed limit by up to 20 km/h
    else:
        return 2000  # Fine for exceeding speed limit by more than 20 km/h

# Example Usage
if __name__ == "__main__":
    monitor_speed("ABC123")
