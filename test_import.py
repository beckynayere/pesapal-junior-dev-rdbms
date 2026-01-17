import sys
print("Python path:", sys.path)

try:
    from db.parser import Parser
    print("Parser imported successfully!")
except ImportError as e:
    print(f"Parser import error: {e}")

try:
    from db.storage import Storage
    print("Storage imported successfully!")
except ImportError as e:
    print(f"Storage import error: {e}")

try:
    from db.executor import Executor
    print("Executor imported successfully!")
except ImportError as e:
    print(f"Executor import error: {e}")

try:
    from db.repl import DatabaseREPL
    print("REPL imported successfully!")
except ImportError as e:
    print(f"REPL import error: {e}")
