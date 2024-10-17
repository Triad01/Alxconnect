from alxconnect import app, db

with app.app_context():
    db.drop_all()
    print("All tables dropped sucessfully")
    db.create_all()
    print("All tables have been created sucessfully")
