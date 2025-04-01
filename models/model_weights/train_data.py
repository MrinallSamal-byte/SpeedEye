class IndianDrivingLaws:
    def __init__(self):
        # Define speed limits for different road types (in km/h)
        self.speed_limits = {
            "highway": 100,
            "city": 50,
            "residential": 30,
            "school_zone": 20,
            "construction_zone": 25
        }
        self.default_speed_limits = self.speed_limits.copy()  # Store default limits

    def get_speed_limit(self, road_type):
        """
        Get the speed limit for a given road type.
        """
        return self.speed_limits.get(road_type, "Unknown road type")

    def validate_speed(self, road_type, speed):
        """
        Validate if the given speed complies with the speed limit for the road type.
        """
        speed_limit = self.get_speed_limit(road_type)
        if speed_limit == "Unknown road type":
            print(f"Road type '{road_type}' is not recognized.")
            return False
        if speed > speed_limit:
            print(f"Speed {speed} km/h exceeds the limit of {speed_limit} km/h for {road_type}.")
            return False
        print(f"Speed {speed} km/h is within the limit for {road_type}.")
        return True

    def update_speed_limit(self, road_type, new_limit):
        """
        Update the speed limit for a specific road type.
        """
        if road_type in self.speed_limits:
            self.speed_limits[road_type] = new_limit
            print(f"Speed limit for {road_type} updated to {new_limit} km/h.")
        else:
            print(f"Road type '{road_type}' does not exist.")

    def is_valid_road_type(self, road_type):
        """
        Check if the given road type is valid.
        """
        return road_type in self.speed_limits

    def reset_to_default_limits(self):
        """
        Reset all speed limits to their default values.
        """
        self.speed_limits = self.default_speed_limits.copy()
        print("Speed limits reset to default values.")

    def add_road_type(self, road_type, speed_limit):
        """
        Add a new road type with a specified speed limit.
        """
        if road_type in self.speed_limits:
            print(f"Road type '{road_type}' already exists.")
        else:
            self.speed_limits[road_type] = speed_limit
            print(f"Road type '{road_type}' added with speed limit {speed_limit} km/h.")

# Example usage:
# laws = IndianDrivingLaws()
# laws.validate_speed("highway", 110)  # Exceeds limit
# laws.validate_speed("city", 40)     # Within limit
# laws.update_speed_limit("city", 60)
# print(laws.is_valid_road_type("highway"))  # True
# laws.add_road_type("expressway", 120)
# laws.reset_to_default_limits()
