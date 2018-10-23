from flask import Flask, request, jsonify, Blueprint, json, make_response
from flask_restplus import Resource, reqparse, Api, Namespace, fields
from ..models.user_model import User

api = Namespace('login_endpoints', description='Login endpoints for the user model')

parser = reqparse.RequestParser()
parser.add_argument('email')
parser.add_argument('password')

"""user login"""
@api.route('')
class UserLogin(Resource):
    login_fields = api.model('Login', {
    'email': fields.String,
    'password': fields.String
})
    @api.doc(body=login_fields)
    def post(self):
        args = parser.parse_args()
        email = args['email']
        password = args['password']
                
        try:
            current_user = User.get_single_user(email)
            if current_user and User.verify_hash(password, current_user['password']): 
                auth_token = User.encode_auth_token(self, email)   
                if auth_token:
                    return make_response(jsonify({
                        'status' : 'Ok',
                        'message' : 'Logged in successfully'
                    }))

                else:

                    return make_response(jsonify({
                        'message' : 'Incorrect email or password'
                    }))

        except Exception as e:
            return make_response(jsonify({
                'message' : str(e),
                'status' : 'failed'
            }), 500)
