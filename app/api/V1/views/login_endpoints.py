from flask import Flask, request, jsonify, Blueprint, json, make_response
from flask_restplus import Resource, reqparse, Api, Namespace
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from ..models.user_model import User

api = Namespace('login_endpoints', description='Login endpoints for the user model')

parser = reqparse.RequestParser()
parser.add_argument('email')
parser.add_argument('password')

"""user login"""
@api.route('')
class UserLogin(Resource):
    def post(self):
        args = parser.parse_args()
        email = args['email']
        
        current_user = User.find_by_email(self, email)

        if not current_user:
            return make_response(jsonify({
                'message' : 'Email doesn\'t exists'
            }))

        if args['password'] == current_user.password:    
            access_token = create_access_token(identity = args['username'])
            refresh_token = create_refresh_token(identity = args['username'])
            return make_response(jsonify({
                'message' : 'Logged in successfully',
                'access_token': access_token,
                'refresh_token': refresh_token
            }))

        else:

            return make_response(jsonify({
                'message' : 'Incorrect email or password'
            }))
