import json
import os
import pickle
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
import csv

class Storage:
    """Simple file-based storage engine"""
    
    def __init__(self, data_dir: str = 'data'):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
        self.metadata_file = os.path.join(data_dir, 'metadata.json')
        self.tables: Dict[str, Table] = {}
        self.load_metadata()
    
    def load_metadata(self):
        """Load database metadata from disk"""
        if os.path.exists(self.metadata_file):
            with open(self.metadata_file, 'r') as f:
                metadata = json.load(f)
                for table_name, table_info in metadata.items():
                    self.tables[table_name] = Table(
                        name=table_name,
                        columns=table_info['columns'],
                        primary_key=table_info.get('primary_key'),
                        unique_keys=table_info.get('unique_keys', [])
                    )
    
    def save_metadata(self):
        """Save database metadata to disk"""
        metadata = {}
        for table_name, table in self.tables.items():
            metadata[table_name] = {
                'columns': table.columns,
                'primary_key': table.primary_key,
                'unique_keys': table.unique_keys,
                'row_count': len(table.rows)
            }
        
        with open(self.metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
    
    def create_table(self, name: str, columns: List[Dict], 
                     primary_key: Optional[str] = None,
                     unique_keys: List[str] = None):
        """Create a new table"""
        if name in self.tables:
            raise ValueError(f"Table '{name}' already exists")
        
        table = Table(name, columns, primary_key, unique_keys or [])
        self.tables[name] = table
        self.save_metadata()
        self.save_table(name)
        return True
    
    def insert(self, table_name: str, data: Dict) -> int:
        """Insert a row into table"""
        table = self.tables.get(table_name)
        if not table:
            raise ValueError(f"Table '{table_name}' not found")
        
        # Validate unique constraints
        for col in table.unique_keys:
            if col in data:
                for row in table.rows:
                    if row.get(col) == data[col]:
                        raise ValueError(f"Duplicate value for unique column '{col}'")
        
        row_id = table.insert(data)
        self.save_table(table_name)
        self.save_metadata()
        return row_id
    
    def select(self, table_name: str, 
               columns: Optional[List[str]] = None,
               conditions: Optional[Dict] = None,
               order_by: Optional[Tuple[str, str]] = None,
               limit: Optional[int] = None) -> List[Dict]:
        """Select rows from table"""
        table = self.tables.get(table_name)
        if not table:
            raise ValueError(f"Table '{table_name}' not found")
        
        return table.select(columns, conditions, order_by, limit)
    
    def update(self, table_name: str, updates: Dict, 
               conditions: Optional[Dict] = None) -> int:
        """Update rows matching conditions"""
        table = self.tables.get(table_name)
        if not table:
            raise ValueError(f"Table '{table_name}' not found")
        
        affected = table.update(updates, conditions)
        if affected > 0:
            self.save_table(table_name)
        return affected
    
    def delete(self, table_name: str, conditions: Optional[Dict] = None) -> int:
        """Delete rows matching conditions"""
        table = self.tables.get(table_name)
        if not table:
            raise ValueError(f"Table '{table_name}' not found")
        
        affected = table.delete(conditions)
        if affected > 0:
            self.save_table(table_name)
        return affected
    
    def drop_table(self, table_name: str) -> bool:
        """Drop a table"""
        if table_name not in self.tables:
            return False
        
        del self.tables[table_name]
        # Remove table file
        table_file = os.path.join(self.data_dir, f"{table_name}.pkl")
        if os.path.exists(table_file):
            os.remove(table_file)
        
        self.save_metadata()
        return True
    
    def save_table(self, table_name: str):
        """Save table data to disk"""
        table = self.tables.get(table_name)
        if table:
            table_file = os.path.join(self.data_dir, f"{table_name}.pkl")
            with open(table_file, 'wb') as f:
                pickle.dump({
                    'rows': table.rows,
                    'next_id': table.next_id
                }, f)
    
    def load_table(self, table_name: str):
        """Load table data from disk"""
        table_file = os.path.join(self.data_dir, f"{table_name}.pkl")
        if os.path.exists(table_file):
            with open(table_file, 'rb') as f:
                data = pickle.load(f)
                table = self.tables[table_name]
                table.rows = data['rows']
                table.next_id = data.get('next_id', len(data['rows']) + 1)

class Table:
    """Table representation with rows and schema"""
    
    def __init__(self, name: str, columns: List[Dict], 
                 primary_key: Optional[str] = None,
                 unique_keys: List[str] = None):
        self.name = name
        self.columns = columns
        self.primary_key = primary_key
        self.unique_keys = unique_keys or []
        self.rows: List[Dict] = []
        self.next_id = 1
    
    def insert(self, data: Dict) -> int:
        """Insert a row and return its ID"""
        # Generate ID if not provided
        if self.primary_key and self.primary_key not in data:
            data[self.primary_key] = self.next_id
            self.next_id += 1
        
        # Validate data types
        self._validate_row(data)
        
        self.rows.append(data.copy())
        return data.get(self.primary_key, len(self.rows))
    
    def _validate_row(self, data: Dict):
        """Validate row data against column definitions"""
        for col_def in self.columns:
            col_name = col_def['name']
            col_type = col_def['type']
            
            if col_name in data:
                value = data[col_name]
                try:
                    if col_type == 'int':
                        data[col_name] = int(value)
                    elif col_type == 'float':
                        data[col_name] = float(value)
                    elif col_type == 'varchar':
                        data[col_name] = str(value)
                    elif col_type == 'boolean':
                        data[col_name] = bool(value)
                    elif col_type == 'timestamp':
                        if isinstance(value, str):
                            # Parse timestamp string
                            pass
                except (ValueError, TypeError):
                    raise ValueError(f"Invalid type for column '{col_name}'. Expected {col_type}")
    
    def select(self, columns: Optional[List[str]] = None,
               conditions: Optional[Dict] = None,
               order_by: Optional[Tuple[str, str]] = None,
               limit: Optional[int] = None) -> List[Dict]:
        """Select rows with filtering and ordering"""
        results = []
        
        for row in self.rows:
            # Apply conditions
            if conditions and not self._row_matches(row, conditions):
                continue
            
            # Select specific columns
            if columns:
                selected_row = {}
                for col in columns:
                    if col in row:
                        selected_row[col] = row[col]
                    elif col == '*':
                        selected_row = row.copy()
                        break
                results.append(selected_row)
            else:
                results.append(row.copy())
        
        # Apply ordering
        if order_by:
            column, direction = order_by
            reverse = (direction.upper() == 'DESC')
            results.sort(key=lambda x: x.get(column, 0), reverse=reverse)
        
        # Apply limit
        if limit is not None:
            results = results[:limit]
        
        return results
    
    def _row_matches(self, row: Dict, conditions: Dict) -> bool:
        """Check if row matches all conditions"""
        for key, value in conditions.items():
            if key not in row or row[key] != value:
                return False
        return True
    
    def update(self, updates: Dict, conditions: Optional[Dict] = None) -> int:
        """Update rows matching conditions"""
        affected = 0
        
        for row in self.rows:
            if not conditions or self._row_matches(row, conditions):
                for key, value in updates.items():
                    row[key] = value
                affected += 1
        
        return affected
    
    def delete(self, conditions: Optional[Dict] = None) -> int:
        """Delete rows matching conditions"""
        if not conditions:
            count = len(self.rows)
            self.rows.clear()
            return count
        
        # Filter rows to keep
        rows_to_keep = []
        deleted = 0
        
        for row in self.rows:
            if self._row_matches(row, conditions):
                deleted += 1
            else:
                rows_to_keep.append(row)
        
        self.rows = rows_to_keep
        return deleted
    
    def join(self, other_table: 'Table', 
             join_type: str, 
             on_condition: Tuple[str, str]) -> List[Dict]:
        """Perform join with another table"""
        result = []
        left_col, right_col = on_condition
        
        if join_type.upper() == 'INNER':
            for left_row in self.rows:
                for right_row in other_table.rows:
                    if left_row.get(left_col) == right_row.get(right_col):
                        merged = {**left_row, **right_row}
                        result.append(merged)
        
        elif join_type.upper() == 'LEFT':
            for left_row in self.rows:
                matched = False
                for right_row in other_table.rows:
                    if left_row.get(left_col) == right_row.get(right_col):
                        merged = {**left_row, **right_row}
                        result.append(merged)
                        matched = True
                
                if not matched:
                    result.append(left_row.copy())
        
        return result