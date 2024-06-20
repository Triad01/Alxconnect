from flask_restx import Namespace, Resource, abort


post_api = Namespace("posts", description="Post Api Routes")


@post_api.route("/", strict_slashes=False)
class Get_and_Create_Post(Resource):
    def get(self):
        """Return all Posts"""
        from alxconnect.models import Post
        posts = Post.query.all()
        if not posts:
            abort(404)

        return [{post.id: post.to_json()}for post in posts]


@post_api.route("/<int:post_id>", strict_slashes=False)
class Get_Post(Resource):
    def get(self, post_id):
        """Return a post"""
        from alxconnect.models import Post
        post = Post.query.get_or_404(post_id)

        return post.to_json()


@post_api.route("/<int:post_id>/comments", strict_slashes=False)
class Post_Comment(Resource):
    def get(self, post_id):
        """Return all comments on a post"""
        from alxconnect.models import Post
        post = Post.query.get(post_id)
        if not post:
            abort(404, message={"Error": "Post Not Found"})
        # print(post.comments[0])
        return [{comment.id: comment.to_json()} for comment in post.comments]
