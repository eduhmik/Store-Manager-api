# Library imports
import json
from .base_test import BaseTest



class TestGetProducts(BaseTest):
    """
    Product data
    """
    data = {
        "product_name": "Home Theatre",
        "categoty": "Electonics",
        "quantity": 7,
        "re_order": 3,
        "price": 7999
    }

    def test_get_products(self):
        """
        Test endpoint to get all products
        """
        products_url = "/api/v1/products"
        with self.client():
            response = self.client().get(products_url)
            self.assertEqual(response.status_code, 200)