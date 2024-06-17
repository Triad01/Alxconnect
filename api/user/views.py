
from flask_restx import Namespace, Resource, fields, abort
from flask import request
user_api = Namespace("users", description="Returns all The user")

create_user_model = user_api.model("CreateUser", {
    "firstname": fields.String(required=True, description="Enter Your FirstName"),
    "lastname": fields.String(required=True),
    "username": fields.String(required=True),
    "email": fields.String(required=True),
    "password": fields.String(required=True)
})


@user_api.route("/")
class Get_Post_User(Resource):

    """
    summary: User API 

    Args:
        Resource (user api): performs Crud operations on the user
    """
    @user_api.response(400, "Page Not Found")
    @user_api.response(200, "Sucessfull")
    def get(self):
        from alxconnect.models import User
        """Get Users

         Returns:
             Json : A dictionary of all User
         """
        return [{obj.to_json()["id"]: obj.to_json()} for obj in User.query.all()]

    @user_api.expect(create_user_model)
    @user_api.response(201, "User created successfully.")
    @user_api.response(400, "Validation Error")
    def post(self):
        """"""
        from alxconnect.models import User
        data = request.json
        user = User(**data)
        user.save()
        return user.to_json(), 201


@user_api.route("/<int:user_id>")
class Get_A_User(Resource):

    """
    summary: Get a Specific User

    Args:
    Resource (user api): performs Crud operations on the user to get a user
    """

    def get(self, user_id):
        from alxconnect.models import User
        user = User.query.get(user_id)
        if not user:
            abort(404, message="Enter a valid id")
        return user.to_json()
