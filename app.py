from flask import Flask, render_template, request, redirect, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import json
import os
import time

app = Flask(__name__)
app.secret_key = 'supersecretkey'

USERS_FILE = 'users.json'
CANVAS_FILE = 'canvas.json'
COOLDOWNS_FILE = 'cooldowns.json'
CANVAS_SIZE = 500

def load_data(file, default):
    if not os.path.exists(file):
        return default
    with open(file, 'r') as f:
        return json.load(f)

def save_data(file, data):
    with open(file, 'w') as f:
        json.dump(data, f)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/canvas')
def index():
    if 'username' not in session:
        return redirect('/login')
    return render_template('index.html', canvas_size=CANVAS_SIZE)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_data(USERS_FILE, {})
        if username in users:
            return 'User already exists!'
        users[username] = generate_password_hash(password)
        save_data(USERS_FILE, users)
        return redirect('/login')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_data(USERS_FILE, {})
        if username in users and check_password_hash(users[username], password):
            session['username'] = username
            return redirect('/canvas')
        return 'Invalid credentials'
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

@app.route('/update_pixel', methods=['POST'])
def update_pixel():
    if 'username' not in session:
        return 'Not logged in', 403

    data = request.get_json()
    x = int(data.get('x', -1))
    y = int(data.get('y', -1))
    color = int(data.get('color', 0))

    if not (0 <= x < CANVAS_SIZE and 0 <= y < CANVAS_SIZE):
        return 'Invalid coordinates', 400

    cooldowns = load_data(COOLDOWNS_FILE, {})
    now = time.time()
    user = session['username']
    if user in cooldowns and now - cooldowns[user] < 30:
        return 'Cooldown active', 429

    canvas = load_data(CANVAS_FILE, [[0]*CANVAS_SIZE for _ in range(CANVAS_SIZE)])
    canvas[y][x] = color
    save_data(CANVAS_FILE, canvas)

    cooldowns[user] = now
    save_data(COOLDOWNS_FILE, cooldowns)

    return 'OK'

@app.route('/get_canvas')
def get_canvas():
    return jsonify(load_data(CANVAS_FILE, [[0]*CANVAS_SIZE for _ in range(CANVAS_SIZE)]))

if __name__ == '__main__':
    app.run(debug=True)
