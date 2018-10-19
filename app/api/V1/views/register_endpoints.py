from flask import Flask, request, jsonify, Blueprint, json, make_response
from flask_restplus import Resource, reqparse, Api, Namespace
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from ..models.user_model import User
from ..models.revoked_token_model import RevokedTokenModel
api = Namespace('regiser_endpoints', description='A collection of endpoints for the user model; includes get and post endpoints')

parser = reqparse.RequestParser()
parser.add_argument('username', help = 'This field cannot be blank', required = True)
parser.add_argument('email', help = 'This field cannot be blank', required = True)
parser.add_argument('phone', help = 'This field cannot be blank', required = True)
parser.add_argument('role', help = 'This field cannot be blank', required = True)
parser.add_argument('password', help = 'This field cannot be blank', required = True)

"""user regitration"""
@api.route('')
class UserRegistration(Resource):
    def post(self):
        args = parser.parse_args()
        username = args['username']
        email = args['email']
        phone = args['phone']
        role = args['role']
        password = args['password']

        found_email = User.find_by_email(self, email)
        if found_email:
            return make_response(jsonify({
                'message' : 'Email already exists'
            }))

        new_user = User(email, password, username, role, phone)
        created_user = new_user.create_user()
        access_token = create_access_token(identity = args['email'])
        refresh_token = create_refresh_token(identity = args['email'])
        return make_response(jsonify({
            'status': 'ok',
            'message': 'User created successfully',
            'access_token': access_token,
            'refresh_token': refresh_token,
            'sales': created_user
        }), 201)


      

      
"""fetch all users""" 
@api.route('')     
class AllUsers(Resource):
    def get(self):
        users_list = User.get_all_users(self)
        return make_response(jsonify({
            'message':  'Get all users successful',
            'status': 'ok',
            'users': users_list
        }), 200)


    def delete(self):
        empty_list = [User.del_users(self)]
        return make_response(jsonify({
            'message':  'Delete all users successful',
            'status': 'ok',
            'users': empty_list
        }), 200)
"""secret resource""" 
@api.route('')  
class SecretResource(Resource):
    def get(self):
        return {
            'answer': 42
}