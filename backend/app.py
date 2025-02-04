from flask import Flask
from datetime import timedelta
from dotenv import load_dotenv
import os
from extensions import db, jwt, cors

def create_app():
    load_dotenv()
    app = Flask(__name__)

    # Configure app
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key')
    app.config['SESSION_COOKIE_NAME'] = 'session'
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=5)
    app.config["JWT_SECRET_KEY"] = "your_secret_key"

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)

    # Import and register blueprints
    # with app.app_context():
    from routes.event_routes import event_bp
    app.register_blueprint(event_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=int(os.getenv("PORT", 5000)))