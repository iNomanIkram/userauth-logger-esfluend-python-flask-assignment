from Services.AuthenticationService import app

def create_app():
    app.run(host='0.0.0.0',port=5000)
    return app

if __name__ == '__main__':
    create_app()