from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from flask_socketio import SocketIO, emit
from werkzeug.security import generate_password_hash, check_password_hash
import pymongo
import threading
import csv
import random
import time
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import pandas as pd

app = Flask(__name__)
app.secret_key = 'your_secret_key'
socketio = SocketIO(app)

load_dotenv()
mongo_url = os.getenv("MongoDB_URI")
client = pymongo.MongoClient(mongo_url)
db = client['traffic_logins']
users_collection = db['users']
verification_codes_collection = db['verification_codes']


def generate_hourly_wait_time_csv(filename, num_days=1):
    headers = ['Hour', 'Average Wait Time (minutes)']
    rows = []

    start_time = datetime.now()
    end_time = start_time + timedelta(days=num_days)

    while start_time < end_time:
        for hour in range(1, 25):
            current_time = start_time.replace(hour=hour-1, minute=0, second=0, microsecond=0)
            average_wait_time = round(random.uniform(0.5, 5.0), 2)
            rows.append([str(hour), average_wait_time])

        start_time += timedelta(days=1)

    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(rows)

    print(f'{filename} created with hourly average wait time data for {num_days} day(s).')

def generate_csv_files_continuously(interval=5, num_files=4, num_days=1):
    file_suffixes = ['r1.csv', 'r2.csv', 'r3.csv', 'r4.csv']
    file_index = 0


    script_dir = os.path.dirname(os.path.abspath(__file__))
    static_dir = os.path.join(script_dir, 'static')

    while True:
        filename = os.path.join(static_dir, file_suffixes[file_index % num_files])
        generate_hourly_wait_time_csv(filename, num_days)
        file_index += 1
        time.sleep(interval)

@app.route('/update_csv', methods=['POST'])
def update_csv():
    data = request.get_json()
    updated_csv = data['updatedCSV'].strip()  # Ensure no extra newlines

    with open('static/traffic_data.csv', 'w', newline='') as file:
        file.write(updated_csv)

    return jsonify({"status": "success"})


def record_user_activity(username, action):
    filename = 'user_activity.xlsx'
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data = {
        'Username': [username],
        'Action': [action],
        'Timestamp': [timestamp]
    }
    df = pd.DataFrame(data)
    
    if os.path.exists(filename):
        existing_df = pd.read_excel(filename)
        df = pd.concat([existing_df, df], ignore_index=True)
    
    df.to_excel(filename, index=False)


@app.route('/')
def index():
    return render_template('login.html')

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    verification_code = request.form['verification_code']
    
    code_entry = verification_codes_collection.find_one({'code': verification_code})
    
    if not code_entry:
        return jsonify({"success": False, "message": "Invalid verification code"}), 400
    
    location = code_entry['location']
    hashed_password = generate_password_hash(password)
    
    try:
        users_collection.insert_one({
            'username': username,
            'email': email,
            'password': hashed_password,
            'verification_code': verification_code,
            'location': location
        })
        return jsonify({"success": True}), 200
    except pymongo.errors.DuplicateKeyError:
        return jsonify({"success": False, "message": "Username already exists"}), 400

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    user = users_collection.find_one({'username': username})

    if user and check_password_hash(user['password'], password):
        session['logged_in'] = True
        session['username'] = username
        session['location'] = user.get('location')  # Set location in session
        session.modified = True
        record_user_activity(username, 'login')
        return jsonify({"success": True, "redirect": url_for('loading'), "location": session['location']}), 200
    else:
        return jsonify({"success": False, "message": "Invalid username or password"}), 400


@app.route('/loading')
def loading():
    if not session.get('logged_in'):
        return redirect(url_for('index'))
    return render_template('loading.html')

@app.route('/home')
def home():
    if not session.get('logged_in'):
        return redirect(url_for('index'))
    return render_template('home.html')

@app.route('/graph')
def graph():
    if not session.get('logged_in'):
        return redirect(url_for('index'))
    return render_template('graph.html')

@app.route('/foul')
def foul():
    if not session.get('logged_in'):
        return redirect(url_for('index'))
    return render_template('foul.html')

@app.route('/signout')
def signout():
    username = session.get('username')
    if username:
        record_user_activity(username, 'logout')
    session.clear()
    return redirect(url_for('index'))

@app.route('/forgot_password')
def forgot_password():
    return render_template('forgot_password.html')

@app.route('/verify_code', methods=['POST'])
def verify_code():
    data = request.get_json()
    email = data['email']
    verification_code = data['verification_code']
    
    user = users_collection.find_one({'email': email, 'verification_code': verification_code})
    
    if user:
        return jsonify({'status': 'verified'})
    else:
        return jsonify({'status': 'failed'}), 400

@app.route('/reset_password', methods=['POST'])
def reset_password():
    data = request.get_json()
    email = data['email']
    new_password = data['new_password']
    
    hashed_password = generate_password_hash(new_password)
    users_collection.update_one({'email': email}, {'$set': {'password': hashed_password}})
    
    return jsonify({'success': True, 'redirect': url_for('index')}), 200

@app.route('/detect_ambulance', methods=['POST'])
def detect_ambulance():
    data = request.json
    detected = data.get('detected')
    road = data.get('road')
    
    if detected == 'yes':
        socketio.emit('ambulance_detected', {'road': road, 'status': 'yes'})
    elif detected == 'no':
        socketio.emit('ambulance_detected', {'road': road, 'status': 'no'})
    
    return jsonify({'success': True}), 200

@app.after_request
def after_request(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

if __name__ == '__main__':
    csv_thread = threading.Thread(target=generate_csv_files_continuously, args=(5, 4, 1))
    csv_thread.daemon = True
    csv_thread.start()
    socketio.run(app, debug=True)
