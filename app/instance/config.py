import os
"""
class for app configurations
"""
class Config():
    """Base Config"""
    DEBUG = True
    SECRET_KEY = 'I am the secret key'

class Development(Config):
    '''Configurations for development'''
    Debug = True

class Testing(Config):
    '''Congigurations for testing'''
    TESTING = True
    Debug = True


app_config = {
    'development' : Development,
    'testing' : Testing
}

secret_key = Config.SECRET_KEY

