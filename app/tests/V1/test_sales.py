# Library imports
import json
# Local application imports
from .base_test import BaseTest

products_url = "/api/v1/sales"

class TestSales(BaseTest):
    """
    Sales data
    """
    data = {
        "sales_id" : 2,
        "product_id": 1,
        "quantity": 1,
        "total": 3,
        "seller": 7999
    }

    def test_post_sales(self):
        """method to test for sales"""
        with test_client():
            response = self.client().post(products_url, data= json.dumps(dict(
                sales_id = 1,
                product_id = 1,
                product_name = Home Theatre,
                quantity = 1,
                total = 7999,
                seller = 'john doe'
            )),
            content_type = 'application/json'
        )
        """Asserts test return true status_code and message"""
        result = json.loads(response.data)
        self.assertEqual('success', result['message'])
        self.assertEqual(result.status_code, 201)



    def test_get_sales(self):
        """Asserts test return true status_code and message"""
        response = self.client().get(products_url)
        self.assertEqual('success', response['message'])
        result = json.loads(response.data)
        self.assertEqual(result.status_code, 200)

    def test_get_single_sale(self):
        """Asserts test return true status_code and message"""
        with self.client():
            self.client().post(products_url, data=json.dumps(dict(
                sales_id = 1,
                product_id = 3,
                product_name = "Home Theatre",
                quantity = 1,
                total = 1,
                seller = 'john doe'
            )),
            content_type='application/json')

            response = self.client().get('/api/v1/sales/3')
            self.assertEqual(response.status_code, 200)

            result = self.client().get('/api/v1/sales/4')
            response = json.loads(result.data)
            self.assertEqual("success", response["message"])

