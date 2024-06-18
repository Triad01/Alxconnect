from flask import Blueprint
from flask_restx import Api
from api.user.views import user_api
from api.status.views import api_status
from api.post.views import post_api

blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(blueprint, title="AlxConnect Api",
          default_swagger_filename="alxconnect")


api.add_namespace(api_status)
api.add_namespace(user_api)
api.add_namespace(post_api)
