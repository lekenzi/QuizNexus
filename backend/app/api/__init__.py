from flask_caching import Cache
from flask_restful import Api

api = Api()
cache = Cache()


# add all the resources and routes here for the API

from app.api.resource import TestResource

api.add_resource(TestResource, "/test", endpoint="test")
