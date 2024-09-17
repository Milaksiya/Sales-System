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

# Function for weekly sales analysis
def weekly_sales_analysis():
    conn = establish_connection()  # Establish MySQL connection
    if not conn:
        return

    try:
        # SQL query to fetch weekly sales data across all branches
        query = "SELECT WEEK(date), SUM(sales_amount) FROM sales GROUP BY WEEK(date) ORDER BY WEEK(date)"
        cursor = conn.cursor()
        cursor.execute(query)
        weekly_sales_data = cursor.fetchall()
        cursor.close()

        # Process and display weekly sales analysis (print or return as needed)
        for week, sales_amount in weekly_sales_data:
            print(f"Week {week}: Sales Amount = {sales_amount}")

    except mysql.connector.Error as err:
        print(f"Error in weekly sales analysis: {err}")

    finally:
        conn.close()  # Close MySQL connection
        print("MySQL connection closed")

# Main function to run the analysis
def main():
    weekly_sales_analysis()  # Perform weekly sales analysis

if __name__ == "__main__":
    main()
