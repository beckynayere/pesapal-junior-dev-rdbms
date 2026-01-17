# db/storage.py

class Database:
    def __init__(self):
        self.tables = {}

    def create_table(self, name, columns, primary_key=None, unique_keys=None):
        self.tables[name] = {
            "columns": columns,
            "rows": [],
            "pk": primary_key,
            "unique": unique_keys or [],
            "indexes": {}
        }
