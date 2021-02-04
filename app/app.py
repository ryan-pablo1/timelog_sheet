'''
This version of the app is structured for utilizing flask-restful function.
Structure:
    >>> import packages:
        flask, local, and system

    >>> declare default DB config
    >>> define get_flask_app
        1) initializing Flask
        2) updating Flask.config.update
        3) Initializing routes and Api
        4) initializing DB connector
'''


#Flask packages
from flask import Flask, app, redirect, url_for
from flask_restful import Api
from flask_mysqldb import MySQL
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


#system packages
import os

#local packages
# from database import Database
from api.routes import create_routes
from resources.config import DBconfig
from tools.create_key import create_key
from create_db_and_tables import create_db, create_tables


#config
default_config = {}

def get_flask_app(config:dict = DBconfig) -> app.Flask:
    '''
    Initializes Flask app with provided configuration.
    Main entry point for Web Server Gateway Interface(wsgi).
    wsgi is a calling convention for web servers to forward requests to web applications or frameworks written in Python language.

    :param config:  Configuration dictionary
    :result: app
    '''

    #Initialize Flask
    flask_app = Flask(__name__)

    #Configuring app with dictionary argument and updating the flask app config to either default_config or config variable when calling the get_flask_app method
    config = default_config if config is None else config
    flask_app.config.update(config)
    flask_app.config['JWT_TOKEN_LOCATION'] = ['cookies']
    flask_app.config['JWT_COOKIE_SECURE'] = True
    flask_app.config['JWT_ACCESS_COOKIE_PATH'] = '/'
    flask_app.config['JWT_REFRESH_COOKIE_PATH'] = '/'
    flask_app.config['JWT_COOKIE_CSRF_PROTECT'] = False

    #load config variables
    if 'JWT_SECRET_KEY' in os.environ:
        flask_app.config['JWT_SECRET_KEY'] = os.environ['JWT_SECRET_KEY']

    #initialize api and routes
    api= Api(app=flask_app)
    create_routes(api=api)

    #import database class with initialized variables
    from database import Database
    mysql = Database().db
    mysql.init_app(app=flask_app)

    #Initialize the login manager, not utilized
    # from api.authentication import login_manager
    # login_manager.init_app(flask_app)

    #initialize jwt manager
    from api.jwt_man import jwt
    jwt.init_app(app=flask_app)

    create_db()
    create_tables()

    return flask_app


if __name__ == '__main__':
    #Main entry point when runnning in stand-alone mode and debugging purposes
    app = get_flask_app()
    create_key()
    app.secret_key = os.environ['JWT_SECRET_KEY']
    app.run(host="0.0.0.0",debug=True)