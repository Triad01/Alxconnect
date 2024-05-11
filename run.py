from alxconnect import app, db
from alxconnect.models import *
if __name__ == "__main__":
    # creates all database model
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=9090)
