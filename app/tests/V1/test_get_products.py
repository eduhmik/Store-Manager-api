# Library imports
import json
from .base_test import BaseTest


products_url = "/api/v1/products"
class TestGetProducts(BaseTest):
    """
    Product data
    """
    data = {
        "product_id" : 2,
        "product_name": "Home Theatre",
        "categoty": "Electonics",
        "quantity": 7,
        "reorder_level": 3,
        "price": 7999
    }

    def test_post_product(self):
        """Test for a successful post"""
        with self.client():
            response = self.client().post(products_url, data=json.dumps(dict(
                product_id=3,
                product_name = "Home Theatre",
                category = "Electronics",
                quantity = 5,
                reoder_level = 3,
                price = 7999
            )),
            content_type='application/json'
        )

            result = json.loads(response.data)
            self.assertEqual("success", result["message"])
            self.assertEqual(response.status_code, 201)

    def test_get_products(self):
        """
        Test endpoint to get all products
        """
        with self.client(): 
            result = self.client().get(products_url)
            self.assertEqual(result.status_code, 200)
            response = json.loads(result.data)
            self.assertEqual("success", response["message"])

    def test_single_product(self):
        """
        Test endpoint to get a single product
        """
        with self.client():
            self.client().post(products_url, data=json.dumps(dict(
                product_id = 3,
                product_name = "Home Theatre",
                category = "Electronics",
                quantity = 5,
                reoder_level = 3,
                price = 7999
            )),
            content_type='application/json')

            response = self.client().get('/api/v1/products/3')
            self.assertEqual(response.status_code, 200)

            result = self.client().get('/api/v1/products/4')
            response = json.loads(result.data)
            self.assertEqual("success", response["message"])
        
