# Library imports
import json
# Local application imports
from .base_test import BaseTest

login_url = "/api/v1/auth/login"
reg_url = "/api/v1/auth/signup"
products_url = "/api/v1/products"
class TestGetProducts(BaseTest):
    """
    Product data
    """
    product_data = {
        "product_id" : 2,
        "product_name": "Home Theatre",
        "category": "Electronics",
        "quantity": 5,
        "reorder_level": 3,
        "price": 7999
    }
    
    def test_post_product(self):
        """Test for a successful post"""
        with self.client():
            self.user_auth_register()
            resp = self.user_auth_login()

            auth_token = json.loads(resp.data.decode())['auth_token']

            post_product = self.client().post(products_url, headers=dict(Authorization="Bearer {}".format(auth_token)),
            data = self.product_data)
            result = json.loads(post_product.data)
            self.assertEqual('product created successfully', result['message'])
            self.assertEqual(post_product.status_code, 201)

    def test_get_products(self):
        """
        Test endpoint to get all products
        """
        with self.client(): 
            self.user_auth_register()
            resp = self.user_auth_login()

            auth_token = json.loads(resp.data)['auth_token']

            post_product = self.client().post(products_url, headers=dict(Authorization="Bearer {}".format(auth_token)), 
            data=self.product_data)
            result = json.loads(post_product.data)
            self.assertEqual(post_product.status_code, 201)
            self.assertEqual('product created successfully', result['message'])

            fetch_products = self.client().get(products_url)
            self.assertEqual(fetch_products.status_code, 200)
            

    def test_single_product(self):
        """
        Test endpoint to get a single product
        """
        with self.client():
            self.user_auth_register()
            resp = self.user_auth_login()

            auth_token = json.loads(resp.data)['auth_token']

            post_product = self.client().post(products_url, headers=dict(Authorization="Bearer {}".format(auth_token)), 
            data=self.product_data)
            result = json.loads(post_product.data)
            self.assertEqual(post_product.status_code, 201)
            self.assertEqual('product created successfully', result['message'])
            

            single_product = self.client().get('/api/v1/products/{}'.format(result['product']['product_id']))
            self.assertEqual(single_product.status_code, 200)
            