import jwt
from app.instance.config import secret_key
from functools import wraps
from app.api.V1.models.user_model import User
from flask import request, jsonify, make_response

def admin_required(f):
    @wraps(f)
    @classmethod
    def decorated(*args, **kwargs):
        auth_token = None
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
                
            if auth_token:
                
                if identity['role'] == 'attendant':
                    return make_response(jsonify({
                        'status': 'failed',
                        'message': 'You are not an admin'
                    }), 401)
        return f(*args, **kwargs)
    return decorated


def token_required(j):
    @wraps(j)
    @classmethod
    def decorated_token(*args, **kwargs):
        auth_token = None
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
        return j(*args, **kwargs)
    return decorated_token