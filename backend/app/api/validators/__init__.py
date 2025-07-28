from flask_restx import reqparse

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
    help="Access token in request body",
    location="json",
)
checkTokenParser.add_argument(
    "Authorization",
    type=str,
    required=False,
    help="Bearer token in Authorization header",
    location="headers",
)

add_subject_parser = reqparse.RequestParser()
add_subject_parser.add_argument(
    "name",
    type=str,
    required=True,
    help="Subject name is required",
    location="json",
)
add_subject_parser.add_argument(
    "description",
    type=str,
    required=True,
    help="Subject description is required",
    location="json",
)


add_chapter_parser = reqparse.RequestParser()
add_chapter_parser.add_argument(
    "name",
    type=str,
    required=True,
    help="Chapter name is required",
    location="json",
)
add_chapter_parser.add_argument(
    "description",
    type=str,
    required=True,
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
    "time_of_day",
    type=str,
    required=True,
    help="Time of day is optional, default is current time",
    location="json",
)
add_quiz_parser.add_argument(
    "remarks",
    type=str,
    required=True,
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


questions_add_parser = reqparse.RequestParser()
questions_add_parser.add_argument(
    "question",
    type=str,
    required=True,
    help="Question is required",
    location="json",
)
questions_add_parser.add_argument(
    "option1",
    type=str,
    required=True,
    help="Option 1 is required",
    location="json",
)
questions_add_parser.add_argument(
    "option2",
    type=str,
    required=True,
    help="Option 2 is required",
    location="json",
)
questions_add_parser.add_argument(
    "option3",
    type=str,
    required=True,
    help="Option 3 is required",
    location="json",
)
questions_add_parser.add_argument(
    "option4",
    type=str,
    required=True,
    help="Option 4 is required",
    location="json",
)
questions_add_parser.add_argument(
    "answer",
    type=str,
    required=True,
    help="Answer is required",
    location="json",
)
questions_add_parser.add_argument(
    "marks",
    type=int,
    required=True,
    help="Marks are optional, default is 1",
    location="json",
)
questions_add_parser.add_argument(
    "quiz_id",
    type=int,
    required=True,
    help="Quiz ID is required",
    location="json",
)
questions_add_parser.add_argument(
    "chapter_id",
    type=int,
    required=True,
    help="Chapter ID is required",
    location="json",
)
questions_add_parser.add_argument(
    "subject_id",
    type=int,
    required=True,
    help="Subject ID is required",
    location="json",
)


take_response_parser = reqparse.RequestParser()
take_response_parser.add_argument(
    "quiz_id",
    type=int,
    required=True,
    help="Quiz ID is required",
    location="json",
)

take_response_parser.add_argument(
    "question_id",
    type=int,
    required=True,
    help="Question ID is required",
    location="json",
)
take_response_parser.add_argument(
    "user_id",
    type=int,
    required=True,
    help="User ID is required",
    location="json",
)
take_response_parser.add_argument(
    "selected_option",
    type=str,
    required=True,
    help="Selected option is required",
    location="json",
)
