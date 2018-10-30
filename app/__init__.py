from flask import Flask
from .instance.config import app_config
from .db_setup import DatabaseSetup


def create_app(config):
    '''configuring the flask app'''
    app = Flask(__name__)
    from .api.V1 import version1 as v1
    from .api.V2 import version2 as v2
    DatabaseSetup(config).create_tables()
    # DatabaseSetup(config).create_app_admin()
    app.register_blueprint(v1)
    app.register_blueprint(v2)
    app.config.from_object(app_config[config])
    app.url_map.strict_slashes = False
    app.config['testing'] = True
    return app