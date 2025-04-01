import mysql.connector

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="device_user",
        password="your_password",
        database="device_project"
    )
print("Database connected!")
