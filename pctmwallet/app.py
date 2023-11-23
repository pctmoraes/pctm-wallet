import os
from flask import Flask
from dotenv import load_dotenv
from pymongo import MongoClient

# from routes import pages
from pctmwallet.routes import pages

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.register_blueprint(pages)

    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

    app.config['MONGODB_URI'] = os.environ.get('MONGODB_URI')
    client = MongoClient(app.config['MONGODB_URI'])
    app.db = client.pctmwallet


    return app
