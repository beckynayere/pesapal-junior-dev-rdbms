import re
from typing import Dict, List, Any

class Parser:
    """Simple SQL parser for educational purposes"""
    
    def parse(self, query: str) -> Dict[str, Any]:
        """Parse SQL query into structured format"""
        query = query.strip()
        
        # Skip empty queries
        if not query:
            raise ValueError("Empty query")
        
        # Remove multiple spaces and newlines
        query = re.sub(r'\s+', ' ', query)
        
        # Check for comments and skip
        if query.startswith('--'):
            raise ValueError("Comments not supported")
        
        if query.lower().startswith('create table'):
            return self._parse_create_table(query)
        elif query.lower().startswith('insert into'):
            return self._parse_insert(query)
        elif query.lower().startswith('select'):
            return self._parse_select(query)
        elif query.lower().startswith('update'):
            return self._parse_update(query)
        elif query.lower().startswith('delete from'):
            return self._parse_delete(query)
        elif query.lower().startswith('drop table'):
            return self._parse_drop_table(query)
        else:
            # Check for REPL commands
            query_lower = query.lower()
            if query_lower == 'tables':
                return {'type': 'repl_tables'}
            elif query_lower.startswith('desc '):
                table_name = query[5:].strip()
                return {'type': 'repl_desc', 'table_name': table_name}
            elif query_lower in ['exit', 'quit']:
                return {'type': 'repl_exit'}
            else:
                raise ValueError(f"Unsupported query: {query}")
    
    def _parse_create_table(self, query: str) -> Dict:
        """Parse CREATE TABLE statement"""
        pattern = r'create table (\w+)\s*\((.*)\)'
        match = re.match(pattern, query, re.IGNORECASE | re.DOTALL)
        
        if not match:
            raise ValueError("Invalid CREATE TABLE syntax")
        
        table_name = match.group(1)
        columns_str = match.group(2).strip()
        
        # Parse columns
        columns = []
        primary_key = None
        unique_keys = []
        
        # Split by comma, handling parentheses
        column_defs = self._split_sql_list(columns_str)
        
        for col_def in column_defs:
            col_def = col_def.strip()
            if col_def.upper().startswith('PRIMARY KEY'):
                # Extract primary key
                pk_match = re.search(r'primary key\s*\((\w+)\)', col_def, re.IGNORECASE)
                if pk_match:
                    primary_key = pk_match.group(1)
            elif col_def.upper().startswith('UNIQUE'):
                # Extract unique constraint
                unique_match = re.search(r'unique\s*\((\w+)\)', col_def, re.IGNORECASE)
                if unique_match:
                    unique_keys.append(unique_match.group(1))
            else:
                # Regular column definition
                col_parts = col_def.split()
                if len(col_parts) >= 2:
                    col_name = col_parts[0]
                    col_type = col_parts[1].upper()
                    
                    # Map to internal types
                    type_map = {
                        'INT': 'int',
                        'INTEGER': 'int',
                        'VARCHAR': 'varchar',
                        'TEXT': 'varchar',
                        'FLOAT': 'float',
                        'BOOLEAN': 'boolean',
                        'TIMESTAMP': 'timestamp'
                    }
                    
                    internal_type = type_map.get(col_type, 'varchar')
                    columns.append({
                        'name': col_name,
                        'type': internal_type
                    })
        
        return {
            'type': 'create_table',
            'table_name': table_name,
            'columns': columns,
            'primary_key': primary_key,
            'unique_keys': unique_keys
        }
    
    def _parse_insert(self, query: str) -> Dict:
        """Parse INSERT INTO statement"""
        pattern = r'insert into (\w+)\s*(?:\(([^)]+)\))?\s*values\s*\(([^)]+)\)'
        match = re.match(pattern, query, re.IGNORECASE)
        
        if not match:
            raise ValueError("Invalid INSERT syntax")
        
        table_name = match.group(1)
        columns_str = match.group(2)
        values_str = match.group(3)
        
        # Parse columns
        columns = []
        if columns_str:
            columns = [col.strip() for col in columns_str.split(',')]
        
        # Parse values
        values = self._parse_values(values_str)
        
        # Create data dictionary
        data = {}
        if columns:
            for i, col in enumerate(columns):
                if i < len(values):
                    data[col] = values[i]
        else:
            # If no columns specified, use positional values
            for i, value in enumerate(values):
                data[f'col_{i}'] = value
        
        return {
            'type': 'insert',
            'table_name': table_name,
            'data': data
        }
    
    def _parse_select(self, query: str) -> Dict:
        """Parse SELECT statement"""
        # Simplified SELECT parser
        pattern = r'select (.+?) from (\w+)(?: where (.+))?'
        match = re.match(pattern, query, re.IGNORECASE)
        
        if not match:
            raise ValueError("Invalid SELECT syntax")
        
        columns_str = match.group(1).strip()
        table_name = match.group(2).strip()
        where_clause = match.group(3) if match.group(3) else None
        
        # Parse columns
        columns = []
        if columns_str == '*':
            columns = None
        else:
            columns = [col.strip() for col in columns_str.split(',')]
        
        # Parse WHERE conditions
        conditions = {}
        if where_clause:
            # Simple equality conditions
            conditions_pattern = r'(\w+)\s*=\s*(?:(\w+)|"([^"]+)"|\'([^\']+)\')'
            conditions_matches = re.findall(conditions_pattern, where_clause)
            
            for match in conditions_matches:
                col_name = match[0]
                # Get value from any of the capturing groups
                value = next((v for v in match[1:] if v), None)
                if value:
                    # Try to convert to number if possible
                    try:
                        if '.' in value:
                            value = float(value)
                        else:
                            value = int(value)
                    except ValueError:
                        # Remove quotes if present
                        value = value.strip("'\"")
                    conditions[col_name] = value
        
        return {
            'type': 'select',
            'table_name': table_name,
            'columns': columns,
            'conditions': conditions if conditions else None
        }
    
    def _parse_update(self, query: str) -> Dict:
        """Parse UPDATE statement - FIXED VERSION"""
        pattern = r'update (\w+) set (.+?)(?: where (.+))?$'
        match = re.match(pattern, query, re.IGNORECASE)
        
        if not match:
            raise ValueError("Invalid UPDATE syntax")
        
        table_name = match.group(1)
        set_clause = match.group(2)
        where_clause = match.group(3) if match.group(3) else None
        
        # Parse SET clause
        updates = {}
        set_items = [item.strip() for item in set_clause.split(',')]
        for item in set_items:
            if '=' in item:
                col, value = item.split('=', 1)
                col = col.strip()
                value = value.strip()
                
                # Remove quotes if present
                if (value.startswith("'") and value.endswith("'")) or \
                   (value.startswith('"') and value.endswith('"')):
                    value = value[1:-1]
                
                # Try to convert to number
                try:
                    if '.' in value:
                        value = float(value)
                    else:
                        value = int(value)
                except ValueError:
                    pass
                
                updates[col] = value
        
        # Parse WHERE conditions
        conditions = {}
        if where_clause:
            # Simple equality condition
            where_match = re.search(r'(\w+)\s*=\s*(.+)$', where_clause.strip())
            if where_match:
                col_name = where_match.group(1).strip()
                value = where_match.group(2).strip()
                
                # Remove quotes if present
                if (value.startswith("'") and value.endswith("'")) or \
                   (value.startswith('"') and value.endswith('"')):
                    value = value[1:-1]
                
                # Try to convert to number
                try:
                    if '.' in value:
                        value = float(value)
                    else:
                        value = int(value)
                except ValueError:
                    pass
                
                conditions[col_name] = value
        
        return {
            'type': 'update',
            'table_name': table_name,
            'updates': updates,
            'conditions': conditions if conditions else None
        }
    
    def _parse_delete(self, query: str) -> Dict:
        """Parse DELETE statement"""
        pattern = r'delete from (\w+)(?: where (.+))?'
        match = re.match(pattern, query, re.IGNORECASE)
        
        if not match:
            raise ValueError("Invalid DELETE syntax")
        
        table_name = match.group(1)
        where_clause = match.group(2) if match.group(2) else None
        
        conditions = {}
        if where_clause:
            # Simple equality condition
            where_match = re.search(r'(\w+)\s*=\s*(.+)$', where_clause.strip())
            if where_match:
                col_name = where_match.group(1).strip()
                value = where_match.group(2).strip()
                
                # Remove quotes if present
                if (value.startswith("'") and value.endswith("'")) or \
                   (value.startswith('"') and value.endswith('"')):
                    value = value[1:-1]
                
                # Try to convert to number
                try:
                    if '.' in value:
                        value = float(value)
                    else:
                        value = int(value)
                except ValueError:
                    pass
                
                conditions[col_name] = value
        
        return {
            'type': 'delete',
            'table_name': table_name,
            'conditions': conditions if conditions else None
        }
    
    def _parse_drop_table(self, query: str) -> Dict:
        """Parse DROP TABLE statement"""
        pattern = r'drop table (\w+)'
        match = re.match(pattern, query, re.IGNORECASE)
        
        if not match:
            raise ValueError("Invalid DROP TABLE syntax")
        
        return {
            'type': 'drop_table',
            'table_name': match.group(1)
        }
    
    def _parse_values(self, values_str: str) -> List[Any]:
        """Parse VALUES clause into list of values"""
        values = []
        current = ''
        in_quotes = False
        quote_char = None
        
        for char in values_str:
            if char in ("'", '"') and not in_quotes:
                in_quotes = True
                quote_char = char
                current += char
            elif char == quote_char and in_quotes:
                in_quotes = False
                current += char
            elif char == ',' and not in_quotes:
                values.append(self._parse_value(current.strip()))
                current = ''
            else:
                current += char
        
        if current:
            values.append(self._parse_value(current.strip()))
        
        return values
    
    def _parse_value(self, value_str: str) -> Any:
        """Parse a single SQL value"""
        if value_str.startswith("'") and value_str.endswith("'"):
            return value_str[1:-1]
        elif value_str.startswith('"') and value_str.endswith('"'):
            return value_str[1:-1]
        elif value_str.lower() == 'null':
            return None
        elif value_str.lower() == 'true':
            return True
        elif value_str.lower() == 'false':
            return False
        else:
            # Try to parse as number
            try:
                if '.' in value_str:
                    return float(value_str)
                else:
                    return int(value_str)
            except ValueError:
                return value_str
    
    def _split_sql_list(self, text: str) -> List[str]:
        """Split SQL list by comma, handling nested parentheses and quotes"""
        result = []
        current = ''
        depth = 0
        in_quotes = False
        quote_char = None
        
        for char in text:
            if char in ("'", '"') and not in_quotes:
                in_quotes = True
                quote_char = char
                current += char
            elif char == quote_char and in_quotes:
                in_quotes = False
                current += char
            elif char == '(' and not in_quotes:
                depth += 1
                current += char
            elif char == ')' and not in_quotes:
                depth -= 1
                current += char
            elif char == ',' and not in_quotes and depth == 0:
                result.append(current.strip())
                current = ''
            else:
                current += char
        
        if current:
            result.append(current.strip())
        
        return result
