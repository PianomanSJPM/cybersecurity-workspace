from flask import Flask, send_from_directory, jsonify
import os
import socket
from contextlib import closing

app = Flask(__name__, static_folder='web')

# Serve the main dashboard
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

# Serve static files (CSS, JS, images)
@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory(app.static_folder, filename)

# Health check API
@app.route('/api/health')
def health():
    return jsonify({
        'status': 'ok',
        'message': 'VPS Update Automation Web Server is running.'
    })

@app.route('/test')
def test():
    return "Flask is serving routes correctly!"

@app.route('/backups')
def backups():
    return send_from_directory(app.static_folder, 'backups.html')

@app.route('/security')
def security():
    return send_from_directory(app.static_folder, 'security.html')

@app.route('/updates')
def updates():
    return send_from_directory(app.static_folder, 'updates.html')

def find_free_port(start_port=5000, max_port=5010):
    for port in range(start_port, max_port):
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
            try:
                sock.bind(('', port))
                return port
            except OSError:
                continue
    raise RuntimeError("No free ports found in range.")

if __name__ == '__main__':
    port = find_free_port()
    print(f"Starting server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=True) 