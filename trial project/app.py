from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import json
import requests
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load configuration from JSON file
def load_config():
    with open('config.json') as f:
        return json.load(f)

# Load user credentials from JSON file
def load_users():
    if not os.path.exists('users.json'):
        return {}
    with open('users.json') as f:
        return json.load(f)

# Save user credentials to JSON file
def save_users(users):
    with open('users.json', 'w') as f:
        json.dump(users, f)

# Home route for login
@app.route('/')
def login():
    return render_template('login.html')

# Login route
@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    users = load_users()
    
    if username in users and users[username] == password:
        session['username'] = username
        return redirect(url_for('operator_screen'))
    return "Invalid credentials", 401

# Configuration page
@app.route('/configuration', methods=['GET', 'POST'])
def configuration():
    if request.method == 'POST':
        data = request.form.to_dict()
        with open('config.json', 'w') as f:
            json.dump(data, f)
        return redirect(url_for('configuration'))
    config = load_config()
    return render_template('configuration.html', config=config)

# Operator screen
@app.route('/operator')
def operator_screen():
    config = load_config()
    return render_template('operator.html', config=config)

# Process control check
@app.route('/process_control', methods=['POST'])
def process_control():
    wip_id = request.json.get('wip_id')
    response = requests.get(f'http://localhost:8765/v2/process_control?serial={wip_id}&serial_type=wip_id')
    return jsonify(response.json())

# Data upload
@app.route('/data_upload', methods=['POST'])
def data_upload():
    data = request.json
    response = requests.post('http://localhost:8765/v2/logs', json=data)
    return jsonify(response.json()), response.status_code

if __name__ == '__main__':
    app.run(debug=True)