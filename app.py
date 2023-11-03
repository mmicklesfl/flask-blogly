from flask import Flask, render_template, redirect, request, url_for
from flask_debugtoolbar import DebugToolbarExtension
from models import db, User, Post

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)
db.init_app(app)

with app.app_context():
    db.create_all()
    
@app.route('/')
def home_redirect():
    """Redirect to list of users."""
    return redirect('/users')

@app.route('/users')
def users_index():
    """Show all users."""
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users/index.html', users=users)

@app.route('/users/new', methods=["GET", "POST"])
def users_new():
    """Show an add form for users."""
    if request.method == "POST":
        new_user = User(
            first_name=request.form['first_name'],
            last_name=request.form['last_name'],
            image_url=request.form['image_url'] or None)
        db.session.add(new_user)
        db.session.commit()
        return redirect("/users")
    else:
        return render_template("users/new.html")

@app.route('/users/<int:user_id>')
def users_profile(user_id):
    """Show information about the given user."""
    user = User.query.get_or_404(user_id)
    return render_template('users/profile.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=["GET", "POST"])
def users_edit(user_id):
    """Show the edit page for a user."""
    user = User.query.get_or_404(user_id)
    if request.method == "POST":
        user.first_name = request.form['first_name']
        user.last_name = request.form['last_name']
        user.image_url = request.form['image_url'] or None
        db.session.add(user)
        db.session.commit()
        return redirect("/users")
    else:
        return render_template('users/edit.html', user=user)

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def users_delete(user_id):
    """Delete the user."""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect("/users")

@app.route('/posts/new', methods=["GET", "POST"])
def posts_new():
    if request.method == "POST":
        title = request.form['title']
        content = request.form['content']
        user_id = request.form['user_id']
        new_post = Post(title=title, content=content, user_id=user_id)
        db.session.add(new_post)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            flash('An error occurred while adding the post. Please try again.')
            return render_template("posts/new.html", user_id=user_id)
        return redirect(url_for('users_profile', user_id=user_id))
    else:
        user_id = request.args.get('user_id')
        if not user_id:
            flash('No user specified for the new post.')
            return redirect(url_for('index'))
        return render_template("posts/new.html", user_id=user_id)

@app.route('/posts/<int:post_id>')
def posts_show(post_id):
    """Show a post."""
    post = Post.query.get_or_404(post_id)
    return render_template('posts/show.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=["GET", "POST"])
def posts_edit(post_id):
    """Edit a post."""
    post = Post.query.get_or_404(post_id)
    if request.method == "POST":
        post.title = request.form['title']
        post.content = request.form['content']
        db.session.commit()
        return redirect(f'/posts/{post_id}')
    return render_template('posts/edit.html', post=post)

@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def posts_delete(post_id):
    """Delete a post."""
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect("/posts")

if __name__ == "__main__":
    app.run(debug=True)
