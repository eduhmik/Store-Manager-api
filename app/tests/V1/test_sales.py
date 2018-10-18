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
        "product_name": "Home Theatre",
        "categoty": "Electonics",
        "quantity": 7,
        "reorder_level": 3,
        "price": 7999
    }