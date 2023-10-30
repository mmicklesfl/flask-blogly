from flask import Flask, render_template, redirect, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, User

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)
db.init_app(app)

# Ensure all tables are created when the app starts up
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

if __name__ == "__main__":
    app.run(debug=True)
