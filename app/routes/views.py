from flask import Blueprint, render_template, redirect

views_bp = Blueprint('views', __name__)

@views_bp.route('/')
def home():
    return render_template('index.html')

@views_bp.route('/login')
def login_page():
    return render_template('login.html')

@views_bp.route('/register')
def register_page():
    return render_template('register.html')

@views_bp.route('/dashboard')
def dashboard_page():
    return render_template('dashboard.html')

@views_bp.route('/analytics')
def analytics_page():
    return render_template('analytics.html')

@views_bp.route('/stats/<int:link_id>')
def link_stats_page(link_id):
    return render_template('stats.html', link_id=link_id)
