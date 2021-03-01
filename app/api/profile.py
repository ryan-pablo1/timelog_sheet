#importing flask packages and such
from flask import Response, render_template, make_response, request, jsonify
from flask_restful import Resource, Api
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql.expression import func
import json
from datetime import datetime as dt
from flask_jwt_extended import get_jwt,create_access_token, create_refresh_token, jwt_required, get_jwt_identity, set_access_cookies, set_refresh_cookies, unset_jwt_cookies
import sys

#importing local packages
from database import Database as DB
from models.users import Users
from models.timelogs import timelogs

class ProfileApi(Resource):

    '''
    Flask-RESTful resource for displaying the user's profile information and timelog

    :Example:

    >>> from flask import Flask
    >>> from flask-restful import Api
    >>> from app import default_config

    #Create flask app, config, and restful api, then add Profile route
    >>> app = Flask(__name__)
    >>> app.config.update(default_config)
    >>> api = Api(app=app)
    >>> api.add_resource(ProfileApi, 'profile')
    '''

    @jwt_required
    def get(self) -> Response:
        """
        GET response for displaying user's time log.

        :return: HTML
        """

        #Collects the jwt current user identity, and query's the database for the said user
        current_username = get_jwt_identity()
        current_user = DB().db_session.query(Users).filter_by(username=current_username).first()
        hours_worked = current_user.hours_worked

        #Selects the timelogs based on user_id foreign key
        time_log = DB().db_session.query(timelogs).filter_by(user_id=current_user.user_id).all()

        #list comprehension for each column
        time_log_start = [dt.strftime(row.time_start, "%Y-%m-%d %H:%M:%S") for row in time_log]
        try:
            time_log_stop = [dt.strftime(row.time_stop, "%Y-%m-%d %H:%M:%S") for row in time_log]
        except TypeError:
            pass
        time_log_hours = [row.hours_shift for row in time_log]

        #Decided to only utilized the time_log variable and use flask for iterating the columns on the profile.html. Added the hours_worked variable
        return make_response(render_template('profile.html',identity=current_username, hours_worked=hours_worked, log=time_log))
