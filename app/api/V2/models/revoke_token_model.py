from psycopg2.extras import RealDictCursor
import psycopg2
from app.db_setup import db_url

'''model class to revoke our auth_token'''
class RevokedTokenModel():
    
    def __init__(self, auth_token):
        self.auth_token = auth_token
    
    def add(self):
        query = '''INSERT INTO revoke_tokens auth_token VALUES (%s)'''

        conn = psycopg2.connect(db_url)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(query, (self.auth_token,))
        conn.commit()
    
    @classmethod
    def is_token_blacklisted(cls, auth_token):
        query = '''SELECT * FROM revoke_tokens WHERE auth_token = %s'''
        conn = psycopg2.connect(db_url)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(query, (auth_token,))
        revoked = cur.fetchone()
        if revoked:
            return revoked