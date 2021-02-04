from flask_restful import Api


from api.authentication import RegisterApi, LoginApi, LogoutApi
from api.index import IndexApi
from api.clock import ClockApi
from debug_db import debug_db
from api.profile import ProfileApi


#routes for api
def create_routes(api):
    '''
    Adds resources to the api.

    :param api: Flask-RESTful Api Object

    :Example:

        api.add_resource(index, '/', '/index')
        api.add_resource(login, '/login')
        api.add_resource(register, '/register')
    '''

    api.add_resource(RegisterApi, '/authentication/register')
    api.add_resource(LoginApi, '/authentication/login')
    api.add_resource(LogoutApi, '/authentication/logout')
    api.add_resource(IndexApi, '/')
    api.add_resource(ClockApi, '/clock')
    api.add_resource(debug_db, '/test')
    api.add_resource(ProfileApi, '/profile')