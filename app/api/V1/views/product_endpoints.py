from flask import Flask, request, jsonify, Blueprint, json, make_response
from flask_restplus import Resource, reqparse, Api, Namespace, fields
from ..models.product_model import Product
from ..models.user_model import User
from ..utils.auth import admin_required, token_required

api = Namespace('Product_endpoints', description='A collection of endpoints for the product model; includes get and post endpoints', 
path='api/v1/products')

parser = reqparse.RequestParser()
parser.add_argument('product_name', help = 'This field cannot be blank', required = True)
parser.add_argument('category', help = 'This field cannot be blank', required = True)
parser.add_argument('quantity', help = 'This field cannot be blank', required = True)
parser.add_argument('reorder_level', help = 'This field cannot be blank', required = True)
parser.add_argument('price', help = 'This field cannot be blank', required = True)


@api.route('')
class ProductEndpoint(Resource):
    product_fields = api.model('Product', {
    'product_name' : fields.String,
    'category': fields.String,
    'quantity': fields.Integer,
    'reorder_level': fields.Integer,
    'price': fields.Integer
})
    @api.expect(product_fields)
    @api.doc(security='apikey')
    @admin_required
    def post(self):
        """ Create a new product """
<<<<<<< HEAD
        args = parser.parse_args()
        product_name = args['product_name']
        category = args['category']
        quantity = args['quantity']
        reoder_level = args['reorder_level']
        price = args['price']

        new_product = Product(product_name, category, quantity, reoder_level, price)
        created_product = new_product.create_product()
        return make_response(jsonify({
            'status': 'ok',
            'message': 'product created successfully',
            'product': created_product
        }), 201)
=======

        """User authentication"""
        authentication_header = request.headers.get('Authorization')
        if authentication_header:    
            try:
                auth_token = authentication_header.split(" ")[1]
                    
                identity = User.decode_auth_token(auth_token)
                print(identity)
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
                product_name = args['product_name']
                category = args['category']
                quantity = args['quantity']
                reoder_level = args['reorder_level']
                price = args['price']

                new_product = Product(product_name, category, quantity, reoder_level, price)
                created_product = new_product.create_product()
                return make_response(jsonify({
                    'status': 'ok',
                    'message': 'product created successfully',
                    'product': created_product
                }), 201)
>>>>>>> develop
       
    @api.doc(security='apikey')
    @token_required
    def get(self):
        """Get all products"""
        #User authentication
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



@api.route('/<int:product_id>')
class GetSingleProduct(Resource):
    """Get single product"""
    @api.doc(security='apikey')
    @token_required
    def get(self, product_id):
        """Get a specific product when provided with an id"""
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


        