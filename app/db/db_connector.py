import mysql.connector

def get_db_connection():
    # Establishing the connection
    conn = mysql.connector.connect(
        host="localhost",        # Replace with your host
        user="root",    # Replace with your username
        password="Madmah@#2024",# Replace with your password
        database="cancer_atlas" # Replace with your database name
    )
    print("Connection successful!")

    cursor = conn.cursor(dictionary=True)
    return conn, cursor
