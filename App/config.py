import os
from .custom_config import *
from datetime import timedelta

# must be updated to inlude addtional secrets/ api keys & use a gitignored custom-config file instad
def load_config():
    config = {'ENV': os.environ.get('ENV', 'DEVELOPMENT')}
    delta = 7
    if config['ENV'] == "DEVELOPMENT":
        delta = JWT_EXPIRATION_DELTA
        config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
        config['SECRET_KEY'] = SECRET_KEY
        config['RAWG_TOKEN'] = RAWG_TOKEN
    else:
        config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
        config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
        config['RAWG_KEY'] = os.environ.get('RAWG_TOKEN')
        config['DEBUG'] = config['ENV'].upper() != 'PRODUCTION'
        delta = int(os.environ.get('JWT_EXPIRATION_DELTA', 7))
    config['JWT_EXPIRATION_DELTA'] = timedelta(days=int(delta))
    return config

config = load_config()