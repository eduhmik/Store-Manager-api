'''class to configure the database'''
import psycopg2
from app.instance.config import app_config

class DatabaseSetup:
    """Initialize a db connection"""
    def __init__(self, app_config):
        db_url = app_config[app_config].DATABASE_CONNECTION_URL
        self.db_connection = psycopg2.connect(db_url)
        self.cursor = self.db_connection.cursor()

    def initialize_database_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS user(
            id          SERIAL PRIMARY KEY,
            username    VARCHAR(50)     UNIQUE NOT NULL,
            email       VARCHAR(80)     NOT NULL,
            phone       VARCHAR(10)     NOT NULL,
            role        VARCHAR(30)     NOT NULL,
            password    VARCHAR(50)     NOT NULL  
        );''')

        self.db_connection.commit()
        self.cursor.close()
        self.db_connection.close()
    