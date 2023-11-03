from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String(200), default='default_profile.jpg')
    posts = db.relationship('Post', back_populates='user', lazy='dynamic')

    @hybrid_property
    def full_name(self):
        return self.last_name + ', ' + self.first_name

    def get_full_name(self):
        """Return the full name of the user in 'last, first' format."""
        return f"{self.last_name}, {self.first_name}"

    def __repr__(self):
        return f"<User {self.id} {self.first_name} {self.last_name}>"

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', back_populates='posts')