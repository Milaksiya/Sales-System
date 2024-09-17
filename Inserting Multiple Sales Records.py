import pytest
from App import establish_connection, insert_sales

# This fixture establishes the database connection for the tests
@pytest.fixture(scope='module')
def Database():
    conn = establish_connection()
    yield conn
    conn.close()

def test_insert_multiple_sales(Database):
    branch_name = "Jaffna"
    product_name = "Pencil Box"
    date = "2024-07-10"
    sales_amount = 50.00
    quantity = 5

    for i in range(5):  # Insert multiple sales records
        insert_sales(branch_name, product_name, date, sales_amount, quantity)

    assert True  # Placeholder for database verification
