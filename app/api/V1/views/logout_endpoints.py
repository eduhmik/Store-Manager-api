from flask import Flask, request, jsonify, Blueprint, json, make_response
from flask_restplus import Resource, reqparse, Api, Namespace
from ..models.user_model import User


api = Namespace('logout_access', description='An endpoint to revoke access token')
ns = Namespace('logout_refresh', description='An endpoint to revoke refresh token')
ns2 = Namespace('token refresh', description='An endpoint to refresh token')
"""user logout"""  
@api.route('')   
class UserLogoutAccess(Resource):
    
    def post(self):
        pass