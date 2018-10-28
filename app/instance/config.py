import os
"""
class for app configurations
"""
class Config():
    """Base Config"""
    Debug = False
    SECRET_KEY = os.getenv('SECRET_KEY')

class Development(Config):
    '''Configurations for development'''
    Debug = True
    DATABASE_CONNECTION_URL = os.getenv('DATABASE_CONNECTION_URL')

class Testing(Config):
    '''Congigurations for testing'''
    TESTING = True
    Debug = True
    DATABASE_CONNECTION_URL = "dbname = 'test_store_manager' user='postgres' host='localhost' password='eduhmik'"

class Production(Config):
    '''Congigurations for production'''
    Debug = False
    Testing = False


app_config = {
    'development' : Development,
    'testing' : Testing,
    'production': Production
}

secret_key = Config.SECRET_KEY

