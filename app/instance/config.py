import os
"""
class for app configurations
"""
class Config():
    """Base Config"""
    DEBUG = False
    SECRET_KEY = os.getenv('SECRET_KEY')

class Development(Config):
    '''Configurations for development'''
    DEBUG = True
    DATABASE_CONNECTION_URL=os.getenv('DATABASE_CONNECTION_URL')

class Testing(Config):
    '''Congigurations for testing'''
    TESTING = True
    DEBUG = True
    DATABASE_CONNECTION_URL = "dbname = 'test_store_manager' user = 'postgres' host='localhost' port ='5432'"

class Production(Config):
    '''Congigurations for production'''
    DEBUG = False
    Testing = False


app_config = {
    'development' : Development,
    'testing' : Testing,
    'production': Production
}

secret_key = Config.SECRET_KEY
db_url = Development.DATABASE_CONNECTION_URL

