from flask import Flask, render_template, request, jsonify
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from db.parser import Parser
from db.executor import Executor
from db.storage import Storage

app = Flask(__name__)

# Initialize database
storage = Storage()
executor = Executor(storage)
parser = Parser()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/query', methods=['POST'])
def execute_query():
    try:
        query = request.json.get('query', '')
        parsed = parser.parse(query)
        result = executor.execute(parsed)
        return jsonify({'success': True, 'result': result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/tables', methods=['GET'])
def list_tables():
    # Return list of tables
    pass

@app.route('/api/table/<name>', methods=['GET'])
def get_table_data(name):
    # Return table data
    pass

if __name__ == '__main__':
    app.run(debug=True, port=5000)