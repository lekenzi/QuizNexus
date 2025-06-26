from flask_restful import reqparse

testparser = reqparse.RequestParser()

testparser.add_argument(
    "test",
    type=str,
    required=True,
    help="Test is required",
    location="json",
)
