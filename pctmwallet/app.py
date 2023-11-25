from flask import Flask
from pctmwallet.routes import pages

def create_app():
    app = Flask(__name__)
    app.register_blueprint(pages)

    app.config['SECRET_KEY'] = 'my-secret-key'

    return app
