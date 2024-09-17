
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

# MySQL Connection Configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '12345',
    'database': 'Sales_System'
}

# Function to establish MySQL connection
def establish_connection():
    try:
        conn = mysql.connector.connect(**db_config)
        print("Connected to MySQL database")
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Function to perform price analysis of each product
def price_analysis(conn):
    try:
        cursor = conn.cursor()

        # Example query for price analysis (replace with your query)
        query = """
            SELECT product_id, AVG(price) AS avg_price
            FROM products
            GROUP BY product_id
        """
        cursor.execute(query)
        price_data = cursor.fetchall()
        cursor.close()

        # Process and display or plot price analysis
        for row in price_data:
            product_id = row[0]
            avg_price = row[1]
            print(f"Product ID: {product_id}, Average Price: {avg_price}")

    except mysql.connector.Error as err:
        print(f"Error in price analysis: {err}")

# Main function to run the analysis
def main():
    # Establish MySQL connection
    conn = establish_connection()
    if not conn:
        return

    # Perform price analysis
    price_analysis(conn)

    # Close MySQL connection
    conn.close()
    print("MySQL connection closed")

if __name__ == "__main__":
    main()
