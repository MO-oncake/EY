import os
from flask import Flask, jsonify, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta
from flask_jwt_extended import create_access_token
from flask_jwt_extended import JWTManager

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Set up the secret key for sessions and security purposes
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key')
app.config['SESSION_COOKIE_NAME'] = 'session'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=5)
app.config["JWT_SECRET_KEY"] = "your_secret_key" 

jwt = JWTManager(app)

# Set up the PostgreSQL database connection using SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Enable Cross-Origin Resource Sharing (CORS)
CORS(app)




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.getenv("PORT", 5000)))
