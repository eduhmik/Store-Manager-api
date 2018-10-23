from flask import Flask, request, jsonify, Blueprint, json, make_response
from flask_restplus import Resource, reqparse, Api, Namespace, fields
from ..models.user_model import User


api = Namespace('register_endpoints', description='A collection of register endpoints for the user model')
ns = Namespace('users', description='Users endpoints to fetch all users and delete them')

parser = reqparse.RequestParser()
parser.add_argument('username', help = 'This field cannot be blank', required = True)
parser.add_argument('email', help = 'This field cannot be blank', required = True)
parser.add_argument('phone', help = 'This field cannot be blank', required = True)
parser.add_argument('role', help = 'This field cannot be blank', required = True)
parser.add_argument('password', help = 'This field cannot be blank', required = True)

"""user regitration"""
@api.route('')
class UserRegistration(Resource):
    registration_fields = api.model('Registration', {
    'username' : fields.String,
    'email': fields.String,
    'phone' : fields.String,
    'role': fields.String,
    'password': fields.String
})
    @api.doc(body=registration_fields)
    def post(self):
        args = parser.parse_args()
        username = args['username']
        email = args['email']
        phone = args['phone']
        role = args['role']
        password = args['password']
        
        found_email = User.get_single_user(email)
        if found_email == 'not found':
            try:    
                    new_user = User(email, User.generate_hash(password), username, role, phone)
                    created_user = new_user.create_user()
                    auth_token = User.encode_auth_token(self, email)
                    return make_response(jsonify({
                        'status': 'ok',
                        'message': 'User created successfully',
                        'auth_token': auth_token.decode(),
                        'users': created_user
                    }), 201)
            except Exception as e:
                return make_response(jsonify({
                    'status': 'fail',
                    'message': str(e)
                }))
    
        return make_response(jsonify({
                'status': 'fail',
                'message' : 'Email already exists'
            }))


      

      
"""fetch all users""" 
@ns.route('')   
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

