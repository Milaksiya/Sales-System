
import mysql.connector
import matplotlib.pyplot as plt
import random
import string
import datetime
import matplotlib.cm as cm

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

# Function to get branch ID from branch name
def get_branch_id(branch_name):
    conn = establish_connection()
    if not conn:
        return None
    try:
        query = "SELECT branch_id FROM branches WHERE branch_name = %s"
        cursor = conn.cursor()
        cursor.execute(query, (branch_name,))
        branch_id = cursor.fetchone()
        cursor.close()
        return branch_id[0] if branch_id else None

    except mysql.connector.Error as err:
        print(f"Error in fetching branch ID: {err}")
        return None
    finally:
        conn.close()
        print("MySQL connection closed")

# Function to get product ID from product name
def get_product_id(product_name):
    conn = establish_connection()
    if not conn:
        return None
    try:
        query = "SELECT product_id FROM products WHERE product_name = %s"
        cursor = conn.cursor()
        cursor.execute(query, (product_name,))
        product_id = cursor.fetchone()
        cursor.close()
        return product_id[0] if product_id else None

    except mysql.connector.Error as err:
        print(f"Error in fetching product ID: {err}")
        return None
    finally:
        conn.close()
        print("MySQL connection closed")


# Function to perform price analysis
def price_analysis():
    conn = establish_connection()
    if not conn:
        return

    try:
        cursor = conn.cursor()

        # Get current month and year
        cursor.execute("SELECT MONTH(NOW()), YEAR(NOW())")
        current_month, current_year = cursor.fetchone()

        # Calculate the previous month and year
        previous_month = current_month - 1 if current_month > 1 else 12
        previous_year = current_year if current_month > 1 else current_year - 1

        # Query to get average prices of products for the current month and the previous month
        query = """
            SELECT p.product_id, p.product_name, 
                   AVG(CASE WHEN MONTH(s.date) = %s AND YEAR(s.date) = %s THEN p.price ELSE NULL END) AS current_month_avg_price,
                   AVG(CASE WHEN MONTH(s.date) = %s AND YEAR(s.date) = %s THEN p.price ELSE NULL END) AS previous_month_avg_price
            FROM products p
            LEFT JOIN sales s ON p.product_id = s.product_id
            WHERE (MONTH(s.date) = %s AND YEAR(s.date) = %s) 
               OR (MONTH(s.date) = %s AND YEAR(s.date) = %s)
            GROUP BY p.product_id, p.product_name
            ORDER BY p.product_id
        """
        cursor.execute(query, (
        current_month, current_year, previous_month, previous_year, current_month, current_year, previous_month,
        previous_year))
        price_data = cursor.fetchall()

        # Print the comparison report
        print("\n===== Price Analysis Summary Report =====")
        print("Product ID | Product Name | Previous Month Price | Current Month Price | Change (%)")
        print("=" * 80)

        for row in price_data:
            product_id, product_name, current_price, previous_price = row
            # Handle None values and calculate percentage change
            if current_price is None:
                current_price = 0
            if previous_price is None:
                previous_price = 0
            change_percentage = ((current_price - previous_price) / previous_price * 100) if previous_price > 0 else (current_price * 100)
            print(
                f"{product_id:<10} | {product_name:<12} | {previous_price:>20.2f} | {current_price:>18.2f} | {change_percentage:>10.2f}%")

        # Query to get branch-wise average product prices and product names
        query_branch_prices = """
            SELECT b.branch_id, b.branch_name, p.product_name, AVG(p.price) AS avg_price
            FROM sales s
            JOIN products p ON s.product_id = p.product_id
            JOIN branches b ON s.branch_id = b.branch_id
            WHERE MONTH(s.date) = %s AND YEAR(s.date) = %s
            GROUP BY b.branch_id, b.branch_name, p.product_name
            ORDER BY b.branch_id, p.product_name
        """
        cursor.execute(query_branch_prices, (current_month, current_year))
        branch_prices = cursor.fetchall()

        # Print the branch-wise price report
        print("\n===== Branch-wise Price Comparison =====")
        print("Branch ID | Branch Name | Product Name | Average Product Price")
        print("=" * 60)

        for branch_id, branch_name, product_name, avg_price in branch_prices:
            print(f"{branch_id:<10} | {branch_name:<12} | {product_name:<12} | {avg_price:>20.2f}")

        # Query to get branch-wise average product prices for the previous month
        query_branch_prices_prev = """
            SELECT b.branch_id, b.branch_name, p.product_name, AVG(p.price) AS avg_price
            FROM sales s
            JOIN products p ON s.product_id = p.product_id
            JOIN branches b ON s.branch_id = b.branch_id
            WHERE MONTH(s.date) = %s AND YEAR(s.date) = %s
            GROUP BY b.branch_id, b.branch_name, p.product_name
            ORDER BY b.branch_id, p.product_name
        """
        cursor.execute(query_branch_prices_prev, (previous_month, previous_year))
        branch_prices_prev = cursor.fetchall()

        # Print the previous month branch-wise price report
        print("\n===== Previous Month Branch-wise Price Comparison =====")
        print("Branch ID | Branch Name | Product Name | Average Product Price")
        print("=" * 60)

        for branch_id, branch_name, product_name, avg_price in branch_prices_prev:
            print(f"{branch_id:<10} | {branch_name:<12} | {product_name:<12} | {avg_price:>20.2f}")

    finally:
        if conn and conn.is_connected():
            conn.close()
            print("MySQL connection closed")

# Function for weekly sales analysis
def get_start_date_of_week(year, week):
    d = datetime.date(year, 1, 1)
    if d.weekday() <= 3:
        d = d - datetime.timedelta(d.weekday())  # Adjust the date to the previous Monday
    else:
        d = d + datetime.timedelta(7 - d.weekday())  # Adjust the date to the next Monday
    dlt = datetime.timedelta(days=(week - 1) * 7)
    return d + dlt

def weekly_sales_analysis():
    conn = establish_connection()
    if not conn:
        return
    try:
        query = "SELECT YEAR(date) AS year, WEEK(date) AS week, SUM(sales_amount) AS total_sales FROM sales GROUP BY YEAR(date), WEEK(date) ORDER BY YEAR(date), WEEK(date)"
        cursor = conn.cursor()
        cursor.execute(query)
        weekly_sales_data = cursor.fetchall()
        cursor.close()

        for year, week, total_sales in weekly_sales_data:
            start_date = get_start_date_of_week(year, week)
            end_date = start_date + datetime.timedelta(days=6)
            print(f"Week {week} ({start_date} to {end_date}): Sales Amount = {total_sales}")

    except mysql.connector.Error as err:
        print(f"Error in weekly sales analysis: {err}")
    finally:
        conn.close()
        print("MySQL connection closed")

# Function for product preference analysis
def product_preference_analysis():
    conn = establish_connection()
    if not conn:
        return

    try:
        # Query to get product preferences by branch
        query = """
            SELECT b.branch_name, p.product_id, p.product_name, SUM(s.quantity) AS total_quantity
            FROM sales s
            JOIN products p ON s.product_id = p.product_id
            JOIN branches b ON s.branch_id = b.branch_id
            WHERE DATE_FORMAT(s.date, '%Y-%m') = DATE_FORMAT(NOW(), '%Y-%m')
            GROUP BY b.branch_name, p.product_id, p.product_name
            ORDER BY b.branch_name, total_quantity DESC
        """
        cursor = conn.cursor()
        cursor.execute(query)
        product_preference_data = cursor.fetchall()
        cursor.close()

        # Organize data by branch
        branch_data = {}
        for branch_name, product_id, product_name, total_quantity in product_preference_data:
            if branch_name not in branch_data:
                branch_data[branch_name] = []
            branch_data[branch_name].append((product_id, product_name, total_quantity))

        # Display branch-wise product preference details
        print("\n===== Product Preference Analysis by Branch =====")
        for branch_name, products in branch_data.items():
            print(f"\nBranch: {branch_name}")
            print(f"{'Product ID':<10} | {'Product Name':<20} | {'Total Quantity Sold':>20}")
            print("=" * 50)
            for product_id, product_name, total_quantity in products:
                print(f"{product_id:<10} | {product_name:<20} | {total_quantity:>20}")

        # Process data for pie chart
        all_products = [(f"{branch_name}: {product_name}", total_quantity) for branch_name, products in branch_data.items() for product_id, product_name, total_quantity in products]
        product_labels = [product[0] for product in all_products]
        total_quantities = [product[1] for product in all_products]

        # Generate a pie chart
        plt.figure(figsize=(14, 10))
        plt.pie(total_quantities, labels=product_labels, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired(range(len(product_labels))))
        plt.title('Sales Distribution of Top Products by Quantity Sold This Month (Branch-wise)')
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.show()

    except mysql.connector.Error as err:
        print(f"Error in product preference analysis: {err}")
    finally:
        conn.close()
        print("MySQL connection closed")





# Function for sales distribution analysis************l

# Function to get branch ID from branch name
def get_branch_id(branch_name):
    conn = establish_connection()
    if not conn:
        return None
    try:
        query = "SELECT branch_id FROM branches WHERE branch_name = %s"
        cursor = conn.cursor()
        cursor.execute(query, (branch_name,))
        branch_id = cursor.fetchone()
        cursor.close()
        if branch_id:
            return branch_id[0]
        else:
            print("Branch not found.")
            return None
    except mysql.connector.Error as err:
        print(f"Error fetching branch ID: {err}")
        return None
    finally:
        conn.close()


# Function for sales distribution analysis
def sales_distribution_analysis():
    conn = establish_connection()
    if not conn:
        return

    try:
        branch_name = input("Enter your branch name: ")
        branch_id = get_branch_id(branch_name)
        if not branch_id:
            return

        # Query to get total purchase quantity and total sales quantity for each product in the specified branch
        query = """
            SELECT p.product_name,
                   COALESCE(SUM(s.quantity), 0) AS total_quantity_sold
            FROM products p
            LEFT JOIN sales s ON p.product_id = s.product_id AND s.branch_id = %s
            GROUP BY p.product_name
            ORDER BY p.product_name
        """
        cursor = conn.cursor()
        cursor.execute(query, (branch_id,))
        sales_distribution_data = cursor.fetchall()

        # Clear any remaining results to avoid "Unread result found" error
        conn.commit()
        cursor.close()

        # Prepare data for the chart
        product_names = [row[0] for row in sales_distribution_data]
        total_quantities_sold = [row[1] for row in sales_distribution_data]

        # Query to get the quantity purchased for each product in the specified branch
        query_purchases = """
            SELECT p.product_name,
                   COALESCE(SUM(s.quantity), 0) AS total_quantity_purchased
            FROM products p
            LEFT JOIN sales s ON p.product_id = s.product_id AND s.branch_id = %s
            GROUP BY p.product_name
            ORDER BY p.product_name
        """
        cursor = conn.cursor()
        cursor.execute(query_purchases, (branch_id,))
        purchase_data = cursor.fetchall()
        cursor.close()

        # Prepare data for the chart
        total_quantities_purchased = [row[1] for row in purchase_data]

        # Plotting the data
        x = range(len(product_names))
        plt.figure(figsize=(14, 8))
        width = 0.35  # Bar width
        plt.bar(x, total_quantities_sold, width=width, color='b', align='center', label='Total Quantity Sold')
        plt.bar([p + width for p in x], total_quantities_purchased, width=width, color='r', align='center',
                label='Total Quantity Purchased')

        plt.xlabel('Product Name')
        plt.ylabel('Quantity')
        plt.title(f'Sales and Purchase Analysis for Branch {branch_name}')
        plt.xticks([p + width / 2 for p in x], product_names, rotation=45, ha='right')
        plt.legend()
        plt.tight_layout()  # Adjust layout to make room for the rotated x-axis labels
        plt.show()

    except mysql.connector.Error as err:
        print(f"Error in sales distribution analysis: {err}")
    finally:
        conn.close()
        print("MySQL connection closed")



# Function for monthly sales analysis
def monthly_sales_analysis(branch_name):
    branch_id = get_branch_id(branch_name)
    if not branch_id:
        print("Invalid branch name")
        return

    conn = establish_connection()
    if not conn:
        return
    try:
        query = "SELECT MONTH(date) AS month, SUM(sales_amount) AS total_sales FROM sales WHERE branch_id = %s GROUP BY MONTH(date) ORDER BY MONTH(date)"
        cursor = conn.cursor()
        cursor.execute(query, (branch_id,))
        sales_data = cursor.fetchall()
        cursor.close()

        months = [row[0] for row in sales_data]
        sales_amounts = [row[1] for row in sales_data]

        plt.figure(figsize=(10, 6))
        plt.plot(months, sales_amounts, marker='o', linestyle='-', color='b')
        plt.xlabel('Month')
        plt.ylabel('Sales Amount')
        plt.title(f'Monthly Sales Analysis for Branch {branch_name}')
        plt.grid(True)
        plt.xticks(months)
        plt.tight_layout()
        plt.show()

    except mysql.connector.Error as err:
        print(f"Error in monthly sales analysis: {err}")
    finally:
        conn.close()
        print("MySQL connection closed")

# Function to insert branch details
def insert_branch(branch_name, location):
    conn = establish_connection()
    if not conn:
        return
    try:
        query = "INSERT INTO branches (branch_name, location) VALUES (%s, %s)"
        cursor = conn.cursor()
        cursor.execute(query, (branch_name, location))
        conn.commit()
        print("Branch inserted successfully")

    except mysql.connector.Error as err:
        print(f"Error in inserting branch: {err}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        conn.close()
        print("MySQL connection closed")

# Function to generate a random product ID
def generate_product_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

# Function to insert product data***********************
# Function to insert product data
def insert_product(product_name, price, quantity):
    conn = establish_connection()
    if not conn:
        return
    try:
        product_id = generate_product_id()
        query = "INSERT INTO products (product_id, product_name, price, quantity) VALUES (%s, %s, %s, %s)"
        cursor = conn.cursor()
        cursor.execute(query, (product_id, product_name, price, quantity))
        conn.commit()
        print("Product inserted successfully with Product ID:", product_id)

    except mysql.connector.Error as err:
        print(f"Error in inserting product: {err}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        conn.close()
        print("MySQL connection closed")


# Function to insert sales data****************
def insert_sales(branch_name, product_name, date, sales_amount, quantity):
    conn = establish_connection()
    if not conn:
        return
    try:
        branch_id = get_branch_id(branch_name)
        product_id = get_product_id(product_name)

        if branch_id and product_id:
            print(f"Debug: Branch ID = {branch_id}, Product ID = {product_id}")  # Debug message
            query = "INSERT INTO sales (branch_id, product_id, date, sales_amount, quantity) VALUES (%s, %s, %s, %s, %s)"
            cursor = conn.cursor()
            cursor.execute(query, (branch_id, product_id, date, sales_amount, quantity))
            conn.commit()
            print("Sales data inserted successfully")
        else:
            print("Invalid branch name or product name")

    except mysql.connector.Error as err:
        print(f"Error in inserting sales data: {err}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        conn.close()
        print("MySQL connection closed")

# Function to display all products
def display_products():
    conn = establish_connection()
    if not conn:
        return
    try:
        query = "SELECT * FROM products"
        cursor = conn.cursor()
        cursor.execute(query)
        products = cursor.fetchall()
        cursor.close()

        for product in products:
            print(f"Product ID: {product[0]}, Product Name: {product[1]}, Price: {product[2]}")

    except mysql.connector.Error as err:
        print(f"Error in displaying products: {err}")
    finally:
        conn.close()
        print("MySQL connection closed")

# Function to display all branches
def display_branches():
    conn = establish_connection()
    if not conn:
        return
    try:
        query = "SELECT * FROM branches"
        cursor = conn.cursor()
        cursor.execute(query)
        branches = cursor.fetchall()
        cursor.close()

        for branch in branches:
            print(f"Branch ID: {branch[0]}, Branch Name: {branch[1]}, Location: {branch[2]}")

    except mysql.connector.Error as err:
        print(f"Error in displaying branches: {err}")
    finally:
        conn.close()
        print("MySQL connection closed")

# Function to display all sales data
def display_sales_data():
    conn = establish_connection()
    if not conn:
        return
    try:
        query = "SELECT * FROM sales"
        cursor = conn.cursor()
        cursor.execute(query)
        sales = cursor.fetchall()
        cursor.close()

        for sale in sales:
            print(f"Sale ID: {sale[0]}, Branch ID: {sale[1]}, Product ID: {sale[2]}, Date: {sale[3]}, Sales Amount: {sale[4]}, Quantity: {sale[5]}")

    except mysql.connector.Error as err:
        print(f"Error in displaying sales data: {err}")
    finally:
        conn.close()
        print("MySQL connection closed")

# Main menu function
# Main menu function
def main_menu():
    while True:
        print("\n===== Sampath Food City Sales Data Analysis System =====")
        print("1. Check Monthly Sales Analysis")
        print("2. Check Price Analysis")
        print("3. Check Weekly Sales Analysis")
        print("4. Check Product Preference Analysis")
        print("5. Check Sales Distribution Analysis")
        print("6. Add Branch")
        print("7. Add Product")
        print("8. Add Sales Data")
        print("9. Display Products lists")
        print("10. Display Branches lists")
        print("11. Display Sales Data lists")
        print("12. Exit")

        choice = input("Enter choice: ")

        if choice == '1':
            branch_name = input("Enter your Branch Name: ")
            monthly_sales_analysis(branch_name)
        elif choice == '2':
            price_analysis()
        elif choice == '3':
            weekly_sales_analysis()
        elif choice == '4':
            product_preference_analysis()
        elif choice == '5':
            sales_distribution_analysis()
        elif choice == '6':
            branch_name = input("Enter Branch Name: ")
            location = input("Enter Branch Location: ")
            insert_branch(branch_name, location)
        elif choice == '7':
            product_name = input("Enter Product Name: ")
            price = float(input("Enter Price: "))
            quantity = int(input("Enter Quantity: "))  # New line to ask for quantity
            insert_product(product_name, price, quantity)  # Pass quantity to the function
        elif choice == '8':
            branch_name = input("Enter Branch Name: ")
            product_name = input("Enter Product Name: ")
            date = input("Enter Date (YYYY-MM-DD): ")
            sales_amount = float(input("Enter Sales Amount: "))
            quantity = int(input("Enter Quantity: "))
            insert_sales(branch_name, product_name, date, sales_amount, quantity)
        elif choice == '9':
            display_products()
        elif choice == '10':
            display_branches()
        elif choice == '11':
            display_sales_data()
        elif choice == '12':
            break
        else:
            print("Invalid choice. Please enter a valid option.")


# Example of how to run the main menu
if __name__ == "__main__":
    main_menu()

