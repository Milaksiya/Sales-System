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

# Function for sales distribution analysis
def sales_distribution_analysis():
    conn = establish_connection()  # Establish MySQL connection
    if not conn:
        return

    try:
        # SQL query to analyze sales distribution by branch and product
        query = """
            SELECT branch_id, product_id, SUM(sales_amount) AS total_sales
            FROM sales
            GROUP BY branch_id, product_id
            ORDER BY branch_id, total_sales DESC
        """
        cursor = conn.cursor()
        cursor.execute(query)
        sales_distribution_data = cursor.fetchall()
        cursor.close()

        # Process and display sales distribution analysis (print or return as needed)
        for row in sales_distribution_data:
            branch_id = row[0]
            product_id = row[1]
            total_sales = row[2]
            print(f"Branch ID: {branch_id}, Product ID: {product_id}, Total Sales: {total_sales}")

    except mysql.connector.Error as err:
        print(f"Error in sales distribution analysis: {err}")

    finally:
        conn.close()  # Close MySQL connection
        print("MySQL connection closed")

# Main function to run the analysis
def main():
    sales_distribution_analysis()  # Perform sales distribution analysis

if __name__ == "__main__":
    main()
