import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv

# Define extensions here so they can be imported elsewhere
db = SQLAlchemy()
jwt = JWTManager()
limiter = Limiter(key_func=get_remote_address, default_limits=["200 per day", "50 per hour"])

def create_app():
    load_dotenv()
    app = Flask(__name__, template_folder='../templates')
    
    # Configuration
    db_url = os.getenv('DATABASE_URL', 'sqlite:///instance/smartlink.db')
    if db_url and db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
        
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'dev-secret-key')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret')

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    limiter.init_app(app)
    CORS(app)

    # Setup Logging
    if not app.debug:
        if not os.path.exists('logs'):
            try:
                os.mkdir('logs')
            except OSError:
                pass
        
        if os.path.exists('logs'):
            file_handler = RotatingFileHandler('logs/smartlink.log', maxBytes=10240, backupCount=10)
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
            ))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)
            
        app.logger.setLevel(logging.INFO)
        app.logger.info('SmartLink startup')

    # Register Blueprints
    from app.routes.auth import auth_bp
    from app.routes.links import links_bp
    from app.routes.analytics import analytics_bp
    from app.routes.redirect import redirect_bp
    from app.routes.views import views_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(links_bp)
    app.register_blueprint(analytics_bp)
    app.register_blueprint(redirect_bp)
    app.register_blueprint(views_bp)

    # Error Handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({"msg": "Resource not found"}), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        app.logger.error(f"Server Error: {error}")
        return jsonify({"msg": "Internal server error"}), 500

    return app
