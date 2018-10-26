# Library imports
import json
# Local application imports
from .base_test import BaseTest

sales_url = "/api/v1/sales"
login_url = "/api/v1/auth/login"
reg_url = "/api/v1/auth/signup"
class TestSales(BaseTest):
    """
    Sales data
    """
    sales_data = {
        "sales_id" : 2,
        "product_id": 1,
        "product_name": 'Home Theatre',
        "quantity": 1,
        "total": 3,
        "seller": 'john doe'
    }
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

    def test_post_sales(self):
        """method to test for sales"""
        with self.client():
            self.user_auth_register()
            resp = self.user_auth_login()

            auth_token = json.loads(resp.data.decode())['auth_token']

            post_sale = self.client().post(sales_url, headers=dict(Authorization="Bearer {}".format(auth_token)),
            data = self.sales_data)
            """Asserts test return true status_code and message"""
            result = json.loads(post_sale.data)
            self.assertEqual('Sale created successfully', result['message'])
            self.assertEqual(post_sale.status_code, 201)



    def test_get_sales(self):
        with self.client():
            resp = self.user_auth_login()

            auth_token = json.loads(resp.data.decode())['auth_token']

            post_sale = self.client().post(sales_url, headers=dict(Authorization="Bearer {}".format(auth_token)),
            data = self.sales_data)
            """Asserts test return true status_code and message"""
            result = json.loads(post_sale.data)
            self.assertEqual('Sale created successfully', result['message'])
            self.assertEqual(post_sale.status_code, 201)

            """Asserts test return true status_code and message"""
            fetch_sales = self.client().get(sales_url)
            self.assertEqual(fetch_sales.status_code, 200)
            
            
            

    def test_get_single_sale(self):
        """Asserts test return true status_code and message"""
        with self.client():
            self.user_auth_register()
            resp = self.user_auth_login()

            auth_token = json.loads(resp.data.decode())['auth_token']

            post_sale = self.client().post(sales_url, headers=dict(Authorization="Bearer {}".format(auth_token)),
            data = self.sales_data)
            """Asserts test return true status_code and message"""
            result = json.loads(post_sale.data)
            self.assertEqual('Sale created successfully', result['message'])
            self.assertEqual(post_sale.status_code, 201)

            single_sale = self.client().get(
                '/api/v1/sales/{}'.format(result['sales']['sales_id']))
            self.assertEqual(single_sale.status_code, 200)

            

