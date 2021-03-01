#import flask and extensions
from flask import flash,Response, request, jsonify, render_template, make_response, session, redirect, url_for
from flask_restful import Resource, Api
from flask_jwt_extended import unset_jwt_cookies,create_refresh_token,set_access_cookies,set_refresh_cookies,create_access_token,get_jwt, get_jwt_identity, jwt_required
from sqlalchemy.sql.expression import func
from sqlalchemy.exc import SQLAlchemyError
import json

#importing local packages
from api.jwt_man import jwt
import datetime as dt
from database import Database as DB
from models.users import Users
from models.timelogs import timelogs



class ClockApi(Resource):
    '''
    Flask-RESTful resource for clockin in work session.

    :Example:
    >>> from flask import Flask
    >>> from flask-restful import Api
    >>> from app import default_config

    #Create flask_app, config, and restful api, then add clockapi route
    >>> app = Flask(__name__)
    >>> app.config.update(default_config)
    >>> api = Api(app=app)
    >>> api.add_resource(ClockApi, '/clock')
    '''
    @jwt_required()
    def get(self) -> Response:
        '''
        GET response method for the clock.html in order to clock in/out

        :return: HTML
        '''

        #collecting the current user identity from the jwt token and query the database for said user
        current_username = get_jwt_identity()
        current_user = DB().db_session.query(Users).filter_by(username=current_username).first()

        #grab the current user active state and convert the json to dict, and also verifies the datatype
        #NOTE: This was necessary for a bug where the default value of "active" column from users had a dict, rather than a json datatype.  This was the workaround.
        try:
            active_json = current_user.active
            active_dict = json.loads(active_json)
            return make_response(render_template('clock.html', identity=current_username, active=active_dict['active']))
        except TypeError:
            return make_response(render_template('clock.html', identity=current_username, active=active_json['active']))

    @jwt_required()
    def post(self) -> Response:
        '''
        POST response method for clocking in/out

        :return: clock.html with variables
        '''
        #If "Clock In" is pressed
        if request.form.get("Clock_In"):
            try:
                #grab the JWT identity for currently signed in user, and the current time stamp for clocking in
                current_username = get_jwt_identity()
                current_user = DB().db_session.query(Users).filter_by(username=current_username).first()
                time_start_stamp = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


                #grab the current user active state and convert the json to dict, and also verifies the datatype
                try:
                    active_json = current_user.active
                    active_dict = json.loads(active_json)
                except TypeError:
                    active_dict = current_user.active

                if active_dict["active"] == False:
                    #Insert a new timelog with a clock in time, and the user_id as a foreign key
                    time_clockin = timelogs(user_id=current_user.user_id, time_start=time_start_stamp)
                    DB().db_session.add(time_clockin)
                    DB().db_session.commit()

                    #grabs the id of the timelog just created
                    current_timelog = DB().db_session.query(func.max(timelogs.time_id)).filter_by(user_id=current_user.user_id).first()


                    #changes the key values, and converts the dict back to json
                    active_dict["active"] = True
                    active_dict["time_id"] = current_timelog
                    active_json = json.dumps(active_dict)

                    #updates the active state of the current user
                    current_user.active = active_json
                    DB().db_session.commit()


                    #response if the template rendered with variables
                    resp = make_response(render_template('clock.html', identity=current_username, active=active_dict['active']))


                    return resp

                #If the user is active and clocked in, it will render the template with a flash message.  This will make sure that you cannot clock in twice, or if the user refreshes the page with the same post
                elif active_dict["active"]==True:
                    flash('Sorry, but you have already have an active clock in for this user.')
                    resp = make_response(render_template('clock.html', identity=current_username, active=active_dict['active']))
                    return resp
            #Exception handling for an SQLError
            except SQLAlchemyError as e:
                return e.__dict__['orig']

        #If 'Clock Out' is pressed
        if request.form.get("Clock_Out"):
            try:
                #setting the timestamp and grabbing the jwt identity, and querying the current user from the database
                time_stop_stamp = dt.datetime.now()
                current_username = get_jwt_identity()
                current_user = DB().db_session.query(Users).filter_by(username=current_username).first()

                #grab the current user active state and convert the json to dict, and verifies the datatype
                try:
                    active_json = current_user.active
                    active_dict = json.loads(active_json)
                except TypeError:
                    active_dict = current_user.active

                #grabbing the active time session id to get it from the database
                if active_dict["active"] == True:
                    current_time_session = DB().db_session.query(timelogs).filter_by(time_id=active_dict['time_id'][0]).first()
                    time_start_stamp = current_time_session.time_start

                    print(type(time_start_stamp))

                    #calculating the timedelta between the clock in and the clock out
                    delta_ = time_stop_stamp - time_start_stamp
                    delta_inhours = delta_.seconds/3600
                    round_num = round(delta_inhours, 4)

                    #update the current time session and calulated hours worked
                    current_time_session.time_stop = time_stop_stamp
                    current_time_session.hours_shift = round_num
                    DB().db_session.commit()

                    #update the active dict data and convert it into json
                    active_dict["active"] = False
                    active_dict["time_id"] = None
                    active_json = json.dumps(active_dict)

                    #setting the object variables then committing them to database
                    current_user.active = active_json
                    DB().db_session.commit()

                    #grabbing the hours_shift column from time logs per user_id, then setting the sum to the user's hours_worked
                    hours_shiff = DB().db_session.query(timelogs.hours_shift).filter_by(user_id=current_user.user_id).all()
                    hours_sum = 0
                    for row in hours_shiff:
                        try:
                            hours_sum += row[0]
                        except TypeError:
                            continue

                    current_user.hours_worked = hours_sum
                    DB().db_session.commit()



                    #creating a flask message and rendering back to the index and unsetting the JWT cookies per response
                    flash(f"Clockout successful, thank you for your time, {current_user.username}")
                    resp = make_response(render_template('index.html'))
                    unset_jwt_cookies(resp)
                    return resp
                #Same is clocked_in condition where it ensures that it won't be done twice
                elif active_dict["active"]==False:
                    flash('Sorry, but you have already clocked out for this user.')
                    resp = make_response(render_template('clock.html', identity=current_username, active=False))
                    return resp
            #SQL exception handling, return code for further debugging
            except SQLAlchemyError as e:
                return e.__dict__['orig']
