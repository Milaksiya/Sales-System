import mysql.connector
import matplotlib.pyplot as plt

# Function to establish a database connection
def establish_db_connection():
    db_connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='12345',
        database='Sales_System'  # Replace with your database name
    )
    return db_connection

# Function to fetch monthly sales data for a branch
def fetch_monthly_sales_data(db_connection, branch_id):
    # SQL query to fetch monthly sales data for a branch
    query = "SELECT MONTH(date) AS month, SUM(sales_amount) AS total_sales FROM sales WHERE branch_id = %s GROUP BY MONTH(date) ORDER BY MONTH(date)"
    cursor = db_connection.cursor()
    cursor.execute(query, (branch_id,))
    sales_data = cursor.fetchall()
    cursor.close()
    return sales_data

# Function for monthly sales analysis
def monthly_sales_analysis(db_connection, branch_id):
    # Retrieve monthly sales data for a specific branch
    sales_data = fetch_monthly_sales_data(db_connection, branch_id)

    # Extract months and sales amounts from fetched data
    months = [row[0] for row in sales_data]
    sales_amounts = [row[1] for row in sales_data]

    # Plotting using matplotlib
    plt.figure(figsize=(10, 6))
    plt.plot(months, sales_amounts, marker='o', linestyle='-', color='b')
    plt.xlabel('Month')
    plt.ylabel('Sales Amount')
    plt.title('Monthly Sales Analysis for Branch {}'.format(branch_id))
    plt.grid(True)
    plt.xticks(months)  # Ensure months are displayed as ticks on x-axis
    plt.tight_layout()
    plt.show()

# Main function to demonstrate usage
def main():
    # Establish database connection
    db_connection = establish_db_connection()

    # Example: Perform monthly sales analysis for Branch 1
    branch_id = 1
    monthly_sales_analysis(db_connection, branch_id)

    # Close database connection when done
    db_connection.close()

if __name__ == "__main__":
    main()
