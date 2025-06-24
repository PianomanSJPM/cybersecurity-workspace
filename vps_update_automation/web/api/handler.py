#!/usr/bin/env python3
import json
import os
import psutil
import time
from datetime import datetime, timedelta
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configuration
CONFIG_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'config', 'config.json')
LOG_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'logs', 'vps_update.log')

def load_config():
    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def get_system_metrics():
    return {
        'cpu': {
            'usage': psutil.cpu_percent(interval=1),
            'cores': psutil.cpu_count(),
            'frequency': psutil.cpu_freq().current if psutil.cpu_freq() else None
        },
        'memory': {
            'total': psutil.virtual_memory().total,
            'used': psutil.virtual_memory().used,
            'percent': psutil.virtual_memory().percent
        },
        'disk': {
            'total': psutil.disk_usage('/').total,
            'used': psutil.disk_usage('/').used,
            'percent': psutil.disk_usage('/').percent
        },
        'network': {
            'bytes_sent': psutil.net_io_counters().bytes_sent,
            'bytes_recv': psutil.net_io_counters().bytes_recv,
            'packets_sent': psutil.net_io_counters().packets_sent,
            'packets_recv': psutil.net_io_counters().packets_recv
        }
    }

def get_security_status():
    # Implement security checks here
    return {
        'status': 'healthy',
        'issues': [],
        'last_scan': datetime.now().isoformat(),
        'open_ports': [],
        'failed_logins': 0
    }

def get_update_status():
    config = load_config()
    return {
        'last_update': config.get('last_update', 'Never'),
        'next_update': config.get('next_update', 'Not scheduled'),
        'pending_updates': [],
        'update_history': []
    }

def get_backup_status():
    config = load_config()
    return {
        'last_backup': config.get('last_backup', 'Never'),
        'next_backup': config.get('next_backup', 'Not scheduled'),
        'backup_size': 0,
        'backup_location': config.get('backup_location', 'Not configured')
    }

def get_recent_activity():
    activities = []
    try:
        with open(LOG_FILE, 'r') as f:
            for line in f.readlines()[-10:]:  # Get last 10 lines
                if line.strip():
                    activities.append({
                        'timestamp': datetime.now().isoformat(),
                        'message': line.strip(),
                        'type': 'info'
                    })
    except FileNotFoundError:
        pass
    return activities

@app.route('/api/metrics', methods=['GET'])
def metrics():
    return jsonify(get_system_metrics())

@app.route('/api/security', methods=['GET'])
def security():
    return jsonify(get_security_status())

@app.route('/api/updates', methods=['GET'])
def updates():
    return jsonify(get_update_status())

@app.route('/api/backups', methods=['GET'])
def backups():
    return jsonify(get_backup_status())

@app.route('/api/activity', methods=['GET'])
def activity():
    return jsonify(get_recent_activity())

@app.route('/api/config', methods=['GET', 'POST'])
def config():
    if request.method == 'POST':
        try:
            new_config = request.json
            with open(CONFIG_FILE, 'w') as f:
                json.dump(new_config, f, indent=4)
            return jsonify({'status': 'success'})
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500
    return jsonify(load_config())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 