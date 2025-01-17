from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
    app.config['SECRET_KEY'] = 'your_secret_key'

    db.init_app(app)
    Markdown(app)  # Enable Markdown support

    with app.app_context():
        from . import routes, models
        db.create_all()  # Create database tables

    return app
