import time

from flask_restful import Resource
from flask_restful.reqparse import RequestParser
import logging

from simplecrypto import decrypt

from Functions.functions import es_logging
from Model.User import User
from base import session_factory
import arrow

# from Functions.functions import id
from main import es

logger = logging.getLogger(__name__)

formatter = logging.Formatter('{"time": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}')

file_handler = logging.FileHandler('Logs/backend_logs')
file_handler.setFormatter(formatter)
logger.setLevel(logging.CRITICAL)
logger.addHandler(file_handler)

# logging.basicConfig(filename='Logs/backend_logs',level=logging.CRITICAL)
logging.info("Creating handler")
root = logging.getLogger()
hdlr = root.handlers[0]
# json_format = logging.Formatter('{"time": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}')
hdlr.setFormatter(formatter)


id = 0

class LoginUser(Resource):
    def post(self):

        global id
        id = id + 1
        service_name = 'login_backend_service'

        parser = RequestParser()
        parser.add_argument('username', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        args = parser.parse_args()

        username = args['username']

        session = session_factory()
        user = session.query(User).filter_by(username=username).first()
        password = args['password']

        if user != None:

            decrypted_password = decrypt(user.password,'secret key').decode("utf-8")

            if  password == decrypted_password:
                message = f'user_logged_in'
                es_logging(message, service_name, id)

                logger.critical(f'{service_name}_logs-{arrow.now().format("YYYY-MM-DD")}:user_logged_in')
                return {'msg': 'user logged in', 'status_code':200}, 200 # success
            else:
                message = f'Invalid Cred'
                es_logging(message, service_name, id)

                logger.critical(f'{service_name}_logs-{arrow.now().format("YYYY-MM-DD")}:Invalid Cred')
                return {'msg': 'Invalid Cred', 'status_code': 401}, 401
        else:
            es_logging('user_not_registered', service_name, id)

            logger.critical(f'{service_name}_logs-{arrow.now().format("YYYY-MM-DD")}:user_not_registered')
            return {'msg': 'user not registered', 'status_code':401}, 401 # unauthorized