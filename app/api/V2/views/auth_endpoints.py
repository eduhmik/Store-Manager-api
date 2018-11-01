from flask import Flask, request, jsonify, Blueprint, json, make_response
from flask_restplus import Resource, reqparse, Api, Namespace, fields
from ..models.user_model import User
from ..models.revoke_token_model import RevokedTokenModel
from app.api.V2.utils.validator import Password, Email
from app.api.V2.utils.auth import admin_required


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
    @ns2.expect(login_fields)
    def post(self):
        args = parser.parse_args()
        email = args['email']
        password = args['password']
                
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


"""user regitration"""
@api.route('')
class UserRegistration(Resource):
    @api.expect(registration_fields)
    @admin_required
    def post(self):
        args = parser.parse_args()
        username = args['username']
        email = args['email']
        phone = args['phone']
        role = args['role']
        password = args['password']

        roles = ['admin', 'attendant']
        if role not in roles:
            return make_response(jsonify({
                'message': 'The role can only be an admin or attendant.'
            }))

        existing_user = User.get_single_user(email)
        if existing_user == {"message": "There are no records found"}:
            
            try:
                if Password.check_is_valid(self, password):
                    if Email.is_valid_email(self, email):
                        new_user = User(username, email, phone, role, User.generate_hash(password))
                        created_user = new_user.create_user()
                        return make_response(jsonify({
                            'status': 'ok',
                            'message': 'User created successfully',
                            'users': created_user
                        }), 201)
                    return make_response(jsonify({
                        'message': 'Enter a valid email address'
                    }))
                return make_response(jsonify({
                    'message': ['The password you entered is invalid password should contain',
                            {'a lowercase character':'an uppercase character', 
                            'a digit': 'a special character e.g $@*', 
                            'length':'length not less than 6 or above 13'
                            }
                    ]
                }))
            
            except Exception as e:
                return make_response(jsonify({
                'message' : str(e),
                'status' : 'failed'
            }), 500)
        
        return make_response(jsonify({
                        'status': 'fail',
                        'message' : 'Email already exists, please log in'
                    }))

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
        authentication_header = request.headers.get('Authorization')
        if authentication_header:    
            try:
                auth_token = authentication_header.split(" ")[1]
                    
                identity = User.decode_auth_token(auth_token)
                
                if identity == 'Invalid token. Please log in again.':
                    return make_response(jsonify({
                        'status': 'failed',
                        'message': 'Invalid token. Please log in again.'
                    }), 401)

            except Exception:
                return make_response(jsonify({
                    'status': 'failed',
                    'message': 'You are not authorized'
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

