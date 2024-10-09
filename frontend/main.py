from flask import Flask, render_template, request
import requests
import logging
import arrow
from flask import Flask
from elasticsearch import Elasticsearch

from Functions.functions import es_logging, set_logger

id = 0
es = Elasticsearch(HOST='http://elasticsearch',PORT=9200)

try:
    es.indices.create(index="frontend_logs")
except:
    print('index: logs, already exists ')

# since logging default level is warning we just changed it to DEBUG
logger = logging.getLogger(__name__)
formatter = logging.Formatter('{"time": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}')

# file_handler = logging.FileHandler('Logs/frontend_logs')
# file_handler.setFormatter(formatter)
# logger.setLevel(logging.CRITICAL)
# logger.addHandler(file_handler)
# # logging.basicConfig(filename='Logs/backend_logs',level=logging.CRITICAL)
# logging.info("Creating handler")
# root = logging.getLogger()
# hdlr = root.handlers[0]
# # json_format = logging.Formatter('{"time": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}')
# hdlr.setFormatter(formatter)

set_logger()

app = Flask(__name__)

@app.route('/')
def home():
 # logging.warning(f'{service_name}_logs:{arrow.now().format("YYYY-MM-DD")}:user_created')
 return render_template('index.html')

@app.route('/form_login',methods=['POST'])
def login():
    global  id
    id = id + 1

    service_name = 'login_frontend_service_call_logs:'
    username = request.form['username']
    password = request.form['password']

    print(username,password)

    if username == "" or password == "":
        message = f'{service_name}_logs:{arrow.now().format("YYYY-MM-DD")}:failed_cannot_be_empty'
        doc = {'time': f'{arrow.now()}', "message": f'{message}'}
        es.index(index="logs", body=doc, id=id)


        logger.critical(f'{service_name}_logs:{arrow.now().format("YYYY-MM-DD")}:failed_cannot_be_empty')
        return render_template('index.html', info=f'username or password field can not be empty')

    r = requests.post("http://backend:5000/user/login", params={'username': username, f'password': f'{password}'})

    if r.status_code == 200:
        message = f'{service_name}_logs:{arrow.now().format("YYYY-MM-DD")}:valid_user'
        doc = {'time': f'{arrow.now()}', "message": f'{message}'}
        es.index(index="logs", body=doc, id=id)


        logger.critical(f'{service_name}_logs:{arrow.now().format("YYYY-MM-DD")}:valid_user')
        return render_template('index.html', info=f'Valid User')
    elif r.status_code == 401:
        message = f'{service_name}_logs:{arrow.now().format("YYYY-MM-DD")}:Invalid Cred'
        doc = {'time': f'{arrow.now()}', "message": f'{message}'}
        es.index(index="logs", body=doc, id=id)

        logger.critical(f'{service_name}_logs:{arrow.now().format("YYYY-MM-DD")}:Invalid Cred')
        return render_template('index.html', info=f'Invalid Cred')
    else:
        message = f'{service_name}_logs:{arrow.now().format("YYYY-MM-DD")}:failure'
        doc = {'time': f'{arrow.now()}', "message": f'{message}'}
        es.index(index="logs", body=doc, id=id)

        logger.critical(f'{service_name}_logs:{arrow.now().format("YYYY-MM-DD")}:failure')
        return render_template('index.html', info=f'Failure')

@app.route('/form_register',methods=['POST'])
def register():
    global id
    id = id + 1

    service_name = 'register_frontend_service_call_logs'

    username = request.form['rusername']
    password = request.form['rpassword']
    confirm_password = request.form['rconfirm_password']

    # confirming if username and password field
    if username == "" or password == "":

        es_logging('valid_user', service_name, id)

        logger.critical(f'{service_name}_logs-{arrow.now().format("YYYY-MM-DD")}:field_cannot_be_empty')
        return render_template('index.html', rinfo=f'username or password field can not be empty')
    if password != confirm_password:
        es_logging('password_not_same', service_name, id)

        logger.critical(f'{service_name}_logs-{arrow.now().format("YYYY-MM-DD")}:password_not_same')
        return render_template('index.html', rinfo=f'password and confirm password not same')

    r = requests.post("http://backend:5000/user/register", params={'username': username, f'password': f'{password}'})

    if r.status_code == 200:
        es_logging('registration_success', service_name, id)

        logger.critical(f'{service_name}_logs-{arrow.now().format("YYYY-MM-DD")}:registration_success')
        return render_template('index.html', rinfo=f'Registration Successful')
    elif r.status_code == 401:
        es_logging('already_exists', service_name, id)

        logger.critical(f'{service_name}_logs-{arrow.now().format("YYYY-MM-DD")}:already_exists')
        return render_template('index.html', rinfo=f'Already exists')
    else:
        es_logging('failure', service_name, id)

        logger.critical(f'{service_name}_logs-{arrow.now().format("YYYY-MM-DD")}:failure')
        return render_template('index.html', rinfo=f'failure')

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8000)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
