from psycopg2.extras import RealDictCursor
import psycopg2
from app.db_setup import db_url

class Sales():
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
        product = self.get_product_by_name(self.product_name)
        if product:
            qty = product['quantity']
            print(qty)
            rem_quantity = int(qty) - int(self.quantity) 
            print(rem_quantity)
            """Adding the sale into sales db"""   
            query = """
                    INSERT INTO sales(product_name, quantity, total, seller)
                    VALUES(%s,%s,%s,%s);
                    """
            update_query = """UPDATE products SET quantity=%sWHERE product_name=%s"""
            conn = psycopg2.connect(db_url)
            cur = conn.cursor(cursor_factory=RealDictCursor)
            cur.execute(query, (self.product_name, self.quantity, self.total, self.seller))
            conn.commit()
            conn = psycopg2.connect(db_url)
            cur = conn.cursor(cursor_factory=RealDictCursor)
            cur.execute(update_query, (rem_quantity, self.product_name))
            conn.commit()
            return sales_item

    """method to fetch for all sales records"""
    def get_all_sales (self):
        query = """SELECT * FROM sales"""
        conn = psycopg2.connect(db_url)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(query)
        sales = cur.fetchall()
        if sales:
            return sales

    """method to fetch for a single sale record by id"""
    def get_single_sale (self, sales_id):
        query = """SELECT * FROM sales WHERE sales_id=%s;"""
        conn = psycopg2.connect(db_url)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(query,(sales_id,))
        sales = cur.fetchone()
        if sales:
            return sales
        return {"message": "There is no sale record found"}

    """method to fetch sales by sellers"""
    def get_sales_by_seller(self, seller):
        query = """
                SELECT * FROM sales 
                WHERE seller=%s; 
                """
        conn = psycopg2.connect(db_url)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(query,(seller,))
        sales = cur.fetchall()
        print(sales)
        if sales:
            return sales
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
           
    # @staticmethod
    # def update_qty_after_sale(quantity, product_name):
    #     update_query = """
    #                     UPDATE products 
    #                     SET quantity = %s
    #                     WHERE product_name = %s;
    #                 """
    #     conn = psycopg2.connect(db_url)
    #     cur = conn.cursor(cursor_factory=RealDictCursor)
    #     cur.execute(update_query, (quantity, product_name))
        # new_product_stock = cur.fetchone()
        # print(new_product_stock)
        # if new_product_stock:
        #     return new_product_stock
        # return {'message': 'something happened'}