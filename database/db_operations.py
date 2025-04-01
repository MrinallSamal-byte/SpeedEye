from db_config import connect_db
import logging

def insert_speed_data(vehicle_id, speed):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        query = "INSERT INTO vehicle_speed (vehicle_id, speed) VALUES (%s, %s)"
        cursor.execute(query, (vehicle_id, speed))
        conn.commit()
        conn.close()
    except Exception as e:
        logging.error(f"Error inserting speed data for vehicle {vehicle_id}: {e}")

def fetch_all_speed_data():
    try:
        conn = connect_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM vehicle_speed")
        data = cursor.fetchall()
        conn.close()
        return data
    except Exception as e:
        logging.error(f"Error fetching all speed data: {e}")
        return []

def insert_vehicle_speed(vehicle_id, speed):
    query = """
    INSERT INTO vehicle_speed (vehicle_id, speed)
    VALUES (%s, %s)
    """
    params = (vehicle_id, speed)
    execute_query(query, params)

def insert_challan(vehicle_id, speed, location, amount):
    query = """
    INSERT INTO challan (vehicle_id, speed, location, amount)
    VALUES (%s, %s, %s, %s)
    """
    params = (vehicle_id, speed, location, amount)
    execute_query(query, params)

def execute_query(query, params):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        conn.close()
    except Exception as e:
        logging.error(f"Error executing query: {e}")

def fetch_all_challans():
    try:
        conn = connect_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM challan")
        data = cursor.fetchall()
        conn.close()
        return data
    except Exception as e:
        logging.error(f"Error fetching all challans: {e}")
        return []
