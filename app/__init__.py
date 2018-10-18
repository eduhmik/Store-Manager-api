from flask import Flask
from flask_restful import Api
from instance.config import app_config
from .api.V1.views.product_endpoints import product

def create_app(config):
    '''configuring the flask app'''
    app = Flask(__name__)
    api = Api(app)
   
    app.config.from_object(app_config[config])
    app.url_map.strict_slashes = False
    app.config['testing'] = True

    app.register_blueprint(product)


    return app