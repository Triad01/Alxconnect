import copy
from alxconnect import (
    db,
    jwt,
    login_manager
)
from typing import (
    Any,
    Dict
)
from sqlalchemy import event
import os
from utils import convert_image_to_base64
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
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now)

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
        self.updated_at = datetime.now()
        self.verified = True
        db.session.commit()

    def rollback(self):
        """Rollback a database commit incase of errors"""
        db.session.rollback()

    def to_json(self) -> Dict[str, Any]:
        obj = copy.deepcopy(vars(self))
        obj['created_at'] = self.created_at.isoformat()
        obj['updated_at'] = self.updated_at.isoformat()

        if '_sa_instance_state' in obj:
            del obj['_sa_instance_state']

        if 'password' in obj:
            del obj['password']

        if 'profile_picture' in obj:
            if obj['profile_picture'] == 'default.png':
                image_path = 'alxconnect/static/uploads/images/default.png'
            else:
                image_path = obj['profile_picture']

            profile_picture = convert_image_to_base64(image_path)
            obj.update(profile_picture=profile_picture)

        elif 'image_url' in obj:
            image_path = obj.pop('image_url')
            image = convert_image_to_base64(image_path)
            obj.update(image=image)

        return obj


class User(UserMixin, BaseModel, db.Model):
    """
        User model for the database
    """
    __tablename__ = 'users'
    firstname = db.Column(db.String(60), nullable=False)
    lastname = db.Column(db.String(60), nullable=False)
    username = db.Column(db.String(60), unique=True, nullable=False)
    bio = db.Column(db.String(120), default="Alx learner")
    email = db.Column(db.String(120), unique=True, nullable=False)
    profile_picture = db.Column(db.String(256), nullable=False, default="default.png")
    password = db.Column(db.String(256), nullable=False)

    # RELATIONSHIP BETWEEN USER OTHER MODELS
    posts = db.relationship("Post", backref="user",
                            lazy='dynamic', cascade="all, delete, delete-orphan")
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

    def __repr__(self) -> str:
        return f"User([{self.firstname} {self.lastname}] username: {self.username}, email: {self.email})"


class Post(BaseModel, db.Model):
    """Post model for the database"""
    __tablename__ = 'posts'
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    image_url = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, default=datetime.now) 
    comments = db.relationship(
        "Comment", backref="post", lazy="dynamic", cascade="all, delete, delete-orphan")
    
    
    def to_json(self):
        post_data = super().to_json()
        post_data['user'] = {
            "id": self.user.id,
            "firstname": self.user.firstname,
            "lastname": self.user.lastname,
            "username": self.user.username,
            "profile_picture": self.user.profile_picture 
        }
        return post_data




    """Not yet implemented"""

    # likes = db.relationship("Like", backref="post", lazy=True)

    def __repr__(self) -> str:
        return f"{self.content}"


class InvalidToken(db.Model, BaseModel):
    """
    Model for storing blacklisted tokens
    """
    __tablename__ = 'invalid_tokens'
    jti = db.Column(db.String(36), nullable=False, index=True)

    def __repr__(self) -> str:
        return f"InvalidToken(id={self.id}, jti={self.jti})"

    @classmethod
    def verify_jti(cls, jti: str) -> bool:
        """
        Verify the JWT identity
        """
        return bool(cls.query.filter_by(jti=jti).first())


class Comment(BaseModel, db.Model):
    """Comment model for the database"""
    __tablename__ = 'comments'
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"))
    likes = db.Column(db.Integer)

    def __repr__(self) -> str:
        return f"Content: {self.content}"


class Notification(BaseModel, db.Model):
    """Notification model for the database"""
    __tablename__ = 'notifications'
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    content = db.Column(db.Text, nullable=False)
    read = db.Column(db.Boolean, default=False)

    def __repr__(self) -> str:
        return f"Content: {self.content} Read: {self.read}"


class Course(BaseModel, db.Model):
    """Course model for the database"""
    __tablename__ = 'courses'
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    instructor = db.Column(db.String(120), nullable=False)
    duration = db.Column(db.Time, nullable=False)
    image_url = db.Column(db.String(256), default="default.jpg")
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    def __repr__(self) -> str:
        return f"Title: {self.title} Description: {self.description} Instructor: {self.instructor} Duration: {self.duration}"


"""Bugs That i am facing for now would be fixed soon"""
"""Followers Model"""
# class Message(BaseModel, db.Model):
#     """Message model for the database"""
#     __tablename__ = 'messages'
#     sender_id = db.Column(db.Integer, db.ForeignKey("users.id"))
#     receiver_id = db.Column(db.Integer, db.ForeignKey("users.id"))
#     content = db.Column(db.Text, nullable=False)
#     recieved_at = db.Column(db.DateTime, nullable=False,
#                             default=datetime.utcnow)

#     def __init__(self, sender_id, receiver_id, content) -> None:
#         self.sender_id = sender_id
#         self.receiver_id = receiver_id
#         self.content = content
#     def __repr__(self) -> str:
#        return f"Content: {self.content} Recieved at: {self.recieved_at} Sender: {self.sender_id} Receiver: {self.receiver_id}"

"""Followers Model"""
# class Followers(BaseModel, db.Model):
#     """Followers model for the database"""
#     __tablename__ = 'followers'
#     sender_id = db.Column(db.Integer, db.ForeignKey("users.id"))
#     # receiver_id = db.Column(db.Integer, db.ForeignKey("users.id"))
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


def delete_image(mapper, connection, target, field):
    """
    Deletes the image file associated with the target model instance.
    """
    image_url = getattr(target, field)
    if image_url and image_url != 'default.png':
        if os.path.exists(image_url):
            try:
                os.remove(image_url)
            except Exception:
                pass


# Event listener for deleting a profile image before a user is deleted
@event.listens_for(User, 'before_delete')
def delete_user_image(mapper, connection, target):
    delete_image(mapper, connection, target, 'profile_picture')


# Event listener for deleting a post image before post instance is deleted
@event.listens_for(Post, 'before_delete')
def delete_post_image(mapper, connection, target):
    delete_image(mapper, connection, target, 'image_url')
