from flask import Flask, request, jsonify, Blueprint, json, make_response
from flask_restplus import Resource, reqparse, Api, Namespace
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt, decode_token)
from ..models.user_model import User
from ..models.revoked_token_model import RevokedTokenModel

api = Namespace('logout_endpoints', description='A collection of endpoints for the user model')
ns = Namespace('logout_refresh', description='An endpoints for the logout/refresh')
ns2 = Namespace('token refresh', description='An endpoints for the token/refresh')
"""user logout"""  
@api.route('')   
class UserLogoutAccess(Resource):
    @jwt_required
    def post(self):
        
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(id, jti = jti)
            revoked_token.add()
            return {'message': 'Access token has been revoked'}
        except:
            return {'message': 'Something went wrong'}

"""user logout refresh"""
@ns.route('')      
class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(id, jti = jti)
            revoked_token.add()
            return {'message': 'Refresh token has been revoked'}
        except:
            return {'message': 'Something went wrong'}
"""token refresh"""  
@ns2.route('')    
class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity = current_user)
        return {'access_token': access_token}
        