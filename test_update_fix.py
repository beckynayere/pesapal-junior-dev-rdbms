import sys
sys.path.append('.')
from db.parser import Parser

parser = Parser()

test_queries = [
    "UPDATE users SET name = 'Jane Doe' WHERE email = 'john@example.com'",
    "UPDATE users SET name = 'John', age = 30 WHERE id = 1",
    "UPDATE products SET price = 99.99 WHERE category = 'electronics'",
]

for query in test_queries:
    try:
        parsed = parser.parse(query)
        print(f"✅ Query: {query}")
        print(f"   Parsed: {parsed}")
    except Exception as e:
        print(f"❌ Query: {query}")
        print(f"   Error: {e}")
