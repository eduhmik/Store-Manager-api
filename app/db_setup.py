'''class to configure the database'''
import psycopg2
from datetime import datetime
from app.api.V2.models.user_model import User
from psycopg2.extras import RealDictCursor
from app.instance.config import app_config

class DatabaseSetup:
    """Initialize a db connection"""
    def __init__(self, app_config):
        db_url = app_config[app_config].DATABASE_CONNECTION_URL
        self.db_connection = psycopg2.connect(db_url)

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

    def initialize_database_tables(self):
        query = """CREATE TABLE IF NOT EXISTS users(
            id          SERIAL PRIMARY KEY,
            username    VARCHAR(50)     UNIQUE NOT NULL,
            email       VARCHAR(80)     NOT NULL,
            phone       VARCHAR(10)     NOT NULL,
            role        VARCHAR(30)     NOT NULL,
            password    VARCHAR(50)     NOT NULL,
            created_on timestamp with time zone DEFAULT ('now'::text)::date NOT NULL  
        )
        """

        query2 = """CREATE TABLE IF NOT EXISTS products(
            sales_id          SERIAL PRIMARY KEY,
            product_name    VARCHAR(50)     UNIQUE NOT NULL,
            quantity       INT     NOT NULL,
            total       VARCHAR(10)     NOT NULL,
            seller        VARCHAR(30)     NOT NULL,
            created_on timestamp with time zone DEFAULT ('now'::text)::date NOT NULL  
        )
        """

        query3 = """CREATE TABLE IF NOT EXISTS sales(
            product_id          SERIAL PRIMARY KEY,
            product_name    VARCHAR(50)     UNIQUE NOT NULL,
            quantity       VARCHAR(80)     NOT NULL,
            reorder_level       VARCHAR(10)     NOT NULL,
            price        VARCHAR(30)     NOT NULL,
            created_on timestamp with time zone DEFAULT ('now'::text)::date NOT NULL  
        )
        """

        queries = [query, query2, query3]
        return queries

    def create_app_admin(self):
        db_connection = self.db_connection
        cursor = self.db_connection.cursor()
        pwd = User.generate_hash('1234')
        query = """
        INSERT INTO users(username, email, phone, role, password)
        VALUES(%s,%s,%s,%s,%s);
        """

        cursor.execute(query, ('Eduhmik', 'edwinkimaita78@gmail.com', 
                                '0718433329', pwd, 'admin'))
                            
        db_connection.commit()

    def cursor(self):
        cursor = self.db_connection.cursor(cursor_factory=RealDictCursor)
        return cursor

    def commit(self):
        '''commits changes to database'''
        db_connection = self.db_connection()
        db_connection.commit()
    