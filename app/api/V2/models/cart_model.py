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
        sales_item = dict(
            product_name = self.product_name,
            quantity = self.quantity,
            total = self.total,
            seller = self.seller
        ) 
        product = Product.get_product_by_name(self.product_name)
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
            return sales_item

    """method to fetch for a single cart item by id"""
    def get_single_cart_item (self, carts_id):
        query = """SELECT * FROM carts WHERE carts_id=%s;"""
        conn = psycopg2.connect(db_url)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(query,(carts_id,))
        cart_item = cur.fetchone()
        if cart_item:
            return cart_item
        return {"message": "There is no sale record found"}

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
        

    def update_cart_item(self, carts_id):
        cart_item = self.get_single_cart_item(carts_id)
        if cart_item:
            qty = cart_item['quantity']
            new_qty = int(qty) - int(self.quantity)
            price = cart_item['price']
            new_price = int(price)*int(self.quantity)
            """Method to get a single product by name"""
            query = """
                    UPDATE carts SET 
                    product_name=%s;
                    quantity=%s;
                    total=%s;
                    seller=%s;
                    WHERE carts_id=%s; 
                    """
            conn = psycopg2.connect(db_url)
            cur = conn.cursor(cursor_factory=RealDictCursor)
            cur.execute(query,(self.product_name, new_qty, new_price, self.seller, carts_id))
            updated_cart_item = cur.fetchone()
            if updated_cart_item:
                return updated_cart_item

    def delete_cart_item(self, carts_id):
        delete_query = """
                        DELETE FROM carts WHERE carts_id = %s
                    """
        conn = psycopg2.connect(db_url)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(delete_query,(carts_id,))
        conn.commit()
        cart_item = Cart.get_single_cart_item(self, carts_id)
        if cart_item:
            qty = cart_item['quantity']
            new_qty = int(qty) + int(self.quantity)
            price = cart_item['price']
            new_price = int(price)*int(self.quantity)
            query = """
                    UPDATE carts SET 
                    product_name=%s;
                    quantity=%s;
                    total=%s;
                    seller=%s;
                    WHERE carts_id=%s; 
                    """
            conn = psycopg2.connect(db_url)
            cur = conn.cursor(cursor_factory=RealDictCursor)
            cur.execute(query,(self.product_name, new_qty, new_price, self.seller, carts_id))
        else:
            return {'message': 'Product does not exist'}


    def delete_cart(self, seller):
        cart_items = self.get_all_cart_items(seller)
        for items in range(len(cart_items)):
            cart_id = cart_items[items]['carts_id']
            self.delete_cart_item(cart_id)
            conn = psycopg2.connect(db_url)
            conn.commit()
            cur = conn.cursor(cursor_factory=RealDictCursor)
            cur.execute("ALTER SEQUENCE carts_id_seq RESTART WITH 1")
            conn.commit()
