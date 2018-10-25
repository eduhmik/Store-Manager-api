# Library imports
import json
# Local application imports
from .base_test import BaseTest
from app.api.V1.models.user_model import User

reg_url = 'api/v1/auth/signup'
login_url = 'api/v1/auth/login'
token_url = 'api/v1/token/refresh'


class TestUser(BaseTest):

    def test_create_user(self):
        with self.client():
            response = self.client().post(reg_url, data=json.dumps(dict(
                username = 'Eduhmik',
                email = 'edwinkimaita@gmail.com',
                phone = '0718433329',
                role = 'admin',
                password = '1234'
            )), 
            content_type = 'application/json'
        )
            result = json.loads(response.data)
            self.assertEqual('User created successfully', result['message'])
            self.assertEqual(response.status_code, 201)
            self.assertEqual('ok', result['status'])
            self.assertTrue(response.content_type == 'application/json')



    def test_get_single_user(self):
        with self.client():
            response = self.client().post(reg_url, data=json.dumps(dict(
                username = 'Eduhmik',
                email = 'edwinkimaita@gmail.com',
                phone = '0718433329',
                role = 'admin',
                password = 1234
            )), 
            content_type = 'application/json'
        )

            self.assertEqual(response.status_code, 200)

    def test_create_user_already_exist(self):
        user = User(
            username = 'eduhmik',
            email = 'edwinkimaita@gmail.com',
            password = '1234',
            phone = '0718433329',
            role = 'admin'
        )
        with self.client():
            response = self.client().post(reg_url, data=json.dumps(dict(
                username = 'Eduhmik',
                email = 'edwinkimaita@gmail.com',
                phone = '0718433329',
                role = 'admin',
                password = 1234
            )),
            content_type = 'application/json'
        )
            result = json.loads(response.data)
            self.assertEqual('fail', result['status'])
            self.assertEqual('Email already exists', result['message'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)

            
    
    def test_user_login(self):
        """test for registered user login"""
        with self.client():
            #User registration
            response = self.client().post(reg_url, data=json.dumps(dict(
                username = 'Eduhmik',
                email = 'edwinkimaita2@gmail.com',
                phone = '0718433329',
                role = 'admin',
                password = '12345'
            )), 
            content_type = 'application/json'
        )

            result = json.loads(response.data)
            self.assertEqual('User created successfully', result['message'])
            self.assertEqual(response.status_code, 201)
            self.assertNotEqual('Incorrect email or password', result['message'])
            self.assertTrue(response.content_type == 'application/json')

            #Registered user login
            response2 = self.client().post(login_url, data=json.dumps(dict(
                email = 'edwinkimaita2@gmail.com',
                password = '12345'
            )), 
            content_type = 'application/json'
        )
            result2 = json.loads(response2.data)
            self.assertEqual('ok', result['status'])
            self.assertTrue('logged in Successfully', result2['message'])
            self.assertEqual(response2.status_code, 200)
            self.assertTrue(response.content_type == 'application/json')
            
            
    def test_encode_auth_token(self):
        user = User(
            username = 'eduhmik',
            email = 'edwinkimaita@gmail.com',
            password = '1234',
            phone = '0718433329',
            role = 'admin'
        )

        auth_token = user.encode_auth_token(user.email, user.role)
        self.assertTrue(isinstance(auth_token, bytes))

    def test_decode_auth_token(self):
        user = User(
            username = 'eduhmik',
            email = 'edwinkimaita@gmail.com',
            password = '1234',
            phone = '0718433329',
            role = 'admin'
        )

        auth_token = user.encode_auth_token(user.email, user.role)
        self.assertTrue(isinstance(auth_token, bytes))
        self.assertTrue(User.decode_auth_token(auth_token)['role'] == 'admin')