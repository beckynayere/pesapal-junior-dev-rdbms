import sys
import os
import cmd

# Add parent directory to path to import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.parser import Parser
from db.executor import Executor
from db.storage import Storage

class DatabaseREPL(cmd.Cmd):
    """Interactive REPL for the database"""
    
    intro = """
    ========================================
    Welcome to PesaPal JuniorDB - Simple RDBMS
    Type 'help' for commands, 'exit' to quit
    ========================================
    """
    prompt = "pesapal_db> "
    
    def __init__(self, parser, executor):
        super().__init__()
        self.parser = parser
        self.executor = executor
    
    def default(self, line):
        """Handle SQL queries"""
        try:
            parsed = self.parser.parse(line)
            result = self.executor.execute(parsed)
            
            if isinstance(result, list):
                # Display as table
                if result:
                    headers = list(result[0].keys())
                    print("\t".join(headers))
                    print("-" * 50)
                    for row in result:
                        values = [str(row.get(h, '')) for h in headers]
                        print("\t".join(values))
                    print(f"\n{len(result)} row(s) returned")
                else:
                    print("No rows found")
            else:
                print(result)
                
        except Exception as e:
            print(f"Error: {e}")
    
    def do_tables(self, arg):
        """List all tables"""
        tables = list(self.executor.storage.tables.keys())
        if tables:
            print("Tables:")
            for table in tables:
                print(f"  - {table}")
        else:
            print("No tables exist")
    
    def do_desc(self, arg):
        """Describe table structure: DESC <table_name>"""
        if not arg:
            print("Usage: DESC <table_name>")
            return
        
        table_name = arg.strip()
        table = self.executor.storage.tables.get(table_name)
        
        if not table:
            print(f"Table '{table_name}' not found")
            return
        
        print(f"Table: {table.name}")
        print("Columns:")
        for col in table.columns:
            pk = " (PK)" if col['name'] == table.primary_key else ""
            unique = " (UNIQUE)" if col['name'] in table.unique_keys else ""
            print(f"  {col['name']}: {col['type']}{pk}{unique}")
    
    def do_exit(self, arg):
        """Exit the REPL"""
        print("Goodbye!")
        return True
    
    def do_quit(self, arg):
        """Exit the REPL"""
        return self.do_exit(arg)


def main():
    """Main entry point for REPL"""
    # Initialize database components
    storage = Storage()
    parser = Parser()
    executor = Executor(storage)
    
    # Start REPL
    repl = DatabaseREPL(parser, executor)
    repl.cmdloop()


if __name__ == "__main__":
    main()