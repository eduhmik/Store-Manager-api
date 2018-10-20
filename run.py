import os

from app import create_app
from flask_jwt_extended import JWTManager
from app.api.V1.models.revoked_token_model import RevokedTokenModel

config_name = "development"
app = create_app(config_name)
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']


jwt = JWTManager(app)

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return RevokedTokenModel.is_jti_blacklisted(self, jti)

if __name__=='__main__':
    app.run()