import mysql.connector

# Define database connection
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345",
    database="Sales_System"
)
