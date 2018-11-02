# Library imports
import json
# Local application imports
from .base_test import BaseTest
from app.api.V1.models.user_model import User

reg_url = 'api/v2/auth/signup'
login_url = 'api/v2/auth/login'
token_url = 'api/v2/token/refresh'


class TestUser(BaseTest):
    user_data = {
            'username' : 'Mikkie',
            'email' : 'edwinkimaita9@gmail.com',
            'phone' : '0718433329',
            'role' : 'admin',
            'password' : '123456'
    }
    user_data2 = {
            'username' : 'Michael',
            'email' : 'edwinkimaita98@gmail.com',
            'phone' : '0718433329',
            'role' : 'admin',
            'password' : '123456'
    }
    user_data3 = {
            'username' : 'Mike',
            'email' : 'edwinkimaita97@gmail.com',
            'phone' : '0718433329',
            'role' : 'admin',
            'password' : '123456'
    }
    user_data4 = {     
            'email' : 'edwinkimaita97@gmail.com',
            'password' : '123456'
    }

    
    def test_create_user(self):
        with self.client():
            resp = self.user_auth_login()
            auth_token = json.loads(resp.data.decode())['auth_token']
            response = self.client().post(reg_url, headers=dict(Authorization="Bearer {}".format(auth_token)),
            data = self.user_data)
            result = json.loads(response.data)
            self.assertEqual('Email already exists, please log in', result['message'])
            self.assertEqual(response.status_code, 200)
            self.assertEqual('fail', result['status'])
            self.assertTrue(response.content_type == 'application/json')



    def test_get_single_user(self):
        with self.client():
            self.user_auth_register()
            resp = self.user_auth_login()

            auth_token = json.loads(resp.data.decode())['auth_token']
            response = self.client().post(reg_url, headers=dict(Authorization="Bearer {}".format(auth_token)),
            data=self.user_data)
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)

    def test_create_user_already_exist(self):
        with self.client():
            self.user_auth_register()
            resp = self.user_auth_login()

            auth_token = json.loads(resp.data.decode())['auth_token']

            create_existing_user = self.client().post(reg_url, headers=dict(Authorization="Bearer {}".format(auth_token)), 
            data=self.user_data)
            result = json.loads(create_existing_user.data)
            self.assertEqual('fail', result['status'])
            self.assertEqual('Email already exists, please log in', result['message'])
            self.assertTrue(create_existing_user.content_type == 'application/json')
            self.assertEqual(create_existing_user.status_code, 200)

            
    
    def test_user_login(self):
        """test for registered user login"""
        with self.client():
            #User registration
            resp = self.user_auth_login()
            auth_token = json.loads(resp.data.decode())['auth_token']
            reg = self.client().post(reg_url, headers=dict(Authorization="Bearer {}".format(auth_token)), 
            data=self.user_data2)
            result = json.loads(reg.data)
            self.assertEqual('Email already exists, please log in', result['message'])
            self.assertEqual(reg.status_code, 200)

            #Registered user login
            resp = self.client().post(login_url, data=self.user_data4)
            result2 = json.loads(resp.data.decode())
            self.assertEqual('fail', result['status'])
            self.assertTrue('logged in Successfully', result2['message'])
            self.assertEqual(resp.status_code, 400)
            self.assertTrue(resp.content_type == 'application/json')


            
            
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

