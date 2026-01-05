# SmartLink Unified

An extremely simplified URL shortening service with a single-file backend and vibrant, multi-themed frontend pages.

## 🚀 Key Features
- **Single-File Backend**: Everything (Models, Logic, API) is in `app.py`.
- **Thematic Multi-Page UI**: Independent themes for Login, Register, and Dashboard.
- **Midnight Nebula Login**: Deep indigo and purple with glowing effects.
- **Emerald Growth Register**: Vibrant green and teal with leaf iconography.
- **Electric Ocean Dashboard**: Sleek slate and cyan for high productivity.

## 🛠️ Tech Stack
- **Backend**: Python, Flask, SQLAlchemy, JWT, Bcrypt.
- **Frontend**: Bootstrap 5, FontAwesome 6, Custom CSS Themes.
- **Database**: SQLite (default) or PostgreSQL.

## 🏃 Quick Start
1. Install dependencies: `pip install flask flask-sqlalchemy flask-jwt-extended flask-cors flask-limiter flask-bcrypt marshmallow marshmallow-sqlalchemy python-dotenv redis validators pandas`
2. Run the app: `python app.py`
3. Access: `http://localhost:5000`

## 📁 Project Structure
```text
Url_shortening/
├── app.py              # The entire backend
├── templates/          # Themed frontend pages
│   ├── login.html      # Midnight Nebula
│   ├── register.html   # Emerald Growth
│   └── dashboard.html  # Electric Ocean
└── .env                # Configuration
```
