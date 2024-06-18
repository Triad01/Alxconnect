
from flask_restx import Namespace, Resource, fields, abort
from sqlalchemy.exc import SQLAlchemyError
from flask import request
user_api = Namespace("users", description="Returns all The user")

create_user_model = user_api.model("CreateUser", {
    "firstname": fields.String(required=True, description="Enter Your FirstName"),
    "lastname": fields.String(required=True, description="Enter your lastname"),
    "username": fields.String(required=True, description="Enter your username"),
    "email": fields.String(required=True, description="enter your email"),
    "password": fields.String(required=True, description="Enter your pasword")
})

put_model = user_api.model("UpdateUser", {
    "firstname": fields.String(required=True, description="Enter Your FirstName"),
    "lastname": fields.String(required=True),
    "username": fields.String(required=True),
    "email": fields.String(required=True),
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
        """Returns All User"""
        from alxconnect.models import User
        return [{obj.to_json()["id"]: obj.to_json()} for obj in User.query.all()]

    @user_api.expect(create_user_model)
    @user_api.response(201, "User created successfully.")
    @user_api.response(400, "Validation Error")
    def post(self):
        """Creates New User"""
        from alxconnect.models import User
        data = request.json
        if not data:
            abort(404)

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
        """Return just a User"""
        from alxconnect.models import User
        user = User.query.get(user_id)
        if not user:
            abort(404, message="Enter a valid id")
        return user.to_json()

    def delete(self, user_id):
        """Deletes a User"""
        from alxconnect.models import User

        user = User.query.get(user_id)
        if not user:
            abort(404, message="Enter a valid id")
        user.delete()
        return {}, 201

    @user_api.expect(put_model)
    @user_api.response(201, description="Succesfully updated")
    def put(self, user_id):
        """Updates a User"""
        from alxconnect.models import User
        # check if user is available
        user = User.query.get(user_id)
        if not user:
            abort(404, message="Enter a valid id")

        data = request.json
        if not data:
            abort(400, message="Enter valid data")
        try:
            for key, value in data.items():
                if value is None or value == "string":
                    continue
                if hasattr(user, key):
                    setattr(user, key, value)
            user.update()
        except SQLAlchemyError as error:
            user.rollback()
            return {"error": error}

        return {"message": "Successfully updated"}, 200
