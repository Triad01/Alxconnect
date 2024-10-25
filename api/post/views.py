from flask_restx import Namespace, Resource, abort
from flask import request
from sqlalchemy import desc


post_api = Namespace("posts", description="Post Api Routes")


@post_api.route("/", strict_slashes=False)
class Get_and_Create_Post(Resource):
    def get(self):
        """Return all Posts"""
        from alxconnect.models import Post

        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('page_size', 10, type=int)

        # posts = Post.query.paginate(page=page, per_page=per_page)
        posts = Post.query.order_by(Post.created_at.desc()).paginate(page=page, per_page=per_page)
        if not posts.items:
            abort(404)

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

        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('page_size', 10, type=int)

        # post = Post.query.get(post_id)
        # post = Post.query.order_by(desc(Post.created_at)).paginate(page=page, per_page=per_page) # type: ignore

        if not post:
            abort(404, message={"Error": "Post Not Found"})
        # print(post.comments[0])

        comments = post.comments.paginate(page=page, per_page=per_page)
        if not comments.items:
            abort(404)

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
