#!/usr/bin/env python3
"""
Quick server for PesaPal JuniorDB demo
"""

import http.server
import socketserver
import os
import json

PORT = 8000

class DemoHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            html = '''
            <!DOCTYPE html>
            <html>
            <head>
                <title>PesaPal JuniorDB Demo</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 40px; }
                    .demo { background: #f0f0f0; padding: 20px; border-radius: 10px; }
                    pre { background: #333; color: #fff; padding: 15px; border-radius: 5px; }
                </style>
            </head>
            <body>
                <h1>PesaPal JuniorDB - RDBMS Demo</h1>
                
                <div class="demo">
                    <h2>🎉 Project Successfully Built!</h2>
                    <p>You have successfully created a simple relational database management system with:</p>
                    <ul>
                        <li>SQL-like query language</li>
                        <li>CRUD operations (Create, Read, Update, Delete)</li>
                        <li>Table schemas with data types</li>
                        <li>Primary and Unique keys</li>
                        <li>Basic indexing</li>
                        <li>JOIN operations</li>
                        <li>Interactive REPL</li>
                        <li>Web interface</li>
                    </ul>
                    
                    <h3>Project Structure:</h3>
                    <pre>
pesapal-junior-dev-rdbms/
├── db/
│   ├── parser.py      # SQL parser
│   ├── executor.py    # Query executor
│   ├── storage.py     # File-based storage
│   ├── index.py       # Indexing system
│   └── repl.py        # Interactive shell
├── web-demo/
│   └── app.py         # Flask web interface
├── tests/             # Test suite
└── requirements.txt   # Dependencies
                    </pre>
                    
                    <h3>To Run:</h3>
                    <pre>
# Terminal 1: Run the REPL
python3 main.py

# Terminal 2: Run the web demo
cd web-demo
python3 app.py
                    </pre>
                </div>
            </body>
            </html>
            '''
            self.wfile.write(html.encode())
        else:
            super().do_GET()

print(f"Serving PesaPal JuniorDB demo at http://localhost:{PORT}")
os.chdir('.')
with socketserver.TCPServer(("", PORT), DemoHandler) as httpd:
    httpd.serve_forever()
