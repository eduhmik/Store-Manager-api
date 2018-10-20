"""
class for app configurations
"""
class Config():
    DEBUG = True
    SECRET_KEY = ''

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