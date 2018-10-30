'''class to configure the database'''
import psycopg2
from datetime import datetime
from app.instance.config import app_config, db_url
from app.api.V2.models.user_model import User
from psycopg2.extras import RealDictCursor


class DatabaseSetup:
    """Initialize a db connection"""
    def __init__(self, config_name):
        self.db_url = db_url
        self.db_connection = psycopg2.connect(self.db_url)

    def create_tables(self):
        db_connection = self.db_connection
        cursor = self.db_connection.cursor()
        queries = self.initialize_database_tables()
        for query in queries:
            cursor.execute(query)
        db_connection.commit()

    def drop_tables(self):
        table1="""DROP TABLE IF EXISTS test_users CASCADE"""
        table2="""DROP TABLE IF EXISTS test_sales CASCADE"""
        table3="""DROP TABLE IF EXISTS test_products CASCADE"""
        
        db_connection = self.db_connection
        cursor = self.db_connection.cursor()
        queries=[table1,table2,table3]
        for query in queries:
            cursor.execute(query)
        db_connection.commit()
        

    def create_app_admin(self):
        db_connection = self.db_connection
        cursor = self.db_connection.cursor()
        pwd = User.generate_hash('1234')
        # stored_user_query = """
        #             SELECT * from users WHERE username=%s
        #             """
        # cursor.execute(stored_user_query,('Eduhmik',))
        # admin=cursor.fetchone()
        # if not admin:
        query = """
        INSERT INTO users(username, email, phone, role, password)
        VALUES(%s,%s,%s,%s,%s)
        """

        cursor.execute(query, ('Eduhmik', 'edwinkimaita78@gmail.com', 
                                '0718433329','admin', pwd))
                            
        db_connection.commit()

    def cursor(self):
        '''Holds temporal data being executed from or to the database'''
        cursor = self.db_connection.cursor(cursor_factory=RealDictCursor)
        return cursor

    def commit(self):
        '''commits changes to database'''
        db_connection = self.db_connection()
        db_connection.commit()

    def initialize_database_tables(self):
        query = """CREATE TABLE IF NOT EXISTS users(
            id          SERIAL PRIMARY KEY,
            username    VARCHAR(50)     UNIQUE NOT NULL,
            email       VARCHAR(80)     NOT NULL,
            phone       VARCHAR(10)     NOT NULL,
            role        VARCHAR(30)     NOT NULL,
            password    VARCHAR(200)     NOT NULL,
            created_on timestamp with time zone DEFAULT ('now'::text)::date NOT NULL  
        )
        """

        query2 = """CREATE TABLE IF NOT EXISTS sales(
            sales_id            SERIAL PRIMARY KEY,
            product_name        VARCHAR(50)     UNIQUE NOT NULL,
            quantity            INT     NOT NULL,
            total               REAL     NOT NULL,
            seller              VARCHAR(30)     NOT NULL,
            created_on timestamp with time zone DEFAULT ('now'::text)::date NOT NULL  
        )
        """

        query3 = """CREATE TABLE IF NOT EXISTS products(
            product_id          SERIAL PRIMARY KEY,
            product_name        VARCHAR(50)     UNIQUE NOT NULL,
            category            VARCHAR(50),
            quantity            INT     NOT NULL,
            reorder_level       INT     NOT NULL,
            price               REAL     NOT NULL,
            created_on timestamp with time zone DEFAULT ('now'::text)::date NOT NULL  
        )
        """

        queries = [query, query2, query3]
        return queries