from flask import Response, jsonify, url_for, redirect, make_response, flash, render_template
from flask_jwt_extended import unset_jwt_cookies,JWTManager, jwt_required, create_access_token, get_jwt, get_jwt_identity

import datetime as dt
from database import Database as DB
from models.users import Users

jwt = JWTManager()


#The following decorators are for managing jwt_errors such as unauthorized headers, and invalid tokens.
@jwt.unauthorized_loader
def unauthorized_callback(callback):
    #no auth header
    flash("Please login before accessing this link..")
    resp = make_response(render_template('index.html'))
    resp.status_code = 401
    return resp


#For invalid or expired tokens
@jwt.expired_token_loader
@jwt.invalid_token_loader
def call_expired_token_loader(expired_token):
    flash("Your session has expired.  Please login to continue.")
    resp = make_response(render_template('index.html'))
    unset_jwt_cookies(resp)

    return resp