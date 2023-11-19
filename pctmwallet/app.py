import secrets
from flask import Flask
from pctmwallet.routes import pages

def create_app():
    app = Flask(__name__)
    app.register_blueprint(pages)

    # the key below was generated with secrets.token_urlsafe()
    app.secret_key = 'fM-IwDXtvsHmppplTmgPZLyXTsEYqlEdtotbAquIiNE'

    return app
