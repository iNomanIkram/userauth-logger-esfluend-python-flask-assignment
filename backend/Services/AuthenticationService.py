from flask_restful import Api
from Resources.Authentication.RegisterResource import RegisterUser
from Resources.Authentication.LoginResource import LoginUser
from main import app

api = Api(app)
api.add_resource(RegisterUser, '/user/register')
api.add_resource(LoginUser, '/user/login')