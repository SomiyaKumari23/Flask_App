import mysql.connector

try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Snakebite@123",
        database="flask_app"
    )
    print("Connection successful!")
except mysql.connector.Error as err:
    print(f"MySQL Error: {err}")
except Exception as e:
    print(f"Other Error: {e}")
