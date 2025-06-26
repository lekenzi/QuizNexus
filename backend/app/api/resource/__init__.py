from flask_restful import Resource

from app.api.validators import testparser


class TestResource(Resource):
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
