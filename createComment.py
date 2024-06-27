from alxconnect import db, app
from alxconnect.models import *


with app.app_context() as ap:
    ap.push()


def create_dummy_comments(num_users=20, num_post=-1, posts_per_user=5):
    users = User.query.all()
    posts = Post.query.all()
    # print(len(users))
    # print(posts, len(posts))

    for user, post in zip(users[:num_users], posts[:num_post]):
        for _ in range(posts_per_user):
            comment = Comment(
                user_id=user.id,
                post_id=post.id,
                content=f"Sample text from User {user.firstname} on post {post.id} and "
            )
            db.session.add(comment)
            db.session.commit()


create_dummy_comments()
