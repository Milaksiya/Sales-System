import mysql.connector

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

# Function for product preference analysis
def product_preference_analysis():
    conn = establish_connection()  # Establish MySQL connection
    if not conn:
        return

    try:
        # SQL query to analyze product preference
        query = """
            SELECT product_id, product_name, SUM(quantity) AS total_quantity
            FROM sales
            JOIN products ON sales.product_id = products.product_id
            WHERE DATE_FORMAT(date, '%Y-%m') = DATE_FORMAT(NOW(), '%Y-%m')
            GROUP BY product_id
            ORDER BY total_quantity DESC
            LIMIT 10
        """
        cursor = conn.cursor()
        cursor.execute(query)
        product_preference_data = cursor.fetchall()
        cursor.close()

        # Process and display product preference analysis (print or return as needed)
        for row in product_preference_data:
            product_id = row[0]
            product_name = row[1]
            total_quantity = row[2]
            print(f"Product ID: {product_id}, Product Name: {product_name}, Total Quantity: {total_quantity}")

    except mysql.connector.Error as err:
        print(f"Error in product preference analysis: {err}")

    finally:
        conn.close()  # Close MySQL connection
        print("MySQL connection closed")

# Main function to run the analysis
def main():
    product_preference_analysis()  # Perform product preference analysis

if __name__ == "__main__":
    main()
