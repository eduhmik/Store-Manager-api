import os
from app import create_app
from app.db_setup import DatabaseSetup


config_name = os.getenv('APP_SETTINGS')
database=DatabaseSetup(config_name)
app = create_app(config_name)


if __name__=='__main__':
    app.run()