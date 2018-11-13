from flask import Flask, request, jsonify, Blueprint, json, make_response
from flask_restplus import Resource, reqparse, Api, Namespace, fields
from ..models.user_model import User
from ..models.revoke_token_model import RevokedTokenModel
from app.api.V2.utils.validator import Password, Email, Verify
from app.api.V2.utils.auth import admin_required
import re


api = Namespace('Register Endpoint', description='A collection of register endpoints for the user model')
ns = Namespace('Users Endpoints', description='Users endpoints to fetch all users and delete them')
ns2 = Namespace('Login_endpoint', description='Login endpoints for the user model')
ns3 = Namespace('Logout Endpoint', description='An endpoint to logout')

parser = reqparse.RequestParser()
parser.add_argument('username', help = 'This field cannot be blank')
parser.add_argument('email', help = 'This field cannot be blank', required = True)
parser.add_argument('phone', help = 'This field cannot be blank')
parser.add_argument('role', help = 'This field cannot be blank')
parser.add_argument('password', help = 'This field cannot be blank', required = True)

login_fields = api.model('Login', {
    'email': fields.String,
    'password': fields.String
})

"""user login"""
@ns2.route('')
class UserLogin(Resource):
    @ns2.expect(login_fields, validate=True)
    def post(self):
        args = parser.parse_args()
        email = args['email']
        password = args['password']

        match = re.match(
            r'^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)
        if not match:
            return {"message": "Enter a valid email address"}
        payload = [email, password]
        if payload is False:
            return {'message':'Payload is invalid'},406
        elif Verify.is_empty(self, payload) is True:
            return {'message':'Required field is empty'},406
        elif Verify.is_whitespace(self, payload) is True:
            return {'message':'Required field contains only white spaces'},406
                
        try:
            current_user = User.get_single_user(email)
            if current_user == {"message": "There are no records found"}:
                return make_response(jsonify({
                    'status': 'success',
                    'message': 'User does not exist, sign up!'
                }), 200)
            if current_user and User.verify_hash(password, current_user['password']):
                role = current_user['role']
                email = current_user['email']
                auth_token = User.encode_auth_token(email, role)   
                if auth_token:
                    return make_response(jsonify({
                        'status' : 'ok',
                        'message' : 'Logged in successfully',
                        'auth_token': auth_token.decode()
                    }), 200) 

            else:

                return make_response(jsonify({
                    'message' : 'Incorrect email or password',
                    'status' : 'fail'
                }), 400)

        except Exception as e:
            return make_response(jsonify({
                'message' : str(e),
                'status' : 'failed'
            }), 500)


registration_fields = api.model('Registration', {
    'username' : fields.String,
    'email': fields.String,
    'phone' : fields.String,
    'role': fields.String,
    'password': fields.String
})
"""user registration"""
@api.route('')
class UserRegistration(Resource):
    @api.expect(registration_fields, validate=True)
    @admin_required
    def post(self):
        args = parser.parse_args()
        username = args['username']
        email = args['email']
        phone = args['phone']
        role = args['role']
        password = args['password']

        roles = ['admin', 'attendant']
        match = re.match(
            r'^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)
        if not match:
            return {"message": "Enter a valid email address"}
        if role not in roles:
            return make_response(jsonify({
                'message': 'The role can only be an admin or attendant.'
            }))
        
        if Password(password).is_valid(password) == 'invalid':
            return {'message':'Password should be atleast 6 characters and \
contains [A-Z],[a-z],[0-9] and either [$, #, @, *, &, !, %]'}

        payload= [username, email, phone, role, password]

        existing_email = User.get_single_user(email)
        existing_username = User.get_user_by_username(username)

        if payload is False:
            return {'message':'Payload is invalid'},406
        elif Verify.is_empty(self, payload) is True:
            return {'message':'Required field is empty'},406
        elif Verify.is_whitespace(self, payload) is True:
            return {'message':'Required field contains only white spaces'},406

        if existing_username == {"message": "There are no records found"}:
        
            if existing_email == {"message": "There are no records found"}:

                try:

                    new_user = User(username, email, phone, role, User.generate_hash(password))
                    created_user = new_user.create_user()
                    return make_response(jsonify({
                        'status': 'ok',
                        'message': 'User created successfully',
                        'users': created_user
                    }), 201)
                            
                    
                except Exception as e:
                    return make_response(jsonify({
                        'message' : str(e),
                        'status' : 'failed'
                    }), 500)
            return make_response(jsonify({
                                'status': 'fail',
                                'message' : 'Email already exists, please log in'
                            }))
        return {'message':'Username already exists'},406
            
"""fetch all users""" 
@ns.route('')  
class AllUsers(Resource):
    @ns.doc(security='apikey')
    def get(self):
        users_list = User.get_all_users()
        return make_response(jsonify({
            'message':  'Get all users successful',
            'status': 'ok',
            'users': users_list
        }), 200)


"""user logout"""  
@ns3.route('') 
class UserLogoutAccess(Resource):
    @ns3.doc(security='apikey')  
    def post(self):
        auth_token = None
        authentication_header = request.headers.get('Authorization')
        if authentication_header:    
            auth_token = authentication_header.split(" ")[1]

            identity = User.decode_auth_token(auth_token)

            if identity == 'Invalid token. Please log in again.':
                    return make_response(jsonify({
                        'status': 'failed',
                        'message': 'Invalid token. Please log in again.'
                    }), 401)

            revoked = RevokedTokenModel.is_token_blacklisted(auth_token)
            if revoked:
                return make_response(jsonify({
                        'message': 'You are logged out. Please log in again.'
                    }), 401)
            try:
                if auth_token:
                    revoked_token = RevokedTokenModel(auth_token = auth_token)
                    revoked_token.add()
                    return make_response(jsonify({
                        'message': 'Authentication token has been revoked'
                }))
            except:
                return make_response(jsonify({
                'message': 'Something unexpected happened'
            }), 500)
        else:
            return make_response(jsonify({
                'status': 'failed',
                'message': 'You are not authorized'
            }), 401)
