from typing import Dict, List, Any, Set

class Index:
    def __init__(self, column_name: str):
        self.column_name = column_name
        self.index: Dict[Any, Set[int]] = {}
    
    def add(self, value: Any, row_id: int):
        if value not in self.index:
            self.index[value] = set()
        self.index[value].add(row_id)
    
    def remove(self, value: Any, row_id: int):
        if value in self.index:
            self.index[value].discard(row_id)
            if not self.index[value]:
                del self.index[value]
    
    def find(self, value: Any) -> Set[int]:
        return self.index.get(value, set())

class IndexManager:
    def __init__(self):
        self.indexes: Dict[str, Dict[str, Index]] = {}
    
    def create_index(self, table_name: str, column_name: str):
        if table_name not in self.indexes:
            self.indexes[table_name] = {}
        self.indexes[table_name][column_name] = Index(column_name)
    
    def add_to_index(self, table_name: str, column_name: str, value: Any, row_id: int):
        if table_name in self.indexes and column_name in self.indexes[table_name]:
            self.indexes[table_name][column_name].add(value, row_id)