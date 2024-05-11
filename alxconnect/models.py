# NO Worry na Excel i Go send give you 😂😂😂😂
from alxconnect import db
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(60), nullable=False)
    lastname = db.Column(db.String(60), nullable=False)
    username = db.Column(db.String(60), unique=True, nullable=False)
    bio = db.Column(db.String(120), default="Alx learner")
    email = db.Column(db.String(120), unique=True, nullable=False)
    profile_picture = db.Column(
        db.String(20), nullable=False, default="default.jpg")
    password = db.Column(db.String(60), nullable=False)
    joined_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # RELATIONSHIP
    posts = db.relationship("Post", backref="author", lazy=True)
    comments = db.relationship("Comment", backref="author", lazy=True)
    """Not yet Implemented"""

    # course = db.relationship("Course", backref="user", lazy=True)
    # followers = db.relationship("Followers", backref="user", lazy=True)

    """WOULD BE IMPLEMENTED LATER ON BEFORE OR AFTER PRODUCTION"""
    # following = db.relationship("Following", backref="user", lazy=True)
    # message = db.relationship("Message", backref="user", lazy=True)
    # notifications = db.relationship("Notification", backref="user", lazy=True)

    def __repr__(self) -> str:
        return f"User({self.firstname} {self.lastname})"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    comments = db.relationship("Comment", backref="post", lazy=True)
    """Not yet implemented"""

    # likes = db.relationship("Like", backref="post", lazy=True)
    # content = db.Column(db.Text, nullable=False)
    # image = db.Column(db.String(20), nullable=False, default="default.jpg")


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    likes = db.Column(db.Integer)
    content = db.Column(db.Text, nullable=False)
