import os
from flask import Flask
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# MySQL configurations from environment variables or defaults
mysql_database_host = os.getenv('MYSQL_DATABASE_HOST', '10.10.0.115')
mysql_database_user = os.getenv('MYSQL_DATABASE_USER', 'db_user')
mysql_database_password = os.getenv('MYSQL_DATABASE_PASSWORD', 'Passw0rd')
mysql_database_db = os.getenv('MYSQL_DATABASE_DB', 'employee_db')

print(f"Configured MySQL with Host: {mysql_database_host}, User: {mysql_database_user}, Database: {mysql_database_db}")

# Establish MySQL connection
def get_db_connection():
    print(f"Attempting to connect to MySQL at {mysql_database_host} as {mysql_database_user}")
    try:
        conn = mysql.connector.connect(
            host=mysql_database_host,
            user=mysql_database_user,
            password=mysql_database_password,
            database=mysql_database_db
        )
        if conn.is_connected():
            print("Connection to MySQL successful")
        return conn
    except Error as e:
        print(f"Error: Could not connect to MySQL at {mysql_database_host} as {mysql_database_user}. Error: {e}")
        return None

@app.route("/")
def main():
    return "Welcome to the Employee Database API!"

@app.route('/how_are_you')
def hello():
    return 'I am good, how about you?'

@app.route('/read_from_database')
def read():
    print("Processing request: /read_from_database")
    conn = get_db_connection()

    if conn is None:
        print("Failed to establish a connection with the database")
        return 'Failed to connect to the database', 500

    try:
        cursor = conn.cursor()
        print("Executing query: SELECT name FROM employees")
        cursor.execute("SELECT name FROM employees")
        rows = cursor.fetchall()

        if not rows:
            print("Query result: No employees found")
            result = "No employees found"
        else:
            print(f"Query result: {len(rows)} employees found")
            result = ",".join([row[0] for row in rows])

        cursor.close()
        conn.close()
        print("Connection closed after query")
        return result

    except Error as e:
        print(f"Database query failed: {e}")
        return f"Failed to query database: {e}", 500
