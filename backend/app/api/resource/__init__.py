import email

from app.api.validators import UserLoginParser, testparser
from app.models import User
from flask import g, make_response
from flask_jwt_extended import create_access_token, jwt_required
from flask_restful import Resource


class TestResource(Resource):
    @jwt_required()
    def get(self):
        return {"message": "This is a test resource"}, 200

    def post(self):
        args = testparser.parse_args()
        return {
            "message": f"This is a test resource for POST with test={args['test']}"
        }, 201

    def put(self):
        args = testparser.parse_args()
        return {
            "message": f"This is a test resource for PUT with test={args['test']}"
        }, 200

    def delete(self):
        args = testparser.parse_args()
        return {
            "message": f"This is a test resource for DELETE with test={args['test']}"
        }, 204


class UserLoginResource(Resource):
    @jwt_required()
    def get(self):
        return {"message": "This is a user login resource"}, 200

    def post(self):
        args = UserLoginParser.parse_args()
        username = args["username"]
        password = args["password"]

        user = User.query.filter_by(username=username).first()

        if not user:
            return {"message": "Invalid username or password"}, 401
        else:
            if not user.check_hash(password):
                return {"message": "Invalid username or password"}, 401
            else:

                access_token = create_access_token(
                    identity={"id": user.id, "role": user.role}
                )

        return make_response(
            {
                "message": "Login successful",
                "access_token": access_token,
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "isAuthenticated": True,
                    "role": user.role,
                },
            },
            200,
        )


class UserRegisterResource(Resource):
    def post(self):
        args = UserLoginParser.parse_args()
        username = args["username"]
        password = args["password"]
