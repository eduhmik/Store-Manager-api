"""
This will contain the configuration to be reused in all tests.
"""
# Library imports 
from unittest import TestCase
import psycopg2
import json

#local application imports
from app.db_setup import DatabaseSetup
from app import create_app
from app.instance.config import app_config


login_url = "/api/v2/auth/login"
reg_url = "/api/v2/auth/signup"
database = DatabaseSetup(config_name='testing')
class BaseTest(TestCase):
    """
    Class to hold all similar test config
    """
    
    
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client
        self.app_context = self.app.app_context()
        database.create_tables()

        with self.app_context:
            self.app_context.push()

    def user_auth_register(self, username="JohnDoe", email="john.doe@mail.com", phone="0718433329", role="admin", password="123456"):
        """authenticate user"""
        reg_data = {
            'username':username,
            'email':email,
            'phone':phone,
            'role':role,
            'password': password
        }
        resp = self.user_auth_login()

        auth_token = json.loads(resp.data.decode())['auth_token']
        return self.client().post(reg_url, headers=dict(Authorization="Bearer {}".format(auth_token)),
            data = reg_data)


    def user_auth_login(self, email="john.doe@mail.com", password="1234"):
        """authenticate user"""
        login_data = {
            'email':email,
            'password': password
        }
        return self.client().post(login_url, data = login_data)


    def tearDown(self):
        '''Remove test variables and clear the test database'''
        with self.app_context:
            self.app_context.pop()
            database.drop_tables()
            