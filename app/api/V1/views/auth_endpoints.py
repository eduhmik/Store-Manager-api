from flask import Flask, request, jsonify, Blueprint, json, make_response
from flask_restplus import Resource, reqparse, Api, Namespace, fields
from ..models.user_model import User


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
<<<<<<< HEAD
            current_user = User.get_single_user(email)
=======
            current_user = User.get_single_user(self, email)
>>>>>>> develop
            if current_user == 'not found':
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
    def post(self):
        args = parser.parse_args()
        username = args['username']
        email = args['email']
        phone = args['phone']
        role = args['role']
        password = args['password']
        
        found_email = User.get_single_user(self, email)
        if found_email == 'not found':

            try:    
                new_user = User(email, User.generate_hash(password), username, role, phone)
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

"""fetch all users""" 
@ns.route('')  
class AllUsers(Resource):
    @ns.doc(security='apikey')
    def get(self):
        users_list = User.get_all_users(self)
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
        pass

