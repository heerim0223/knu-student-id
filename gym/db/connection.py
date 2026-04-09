import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        # DB password
        password="",
        database="gym_db"
    )
