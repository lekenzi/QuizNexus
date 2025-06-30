from flask_restful import reqparse

testparser = reqparse.RequestParser()

testparser.add_argument(
    "test",
    type=str,
    required=True,
    help="Test is required",
    location="json",
)


UserLoginParser = reqparse.RequestParser()

UserLoginParser.add_argument(
    "username", type=str, required=True, help="Username is required", location="json"
)
UserLoginParser.add_argument(
    "password", type=str, required=True, help="Password is required", location="json"
)


UserRegisterParser = reqparse.RequestParser()

UserRegisterParser.add_argument(
    "username", type=str, required=True, help="Username is required", location="json"
)
UserRegisterParser.add_argument(
    "password", type=str, required=True, help="Password is required", location="json"
)
UserRegisterParser.add_argument(
    "full_name", type=str, required=True, help="Full name is required", location="json"
)

UserRegisterParser.add_argument(
    "date_of_birth",
    type=str,
    required=True,
    help="Date of birth is required",
    location="json",
)
