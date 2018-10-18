""" product model class and various functions"""
PRODS_DICT = {}
class Product():
    
    """ Initializing the constructor"""
    def __init__(self):
        self.products_dict = {}


    def create_product(self, product_id, product_name, category, quantity, reoder_level, price):
        """Method to create a new product into list"""
        self.products_dict["product_id"] = product_id
        self.products_dict["product_name"] = product_name
        self.products_dict["category"] = category
        self.products_dict["quantity"] = quantity
        self.products_dict["reoder_level"] = reoder_level
        self.products_dict["price"] = price

        PRODS_DICT[product_id]=self.products_dict
        return {"message": "Product created successfully"}

    

    def get_all_products(self):
        """method to get all the products"""
        return PRODS_DICT

    def get_single_product(self, product_id):
        if product_id in PRODS_DICT:
            return PRODS_DICT[product_id]
        return {"message":"product not found"}