# pesapal-junior-dev-rdbms

PesaPal JuniorDB - Simple RDBMS
A lightweight relational database management system built in Python with SQL-like interface and web demo.

🚀 Quick Start
bash
# Setup
python3 -m venv venv
source venv/bin/activate
pip install flask

# Run REPL
python3 main.py

# Run Web Demo
python3 web-demo/app.py
✨ Features
SQL-like query language with CREATE, SELECT, INSERT, UPDATE, DELETE

Table schemas with INT, VARCHAR, FLOAT, BOOLEAN types

Primary & Unique keys for data integrity

JOIN operations (INNER, LEFT)

Interactive REPL for command-line use

Web interface with full CRUD operations

File-based storage with persistence

📖 Usage Examples
SQL Operations
sql
-- Create table
CREATE TABLE users (id INT PRIMARY KEY, name VARCHAR(50), email VARCHAR(100))

-- Insert data
INSERT INTO users (name, email) VALUES ('John Doe', 'john@example.com')

-- Query data
SELECT * FROM users WHERE email = 'john@example.com'

-- Join tables
SELECT u.name, o.amount 
FROM users u 
JOIN orders o ON u.id = o.user_id
REPL Commands
bash
tables      # List all tables
desc users  # Show table structure
exit        # Quit REPL
🏗️ Architecture
text
Application Layer
├── Web Interface (Flask)
└── REPL Interface

Query Layer
├── Parser (SQL → AST)
└── Executor (AST → Results)

Storage Layer
├── Table Manager
├── Index Manager
└── File Storage
📁 Project Structure
text
db/
├── parser.py      # SQL parser
├── executor.py    # Query executor
├── storage.py     # File storage
├── index.py       # Indexing
└── repl.py        # Interactive shell

web-demo/
├── app.py         # Flask app
└── templates/     # HTML templates

data/              # Database files
tests/             # Test suite
main.py            # Entry point
🌐 Web Demo
Run python3 web-demo/app.py and visit http://localhost:5000 for:

Products CRUD management

Customer records

Orders with JOIN operations

SQL console for direct queries

Real-time statistics dashboard

🔧 Technical Details
Language: Python 3.10+

Storage: JSON + pickle files

Dependencies: Flask, Colorama

Indexing: Simple hash-based indexes

Parsing: Regex-based SQL parser

Web Framework: Flask with Bootstrap

📊 Supported SQL Syntax
sql
-- DDL
CREATE TABLE table_name (col1 TYPE, col2 TYPE PRIMARY KEY)
DROP TABLE table_name

-- DML
INSERT INTO table VALUES (val1, val2)
SELECT col1, col2 FROM table WHERE condition
UPDATE table SET col = value WHERE condition
DELETE FROM table WHERE condition

-- Joins
SELECT * FROM table1 JOIN table2 ON condition
🧪 Testing
bash
# Run tests
python3 -m pytest tests/

# Test specific module
python3 tests/test_parser.py
📝 Notes
Educational implementation focused on clarity over performance

All components built from scratch (no external DB libraries)

Demonstrates RDBMS fundamentals: parsing, execution, storage, indexing

Web app shows practical application with complete CRUD operations

📄 License
MIT License - Free for educational and personal use @[beckynayere](https://github.com/beckynayere/pesapal-junior-dev-rdbms)2026.


