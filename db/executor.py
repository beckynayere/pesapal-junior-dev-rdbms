
from typing import Dict, List, Any
from .storage import Storage

class Executor:
    """Execute parsed SQL queries"""
    
    def __init__(self, storage: Storage):
        self.storage = storage
    
    def execute(self, parsed_query: Dict) -> Any:
        """Execute a parsed query"""
        query_type = parsed_query['type']
        
        if query_type == 'create_table':
            return self._execute_create_table(parsed_query)
        elif query_type == 'insert':
            return self._execute_insert(parsed_query)
        elif query_type == 'select':
            return self._execute_select(parsed_query)
        elif query_type == 'update':
            return self._execute_update(parsed_query)
        elif query_type == 'delete':
            return self._execute_delete(parsed_query)
        elif query_type == 'drop_table':
            return self._execute_drop_table(parsed_query)
        else:
            raise ValueError(f"Unknown query type: {query_type}")
    
    def _execute_create_table(self, query: Dict) -> str:
        """Execute CREATE TABLE"""
        self.storage.create_table(
            name=query['table_name'],
            columns=query['columns'],
            primary_key=query.get('primary_key'),
            unique_keys=query.get('unique_keys', [])
        )
        return f"Table '{query['table_name']}' created successfully"
    
    def _execute_insert(self, query: Dict) -> str:
        """Execute INSERT"""
        row_id = self.storage.insert(
            table_name=query['table_name'],
            data=query['data']
        )
        return f"Row inserted with ID: {row_id}"
    
    def _execute_select(self, query: Dict) -> List[Dict]:
        """Execute SELECT"""
        return self.storage.select(
            table_name=query['table_name'],
            columns=query.get('columns'),
            conditions=query.get('conditions')
        )
    
    def _execute_update(self, query: Dict) -> str:
        """Execute UPDATE"""
        affected = self.storage.update(
            table_name=query['table_name'],
            updates=query['updates'],
            conditions=query.get('conditions')
        )
        return f"{affected} row(s) updated"
    
    def _execute_delete(self, query: Dict) -> str:
        """Execute DELETE"""
        affected = self.storage.delete(
            table_name=query['table_name'],
            conditions=query.get('conditions')
        )
        return f"{affected} row(s) deleted"
    
    def _execute_drop_table(self, query: Dict) -> str:
        """Execute DROP TABLE"""
        if self.storage.drop_table(query['table_name']):
            return f"Table '{query['table_name']}' dropped"
        else:
            return f"Table '{query['table_name']}' not found"