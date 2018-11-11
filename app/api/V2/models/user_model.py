from passlib.hash import pbkdf2_sha256 as sha256
from app.instance.config import secret_key
from psycopg2.extras import RealDictCursor
import psycopg2
from app.db_setup import db_url
from datetime import datetime, timedelta
import jwt

class User():

    def __init__(self, username, email, phone, role, password):
        self.username = username
        self.email = email
        self.password =password
        self.role = role
        self.phone = phone

    def create_user(self):
        user = dict(   
            username = self.username,
            email = self.email,
            phone = self.phone,
            role = self.role,
            password = self.password
        )
        
        query = """
                INSERT INTO users(username, email, phone, role, password)
                VALUES(%s,%s,%s,%s,%s);
                """
        conn = psycopg2.connect(db_url)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(query, (self.username, self.email, self.phone, self.role, self.password))
        conn.commit()
        return user
        
    @staticmethod
    def get_single_user(email):
        """Retrieve user details by email"""
        query = """
                SELECT * FROM users 
                WHERE email=%s; 
                """
        conn = psycopg2.connect(db_url)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(query,(email,))
        user = cur.fetchone()
        if user:
            return user
        return {"message": "There are no records found"}

    @staticmethod
    def get_user_by_username(username):
        """Retrieve user details by username"""
        query = """
                SELECT * FROM users 
                WHERE username=%s; 
                """
        conn = psycopg2.connect(db_url)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(query,(username,))
        user = cur.fetchone()
        if user:
            return user
        return {"message": "There are no records found"}
        

    @staticmethod
    def get_all_users():
        query = """
                SELECT * FROM users;
                """
        conn = psycopg2.connect(db_url)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(query)
        user = cur.fetchall()
        if user:
            return user
        else:
            return {"message": "There are no records"}
        
   

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
            return payload
        except jwt.ExpiredSignatureError:
            return {'message': 'Signature expired. Please log in again.'}
        except jwt.InvalidTokenError:
            return {'message': 'Invalid token. Please log in again.'}