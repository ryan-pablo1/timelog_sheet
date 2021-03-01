from flask import Response, request, render_template, make_response, redirect, url_for, jsonify, flash
from flask_restful import Resource, Api
from flask_login import LoginManager
from flask_jwt_extended import get_jwt,create_access_token, create_refresh_token, jwt_required, get_jwt_identity, set_access_cookies, set_refresh_cookies, unset_jwt_cookies

from sqlalchemy.exc import SQLAlchemyError
import datetime


#importing local classes
from models.users import Users
from database import Database as DB
# from app import mysql

#initializing the loginmanager, then adding the flask_app into the method.
# login_manager = LoginManager()



class RegisterApi(Resource):
    '''
    Flask-RESTful resource for creating a new user.

    :Example:

    >>> from flask import Flask
    >>> from flask-restful import Api
    >>> from app import default_config

    #Create flask app, config, and restful api, then add Register route
    >>> app = Flask(__name__)
    >>> app.config.update(default_config)
    >>> api = Api(app=app)
    >>> api.add_resource(Register, 'authentication/register')

    '''
    @jwt_required(optional=True)
    def get(self) -> Response:
        '''
        GET response method for requesting a register form for creating a user

        :return: HTML

        '''
        identity = get_jwt_identity()
        if identity == None:
            return make_response(render_template('register.html'))
        else:
            DB().read_user_table()
            return make_response(render_template('register.html', identity=identity))


    @staticmethod
    def post() -> Response:
        '''
        POST response method for creating user.

        :return: redirect_for html
        '''

        #collecting the form inputs
        username = request.form.get('username_input')
        email = request.form.get('email_input')
        password = request.form.get('password_input')

        #Exception handling for any sql errors
        try:
            u = Users(username=username, email=email)
            u.set_password_hash(password=password)
            DB().db_session.add(u)
            DB().db_session.commit()
            flash('Account registration successful.')
            return redirect(url_for('indexapi'))

        except SQLAlchemyError as e:
            code = int(str((e.__dict__['orig']))[1:5])
            print(str((e.__dict__['orig'])))

            #Duplicate email insert
            if code == 1062:
                flash('Sorry, but a user has already registered with the provided email.  Please enter a different email.')
                return make_response(render_template('register.html'))
            else:
                error = str(e.__dict__['orig'])
                return error


class LoginApi(Resource):
    '''
    Flask-RESTful resource for creating a new user.

    :Example:

    >>> from flask import Flask
    >>> from flask-restful import Api
    >>> from app import default_config

    #Create flask app, config, and restful api, then add Register route
    >>> app = Flask(__name__)
    >>> app.config.update(default_config)
    >>> api = Api(app=app)
    >>> api.add_resource(Register, 'authentication/login')

    '''
    @jwt_required(optional=True)
    def get(self) -> Response:
        '''
        GET response method for requesting a register form for creating a user

        :return: HTML

        '''

        #If get_jwt_identity() returns none, then can continue with login, otherwise redirect to index.html
        identity = get_jwt_identity()
        if identity == None:
            return make_response(render_template('login.html'))
        else:
            flash(f'You are already logged in as: {identity}')
            return make_response(redirect(url_for('indexapi')))

    @jwt_required(optional=True)
    def post(self) -> Response:
        '''
        POST response method for creating user.

        :return: redirect to index.html
        '''

        current_user = get_jwt_identity()
        print(current_user)

        if current_user == None:

            #collect inputs from login.html
            username = request.form.get('username_input')
            password = request.form.get('password_input')

            try:
                #create db query from users and filter by the username, creating a Users class object from the query results as arguments
                user = DB().db_session.query(Users).filter_by(username=username).first()

                #if the query does not return anything, then the client will go back to the login form
                if user == None:
                    flash('Sorry, incorrect username and/or password. Please try again')
                    return make_response(render_template('login.html'))

                else:
                    #Creating a User object with the successful query result
                    u = Users(username=user.username, password_hashed=user.password_hashed)

                    #verifying if the password provided is valid or not.  check_hashed_password returns boolean
                    if u.check_hashed_password(password):

                        #creating the access and refresh token, with expiration for the tokens
                        expire_time = datetime.timedelta(seconds=600)
                        access_token = create_access_token(identity=str(u.username), expires_delta=(expire_time))
                        refresh_token = create_refresh_token(identity=str(u.username))

                        #creating the response
                        response_ = make_response(redirect(url_for('indexapi')))

                        #Setting the access and refresh cookies to the appropriate response
                        set_access_cookies(response_, access_token)
                        set_refresh_cookies(response_, refresh_token)

                        #Flash message indicating that the login was successful.
                        flash(f'Login Successful! Welcome {u.username}!')

                        return response_

                    #If the password provided is incorrect
                    else:
                        flash('Sorry, incorrect username and/or password, please try again.')
                        return make_response(render_template('login.html'))
            #Catch exceptions and specifying the error
            except SQLAlchemyError as e:
                code = int(str((e.__dict__['orig']))[1:5])
                print(str((e.__dict__['orig'])))

                #occurs when server is not active
                if code == 2002:
                    flash('Sorry, but there seems to be a problem with the server, please try again later.')
                    print(code)
                    return make_response(render_template('login.html'))
                else:
                    error = str(e.__dict__['orig'])
                    return error
        else:
            flash('Sorry, you have already logged in')
            return make_response(render_template('index.html'))

class LogoutApi(Resource):
    '''
    Flask-restful resource for logging out user.

    :Example:

    >>> from flask import Flask
    >>> from flask-restful import Api
    >>> from app import default_config

    #Create flask app, config, and restful api, then add LogoutApi route
    >>> app = Flask(__name__)
    >>> app.config.update(default_config)
    >>> api = Api(app=app)
    >>> api.add_resource(LogoutApi, 'authentication/login')
    '''

    @jwt_required(optional=True)
    def get(self) -> Response:
        #getting jwt identity, if it exists
        identity = get_jwt_identity()

        #If there is no JWT token, then the client has not logged in
        if identity == None:
            flash('You are currently not logged in')
            return make_response(redirect(url_for('indexapi')))

        #If there is a jwt token present, then we will clear the cookies.
        else:
            #creating the Response
            flash('You have successfully logged out.')
            resp = make_response(redirect(url_for('indexapi')), 302)

            #This method will clear the access and refresh token jwt cookies
            unset_jwt_cookies(resp)
            return resp

