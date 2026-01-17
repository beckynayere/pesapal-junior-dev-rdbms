#!/usr/bin/env python3
"""
PesaPal JuniorDB - Web Demo
A complete CRUD web application demonstrating the RDBMS
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for
import sys
import os

# Add parent directory to path to import db modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from db.parser import Parser
from db.executor import Executor
from db.storage import Storage

app = Flask(__name__)

# Initialize database
storage = Storage()
parser = Parser()
executor = Executor(storage)

def init_sample_data():
    """Initialize sample data for the demo"""
    sample_queries = [
        # Drop existing tables
        "DROP TABLE IF EXISTS products",
        "DROP TABLE IF EXISTS customers",
        "DROP TABLE IF EXISTS orders",
        
        # Create products table
        """CREATE TABLE products (
            id INT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            description TEXT,
            price DECIMAL(10,2) NOT NULL,
            category VARCHAR(50),
            stock_quantity INT DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""",
        
        # Create customers table
        """CREATE TABLE customers (
            id INT PRIMARY KEY,
            first_name VARCHAR(50) NOT NULL,
            last_name VARCHAR(50) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            phone VARCHAR(20),
            address TEXT,
            city VARCHAR(50),
            country VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""",
        
        # Create orders table
        """CREATE TABLE orders (
            id INT PRIMARY KEY,
            customer_id INT NOT NULL,
            product_id INT NOT NULL,
            quantity INT NOT NULL,
            total_price DECIMAL(10,2) NOT NULL,
            status VARCHAR(20) DEFAULT 'pending',
            order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            notes TEXT
        )""",
        
        # Insert sample products
        "INSERT INTO products (name, description, price, category, stock_quantity) VALUES ('Laptop Pro', 'High-performance laptop for professionals', 1299.99, 'Electronics', 50)",
        "INSERT INTO products (name, description, price, category, stock_quantity) VALUES ('Wireless Mouse', 'Ergonomic wireless mouse with long battery life', 29.99, 'Electronics', 200)",
        "INSERT INTO products (name, description, price, category, stock_quantity) VALUES ('Coffee Maker', 'Programmable coffee maker with thermal carafe', 89.99, 'Home Appliances', 75)",
        "INSERT INTO products (name, description, price, category, stock_quantity) VALUES ('Desk Chair', 'Ergonomic office chair with lumbar support', 249.99, 'Furniture', 30)",
        "INSERT INTO products (name, description, price, category, stock_quantity) VALUES ('Backpack', 'Water-resistant laptop backpack with USB port', 49.99, 'Accessories', 150)",
        
        # Insert sample customers
        "INSERT INTO customers (first_name, last_name, email, phone, address, city, country) VALUES ('John', 'Doe', 'john.doe@email.com', '+1234567890', '123 Main St', 'Nairobi', 'Kenya')",
        "INSERT INTO customers (first_name, last_name, email, phone, address, city, country) VALUES ('Jane', 'Smith', 'jane.smith@email.com', '+0987654321', '456 Park Ave', 'Mombasa', 'Kenya')",
        "INSERT INTO customers (first_name, last_name, email, phone, address, city, country) VALUES ('David', 'Johnson', 'david.j@email.com', '+1122334455', '789 Market St', 'Kampala', 'Uganda')",
        "INSERT INTO customers (first_name, last_name, email, phone, address, city, country) VALUES ('Sarah', 'Williams', 'sarah.w@email.com', '+5566778899', '321 Oak Rd', 'Dar es Salaam', 'Tanzania')",
        
        # Insert sample orders
        "INSERT INTO orders (customer_id, product_id, quantity, total_price, status) VALUES (1, 1, 1, 1299.99, 'delivered')",
        "INSERT INTO orders (customer_id, product_id, quantity, total_price, status) VALUES (1, 2, 2, 59.98, 'processing')",
        "INSERT INTO orders (customer_id, product_id, quantity, total_price, status) VALUES (2, 3, 1, 89.99, 'delivered')",
        "INSERT INTO orders (customer_id, product_id, quantity, total_price, status) VALUES (3, 4, 1, 249.99, 'pending')",
        "INSERT INTO orders (customer_id, product_id, quantity, total_price, status) VALUES (4, 5, 3, 149.97, 'shipped')",
    ]
    
    for query in sample_queries:
        try:
            parsed = parser.parse(query)
            executor.execute(parsed)
        except Exception as e:
            # Ignore errors for DROP TABLE IF EXISTS
            if "not found" not in str(e):
                print(f"Warning: Could not execute: {query[:50]}...")
                print(f"Error: {e}")

# Initialize sample data on startup
init_sample_data()

@app.route('/')
def dashboard():
    """Main dashboard"""
    return render_template('dashboard.html')

# ========== PRODUCTS CRUD ==========
@app.route('/products')
def products_list():
    """List all products"""
    try:
        result = executor.execute(parser.parse("SELECT * FROM products ORDER BY id"))
        return render_template('products.html', products=result if isinstance(result, list) else [])
    except Exception as e:
        return render_template('products.html', products=[], error=str(e))

@app.route('/products/create', methods=['GET', 'POST'])
def create_product():
    """Create new product"""
    if request.method == 'POST':
        try:
            name = request.form['name']
            description = request.form['description']
            price = float(request.form['price'])
            category = request.form['category']
            stock = int(request.form['stock_quantity'])
            
            query = f"""INSERT INTO products (name, description, price, category, stock_quantity) 
                       VALUES ('{name}', '{description}', {price}, '{category}', {stock})"""
            
            result = executor.execute(parser.parse(query))
            return redirect(url_for('products_list'))
        except Exception as e:
            return render_template('product_form.html', error=str(e), title="Create Product")
    
    return render_template('product_form.html', title="Create Product")

@app.route('/products/<int:product_id>/edit', methods=['GET', 'POST'])
def edit_product(product_id):
    """Edit existing product"""
    if request.method == 'POST':
        try:
            name = request.form['name']
            description = request.form['description']
            price = float(request.form['price'])
            category = request.form['category']
            stock = int(request.form['stock_quantity'])
            
            query = f"""UPDATE products SET 
                       name = '{name}', 
                       description = '{description}', 
                       price = {price}, 
                       category = '{category}', 
                       stock_quantity = {stock} 
                       WHERE id = {product_id}"""
            
            executor.execute(parser.parse(query))
            return redirect(url_for('products_list'))
        except Exception as e:
            return render_template('product_form.html', error=str(e), title="Edit Product")
    
    # GET: Load existing product
    try:
        query = f"SELECT * FROM products WHERE id = {product_id}"
        result = executor.execute(parser.parse(query))
        if result and isinstance(result, list):
            product = result[0]
            return render_template('product_form.html', product=product, title="Edit Product")
        else:
            return redirect(url_for('products_list'))
    except Exception as e:
        return redirect(url_for('products_list'))

@app.route('/products/<int:product_id>/delete', methods=['POST'])
def delete_product(product_id):
    """Delete product"""
    try:
        query = f"DELETE FROM products WHERE id = {product_id}"
        executor.execute(parser.parse(query))
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# ========== CUSTOMERS CRUD ==========
@app.route('/customers')
def customers_list():
    """List all customers"""
    try:
        result = executor.execute(parser.parse("SELECT * FROM customers ORDER BY id"))
        return render_template('customers.html', customers=result if isinstance(result, list) else [])
    except Exception as e:
        return render_template('customers.html', customers=[], error=str(e))

@app.route('/customers/create', methods=['GET', 'POST'])
def create_customer():
    """Create new customer"""
    if request.method == 'POST':
        try:
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            email = request.form['email']
            phone = request.form.get('phone', '')
            address = request.form.get('address', '')
            city = request.form.get('city', '')
            country = request.form.get('country', '')
            
            query = f"""INSERT INTO customers (first_name, last_name, email, phone, address, city, country) 
                       VALUES ('{first_name}', '{last_name}', '{email}', '{phone}', '{address}', '{city}', '{country}')"""
            
            executor.execute(parser.parse(query))
            return redirect(url_for('customers_list'))
        except Exception as e:
            return render_template('customer_form.html', error=str(e), title="Create Customer")
    
    return render_template('customer_form.html', title="Create Customer")

# ========== ORDERS CRUD ==========
@app.route('/orders')
def orders_list():
    """List all orders with customer and product details"""
    try:
        query = """SELECT o.id, o.order_date, o.quantity, o.total_price, o.status,
                          c.first_name || ' ' || c.last_name as customer_name,
                          p.name as product_name
                   FROM orders o
                   JOIN customers c ON o.customer_id = c.id
                   JOIN products p ON o.product_id = p.id
                   ORDER BY o.order_date DESC"""
        
        result = executor.execute(parser.parse(query))
        return render_template('orders.html', orders=result if isinstance(result, list) else [])
    except Exception as e:
        return render_template('orders.html', orders=[], error=str(e))

# ========== API ENDPOINTS ==========
@app.route('/api/execute', methods=['POST'])
def execute_query():
    """Execute raw SQL query"""
    try:
        query = request.json.get('query', '').strip()
        if not query:
            return jsonify({'success': False, 'error': 'Empty query'})
        
        parsed = parser.parse(query)
        result = executor.execute(parsed)
        
        return jsonify({
            'success': True,
            'result': result if isinstance(result, str) else result,
            'type': 'string' if isinstance(result, str) else 'list'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/stats')
def get_stats():
    """Get database statistics"""
    try:
        stats = {
            'products': 0,
            'customers': 0,
            'orders': 0,
            'revenue': 0
        }
        
        # Count products
        result = executor.execute(parser.parse("SELECT COUNT(*) as count FROM products"))
        if isinstance(result, list) and result:
            stats['products'] = result[0].get('count', 0)
        
        # Count customers
        result = executor.execute(parser.parse("SELECT COUNT(*) as count FROM customers"))
        if isinstance(result, list) and result:
            stats['customers'] = result[0].get('count', 0)
        
        # Count orders and calculate revenue
        result = executor.execute(parser.parse("SELECT COUNT(*) as count, SUM(total_price) as revenue FROM orders"))
        if isinstance(result, list) and result:
            stats['orders'] = result[0].get('count', 0)
            stats['revenue'] = float(result[0].get('revenue', 0) or 0)
        
        return jsonify({'success': True, 'stats': stats})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# ========== ERROR HANDLERS ==========
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error='Page not found'), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template('error.html', error='Internal server error'), 500

if __name__ == '__main__':
    print("=" * 60)
    print("PesaPal JuniorDB - Web Demo")
    print("=" * 60)
    print("Database initialized with sample data:")
    print("  • 5 products")
    print("  • 4 customers")
    print("  • 5 orders")
    print("\nAvailable routes:")
    print("  • http://localhost:5000/ - Dashboard")
    print("  • http://localhost:5000/products - Products CRUD")
    print("  • http://localhost:5000/customers - Customers CRUD")
    print("  • http://localhost:5000/orders - Orders with JOIN")
    print("\nStarting server...")
    print("Open http://localhost:5000 in your browser")
    print("=" * 60)
    
    app.run(debug=True, port=5000)
