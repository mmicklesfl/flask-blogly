from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property

db = SQLAlchemy()

class User(db.Model):
    """User in the Blogly application."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String(200), default='default_profile.jpg')

    @hybrid_property
    def full_name(self):
        return self.last_name + ', ' + self.first_name

    def get_full_name(self):
        """Return the full name of the user in 'last, first' format."""
        return f"{self.last_name}, {self.first_name}"

    def __repr__(self):
        return f"<User {self.id} {self.first_name} {self.last_name}>"
