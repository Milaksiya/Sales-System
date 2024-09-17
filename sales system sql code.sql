
CREATE DATABASE IF NOT EXISTS Sales_System;

USE Sales_System;

-- Create tables
CREATE TABLE IF NOT EXISTS branches (
    branch_id INT AUTO_INCREMENT PRIMARY KEY,
    branch_name VARCHAR(255) NOT NULL,
    location VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS products (
    product_id VARCHAR(10) PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL
);

CREATE TABLE IF NOT EXISTS sales (
    sale_id INT AUTO_INCREMENT PRIMARY KEY,
    branch_id INT,
    product_id VARCHAR(10),
    date DATE,
    sales_amount DECIMAL(10, 2),
    quantity INT,
    FOREIGN KEY (branch_id) REFERENCES branches(branch_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- Insert sample data into tables
INSERT INTO branches (branch_name, location) VALUES
    ('Jaffna', 'Jaffna'),
    ('Mannar', 'Mannar'),
    ('Vavuniya', 'Vavuniya');

INSERT INTO products (product_id, product_name, price) VALUES
    ('P001', 'Mango', 10.99),
    ('P002', 'Biscuit', 15.50),
    ('P003', 'Shampoo', 7.25),
    ('P004', 'Rice', 50.00);

INSERT INTO sales (branch_id, product_id, date, sales_amount, quantity) VALUES
    (1, 'P001', '2024-06-01', 109.90, 10),
    (1, 'P002', '2024-06-02', 46.50, 3),
    (2, 'P001', '2024-06-03', 21.98, 2),
    (3, 'P003', '2024-06-04', 72.50, 5);

-- Display success message
SELECT 'Database, tables, and data insertion completed successfully.' AS status;

SELECT * FROM products;
SELECT * FROM sales;
SELECT * FROM branches;
ALTER TABLE products ADD COLUMN category VARCHAR(100);
ALTER TABLE products ADD COLUMN category VARCHAR(100);

-- Make sure to also update existing products to include a category
UPDATE products SET category = 'Fruits' WHERE product_id = 'P001';
UPDATE products SET category = 'Snacks' WHERE product_id = 'P002';
UPDATE products SET category = 'Personal Care' WHERE product_id = 'P003';
UPDATE products SET category = 'Staples' WHERE product_id = 'P004';

select * from products;
DELETE FROM branches WHERE branch_id = 15;
SELECT * FROM branches;
DELETE FROM branches WHERE branch_id = 6;
SELECT * FROM branches;

ALTER TABLE products ADD COLUMN quantity INT DEFAULT 0;
SELECT * FROM products;
SELECT * FROM sales;
SELECT * FROM branches;
