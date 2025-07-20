from flask_caching import Cache
from flask_restful import Api

api = Api()
cache = Cache()


# add all the resources and routes here for the API

from app.api.resource import (
    ChapterResources,
    CheckTokenValidResource,
    QuizResources,
    SubjectResources,
    TestPostResource,
    UserLoginResource,
    UserLogoutResource,
    UserRegisterResource,
)

api.add_resource(UserLoginResource, "/api/login", endpoint="login")
api.add_resource(UserRegisterResource, "/api/register", endpoint="register")
api.add_resource(UserLogoutResource, "/api/logout", endpoint="logout")
api.add_resource(SubjectResources, "/api/subjects", endpoint="subjects")
api.add_resource(
    CheckTokenValidResource, "/api/check_token_valid", endpoint="check_token_valid"
)
api.add_resource(TestPostResource, "/api/test", endpoint="test")
api.add_resource(ChapterResources, "/api/chapters", endpoint="chapters")
api.add_resource(QuizResources, "/api/quizzes", endpoint="quizzes")
