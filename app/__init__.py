from flask import Flask
from .instance.config import app_config
from flask_jwt_extended import JWTManager
from app.api.V1.models.revoked_token_model import RevokedTokenModel



def create_app(config):
    '''configuring the flask app'''
    app = Flask(__name__)

    from .api.V1 import version1 as v1
    app.register_blueprint(v1)
   
    app.config.from_object(app_config[config])
    app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']


    jwt = JWTManager(app)

    app.url_map.strict_slashes = False
    app.config['testing'] = True

    return app