from models.timelogs import timelogs
from models.users import Users

from database import Database as DB
from sqlalchemy.sql.expression import func
from flask import Response, render_template, make_response, request, jsonify
from flask_restful import Resource, Api
from sqlalchemy.exc import SQLAlchemyError

import datetime as dt
import json





class debug_db(Resource):
    '''
    def get(self) -> Response:
        current_user = 59

        resp = make_response(render_template('clock.html', identity=current_user, active=False))

        return resp

    def post(self) -> Response:
        if request.form.get('Clock_In'):
            # clock_in
            try:
                #stamps the time and collects current user
                time_stamp = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                current_user = DB().db_session.query(Users).filter_by(username='user1').first()

                #creates a timelog object, adds, and commits to the server
                time_in = timelogs(user_id=current_user.user_id, time_start=time_stamp)
                DB().db_session.add(time_in)
                DB().db_session.commit()

                print('check')

                #grabs the most recent time_id where user_id is the current user
                recent_time_id = DB().db_session.query(func.max(timelogs.time_id)).filter_by(user_id=current_user.user_id).first()
                current_user = DB().db_session.query(Users).filter_by(username='user1').first()
                active_data = {
                    'active': True,
                    'time_id': recent_time_id
                }

                #converts the dict to json
                active_json = json.dumps(active_data)
                print(active_json)
                print(current_user.active)

                #update the data in the active column from the query "current_user"
                current_user.active = active_json
                DB().db_session.commit()

                print(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

                return make_response(render_template('clock.html', identity=current_user.username, active=active_data['active']))
            except SQLAlchemyError as e:
                return e.__dict__['orig']
        if request.form.get('Clock_Out'):
            #clock_out
            try:
                #current user and timestamp, and active time id from user
                time_stamp = dt.datetime.now()
                current_user = DB().db_session.query(Users).filter_by(username='user1').first()
                active_column = current_user.active

                #converts json to dict
                x = json.loads(active_column)

                #prints the contents of the active column: 'time_id'
                print(x['time_id'][0])
                print(type(x['time_id'][0]))

                #grabs the time id, then grabs the time start from the active time session
                active_time_id = x['time_id'][0]
                active_time_shift = DB().db_session.query(timelogs).filter_by(time_id=active_time_id).first()

                #printing data and types
                print(active_time_shift.time_start)
                print(type(active_time_shift.time_start))
                print(type(time_stamp))

                #Calculating the delta from the timestamp and previous clock in
                delta_ = time_stamp - active_time_shift.time_start
                round_num = round((delta_.seconds)/3600, 4)

                # printing the time in hours
                print((delta_.seconds)/3600)
                print(round_num)

                #update the data for the active_time_id
                active_time_shift.time_stop = time_stamp
                active_time_shift.hours_shift = round_num
                DB().db_session.commit()

                #set the user active to False, and none for the time_id
                x['active'] = False
                x['time_id'] = None

                not_active = json.dumps(x)
                current_user.active = not_active
                DB().db_session.commit()

                return make_response('success')

            except SQLAlchemyError as e:
                return e.__dict__['orig']

        '''

    def get(self):
        Users.__table__.create(bind=DB().engine, checkfirst=True)