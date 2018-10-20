from flask_restplus import Api
from flask import Blueprint 


# Import all endpoints for all models
from .views.product_endpoints import api as product_namespace
from .views.sales_endpoints import api as sales_namespace
from .views.login_endpoints import api as userLogin_namespace
from .views.register_endpoints import api as userRegistration_namespace 
from .views.logout_endpoints import api as userLogoutAccess_namespace 
from .views.logout_endpoints import api as userLogoutRefresh_namespace 
from .views.logout_endpoints import api as tokenRefresh_namespace 
from .views.register_endpoints import api as allUsers_namespace 

version1 = Blueprint('api version 1', __name__, url_prefix='/api/v1')


api = Api(version1,
          title='Store manager API',
          version='1.0',
          description='An application that helps store owners manage sales  \
            and product inventory records')

api.add_namespace(product_namespace, path='/products')
api.add_namespace(sales_namespace, path='/sales')
api.add_namespace(userRegistration_namespace, path='/registration')
api.add_namespace(userLogin_namespace, path='/login')
api.add_namespace(userLogoutAccess_namespace, path='/logout/access')
api.add_namespace(userLogoutRefresh_namespace, path='/logout/refresh')
api.add_namespace(tokenRefresh_namespace, path='/token/refresh')
api.add_namespace(allUsers_namespace, path='/users')
