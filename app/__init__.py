from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import markdown
import bleach
import os

db = SQLAlchemy()

ALLOWED_TAGS = [
    'a', 'b', 'i', 'u', 'strong', 'em', 'p', 'ul', 'ol', 'li',
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'pre', 'code', 'blockquote'
]
ALLOWED_ATTRIBUTES = {
    'a': ['href', 'title'],
}

def render_markdown(content):
    html = markdown.markdown(content, extensions=['extra'])
    sanitized_html = bleach.clean(html, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES, strip=True)
    return sanitized_html

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'  # Relative path keeps it in instance/
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'fallback-secret-key')

    db.init_app(app)

    with app.app_context():
        from app import models
        print("Creating all tables...")
        db.create_all()
        print("Tables:", db.metadata.tables.keys())  # Check recognized tables

        # Import and register the blueprint
        from .routes import main
        app.register_blueprint(main)

    return app
