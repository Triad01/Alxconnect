from flask_wtf import FlaskForm
from alxconnect.models import User
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError


class RegisterationForm(FlaskForm):
    firstname = StringField("Firstname", validators=[
                           DataRequired(), Length(min=2, max=20)])

    lastname = StringField("Lastname", validators=[
                           DataRequired(), Length(min=2, max=20)])
    username = StringField("Username", validators=[
                           DataRequired(), Length(min=2, max=20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm password", validators=[
                                     DataRequired(), EqualTo("password")])
    submit = SubmitField("Sign up")

    # Custom validation for username and email
    # if username or email already exists in the database
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Username already taken")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Email already taken")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember me")
    submit = SubmitField("Login")

    # Custom validation for email and password
    # if email or password does not exist in the database
    # def validate_email(self, email):
    #     user = User.query.filter_by(email=email.data).first()
    #     if not user:
    #         raise ValidationError("Email does not exist")
    #     return user

    # # still skeptical about this validation
    # # think we should use the bcript library to hash the password here
    # def validate_password(self, password):
    #     user = User.query.filter_by(password=password.data).first()
    #     if not user:
    #         raise ValidationError("Password is incorrect")
    #     return user
