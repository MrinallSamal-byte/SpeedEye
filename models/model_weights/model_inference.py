import requests
from datetime import datetime, timedelta
from models.model_weights.train_data import IndianDrivingLaws
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from playsound import playsound  # Import playsound for playing audio
from utils.logger import setup_logger  # Import logger setup

class SpeedMonitor:
    def __init__(self, speed_limit, google_maps_api_key):
        self.speed_limit = speed_limit
        self.google_maps_api_key = google_maps_api_key
        self.monitoring_active = False  # Monitoring is off by default
        self.violations_log = []  # Table to store violations
        self.violation_start_time = None  # Track when the speed violation starts
        self.laws = IndianDrivingLaws()  # Initialize Indian driving laws
        self.logger = setup_logger()  # Initialize logger
        self.emergency_mode = False  # Emergency mode is off by default

    def activate_monitoring(self):
        """
        Activate monitoring manually.
        """
        self.monitoring_active = True
        self.logger.info("Monitoring activated.")
        print("Monitoring activated.")

    def deactivate_monitoring(self):
        """
        Deactivate monitoring manually.
        """
        self.monitoring_active = False
        self.logger.info("Monitoring deactivated.")
        print("Monitoring deactivated.")

    def activate_emergency_mode(self):
        """
        Activate emergency mode to temporarily disable speed monitoring.
        """
        self.emergency_mode = True
        self.logger.info("Emergency mode activated. Speed monitoring disabled.")
        print("Emergency mode activated. Speed monitoring disabled.")

    def deactivate_emergency_mode(self):
        """
        Deactivate emergency mode to resume speed monitoring.
        """
        self.emergency_mode = False
        self.logger.info("Emergency mode deactivated. Speed monitoring resumed.")
        print("Emergency mode deactivated. Speed monitoring resumed.")

    def play_sound_alert(self):
        """
        Play a sound alert to notify the user that they are crossing the speed limit.
        """
        try:
            # Replace 'alert.mp3' with the path to your sound file
            playsound('/workspaces/SpeedEye/assets/alert.mp3')
            self.logger.info("Sound alert played.")
            print("Sound alert played.")
        except Exception as e:
            self.logger.error(f"Failed to play sound alert: {e}")
            print(f"Failed to play sound alert: {e}")

    def compare_speed(self, gps_speed, instrument_speed, road_type, gps_signal_strength, user_email, vehicle_lat=None, vehicle_lng=None):
        """
        Compare the GPS speed and instrument speed with the speed limit.
        Handle weak GPS signals and notify the user if the difference between readings is too high.
        """
        if self.emergency_mode:
            print("Emergency mode is active. Skipping speed monitoring.")
            self.logger.info("Speed monitoring skipped due to emergency mode.")
            return

        if not self.monitoring_active:
            print("Monitoring is currently inactive.")
            self.logger.info("Monitoring is inactive.")
            return

        # Handle weak GPS signal
        if gps_signal_strength < 3:  # Assuming signal strength is on a scale of 1 to 5
            print("Weak GPS signal detected. Relying on instrument speed only.")
            self.logger.warning("Weak GPS signal detected. Using instrument speed only.")
            average_speed = instrument_speed
        else:
            # Calculate average speed from both readings
            average_speed = (gps_speed + instrument_speed) / 2

            # Check for significant difference between readings
            if abs(gps_speed - instrument_speed) > 15:  # Threshold for significant difference
                print("Significant difference detected between GPS and instrument readings.")
                self.logger.warning("Significant difference detected between GPS and instrument readings.")
                self.notify_repair(user_email)
        
        # Validate speed against Indian driving laws
        if not self.laws.validate_speed(road_type, average_speed):
            self.logger.warning(f"Speed violation detected: {average_speed} km/h on {road_type}.")
            print("Violation detected based on Indian driving laws.")
            self.play_sound_alert()  # Play sound alert when speed limit is crossed
            if self.violation_start_time is None:
                self.violation_start_time = datetime.now()
                self.logger.info("Speed violation detected. Timer started.")
                print("Speed violation detected. Timer started.")
            elif datetime.now() - self.violation_start_time > timedelta(seconds=5):
                location = None
                if vehicle_lat is not None and vehicle_lng is not None:
                    location = self.get_live_location(vehicle_lat, vehicle_lng)
                self.log_violation(average_speed, location)
                self.issue_challan(average_speed)
                self.violation_start_time = None  # Reset the timer after logging
        else:
            self.violation_start_time = None  # Reset the timer if speed is back within the limit
            self.logger.info(f"Speed within limit: {average_speed} km/h on {road_type}.")
            print("Speed is within the limit.")

    def issue_challan(self, speed):
        """
        Issue a challan for exceeding the speed limit.
        """
        print(f"Challan issued! Speed recorded: {speed} km/h, which exceeds the limit of {self.speed_limit} km/h.")
        self.logger.info(f"Challan issued for speed: {speed} km/h.")
        # Logic to send a copy of the challan to the user can be added here.

    def log_violation(self, speed, location):
        """
        Log the violation details including date, time, speed, and location.
        """
        violation_entry = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "time": datetime.now().strftime("%H:%M:%S"),
            "speed": speed,
            "location": location or "Unknown"
        }
        self.violations_log.append(violation_entry)
        self.logger.info(f"Violation logged: Speed={speed} km/h, Location={location}.")
        print(f"Violation logged: {violation_entry}")

    def get_live_location(self, vehicle_lat, vehicle_lng):
        """
        Fetch the live location of the vehicle using Google Maps API.
        """
        url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={vehicle_lat},{vehicle_lng}&key={self.google_maps_api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            location_data = response.json()
            if location_data.get("results"):
                address = location_data["results"][0]["formatted_address"]
                self.logger.info(f"Live location fetched: {address}")
                print(f"Live location: {address}")
                return address
            else:
                self.logger.warning("No address found for the given coordinates.")
                print("No address found for the given coordinates.")
        else:
            self.logger.error(f"Failed to fetch location. HTTP Status Code: {response.status_code}")
            print(f"Failed to fetch location. HTTP Status Code: {response.status_code}")
        return None

    def send_notification(self, user_email, speed, location):
        """
        Send a notification to the user when a challan is issued.
        """
        try:
            sender_email = "your_email@example.com"
            sender_password = "your_password"
            subject = "Speed Violation Notification"
            body = f"""
            Dear User,

            A speed violation has been detected:
            - Speed: {speed} km/h
            - Location: {location or 'Unknown'}

            Please address this issue promptly.

            Regards,
            SpeedEye Team
            """

            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = user_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))

            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.send_message(msg)

            self.logger.info(f"Notification sent to {user_email}.")
            print(f"Notification sent to {user_email}.")
        except Exception as e:
            self.logger.error(f"Failed to send notification: {e}")
            print(f"Failed to send notification: {e}")

    def notify_repair(self, user_email):
        """
        Notify the user to visit a car repair center within 3 days for a checkup.
        """
        try:
            sender_email = "your_email@example.com"
            sender_password = "your_password"
            subject = "Car Repair Notification"
            body = f"""
            Dear User,

            A significant difference between GPS and instrument speed readings has been detected.
            Please visit a car repair center within 3 days for a checkup.

            Regards,
            SpeedEye Team
            """

            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = user_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))

            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.send_message(msg)

            self.logger.info(f"Repair notification sent to {user_email}.")
            print(f"Repair notification sent to {user_email}.")
        except Exception as e:
            self.logger.error(f"Failed to send repair notification: {e}")
            print(f"Failed to send repair notification: {e}")

    def generate_violation_summary(self):
        """
        Generate a summary of all logged violations.
        """
        print("\nViolation Summary:")
        self.logger.info("Generating violation summary.")
        for idx, violation in enumerate(self.violations_log, start=1):
            print(f"{idx}. Date: {violation['date']}, Time: {violation['time']}, "
                  f"Speed: {violation['speed']} km/h, Location: {violation['location']}")
        print("\n")

# Example usage:
# monitor = SpeedMonitor(speed_limit=80, google_maps_api_key="YOUR_GOOGLE_MAPS_API_KEY")
# monitor.activate_monitoring()
# monitor.compare_speed(gps_speed=85, instrument_speed=90, road_type="highway", gps_signal_strength=4, user_email="user@example.com", vehicle_lat=28.7041, vehicle_lng=77.1025)
# monitor.deactivate_monitoring()
