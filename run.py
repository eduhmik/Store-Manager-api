import os
from app import create_app


config_name = "development"
app = create_app(os.getenv('APP_SETTINGS'))


if __name__=='__main__':
    app.run()