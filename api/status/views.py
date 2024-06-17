from flask_restx import Namespace, Resource


api_status = Namespace("status")


@api_status.route("/")
class UserApi(Resource):
    """
    summary: Get Api Status

    Args:
        Resource (api status): Gets the Api Status
    """

    def get(self):
        """
            Get The Api Status
        """

        return {"status": "success"}
