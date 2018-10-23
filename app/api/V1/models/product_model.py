""" product model class and various functions"""
class Product():
    product_id = 1
    products = []
    
    """ Initializing the constructor"""
    def __init__(self, product_id, product_name, category, quantity, reoder_level, price):
        self.product_id = len(Product.products) + 1
        self.product_name = product_name
        self.category = category
        self.quantity = quantity
        self.reorder_level = reoder_level
        self.price = price

    def create_product(self):
        """Method to create a new product into list"""
        product_item = dict(
            product_id = self.product_id,
            product_name = self.product_name,
            category = self.category,
            quantity = self.quantity,
            reoder_level = self.reorder_level,
            price = self.price
        )    
        self.products.append(product_item)
        return product_item

    def get_all_products(self):
        """method to get all the products"""
        return Product.products
        
        
    @staticmethod
    def get_single_product(product_id):
        """Method to get a single product by id"""
        product_item = [prod for prod in Product.products if prod['product_id'] == product_id]
        if product_item:
            return product_item
        return {'message':'product not found'}
        