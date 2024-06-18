from flask_restx import Namespace, Resource, abort, fields
from flask import request


post_api = Namespace("posts")

create_post_model = post_api.model("Create a post", {
    "content": fields.String(required=True, descriptiion="Enter the post content")
})


@post_api.route("/")
class Get_and_Create_Post(Resource):
    def get(self):
        """Return all Posts"""
        from alxconnect.models import Post
        posts = Post.query.all()
        if not posts:
            abort(404)

        return [{post.id: post.to_json()}for post in posts]


@post_api.route("/<int:post_id>")
class Get_Post(Resource):
    def get(self, post_id):
        """Return a post"""
        from alxconnect.models import Post
        post = Post.query.get_or_404(post_id)

        return post.to_json()


@post_api.route("/<int:user_id>/posts", strict_slashes=False)
class Get_a_user_post(Resource):
    def get(self, user_id):
        """Returns all post created by a user"""
        from alxconnect.models import User
        user = User.query.get_or_404(user_id)

        return [{post.id: post.to_json()} for post in user.posts]

    @post_api.response(201, "Post created successfully.")
    @post_api.response(400, "Validation Error")
    @post_api.expect(create_post_model)
    def post(self, user_id):
        """Creates a Post for a User"""
        from alxconnect.models import Post, User

        user = User.query.get(user_id)
        if not user:
            return abort(404, message='{"Error":"invalid user"}')

        data = request.json
        if not data:
            abort(404)

        post = Post(user_id=user.id, content=data.get("content"))
        post.save()
        return {"created": "Sucessfull"}, 201

    def delete(self, user_id):
        """Delete all post created by user"""
        from alxconnect.models import User
        user = User.query.get(user_id)
        if not user:
            abort(404, message={"Error": "User Not Found"})
            [post.delete() for post in user.posts]
        return {"message": "all post deleted"}


@post_api.route("/<int:user_id>/posts/<int:post_id>", strict_slashes=False)
class Get_a_user_post(Resource):
    def get(self, user_id, post_id):
        """Return a single post by a user
            based on the post_id
        """
        from alxconnect.models import User
        user = User.query.get_or_404(user_id)
        return [{post.id: post.to_json()} for post in user.posts if post.id == post_id]

    @post_api.expect(create_post_model)
    def patch(self, user_id, post_id):
        """Updates a Post"""
        from alxconnect.models import User, Post

        user = User.query.get(user_id)
        if not user:
            abort(404, message='{"Error":"User Not Found"}')

        post = Post.query.get(post_id)
        if post.user_id != user.id:
            abort(404, message='{"Error":"Post Not Found"}')
        data = request.json
        if not data:
            abort(404, message='{"Error":"Empty content"}')

        post.content = data.get("content")
        post.update()

        return {"updated": "success"}, 201

    def delete(self, user_id, post_id):
        """Delete a post"""
        from alxconnect.models import User, Post

        user = User.query.get(user_id)
        if not user:
            abort(404, message='{"Error":"User Not Found"}')

        post = Post.query.get(post_id)
        if post.user_id != user.id:
            abort(404, message='{"Error":"Post Not Found"}')
        post.delete()
        return {"message": "Deleted Sucessfully"}
