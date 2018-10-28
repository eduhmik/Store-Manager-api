"""
This will contain the configuration to be reused in all tests.
"""
# Library imports 
from unittest import TestCase
import psycopg2

#local application imports
from app import create_app
from app.instance.config import app_config


login_url = "/api/v2/auth/login"
reg_url = "/api/v2/auth/signup"
class BaseTest(TestCase):
    """
    Class to hold all similar test config
    """
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client
        self.app_context = self.app.app_context()
        self.app_context.push()

    def user_auth_register(self, email="john.doe@mail.com", phone="0718433329", role="admin", username="Eduhmik", password="1234"):
        """authenticate user"""
        reg_data = {
            'email':email,
            'username':username,
            'phone':phone,
            'role':role,
            'password': password
        }
        return self.client().post(reg_url, data = reg_data)

    def user_auth_login(self, email="john.doe@mail.com", password="1234"):
        """authenticate user"""
        login_data = {
            'email':email,
            'password': password
        }
        return self.client().post(login_url, data = login_data)


    def tearDown(self):
        '''Remove test variables and clear the test database'''
        db_connection = app_config['testing'].DATABASE_CONNECTION_URL
        connection = psycopg2.connect(db_connection)
        cursor = connection.cursor()
        cursor.execute("DROP TABLE users")
        connection.commit()
        connection.close()
        self.app_context.pop()