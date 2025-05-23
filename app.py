from flask import Flask, render_template, request, redirect, session, jsonify
import json
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'

USERS_FILE = 'users.json'
CANVAS_FILE = 'canvas.json'

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, 'r') as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f)

def load_canvas():
    if not os.path.exists(CANVAS_FILE):
        return [[0 for _ in range(128)] for _ in range(128)]
    with open(CANVAS_FILE, 'r') as f:
        return json.load(f)

def save_canvas(canvas):
    with open(CANVAS_FILE, 'w') as f:
        json.dump(canvas, f)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/canvas')
def index():
    if 'username' not in session:
        return redirect('/login')
    canvas = load_canvas()
    return render_template('index.html', canvas=canvas)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        if username in users:
            return 'User already exists!'
        users[username] = password
        save_users(users)
        return redirect('/login')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        if users.get(username) == password:
            session['username'] = username
            return redirect('/canvas')
        return 'Invalid credentials'
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')

@app.route('/update_pixel', methods=['POST'])
def update_pixel():
    if 'username' not in session:
        return 'Not logged in', 403
    x = int(request.json['x'])
    y = int(request.json['y'])
    color = int(request.json['color'])
    canvas = load_canvas()
    canvas[y][x] = color
    save_canvas(canvas)
    return 'OK'

@app.route('/get_canvas')
def get_canvas():
    return jsonify(load_canvas())

if __name__ == '__main__':
    app.run(debug=True)