from passlib.hash import pbkdf2_sha256 as sha256
from app.instance.config import secret_key
from datetime import datetime, timedelta
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
            username = self.username,
            email = self.email,
            password = self.password, 
            role = self.role,
            phone = self.phone
        )
        User.users.append(user)
        return user
        
    
    def get_single_user(self, email):
        """Retrieve user details by email"""
<<<<<<< HEAD

=======
>>>>>>> develop
        single_user = [user for user in User.users if user['email'] == email]
        if single_user:
            return single_user[0]
        return 'not found'


    def get_all_users(self):
        return User.users

   

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)

    @staticmethod
    def encode_auth_token(email, role):
        """ Generates an Auth token"""
        try:
            payload = {
                'exp': datetime.now() + timedelta(days=1, seconds=5),
                'iat': datetime.now(),
                'sub': email,
                'role':role
            }
            
            token = jwt.encode(
                payload,
                secret_key,
                algorithm='HS256'
            )
            return token

        except Exception as e:
            return e 

    @staticmethod
    def decode_auth_token(auth_token):
        """Method to decode the auth token"""
        
        try:
            payload = jwt.decode(auth_token, secret_key, options={'verify_iat': False})
            # print (payload)
            return payload
        except jwt.ExpiredSignatureError:
            return {'message': 'Signature expired. Please log in again.'}
        except jwt.InvalidTokenError:
            return {'message': 'Invalid token. Please log in again.'}