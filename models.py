from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime

db = SQLAlchemy()

post_tags = db.Table('post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String(200), default='default_profile.jpg')
    
    posts = db.relationship('Post', back_populates='user', cascade="all, delete-orphan")

    @hybrid_property
    def full_name(self):
        return f"{self.last_name}, {self.first_name}"

    def get_full_name(self):
        """Returns the full name of the user in 'last, first' format."""
        return self.full_name

    def __repr__(self):
        return f"<User {self.id} {self.first_name} {self.last_name}>"

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', back_populates='posts')
    tags = db.relationship('Tag', secondary='post_tags', back_populates='posts')

    def __repr__(self):
        return f"<Post {self.id} {self.title}>"
    
class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    posts = db.relationship('Post', secondary='post_tags', back_populates='tags')