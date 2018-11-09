from psycopg2.extras import RealDictCursor
import psycopg2
from app.db_setup import db_url
from ..models.product_model import Product

class Cart():
    """initializing the constructor"""
    def __init__(self, product_name, quantity, total, seller):
        self.product_name = product_name
        self.quantity = quantity
        self.total = total
        self.seller = seller

    def create_sale(self):
        """Method to create a new sale into list"""
        cart_item = dict(
            product_name = self.product_name,
            quantity = self.quantity,
            total = self.total,
            seller = self.seller
        ) 
        product = self.get_product_by_name(self.product_name)
        if product:
            qty = product['quantity']
            rem_quantity = int(qty) - int(self.quantity) 
            price = product['price']
            total = int(price)*int(self.quantity)
            print(total)
            """Adding the items into carts db"""   
            query = """
                    INSERT INTO carts(product_name, quantity, total, seller)
                    VALUES(%s,%s,%s,%s);
                    """
            update_query = """UPDATE products SET quantity=%sWHERE product_name=%s"""
            conn = psycopg2.connect(db_url)
            cur = conn.cursor(cursor_factory=RealDictCursor)
            cur.execute(query, (self.product_name, self.quantity, total, self.seller))
            conn.commit()
            conn = psycopg2.connect(db_url)
            cur = conn.cursor(cursor_factory=RealDictCursor)
            cur.execute(update_query, (rem_quantity, self.product_name))
            conn.commit()
            return cart_item

    """method to fetch for a single cart item by id"""
    def get_single_cart_item (self, carts_id):
        query = """SELECT * FROM carts WHERE carts_id=%s;"""
        conn = psycopg2.connect(db_url)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(query,(carts_id,))
        cart_item = cur.fetchone()
        if cart_item:
            return cart_item
        return {"message": "There is no item found"}

    """method to fetch cart itens by sellers"""
    def get_all_cart_items(self, seller):
        query = """
                SELECT * FROM carts 
                WHERE seller=%s; 
                """
        conn = psycopg2.connect(db_url)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(query,(seller,))
        carts = cur.fetchall()
        if carts:
            return carts
        return {"message": "There is no sales record for this seller"}

    def get_product_by_name(self, product_name):
        """Method to get a single product by name"""
        query = """
                SELECT * FROM products 
                WHERE product_name=%s; 
                """
        conn = psycopg2.connect(db_url)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(query,(product_name,))
        product = cur.fetchone()
        if product:
            return product
        

    def update_cart_item(self, carts_id, product_name):
        updated_item = dict(
            product_name = self.product_name,
            quantity = self.quantity,
            total = self.total,
            seller = self.seller
        ) 
        cart_item = self.get_product_by_name(product_name)
        if cart_item:
            qty = cart_item['quantity']
            new_qty = int(qty) - int(self.quantity)
            price = cart_item['price']
            new_price = int(price)*int(self.quantity)
            """Method to get a single product by name"""
            query = """
                    UPDATE carts SET 
                    quantity=%s,
                    total=%s
                    WHERE carts_id=%s; 
                    """
            conn = psycopg2.connect(db_url)
            cur = conn.cursor(cursor_factory=RealDictCursor)
            cur.execute(query,(new_qty, new_price, carts_id))
            conn.commit()
            item = self.get_single_cart_item(carts_id)
            self.update_product_quantity(product_name, item['quantity'])
            update_query = """UPDATE products SET quantity=%sWHERE product_name=%s"""
            conn = psycopg2.connect(db_url)
            cur = conn.cursor(cursor_factory=RealDictCursor)
            cur.execute(update_query, (new_qty, product_name))
            conn.commit()
            return updated_item
    
    def delete_cart_item(self, carts_id):
        delete_query = """
                        DELETE FROM carts WHERE carts_id = %s
                    """
        conn = psycopg2.connect(db_url)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(delete_query,(carts_id,))
        conn.commit()

    def update_product_quantity(self, product_name, quantity):
        product = Product.get_product_by_name(product_name)
        if product:
            qty = product['quantity']
            rollback_qty = int(quantity)
            new_qty = int(qty) + int(rollback_qty)
            query = """UPDATE products SET quantity=%s
                    WHERE product_name=%s; 
                    """
            conn = psycopg2.connect(db_url)
            cur = conn.cursor(cursor_factory=RealDictCursor)
            cur.execute(query,(new_qty, product_name))
            conn.commit()
        else:
            return {'message': 'Product does not exist'}


    def delete_cart(self, seller):
        query = """
                DELETE from carts WHERE seller=%s;
                """
        conn = psycopg2.connect(db_url)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(query,(seller,))
        cur.execute("""ALTER SEQUENCE carts_carts_id_seq RESTART WITH 1""")
        conn.commit()
