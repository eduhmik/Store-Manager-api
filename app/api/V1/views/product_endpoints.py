from flask import Flask, request, jsonify, Blueprint, json, make_response
from flask_restplus import Resource, reqparse, Api, Namespace, fields
from ..models.product_model import Product
from ..models.user_model import User

api = Namespace('Product_endpoints', description='A collection of endpoints for the product model; includes get and post endpoints', 
path='api/v1/products')
ns = Namespace('index_endpoint', description='Returns a simple hello world message')

parser = reqparse.RequestParser()
parser.add_argument('product_id')
parser.add_argument('product_name', help = 'This field cannot be blank', required = True)
parser.add_argument('category', help = 'This field cannot be blank', required = True)
parser.add_argument('quantity', help = 'This field cannot be blank', required = True)
parser.add_argument('reorder_level', help = 'This field cannot be blank', required = True)
parser.add_argument('price', help = 'This field cannot be blank', required = True)


@api.route('')
class ProductEndpoint(Resource):
    product_fields = api.model('Product', {
    'product_id' : fields.Integer,
    'product_name' : fields.String,
    'category': fields.String,
    'quantity': fields.Integer,
    'reorder_level': fields.Integer,
    'price': fields.Integer
})
    @api.expect(product_fields)
    @api.doc(security='apikey')
    def post(self):
        """ Create a new product """

        """User authentication"""
        authentication_header = request.headers.get('Authorization')
        if authentication_header:    
            try:
                auth_token = authentication_header.split(" ")[1]
                identity = User.decode_auth_token(auth_token)
                if identity == 'Invalid token. Please log in again.':
                    return make_response(jsonify({
                        'status': 'failed',
                        'message': 'Invalid token. Please log in again.'
                    }), 401)

            except Exception:
                return make_response(jsonify({
                    'status': 'failed',
                    'message': 'You are not authorized'
                }), 401)
                
            if auth_token:
                if identity['role'] == 'attendant':
                    return make_response(jsonify({
                        'status': 'failed',
                        'message': 'You are not an admin'
                    }), 401)

                args = parser.parse_args()
                product_id = args['product_id']
                product_name = args['product_name']
                category = args['category']
                quantity = args['quantity']
                reoder_level = args['reorder_level']
                price = args['price']

                new_product = Product(product_id, product_name, category, quantity, reoder_level, price)
                created_product = new_product.create_product()
                return make_response(jsonify({
                    'status': 'ok',
                    'message': 'product created successfully',
                    'product': created_product
                }), 201)
       
    @api.doc(security='apikey')
    def get(self):
        """Get all products"""
        #User authentication
        authentication_header = request.headers.get('Authorization')

        if authentication_header:
            
            auth_token = authentication_header.split(" ")[1]
            identity = User.decode_auth_token(auth_token)
            if identity == 'Invalid token. Please sign in again':
                return make_response(jsonify({
                    'status': 'failed',
                    'message': 'Invalid token. Please sign in again'
                }), 401)

            else:    
                return make_response(jsonify({
                    'status': 'failed',
                    'message': 'You are not authorized'
                }), 401)
        if auth_token:
            products = Product.get_all_products(self)
            if len(products) == 0:
                return make_response(jsonify({
                    'message':  'success',
                    'status': 'ok',
                    'product': 'Inventory empty. Add products'
                }), 200)
            return make_response(jsonify({
                'message':  'success',
                'status': 'ok',
                'product': products
            }), 200)
        return make_response(jsonify({
                    'status': 'failed',
                    'message': 'You are not authorized'
                }), 401)



@api.route('/<int:product_id>')
class GetSingleProduct(Resource):
    """Get single product"""
    @api.doc(security='apikey')
    def get(self, product_id):
        """Get a specific product when provided with an id"""
        #User authentication
        authentication_header = request.headers.get('Authorization')

        if authentication_header:
            try:
                auth_token = authentication_header.split(" ")[1]
                identity = User.decode_auth_token(auth_token)
                if identity == 'Invalid token. Please sign in again':
                    return make_response(jsonify({
                        'status': 'failed',
                        'message': 'Invalid token. Please sign in again'
                    }), 401)

            except Exception:
                return make_response(jsonify({
                    'status': 'failed',
                    'message': 'You are not authorized'
                }), 401)
            if auth_token:
                single_product = Product.get_single_product(product_id) 
                if single_product:
                    return make_response(jsonify({
                        'status': 'ok',
                        'message': 'success',
                        'product': single_product
                    }), 200)
                return make_response(jsonify({
                    'status': 'failed',
                    'message': 'not found'
                }), 404)  


        