from psycopg2.extras import RealDictCursor
import psycopg2
from app.db_setup import db_url

""" product model class and various functions"""
class Product():
    """ Initializing the constructor"""
    def __init__(self, product_name, category, quantity, reoder_level, price):
        self.product_name = product_name
        self.category = category
        self.quantity = quantity
        self.reorder_level = reoder_level
        self.price = price

    def create_product(self):
        """Method to create a new product into db"""
        product_item = dict(
            product_name = self.product_name,
            category = self.category,
            quantity = self.quantity,
            reorder_level = self.reorder_level,
            price = self.price
        )

        query = """
                INSERT INTO products(product_name, category, quantity, reorder_level, price)
                VALUES(%s,%s,%s,%s,%s);
                """
        conn = psycopg2.connect(db_url)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(query, (self.product_name, self.category, self.quantity, self.reorder_level, self.price))
        conn.commit()
        return product_item

        

    def get_all_products(self):
        """method to get all the products"""
        query = """
                SELECT * FROM products 
                """
        conn = psycopg2.connect(db_url)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(query)
        products = cur.fetchall()
        if products:
            return products
        return {"message": "There are no products found"}
        
        
    @staticmethod
    def get_single_product(product_id):
        """Method to get a single product by id"""
        query = """
                SELECT * FROM products 
                WHERE product_id=%s; 
                """
        conn = psycopg2.connect(db_url)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(query,(product_id,))
        product = cur.fetchone()
        print(product)
        if product:
            return product
        return {"message": "There is no product found"}
    
    def update_product(self, product_id):
        product_item = dict(
            product_name = self.product_name,
            category = self.category,
            quantity = self.quantity,
            reorder_level = self.reorder_level,
            price = self.price
        )
        update_query = """
                            UPDATE products SET product_name =%s, 
                            category =%s,
                            quantity =%s,
                            reorder_level =%s,
                            price =%s
                            WHERE product_id = %s
                        """
        conn = psycopg2.connect(db_url)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(update_query,(self.product_name, self.category, self.quantity, self.reorder_level, self.price, product_id))
        conn.commit()
        return product_item

    def delete_product(self, product_id):

        delete_query = """
                        DELETE FROM products WHERE product_id = %s
                    """
        conn = psycopg2.connect(db_url)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(delete_query,(product_id,))
        conn.commit()



        
        