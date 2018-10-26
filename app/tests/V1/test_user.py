# Library imports
import json
# Local application imports
from .base_test import BaseTest

reg_url = 'api/v1/registration'
login_url = 'api/v1/login'
token_url = 'api/v1/token/refresh'

data = {
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1Mzk5ODQ5MDEsIm5iZiI6MTUzOTk4NDkwMSwianRpIjoiMTEwZDhmNjUtNmE0ZS00ZjdmLWI1MmItNDNlYWQyNWY2ZGIwIiwiZXhwIjoxNTM5OTg1ODAxLCJpZGVudGl0eSI6ImVkd2lua2ltYWl0YTNAZ21haWwuY29tIiwiZnJlc2giOmZhbHNlLCJ0eXBlIjoiYWNjZXNzIn0.dnZgmLljm6uGWTxcM3SbETRAQ6qGP7-JoT9y7dLRcqo",
    "message": "User created successfully",
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1Mzk5ODQ5MDEsIm5iZiI6MTUzOTk4NDkwMSwianRpIjoiYTM2ODUzMWQtODA1OC00NTYyLWJhYTEtNTlkZDRjNWE4MGY1IiwiZXhwIjoxNTQyNTc2OTAxLCJpZGVudGl0eSI6ImVkd2lua2ltYWl0YTNAZ21haWwuY29tIiwidHlwZSI6InJlZnJlc2gifQ.5sQjabj9u9HfPe6alYvy73jnNDpyUSuhNOM92qCaMcc",
    "status": "ok",
    "users": {
        "email": "edwinkimaita3@gmail.com",
        "password": "$pbkdf2-sha256$29000$rTWGsNZaS4mREiJk7F0L4Q$Wmrza5o7jy.kPhF.5eP.EukfSHyK4k2OCJWFyScdWVU",
        "phone": "0718433329",
        "role": "admin",
        "username": "Eduhmik"
    }
}

class TestUser(BaseTest):

    def test_create_user(self):
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
        self.assertEqual(response.status_code, 201)
        self.assertEqual('User created successfully', result['message'])
        self.assertEqual('ok', result['status'])


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

            result = self.client().get('/api/v1/registration')
            self.assertEqual(response.status_code, 200)
            
    
    def test_user_login(self):
        with self.client():
            response = self.client().post(login_url, data=json.dumps(dict(
                username = 'Eduhmik',
                email = 'edwinkimaita@gmail.com',
                phone = '0718433329',
                role = 'admin',
                password = 1234
            )), 
            content_type = 'application/json'
        )

            result = json.loads(response.data)
            self.assertEqual(response.status_code, 200)
            self.assertEqual('Logged in successfully', result['message'])
            self.assertNotEqual('Incorrect email or password', result['message'])

            
    def test_logout_access(self):
        with self.client():
            access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1Mzk5ODQ5MDEsIm5iZiI6MTUzOTk4NDkwMSwianRpIjoiMTEwZDhmNjUtNmE0ZS00ZjdmLWI1MmItNDNlYWQyNWY2ZGIwIiwiZXhwIjoxNTM5OTg1ODAxLCJpZGVudGl0eSI6ImVkd2lua2ltYWl0YTNAZ21haWwuY29tIiwiZnJlc2giOmZhbHNlLCJ0eXBlIjoiYWNjZXNzIn0.dnZgmLljm6uGWTxcM3SbETRAQ6qGP7-JoT9y7dLRcqo"
            headers = {
                'Authorization': 'Bearer {}'.format(access_token)
            }
            response = self.client().post(
                '/api/v1/logout/access', headers=headers)
    
            result = json.loads(response.data)
            self.assertEqual(response.status_code, 405)
            

    def test_logout_refresh(self):
        with self.client():
            refresh_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1Mzk5ODQ5MDEsIm5iZiI6MTUzOTk4NDkwMSwianRpIjoiMTEwZDhmNjUtNmE0ZS00ZjdmLWI1MmItNDNlYWQyNWY2ZGIwIiwiZXhwIjoxNTM5OTg1ODAxLCJpZGVudGl0eSI6ImVkd2lua2ltYWl0YTNAZ21haWwuY29tIiwiZnJlc2giOmZhbHNlLCJ0eXBlIjoiYWNjZXNzIn0.dnZgmLljm6uGWTxcM3SbETRAQ6qGP7-JoT9y7dLRcqo"
            headers = {
                'Authorization': 'Bearer {}'.format(refresh_token)
            }
            response = self.client().get('api/v1/logout/refresh', headers=headers)
            response2 = self.client().post('api/v1/logout/refresh', data=json.dumps(data))
            result = json.loads(response.data)
            self.assertEqual(response.status_code, 405)
            
    
    def test_token_refresh(self):
        with self.client():
            response = self.client().post(token_url, data=json.dumps(data))
            result = json.loads(response.data)
            self.assertEqual(response.status_code, 500)
