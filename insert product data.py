
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

# Function to insert product data
def insert_product(product_id, product_name, price):
    conn = establish_connection()  # Establish MySQL connection
    if not conn:
        return

    try:
        # SQL query to insert product data
        query = "INSERT INTO products (product_id, product_name, price) VALUES (%s, %s, %s)"
        cursor = conn.cursor()
        cursor.execute(query, (product_id, product_name, price))
        conn.commit()
        print("Product inserted successfully")

    except mysql.connector.Error as err:
        print(f"Error in inserting product: {err}")

    finally:
        if 'cursor' in locals():
            cursor.close()
        conn.close()  # Close MySQL connection
        print("MySQL connection closed")

# Main function to run the insert operation
def main():
    # Example usage: Insert a product
    insert_product('P001', 'Product A', 19.99)

if __name__ == "__main__":
    main()
