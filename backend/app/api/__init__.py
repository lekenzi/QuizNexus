from flask_caching import Cache
from flask_restful import Api

api = Api()
cache = Cache()


# add all the resources and routes here for the API

from app.api.resource import (
    HomeResource,
    UserLoginResource,
    UserLogoutResource,
    UserRegisterResource,
)

api.add_resource(UserLoginResource, "/api/login", endpoint="login")
api.add_resource(UserRegisterResource, "/api/register", endpoint="register")
api.add_resource(UserLogoutResource, "/api/logout", endpoint="logout")
api.add_resource(HomeResource, "/api/home", endpoint="home")
