
import arrow

from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from simplecrypto import encrypt

from Functions.functions import es_logging
from Model.User import User
from Resources.Authentication.LoginResource import id
from base import session_factory

import logging

# logging.basicConfig(filename='Logs/backend_logs',level=logging.WARNING)
from main import es

class RegisterUser(Resource):
    def post(self):
        service_name = 'registration_backend_service'

        parser = RequestParser()
        parser.add_argument('username', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        args = parser.parse_args()

        username = args['username']

        session = session_factory()
        test = session.query(User).filter_by(username=username).first()

        if test:
            es_logging('user_exists', service_name, id)

            logging.warning(f'{service_name}_logs-{arrow.now().format("YYYY-MM-DD")}:user_exists')
            return { 'msg': 'username already exists', 'status_code':401 } , 401 # unauthorized
        else:
            encrypted_password = encrypt(args['password'], 'secret key')

            user = User(
            username = args['username'],
            password = encrypted_password,
            )
            session.add(user)
            session.commit()
            session.close()

            # message = f'user_created'
            # doc = {'time': f'{arrow.now()}', "message": f'{message}'}
            # es.index(index=f"{service_name}_logs:{arrow.now().format('YYYY-MM-DD')}", body=doc, id=id)

            es_logging('user_created', service_name, id)

            logging.warning(f'{service_name}_logs-{arrow.now().format("YYYY-MM-DD")}:user_created')
            return { 'msg': 'user created', 'status_code':200 } , 200 # success