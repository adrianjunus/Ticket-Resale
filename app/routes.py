from flask import Blueprint, render_template, request, redirect, url_for
from .models import Post, db
from .__init__ import render_markdown

# Create a Blueprint for the routes
main = Blueprint('main', __name__)

@main.route('/')
def index():
    posts = Post.query.order_by(Post.created_at.desc()).all()  # Get all posts, newest first
    return render_template('index.html', posts=posts)

@main.route('/post/<int:id>')
def view_post(id):
    post = Post.query.get_or_404(id)
    return render_template('post.html', post=post)

@main.route('/create', methods=['GET', 'POST'])
def create_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        category = request.form['category']
        tags = request.form['tags']

        new_post = Post(title=title, content=content, category=category, tags=tags, user_id=1)  # Replace with actual user_id
        db.session.add(new_post)
        db.session.commit()

        return redirect(url_for('main.index'))

    return render_template('create.html')
