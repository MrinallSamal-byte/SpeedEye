import unittest
from backend.speed_detection import monitor_speed

class TestSpeedDetection(unittest.TestCase):
    def test_monitor_speed_within_limit(self):
        vehicle_id = "TEST123"
        location = "TestLocation"
        # Mock get_gps_location and get_speed to return a location and speed within the limit
        with unittest.mock.patch('hardware.gps_module.get_gps_location', return_value=location):
            with unittest.mock.patch('hardware.speed_sensor.get_speed', return_value=50):
                monitor_speed(vehicle_id)
                # Add assertions to verify the behavior

    def test_monitor_speed_exceeding_limit(self):
        vehicle_id = "TEST123"
        location = "TestLocation"
        # Mock get_gps_location and get_speed to return a location and speed exceeding the limit
        with unittest.mock.patch('hardware.gps_module.get_gps_location', return_value=location):
            with unittest.mock.patch('hardware.speed_sensor.get_speed', return_value=90):
                monitor_speed(vehicle_id)
                # Add assertions to verify the behavior

    def test_monitor_speed_inaccuracy(self):
        vehicle_id = "TEST123"
        location = "TestLocation"
        # Mock get_gps_location and get_speed to return a location and speed below the threshold
        with unittest.mock.patch('hardware.gps_module.get_gps_location', return_value=location):
            with unittest.mock.patch('hardware.speed_sensor.get_speed', return_value=3):
                monitor_speed(vehicle_id)
                # Add assertions to verify the behavior

if __name__ == '__main__':
    unittest.main()
