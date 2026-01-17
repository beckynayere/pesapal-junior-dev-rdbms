import sys
import os

print("Current directory:", os.getcwd())
print("Python path:", sys.path)

# Add current directory
sys.path.insert(0, os.getcwd())

try:
    print("\nTrying to import from db.repl...")
    from db.repl import main
    print("Import successful!")
    
    print("\nStarting main()...")
    main()
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
