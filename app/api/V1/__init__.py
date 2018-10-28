#Library imports
from flask_restplus import Api
from flask import Blueprint 

# Import all endpoints for all models
from .views.product_endpoints import api as product_namespace
from .views.sales_endpoints import api as sales_namespace
from .views.auth_endpoints import ns2 as userLogin_namespace
from .views.auth_endpoints import api as userRegistration_namespace 
from .views.auth_endpoints import ns as allUsers_namespace 
from .views.auth_endpoints import ns3 as logout_namespace

authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

version1 = Blueprint('api version 1', __name__, url_prefix='/api/v1')
api = Api(version1, title='Store manager API', version='1.0', description='An application that helps store owners manage sales and product inventory records', authorizations=authorizations)

api.add_namespace(product_namespace, path='/products')
api.add_namespace(sales_namespace, path='/sales')
api.add_namespace(userRegistration_namespace, path='/auth/signup')
api.add_namespace(userLogin_namespace, path='/auth/login')
api.add_namespace(logout_namespace, path='/signout')
api.add_namespace(allUsers_namespace, path='/users')
