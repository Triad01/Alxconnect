from alxconnect import (
    db,
    jwt,
    login_manager
)
from datetime import datetime
from typing import Mapping
from flask_login import UserMixin


@jwt.token_in_blocklist_loader
def check_if_token_is_blacklisted(jwt_header: Mapping[str, str],
                                  jwt_payload: Mapping[str, str]) -> bool:
    """
    Check if user has logged out
    """
    jti = jwt_payload['jti']
    return InvalidToken.verify_jti(jti)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class BaseModel:
    """BaseModel For Other Models"""

    def save(self):
        """Saves a model to the database
        """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Deletes the a model instance from the database"""
        db.session.delete(self)
        db.session.commit()

    def update(self):
        """Update a Model instance in the database"""
        # db.session.merge(self)
        self.verified = True
        db.session.commit()

    def rollback():
        """Rollback a database commit incase of errors"""
        db.session.rollback()

    def to_json(self):
        """Convert instance into dict format"""
        dictionary = {}
        for key in self.__mapper__.c.keys():
            value = getattr(self, key)
            if key == "password":
                continue
            if isinstance(value, datetime):
                dictionary[key] = value.isoformat()
            else:
                dictionary[key] = value
        return dictionary


class User(db.Model, UserMixin, BaseModel):
    """
        User model for the database
    """
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(60), nullable=False)
    lastname = db.Column(db.String(60), nullable=False)
    username = db.Column(db.String(60), unique=True, nullable=False)
    bio = db.Column(db.String(120), default="Alx learner")
    email = db.Column(db.String(120), unique=True, nullable=False)
    profile_picture = db.Column(
        db.String(20), nullable=False, default="default.jpg")
    password = db.Column(db.String(256), nullable=False)
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)

    # RELATIONSHIP BETWEEN USER OTHER MODELS

    posts = db.relationship("Post", backref="user",
                            lazy=True, cascade="all, delete, delete-orphan")
    comments = db.relationship(
        "Comment", backref="user", lazy="dynamic", cascade="all, delete, delete-orphan")

    """Not Yet Implemented"""
    # course = db.relationship("Course", backref="user",
    #                          lazy=True, cascade="all, delete, delete-orphan")
    # notifications = db.relationship(
    #     "Notification", backref="user", lazy=True, cascade="all, delete, delete-orphan")
    # followers = db.relationship(
    #     "Followers", backref="user", lazy=True, cascade="all, delete, delete-orphan")
    # message = db.relationship(
    #     "Message", backref="user", lazy=True, cascade="all, delete, delete-orphan")

    def __init__(self, firstname, lastname, username, email, password) -> None:
        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self) -> str:
        return f"User([{self.firstname} {self.lastname}] username: {self.username}, email: {self.email})"


class Post(db.Model, BaseModel):
    """Post model for the database"""
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    comments = db.relationship(
        "Comment", backref="post", lazy="dynamic", cascade="all, delete, delete-orphan")
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)

    """Not yet implemented"""

    # likes = db.relationship("Like", backref="post", lazy=True)

    # image = db.Column(db.String(20), nullable=False, default="default.jpg")

    def __init__(self, user_id, content) -> None:
        self.user_id = user_id
        self.content = content

    def __repr__(self) -> str:
        return f"{self.content}"


class InvalidToken(db.Model, BaseModel):
    """
    Model for storing blacklisted tokens
    """
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, index=True)

    def __init__(self, jti: str) -> None:
        self.jti = jti

    def __repr__(self) -> str:
        return f"InvalidToken(id={self.id}, jti={self.jti})"

    @classmethod
    def verify_jti(cls, jti: str) -> bool:
        """
        Verify the JWT identity
        """
        return bool(cls.query.filter_by(jti=jti).first())


class Comment(db.Model, BaseModel):
    """Comment model for the database"""
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"))
    likes = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)

    def __init__(self, post_id, user_id, content) -> None:
        self.post_id = post_id
        self.user_id = user_id
        self.content = content

    def __repr__(self) -> str:
        return f"Content: {self.content}"


class Notification(db.Model, BaseModel):
    """Notification model for the database"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    read = db.Column(db.Boolean, default=False)

    def __init__(self, user_id, content) -> None:
        self.user_id = user_id
        self.content = content

    def __repr__(self) -> str:
        return f"Content: {self.content} Read: {self.read}"


class Course(db.Model):
    """Course model for the database"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    instructor = db.Column(db.String(120), nullable=False)
    duration = db.Column(db.Time, nullable=False)
    image_url = db.Column(db.String(60), default="default.jpg")
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    uploaded_at = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __init__(self, title, description, instructor, duration) -> None:
        self.title = title
        self.description = description
        self.instructor = instructor
        self.duration = duration

    def __repr__(self) -> str:
        return f"Title: {self.title} Description: {self.description} Instructor: {self.instructor} Duration: {self.duration}"


"""Bugs That i am facing for now would be fixed soon"""
"""Followers Model"""
# class Message(db.Model):
#     """Message model for the database"""
#     msg_id = db.Column(db.Integer, primary_key=True)
#     sender_id = db.Column(db.Integer, db.ForeignKey("user.id"))
#     receiver_id = db.Column(db.Integer, db.ForeignKey("user.id"))
#     content = db.Column(db.Text, nullable=False)
#     created_at = db.Column(db.DateTime, nullable=False,
#                            default=datetime.utcnow)
#     recieved_at = db.Column(db.DateTime, nullable=False,
#                             default=datetime.utcnow)

#     def __init__(self, sender_id, receiver_id, content) -> None:
#         self.sender_id = sender_id
#         self.receiver_id = receiver_id
#         self.content = content
#     def __repr__(self) -> str:
#        return f"Content: {self.content} Recieved at: {self.recieved_at} Sender: {self.sender_id} Receiver: {self.receiver_id}"

"""Followers Model"""
# class Followers(db.Model):
#     """Followers model for the database"""
#     id = db.Column(db.Integer, primary_key=True)
#     sender_id = db.Column(db.Integer, db.ForeignKey("user.id"))
#     # receiver_id = db.Column(db.Integer, db.ForeignKey("user.id"))
#     created_at = db.Column(db.DateTime, nullable=False,
#                            default=datetime.utcnow)
#     status = db.Column(db.Boolean, default=False)

# Define relationships explicitly
# sender = db.relationship("User", foreign_keys=[
#                          sender_id], backref="sent_follows")
# receiver = db.relationship("User", foreign_keys=[
#                            receiver_id], backref="received_follows")

# def __init__(self, sender_id, receiver_id) -> None:
#     self.sender_id = sender_id
#     self.receiver_id = receiver_id

# def __repr__(self) -> str:
#     return f"Status {self.status}"
