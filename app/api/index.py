from flask import Response, render_template, make_response, request, url_for, jsonify
from flask_jwt_extended import get_jwt_identity, get_jwt, jwt_required
from flask_restful import Resource, Api

class IndexApi(Resource):
    '''
    Flask-RESTful resource for creating a new user.

    :Example:

    >>> from flask import Flask
    >>> from flask-restful import Api
    >>> from app import default_config

    #Create flask app, config, and restful api, then add IndexApi route
    >>> app = Flask(__name__)
    >>> app.config.update(default_config)
    >>> api = Api(app=app)

    '''
    @jwt_required(optional=True)
    def get(self) -> Response:
        identity = get_jwt_identity()
        # claims = get_jwt_claims()
        return make_response(render_template('index.html', identity=identity))
