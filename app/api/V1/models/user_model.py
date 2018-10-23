from passlib.hash import pbkdf2_sha256 as sha256
from app.instance.config import secret_key
import datetime
import jwt

class User():
    user_id = 1
    users = []

    def __init__(self, email, password, username, role, phone):
        self.username = username
        self.email = email
        self.password =password
        self.role = role
        self.phone = phone

    def create_user(self):
        user = dict(
            email = self.email,
            password = self.password,
            username = self.username,
            role = self.role,
            phone = self.phone
        )
        User.users.append(user)
        return user
        
    @staticmethod
    def get_single_user(email):
        """Retrieve user details by email"""

        single_user = [user for user in User.users if user['email'] == email]
        if single_user:
            return single_user[0]
        return 'not found'


    def get_all_users(self):
        return User.users

    def del_users(self):
        User.users.clear()
        del User.users[:]

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)

    def encode_auth_token(self, email):
        """ Generates an Auth token"""
        try:
            payload = {
                'exp': datetime.datetime.now() + datetime.timedelta(days=0, seconds=5),
                'iat': datetime.datetime.now(),
                'sub': email
            }
            return jwt.encode(
                payload,
                secret_key,
                algorithm='HS256'
            )
        except Exception as e:
            return e 

    @staticmethod
    def decode_auth_token(auth_token):
        """Method to decode the auth token"""

        try:
            payload = jwt.decode(auth_token, secret_key)
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return {'message': 'Signature expired. Please log in again.'}
        except jwt.InvalidTokenError:
            return {'message': 'Invalid token. Please log in again.'}