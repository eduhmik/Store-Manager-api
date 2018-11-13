import jwt
from app.instance.config import secret_key
from functools import wraps
from app.api.V2.models.user_model import User
from flask import request, jsonify, make_response
from ..models.revoke_token_model import RevokedTokenModel

def admin_required(f):
    @wraps(f)
    @classmethod
    def decorated(*args, **kwargs):
        auth_token = None
        
        authentication_header = request.headers.get('Authorization')
        if authentication_header:    
            
            auth_token = authentication_header.split(" ")[1]

            revoked = RevokedTokenModel.is_token_blacklisted(auth_token)
            if revoked:
                return make_response(jsonify({
                        'message': 'You are logged out. Please log in again.'
                    }), 401)
            try:        
                identity = User.decode_auth_token(auth_token)
                print(identity)
                
                if identity == 'Invalid token. Please log in again.':
                    return make_response(jsonify({
                        'status': 'failed',
                        'message': 'Invalid token. Please log in again.'
                    }), 401)
                
                elif "message" in identity:
                    return identity
                    
                elif identity['role'] != 'admin':
                    return make_response(jsonify({
                        'status': 'failed',
                        'message': 'You are not an admin'
                    }), 401)

            except Exception as e:
                return e
        else:
            return make_response(jsonify({
                'status': 'failed',
                'message': 'You are not authorized'
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
            auth_token = authentication_header.split(" ")[1]

            revoked = RevokedTokenModel.is_token_blacklisted(auth_token)
            if revoked:
                return make_response(jsonify({
                        'message': 'You are logged out. Please log in again.'
                    }), 401)
            try:    
                identity = User.decode_auth_token(auth_token)
                
                if identity == 'Invalid token. Please log in again.':
                    return make_response(jsonify({
                        'status': 'failed',
                        'message': 'Invalid token. Please log in again.'
                    }), 401)

                elif "message" in identity == 'Signature expired. Please log in again.':
                    return identity
            except Exception as e:
                return e
        else:
            return make_response(jsonify({
                'status': 'failed',
                'message': 'You are not authorized'
            }), 401)
        return j(*args, **kwargs)
    return decorated_token