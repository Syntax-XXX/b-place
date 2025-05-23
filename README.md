# 🎨 B-Place — A Collaborative Pixel Canvas

**B-Place** is a simple clone of Reddit's [r/place](https://www.reddit.com/r/place/) — a 128×128 collaborative canvas where users can place colored pixels in real-time with a cooldown period. This project uses Python and Flask, with all data stored in local `.json` files. No database needed!

---

## ✨ Features

- 👤 Register and Login system (stored in `users.json`)
- 🎨 128x128 pixel canvas with 5 static colors
  - White
  - Black
  - Red
  - Green
  - Blue
- ⏳ 30-second cooldown between pixel placements per user
- 🖌️ Real-time canvas updates (on refresh)
- 💾 All user and canvas data stored locally in JSON
- 🧼 Clean and minimal CSS interface

---

## 🚀 Getting Started

### Prerequisites

- Python 3.x
- `pip` (Python package manager)

### Installation

1. **Clone or download the repo**
    ```bash
    unzip b-place.zip
    cd b-place
    ```

2. **Install dependencies**
    ```bash
    pip install flask
    ```

3. **Run the app**
    ```bash
    python app.py
    ```

4. **Open in browser**
    ```
    http://127.0.0.1:5000/
    ```

---

## 📁 Project Structure

b-place/
│
├── app.py # Main Flask app
├── users.json # Auto-created for storing user accounts
├── canvas.json # Auto-created to store canvas pixel data
│
├── templates/ # HTML templates
│ ├── home.html
│ ├── login.html
│ ├── register.html
│ └── index.html
│
├── static/
│ ├── css/style.css # Styles
│ └── js/app.js # Canvas logic + cooldown
└──────────────────────────────────────── more comming soon

---

## 📦 Future Ideas

- Real-time WebSocket updates (e.g. using Flask-SocketIO)
- Admin panel or moderation tools
- Color palette expansion
- User profiles and pixel stats

---

## 📜 License

MIT — free to use, modify, and share.

---

## ❤️ Built with love by [Your Name or Username]