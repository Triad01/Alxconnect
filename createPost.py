from alxconnect import db, app
from alxconnect.models import *


with app.app_context() as ap:
    ap.push()


def create_dummy_posts(num_users=20, posts_per_user=5):
    # Fetch the first 20 users from the database
    users = User.query.limit(num_users).all()

    if not users:
        print("No users found in the database.")
        return

    for user in users:
        for _ in range(posts_per_user):
            post = Post(
                user_id=user.id,
                content=f"Sample content for post by user {user.id}"
            )
            db.session.add(post)

    db.session.commit()
    print(f"Added {num_users * posts_per_user} posts to the database.")


# Call the function
create_dummy_posts()
