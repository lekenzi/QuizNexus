import email
import logging
from datetime import datetime

from flask import g, make_response
from flask_jwt_extended import (create_access_token, get_jwt, get_jwt_identity,
                                jwt_required)
from flask_restful import Resource
from werkzeug.security import check_password_hash, generate_password_hash

from app.api.validators import UserLoginParser, UserRegisterParser, testparser
from app.models import User, db

# class TestResource(Resource):
#     @jwt_required()
#     def get(self):
#         return {"message": "This is a test resource"}, 200

#     def post(self):
#         args = testparser.parse_args()
#         return {
#             "message": f"This is a test resource for POST with test={args['test']}"
#         }, 201

#     def put(self):
#         args = testparser.parse_args()
#         return {
#             "message": f"This is a test resource for PUT with test={args['test']}"
#         }, 200

#     def delete(self):
#         args = testparser.parse_args()
#         return {
#             "message": f"This is a test resource for DELETE with test={args['test']}"
#         }, 204


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
                    identity=str(user.id), additional_claims={"role": user.role}
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
        args = UserRegisterParser.parse_args()
        username = args["username"]
        password = args["password"]
        full_name = args["full_name"]
        date_of_birth = args["date_of_birth"]

        print(
            f"""s
                {username}
                {password}
                {full_name}
                {date_of_birth}
        """
        )

        user = User.query.filter_by(username=username).first()

        if user:
            return {"message": "Username already exists"}, 400

        new_user = User()
        new_user.username = username
        new_user.full_name = full_name
        new_user.date_of_birth = datetime.strptime(date_of_birth, "%Y-%m-%d")
        new_user.password_hash = generate_password_hash(password)
        new_user.qualification = "Student"  # Default qualification
        new_user.role = "user"  # Default role

        db.session.add(new_user)
        db.session.commit()

        access_token = create_access_token(
            identity=str(new_user.id),
        )

        return make_response(
            {
                "message": "User registered successfully",
                "access_token": access_token,
                "user": {
                    "id": new_user.id,
                    "username": new_user.username,
                    "isAuthenticated": True,
                    "role": new_user.role,
                },
            },
            201,
        )


class UserLogoutResource(Resource):
    @jwt_required()
    def post(self):
        try:
            jwt_claims = get_jwt()
            jti = jwt_claims.get("jti")
            current_user_id = get_jwt_identity()  # now a string like "1"
            logging.info(f"User {current_user_id} logging out, JWT ID: {jti}")
            return {
                "message": "User logged out successfully",
                "logged_out": True,
                "user_id": current_user_id,
            }, 200
        except Exception as e:
            logging.error(f"Logout error: {str(e)}")
            return {
                "message": "An error occurred while logging out",
                "error": str(e),
            }, 500


class HomeResource(Resource):
    @jwt_required()
    def get(self):
        return {"message": "Welcome to the Quiz Nexus API!"}, 200

    @jwt_required()
    def post(self):
        return {"message": "This is a POST request to the home resource"}, 201

    @jwt_required()
    def put(self):
        return {"message": "This is a PUT request to the home resource"}, 200

    @jwt_required()
    def delete(self):
        return {"message": "This is a DELETE request to the home resource"}, 204
