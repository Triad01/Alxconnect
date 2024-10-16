from alxconnect import app, db

with app.app_context():
    db.drop_all()
    print("ALl tables dropped sucessfully")
    db.create_all()
    print("ALl tables have been created sucessfully")
