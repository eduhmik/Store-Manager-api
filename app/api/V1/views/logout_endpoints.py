from flask import Flask, request, jsonify, Blueprint, json, make_response
from flask_restplus import Resource, reqparse, Api, Namespace
from ..models.user_model import User


api = Namespace('logout', description='An endpoint to logout')

"""user logout"""  
@api.route('')   
class UserLogoutAccess(Resource):
    
    def post(self):
        pass