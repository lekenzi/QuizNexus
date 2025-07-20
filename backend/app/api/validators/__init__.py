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
"""
usrname, password, full_name, date_of_birth
"""

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


checkTokenParser = reqparse.RequestParser()
checkTokenParser.add_argument(
    "access_token",
    type=str,
    required=False,
    help="Access token",
    location="json",
)


add_subject_parser = reqparse.RequestParser()
add_subject_parser.add_argument(
    "name",
    type=str,
    required=False,  # Changed to False for better error handling
    help="Subject name is required",
    location="json",
)
add_subject_parser.add_argument(
    "description",
    type=str,
    required=False,  # Changed to False for better error handling
    help="Subject description is required",
    location="json",
)


add_chapter_parser = reqparse.RequestParser()
add_chapter_parser.add_argument(
    "name",
    type=str,
    required=False,  # Changed to False for better error handling
    help="Chapter name is required",
    location="json",
)
add_chapter_parser.add_argument(
    "description",
    type=str,
    required=False,  # Changed to False for better error handling
    help="Chapter description is required",
    location="json",
)
add_chapter_parser.add_argument(
    "subject_id",
    type=int,
    required=True,
    help="Subject ID is required",
    location="json",
)


add_quiz_parser = reqparse.RequestParser()
add_quiz_parser.add_argument(
    "title",
    type=str,
    required=True,
    help="Quiz title is required",
    location="json",
)
add_quiz_parser.add_argument(
    "timeduration",
    type=int,
    required=True,
    help="Time duration is required",
    location="json",
)
add_quiz_parser.add_argument(
    "remarks",
    type=str,
    required=False,
    help="Remarks are optional",
    location="json",
)
add_quiz_parser.add_argument(
    "chapter_id",
    type=int,
    required=True,
    help="Chapter ID is required",
    location="json",
)
add_quiz_parser.add_argument(
    "subject_id",
    type=int,
    required=True,
    help="Subject ID is required",
    location="json",
)
add_quiz_parser.add_argument(
    "date",
    type=str,
    required=True,
    help="Date is required",
    location="json",
)
