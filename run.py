from alxconnect import app, db
from alxconnect.models import *
if __name__ == "__main__":
    # creates all database model
    app_cont = app.app_context()
    app_cont.push()
    db.create_all()
    app.run(debug=True, port=9090)
