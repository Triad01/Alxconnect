
from flask_restx import Namespace, Resource, fields, abort
from sqlalchemy.exc import SQLAlchemyError
from flask import request
from http import HTTPStatus
from utils import save_image
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
import datetime
import os


#API NAMESPACE==========================================================================
# Create a namespace for the user API
user_api = Namespace("users", description="User Api Routes", ordered=True)
auth_api = Namespace("auth", description="Authentication API")


#API MODELS =========================================================================
# model for creating a new user
create_user_model = user_api.model("CreateUser", {
    "firstname": fields.String(required=True, description="Enter Your FirstName"),
    "lastname": fields.String(required=True, description="Enter your lastname"),
    "username": fields.String(required=True, description="Enter your username"),
    "email": fields.String(required=True, description="Enter your email"),
    "password": fields.String(required=True, description="Enter your pasword")
})

#model for updating a user
put_model = user_api.model("UpdateUser", {
    "firstname": fields.String(required=True, description="Enter Your FirstName"),
    "lastname": fields.String(required=True),
    "username": fields.String(required=True),
    "email": fields.String(required=True),
})

#model for creating a post

create_post_model = user_api.model("Create a post", {
    "content": fields.String(required=True, descriptiion="Enter the post content")
})

#model for creating a comment
create_comment_model = user_api.model("Create a comment", {
    "content": fields.String(required=True, descriptiion="Enter the comment content")
})

# Model for login request
login_model = auth_api.model("Login", {
    "email": fields.String(required=True, description="Your email"),
    "password": fields.String(required=True, description="Your password")
})


# USER SECTION ==================================================================================

@user_api.route("/", strict_slashes=False)
class Get_Post_User(Resource):
    """
    summary: User API

    Args:
        Resource (user api): performs Crud operations on the user
    """
    @user_api.response(400, "Page Not Found")
    @user_api.response(200, "Sucessfull")
    def get(self):
        """Returns All User"""
        from alxconnect.models import User
        return [obj.to_json() for obj in User.query.all()]

    @user_api.expect(create_user_model)
    @user_api.response(201, "User created successfully.")
    @user_api.response(400, "Validation Error")
    def post(self):
        """Creates New User"""
        from alxconnect.models import User

        data = request.json

        # Check if request data is provided
        if not data:
            abort(404, "No input data provided")

        user = User.query.filter_by(email=data.get("email")).first()
        if user:
            abort(400)

        # Hash the password before saving it to the database
        hashed_password = generate_password_hash(data['password'])

        # Replace the plain text password with the hashed password in the user data
        data['password'] = hashed_password
        try:
            user = User(**data)
            user.save()
            return user.to_json(), 201
        except Exception as e:
            abort(500, f"An error occurred: {str(e)}")


@user_api.route("/<int:user_id>", strict_slashes=False)
class Get_A_User(Resource):

    """
    summary: Get a Specific User

    Args:
    Resource (user api): performs Crud operations on the user to get a user
    """

    def get(self, user_id):
        """Return just a User"""
        from alxconnect.models import User

        user = User.query.get(user_id)
        if not user:
            return "Enter a valid id", HTTPStatus.NOT_IMPLEMENTED

        return user.to_json(), 200

    def delete(self, user_id):
        """Deletes a User"""
        from alxconnect.models import User

        user = User.query.get(user_id)
        if not user:
            return "Enter a valid id", HTTPStatus.NOT_IMPLEMENTED

        user.delete()
        return {"message": "Deleted successfully"}, HTTPStatus.NO_CONTENT

    @ user_api.response(200, description="Succesfully updated")
    def patch(self, user_id):
        """Updates a User"""
        from alxconnect.models import User
        # check if user is available

        user = User.query.get(user_id)
        if not user:
            return "Enter a valid id", HTTPStatus.NOT_ACCEPTABLE

        data = request.form
        if not data:
            abort(400, message="Enter valid data")

        profile_picture_url = None
        if 'profile_picture' in request.files:
            profile_picture = request.files['profile_picture']
            profile_picture_url = save_image(profile_picture)

            if user.profile_picture != 'default.png':
                if os.path.exists(user.profile_picture):
                    os.remove(user.profile_picture)

        try:
            for key, value in data.items():
                if value == "" or value == "string":
                    continue
                if hasattr(user, key):
                    setattr(user, key, value)

            if profile_picture_url:
                user.profile_picture = profile_picture_url

            user.update()
        except SQLAlchemyError as error:
            user.rollback()
            return {"error": error}

        return {"message": "Successfully updated"}, HTTPStatus.CREATED


# POST SECTION ================================================================================================
@ user_api.route("/<int:user_id>/posts", strict_slashes=False)
class Get_a_user_post(Resource):
    def get(self, user_id):
        """Returns all post created by a user"""
        from alxconnect.models import User

        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('page_size', 10, type=int)

        user = User.query.get_or_404(user_id)
        posts = user.posts.paginate(page=page, per_page=per_page)
        return {
            'posts': [post.to_json() for post in posts.items],
            'page': posts.page,
            'page_size': posts.per_page,
            'total_page_items': len(posts.items),
            'prev_page': posts.prev_num,
            'next_page': posts.next_num,
            'total': posts.total,
            'total_pages': posts.pages
        }, 200

    @ user_api.response(201, "Post created successfully.")
    @ user_api.response(400, "Validation Error")
    def post(self, user_id):
        """Creates a Post for a User"""
        from alxconnect.models import Post, User

        user = User.query.get(user_id)
        if not user:
            return {"Error": "invalid user"}, HTTPStatus.NOT_FOUND

        data = request.form
        if not data:
            return {"Error": "Enter Content"}, HTTPStatus.NO_CONTENT

        post = Post(user_id=user.id, content=data.get("content"))
        image_url = None
        if 'image' in request.files:
            image = request.files['image']
            image_url = save_image(image)

        if image_url:
            post.image_url = image_url

        post.save()
        return {"created": "Sucessfull"}, HTTPStatus.CREATED

    def delete(self, user_id):
        """Delete all post created by user"""
        from alxconnect.models import User

        user = User.query.get(user_id)
        if not user:
            return {"Error": "User Not Found"}, HTTPStatus.NOT_FOUND

        [post.delete() for post in user.posts]
        return {"message": "all post deleted"}, HTTPStatus.NO_CONTENT


@ user_api.route("/<int:user_id>/posts/<int:post_id>", strict_slashes=False)
class Get_a_user_post(Resource):
    def get(self, user_id, post_id):
        """Return a single post by a user
            based on the post_id
        """
        from alxconnect.models import User

        user = User.query.get_or_404(user_id)
        return [{post.id: post.to_json()} for post in user.posts if post.id == post_id]

    def patch(self, user_id, post_id):
        """Updates a Post"""
        from alxconnect.models import User, Post

        user = User.query.get(user_id)
        if not user:
            return {"Error": "User Not Found"}, HTTPStatus.NOT_FOUND

        post = Post.query.get(post_id)
        if post.user_id != user.id:
            return {"Error": "Post Not Found"}, HTTPStatus.NOT_FOUND

        data = request.form
        if not data:
            return {"Error": "Empty content"},  HTTPStatus.NOT_FOUND

        if data.get('content'):
            post.content = data.get("content")

        image_url = None
        if 'image' in request.files:
            image = request.files['image']
            image_url = save_image(image)

        if image_url:
            post.image_url = image_url

        post.update()
        return {"updated": "success"}, 201

    def delete(self, user_id, post_id):
        """Delete a post"""
        from alxconnect.models import User, Post

        user = User.query.get(user_id)
        if not user:
            return {"Error": "User Not Found"}, HTTPStatus.NOT_FOUND

        post = Post.query.get(post_id)
        if post.user_id != user.id:
            return {"Error": "Post Not Found"}, HTTPStatus.NOT_FOUND

        post.delete()
        return {"message": "Deleted Sucessfully"}, HTTPStatus.NO_CONTENT


# COMMENTS SECTION ===============================================================================================
@ user_api.route("/<int:user_id>/post/<int:post_id>/comments")
class Get_UserComment_and_Post_Comment(Resource):
    def get(self, user_id, post_id):
        """Get all user comment"""
        from alxconnect.models import User, Post, Comment

        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('page_size', 10, type=int)

        user = User.query.get(user_id)
        if not user:
            return {"Error": "User Not Found"}, HTTPStatus.NOT_FOUND

        post = Post.query.get(post_id)
        if not post:
            return {"Error": "Post Not Found"}, HTTPStatus.NOT_FOUND

        comments = Comment.query.filter_by(
            user_id=user_id,
            post_id=post_id
        ).paginate(page=page, per_page=per_page)

        return {
            'comments': [comment.to_json() for comment in comments.items],
            'page': comments.page,
            'page_size': comments.per_page,
            'total_page_items': len(comments.items),
            'prev_page': comments.prev_num,
            'next_page': comments.next_num,
            'total': comments.total,
            'total_pages': comments.pages
        }, 200
        # comments = [
        #     comment for comment in post.comments if comment.user_id == user_id]

        # return [{user_comment.id: user_comment.to_json()} for user_comment in comments], HTTPStatus.OK

    @ user_api.expect(create_comment_model)
    def post(self, user_id, post_id):
        """Create a comment on a post"""
        from alxconnect.models import User, Post, Comment

        user = User.query.get(user_id)
        if not user:
            return {"Error": "User Not Found"}, HTTPStatus.NOT_FOUND
        post = Post.query.get(post_id)
        if not post:
            return {"Error": "Post Not Found"}, HTTPStatus.NOT_FOUND

        try:
            data = request.json
        except Exception:
            return {"Error": "Enter your content"}, HTTPStatus.NO_CONTENT
        # creating a new comment
        com_content = data.get("content")
        comment = Comment(user_id=user.id, post_id=post.id,
                          content=com_content)
        comment.save()
        return {"status": "Created"}, HTTPStatus.CREATED


@ user_api.route("/<int:user_id>/post/<int:post_id>/comments/<int:comment_id>")
class Get_Signle_comment(Resource):
    """GET, DELETE, UPDATE a comment by a user"""

    def get(self, user_id, post_id, comment_id):
        """Return a single User comment on a post"""
        from alxconnect.models import User, Post, Comment

        user = User.query.get(user_id)
        if not user:
            return {"Error": "User Not Found"}, HTTPStatus.NOT_FOUND

        post = Post.query.get(post_id)
        if not post:
            return {"Error": "Post Not Found"}, HTTPStatus.NOT_FOUND

        comment = Comment.query.get(comment_id)
        if not comment:
            return {"Error": "Comment not found"}, HTTPStatus.NOT_FOUND

        if comment.user_id == user_id:
            return comment.to_json(), HTTPStatus.OK

        return HTTPStatus.FORBIDDEN

    @user_api.expect(create_comment_model)
    def patch(self, user_id, post_id, comment_id):
        """Update a single User comment on a post"""
        from alxconnect.models import User, Post, Comment

        user = User.query.get(user_id)
        if not user:
            return {"Error": "User Not Found"}, HTTPStatus.NOT_FOUND

        post = Post.query.get(post_id)
        if not post:
            return {"Error": "Post Not Found"}, HTTPStatus.NOT_FOUND

        comment = Comment.query.get(comment_id)
        if not comment:
            return {"Error": "Comment not found"}, HTTPStatus.NOT_FOUND
        data = request.json

        if not data:
            return {"Error": "Input content"}, HTTPStatus.NOT_FOUND

        if comment.user_id == user_id:
            comment.content = data.get("content")
            comment.update()
            return {}, HTTPStatus.OK

        return {"Error": "comment not found"}, HTTPStatus.NOT_FOUND

    def delete(self, user_id, post_id, comment_id):
        """Delete a single User comment on a post"""
        from alxconnect.models import User, Post, Comment

        user = User.query.get(user_id)
        if not user:
            return {"Error": "User Not Found"}, HTTPStatus.NOT_FOUND

        post = Post.query.get(post_id)
        if not post:
            return {"Error": "Post Not Found"}, HTTPStatus.NOT_FOUND

        comment = Comment.query.get(comment_id)
        if not comment:
            return {"Error": "Comment not found"}, HTTPStatus.NOT_FOUND

        if comment.user_id == user_id:
            comment.delete()
            return {}, HTTPStatus.OK

        return {"Error": "comment not found"}, HTTPStatus.NOT_FOUND


#LOGIN FUNCTIONALITY ============================================================================
@auth_api.route("/login", strict_slashes=False)
class Login(Resource):
    @auth_api.expect(login_model)
    def post(self):
        """Authenticate a user and return a JWT token"""
        from alxconnect.models import User

        data = request.json
        email = data.get('email')
        password = data.get('password')
        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            return {"error": "Invalid email or password"}, HTTPStatus.UNAUTHORIZED

        # Create JWT token
        access_token = create_access_token(identity=user.id)
        return {"access_token": access_token}, HTTPStatus.OK


@user_api.route("/profile", strict_slashes=False)
class UserProfile(Resource):
    @jwt_required()
    def get(self):
        """Get the profile of the currently logged-in user"""
        from alxconnect.models import User
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return {"error": "User not found"}, HTTPStatus.NOT_FOUND
        return user.to_json(), HTTPStatus.OK


@auth_api.route("/logout", strict_slashes=False)
class User_Logout(Resource):
    """
    Log out a user
    """
    @auth_api.response(200, "Sucessfull")
    @jwt_required()
    def get(self):
        """
        Log out a user
        """
        from flask_jwt_extended import get_jwt
        from alxconnect.models import InvalidToken

        jti = get_jwt()['jti']
        token = InvalidToken(jti=jti)
        token.save()

        return {}, 200


# PASSWORD RESET FUNCTIONALITY =================================================================

def send_message(token, recipient_email):
    from flask_mail import Message, Mail
    from alxconnect import mail
    from alxconnect import app
    mail = Mail(app)

    reset_link = f"http://localhost:9090/auth/reset-password-confirm?token={token}"

    message = Message("Password Reset Request",
                      sender="luckypee01@gmail.com", recipients=[recipient_email])


    message.html = f"""
        <p>Click the link below to reset your password:</p>
        <a href="{reset_link}">Reset Password</a>
        <p>If you did not request a password reset, please ignore this email.</p>
    """

    mail.send(message)

@auth_api.route("/reset-password", strict_slashes=False)
class ResetPasswordRequest(Resource):
    def post(self):
        """Request password reset"""
        from alxconnect.models import User
        data = request.json
        email = data.get('email')

        # Check if the email exists in the system
        user = User.query.filter_by(email=email).first()
        if not user:
            return {"error": "Email not found"}, HTTPStatus.NOT_FOUND

        # Generate a JWT token for password reset (valid for 15 minutes)
        reset_token = create_access_token(identity=user.id, expires_delta=datetime.timedelta(minutes=15))
        send_message(reset_token, user.email)


        return {"message": "Password reset token sent to your email"}, HTTPStatus.OK


# password change functionlity (already logged in users) ======================================
@auth_api.route("/change-password", strict_slashes=False)
class ChangePassword(Resource):
    @jwt_required()  # Only logged-in users can change their password
    def post(self):
        """Allow user to change their password"""
        from alxconnect.models import User
        data = request.json

        # Get the current user's ID from the token
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user:
            return {"error": "User not found"}, HTTPStatus.NOT_FOUND

        # Get the old and new password from the request
        old_password = data.get('old_password')
        new_password = data.get('new_password')

        # Verify the old password
        if not check_password_hash(user.password, old_password):
            return {"error": "Incorrect current password"}, HTTPStatus.UNAUTHORIZED

        # Hash the new password and save it
        user.password = generate_password_hash(new_password)
        user.update()

        return {"message": "Password changed successfully"}, HTTPStatus.OK


# password confirmation functionlity ======================================
@auth_api.route("/reset-password-confirm", strict_slashes=False)
class ResetPasswordConfirm(Resource):
    def post(self):
        """Reset the user's password using the token"""
        from alxconnect.models import User
        data = request.json
        token = data.get('token')
        new_password = data.get('new_password') # Front end note: Ensure the user enters the new password twice for confirmation and name the fields new_password and confirm_password

        try:
            # Decode the token to get the user identity (user id)
            user_id = get_jwt_identity(token)
            user = User.query.get(user_id)

            if not user:
                return {"error": "Invalid token or user not found"}, HTTPStatus.NOT_FOUND

            # Hash the new password and update the user's record
            user.password = generate_password_hash(new_password)
            user.update()

            return {"message": "Password has been reset successfully"}, HTTPStatus.OK
        except Exception as e:
            return {"error": str(e)}, HTTPStatus.BAD_REQUEST
