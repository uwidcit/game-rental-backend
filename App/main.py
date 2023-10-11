import os
import logging
from flask import Flask
from flask_login import LoginManager, current_user
from flask_uploads import DOCUMENTS, IMAGES, TEXT, UploadSet, configure_uploads
from flask_cors import CORS
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
from datetime import timedelta

from App.config import config
from App.database import init_db, db

from App.controllers import (
    setup_jwt
)

from App.views import app_views

def add_views(app):
    for view in app_views:
        app.register_blueprint(view)

def configure_app(app, config):
    for key, value in config.items():
        app.config[key] = config[key]

def create_app(config_overrides={}):
    app = Flask(__name__, static_url_path='/static')
    CORS(app)
    configure_app(app, config)
    configure_app(app, config_overrides)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['PREFERRED_URL_SCHEME'] = 'https'
    app.config['UPLOADED_PHOTOS_DEST'] = "App/uploads"
    photos = UploadSet('photos', TEXT + DOCUMENTS + IMAGES)
    logging.basicConfig(level=logging.DEBUG)
    configure_uploads(app, photos)
    add_views(app)
    init_db(app)
    setup_jwt(app)

    app.app_context().push()
    return app