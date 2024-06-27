from alxconnect import app, db
from alxconnect.models import *


app.app_context().push()
users = [
    User(firstname="Leo", lastname="Garcia", username="lgarcia",
         email="leo.garcia@gmail.com", password="password567"),
    User(firstname="Paul", lastname="Martin", username="pmartin",
         email="paul.martin@gmail.com", password="password690"),
    User(firstname="Jane", lastname="Wilson", username="jwilson",
         email="jane.wilson@hotmail.com", password="password834"),
    User(firstname="Eve", lastname="Smith", username="esmith",
         email="eve.smith@outlook.com", password="password441"),
    User(firstname="John", lastname="Anderson", username="janderson",
         email="john.anderson@aol.com", password="password105"),
    User(firstname="Nina", lastname="Martin", username="nmartin",
         email="nina.martin@gmail.com", password="password393"),
    User(firstname="Jack", lastname="Thomas", username="jthomas",
         email="jack.thomas@yahoo.com", password="password253"),
    User(firstname="Leo", lastname="Jackson", username="ljackson",
         email="leo.jackson@aol.com", password="password126"),
    User(firstname="Frank", lastname="Taylor", username="ftaylor",
         email="frank.taylor@gmail.com", password="password805"),
    User(firstname="Grace", lastname="Williams", username="gwilliams",
         email="grace.williams@gmail.com", password="password506"),
    User(firstname="Grace", lastname="Martin", username="gmartin",
         email="grace.martin@outlook.com", password="password182"),
    User(firstname="Bob", lastname="Brown", username="bbrown",
         email="bob.brown@gmail.com", password="password444"),
    User(firstname="Bob", lastname="Johnson", username="bjohnson",
         email="bob.johnson@hotmail.com", password="password212"),
    User(firstname="Oscar", lastname="Garcia", username="ogarcia",
         email="oscar.garcia@aol.com", password="password996"),
    User(firstname="Oscar", lastname="Wilson", username="owilson",
         email="oscar.wilson@hotmail.com", password="password440"),
    User(firstname="Rita", lastname="Martinez", username="rmartinez",
         email="rita.martinez@outlook.com", password="password834"),
    User(firstname="Leo", lastname="White", username="lwhite",
         email="leo.white@yahoo.com", password="password472"),
    User(firstname="Leo", lastname="Wilson", username="lwilson",
         email="leo.wilson@gmail.com", password="password951"),
    User(firstname="Ivy", lastname="Garcia", username="igarcia",
         email="ivy.garcia@hotmail.com", password="password792"),
    User(firstname="Diana", lastname="Wilson", username="dwilson",
         email="diana.wilson@yahoo.com", password="password981")
]
db.session.add_all(users)
db.session.commit()
print("Users Created Sucessfully")
