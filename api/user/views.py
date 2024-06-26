
from flask_restx import Namespace, Resource, fields, abort
from sqlalchemy.exc import SQLAlchemyError
from flask import request
from http import HTTPStatus
user_api = Namespace("users", description="User Api Routes", ordered=True)

create_user_model = user_api.model("CreateUser", {
    "firstname": fields.String(required=True, description="Enter Your FirstName"),
    "lastname": fields.String(required=True, description="Enter your lastname"),
    "username": fields.String(required=True, description="Enter your username"),
    "email": fields.String(required=True, description="enter your email"),
    "password": fields.String(required=True, description="Enter your pasword")
})

put_model = user_api.model("UpdateUser", {
    "firstname": fields.String(required=True, description="Enter Your FirstName"),
    "lastname": fields.String(required=True),
    "username": fields.String(required=True),
    "email": fields.String(required=True),
})
create_post_model = user_api.model("Create a post", {
    "content": fields.String(required=True, descriptiion="Enter the post content")
})
create_comment_model = user_api.model("Create a comment", {
    "content": fields.String(required=True, descriptiion="Enter the comment content")
})

# USER SECTION


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
        return [{obj.to_json()["id"]: obj.to_json()} for obj in User.query.all()]

    @user_api.expect(create_user_model)
    @user_api.response(201, "User created successfully.")
    @user_api.response(400, "Validation Error")
    def post(self):
        """Creates New User"""
        from alxconnect.models import User
        data = request.json
        if not data:
            abort(404)

        user = User(**data)
        user.save()
        return user.to_json(), 201


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

    @ user_api.expect(put_model)
    @ user_api.response(201, description="Succesfully updated")
    def patch(self, user_id):
        """Updates a User"""
        from alxconnect.models import User
        # check if user is available
        user = User.query.get(user_id)
        if not user:
            return "Enter a valid id", HTTPStatus.NOT_ACCEPTABLE

        data = request.json
        if not data:
            abort(400, message="Enter valid data")
        try:
            for key, value in data.items():
                if value == "" or value == "string":
                    continue
                if hasattr(user, key):
                    setattr(user, key, value)
            user.update()
        except SQLAlchemyError as error:
            user.rollback()
            return {"error": error}

        return {"message": "Successfully updated"}, HTTPStatus.CREATED


# POST SECTION
@ user_api.route("/<int:user_id>/posts", strict_slashes=False)
class Get_a_user_post(Resource):
    def get(self, user_id):
        """Returns all post created by a user"""
        from alxconnect.models import User
        user = User.query.get_or_404(user_id)

        return [{post.id: post.to_json()} for post in user.posts]

    @ user_api.response(201, "Post created successfully.")
    @ user_api.response(400, "Validation Error")
    @ user_api.expect(create_post_model)
    def post(self, user_id):
        """Creates a Post for a User"""
        from alxconnect.models import Post, User

        user = User.query.get(user_id)
        if not user:
            return {"Error": "invalid user"}, HTTPStatus.NOT_FOUND

        data = request.json
        if not data:
            return {"Error": "Enter Content"}, HTTPStatus.NO_CONTENT

        post = Post(user_id=user.id, content=data.get("content"))
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

    @ user_api.expect(create_post_model)
    def patch(self, user_id, post_id):
        """Updates a Post"""
        from alxconnect.models import User, Post

        user = User.query.get(user_id)
        if not user:
            return {"Error": "User Not Found"}, HTTPStatus.NOT_FOUND

        post = Post.query.get(post_id)
        if post.user_id != user.id:
            return {"Error": "Post Not Found"}, HTTPStatus.NOT_FOUND
        data = request.json
        if not data:
            return {"Error": "Empty content"},  HTTPStatus.NOT_FOUND

        post.content = data.get("content")
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


# COMMENTS SECTION
@ user_api.route("/<int:user_id>/post/<int:post_id>/comments")
class Get_UserComment_and_Post_Comment(Resource):
    def get(self, user_id, post_id):
        """Get all user comment"""
        from alxconnect.models import User, Post

        user = User.query.get(user_id)
        if not user:
            return {"Error": "User Not Found"}, HTTPStatus.NOT_FOUND
        post = Post.query.get(post_id)
        if not post:
            return {"Error": "Post Not Found"}, HTTPStatus.NOT_FOUND
        comments = [
            comment for comment in post.comments if comment.user_id == user_id]

        return [{user_comment.id: user_comment.to_json()} for user_comment in comments], HTTPStatus.OK

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
