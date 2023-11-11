from flask import flash, Flask, render_template, redirect, request, url_for
from flask_debugtoolbar import DebugToolbarExtension
from models import db, User, Post, Tag

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
    recent_posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template('homepage.html', posts=recent_posts)

@app.route('/users', endpoint='users_list')
def users_index():
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users/index.html', users=users)

@app.route('/users/new', methods=["GET", "POST"])
def users_new():
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
    user = User.query.get_or_404(user_id)
    return render_template('users/profile.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=["GET", "POST"])
def users_edit(user_id):
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
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect("/users")

@app.route('/posts/new', methods=["GET", "POST"])
def posts_new():
    tags = Tag.query.all()
    if request.method == "POST":
        title = request.form['title']
        content = request.form['content']
        user_id = request.form['user_id']
        new_post = Post(title=title, content=content, user_id=user_id)

        # Get selected tags
        selected_tags = request.form.getlist('tags')
        for tag_id in selected_tags:
            tag = Tag.query.get(tag_id)
            if tag:
                new_post.tags.append(tag)

        db.session.add(new_post)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            flash('An error occurred while adding the post. Please try again.')
            return render_template("posts/new.html", user_id=user_id, tags=tags)
        return redirect(url_for('users_profile', user_id=user_id))
    else:
        user_id = request.args.get('user_id')
        if not user_id:
            flash('No user specified for the new post.')
            return redirect(url_for('home_redirect'))
        return render_template("posts/new.html", user_id=user_id, tags=tags)

@app.route('/posts')
def posts_index():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('posts/index.html', posts=posts)

@app.route('/posts/<int:post_id>')
def posts_show(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('posts/show.html', post=post, tags=post.tags)

@app.route('/posts/<int:post_id>/edit', methods=["GET", "POST"])
def posts_edit(post_id):
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    if request.method == "POST":
        post.title = request.form['title']
        post.content = request.form['content']

        # Update tags
        selected_tags = request.form.getlist('tags')
        post.tags = []
        for tag_id in selected_tags:
            tag = Tag.query.get(tag_id)
            if tag:
                post.tags.append(tag)

        db.session.commit()
        return redirect(f'/posts/{post_id}')
    return render_template('posts/edit.html', post=post, tags=tags)


@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def posts_delete(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect("/posts")

@app.route('/tags')
def tags_index():
    tags = Tag.query.all()
    return render_template('tags/index.html', tags=tags)

@app.route('/tags/new', methods=['GET', 'POST'])
def tags_new():
    if request.method == 'POST':
        name = request.form['name']
        tag = Tag(name=name)
        db.session.add(tag)
        db.session.commit()
        return redirect(url_for('tags_index'))
    return render_template('tags/new.html')

@app.route('/tags/<int:tag_id>')
def tags_show(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    return render_template('tags/show.html', tag=tag)

@app.route('/tags/<int:tag_id>/edit', methods=['GET', 'POST'])
def tags_edit(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    if request.method == 'POST':
        tag.name = request.form['name']
        db.session.commit()
        return redirect(url_for('tags_show', tag_id=tag.id))
    return render_template('tags/edit.html', tag=tag)

@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def tags_delete(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return redirect(url_for('tags_index'))

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run(debug=True)
