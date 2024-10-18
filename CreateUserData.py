from alxconnect import app, db
from alxconnect.models import *
from werkzeug.security import generate_password_hash


app.app_context().push()
users = [
    User(firstname="Leo", lastname="Garcia", username="lgarcia",
         email="leo.garcia@gmail.com", password=generate_password_hash("password567")),
    User(firstname="Paul", lastname="Martin", username="pmartin",
         email="paul.martin@gmail.com", password=generate_password_hash("password690")),
    User(firstname="Jane", lastname="Wilson", username="jwilson",
         email="jane.wilson@hotmail.com", password=generate_password_hash("password834")),
    User(firstname="Eve", lastname="Smith", username="esmith",
         email="eve.smith@outlook.com", password=generate_password_hash("password441")),
    User(firstname="John", lastname="Anderson", username="janderson",
         email="john.anderson@aol.com", password=generate_password_hash("password105")),
    User(firstname="Nina", lastname="Martin", username="nmartin",
         email="nina.martin@gmail.com", password=generate_password_hash("password393")),
    User(firstname="Jack", lastname="Thomas", username="jthomas",
         email="jack.thomas@yahoo.com", password=generate_password_hash("password253")),
    User(firstname="Leo", lastname="Jackson", username="ljackson",
         email="leo.jackson@aol.com", password=generate_password_hash("password126")),
    User(firstname="Frank", lastname="Taylor", username="ftaylor",
         email="frank.taylor@gmail.com", password=generate_password_hash("password805")),
    User(firstname="Grace", lastname="Williams", username="gwilliams",
         email="grace.williams@gmail.com", password=generate_password_hash("password506")),
    User(firstname="Grace", lastname="Martin", username="gmartin",
         email="grace.martin@outlook.com", password=generate_password_hash("password182")),
    User(firstname="Bob", lastname="Brown", username="bbrown",
         email="bob.brown@gmail.com", password=generate_password_hash("password444")),
    User(firstname="Bob", lastname="Johnson", username="bjohnson",
         email="bob.johnson@hotmail.com", password=generate_password_hash("password212")),
    User(firstname="Oscar", lastname="Garcia", username="ogarcia",
         email="oscar.garcia@aol.com", password=generate_password_hash("password996")),
    User(firstname="Oscar", lastname="Wilson", username="owilson",
         email="oscar.wilson@hotmail.com", password=generate_password_hash("password440")),
    User(firstname="Rita", lastname="Martinez", username="rmartinez",
         email="rita.martinez@outlook.com", password=generate_password_hash("password834")),
    User(firstname="Leo", lastname="White", username="lwhite",
         email="leo.white@yahoo.com", password=generate_password_hash("password472")),
    User(firstname="Leo", lastname="Wilson", username="lwilson",
         email="leo.wilson@gmail.com", password=generate_password_hash("password951")),
    User(firstname="Ivy", lastname="Garcia", username="igarcia",
         email="ivy.garcia@hotmail.com", password=generate_password_hash("password792")),
    User(firstname="Diana", lastname="Wilson", username="dwilson",
         email="diana.wilson@yahoo.com", password=generate_password_hash("password981"))
]

db.session.add_all(users)
db.session.commit()
print("Users Created Sucessfully")
