# Simple test script
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    print("Testing database imports...")
    from db.storage import Storage
    from db.parser import Parser
    from db.executor import Executor
    
    print("✓ All imports successful!")
    
    # Initialize components
    storage = Storage()
    parser = Parser()
    executor = Executor(storage)
    
    print("✓ Components initialized!")
    
    # Test a simple query
    test_query = "CREATE TABLE test_users (id INT PRIMARY KEY, name VARCHAR(50))"
    print(f"\nTesting query: {test_query}")
    
    parsed = parser.parse(test_query)
    result = executor.execute(parsed)
    print(f"Result: {result}")
    
    # List tables
    print(f"\nTables in database: {list(storage.tables.keys())}")
    
    print("\n✅ Database is working correctly!")
    
except ImportError as e:
    print(f"✗ Import error: {e}")
    print("Current directory:", os.getcwd())
    print("Python path:", sys.path)
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
