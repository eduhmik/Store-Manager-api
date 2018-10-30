from flask import Flask, request, jsonify, Blueprint, json, make_response
from flask_restplus import Resource, reqparse, Api, Namespace, fields
from ..models.product_model import Product
from ..models.user_model import User
from app.api.V2.utils.auth import admin_required, token_required

api = Namespace('Product_endpoints', description='A collection of endpoints for the product model; includes get and post endpoints', 
path='api/v2/products')

parser = reqparse.RequestParser()
parser.add_argument('product_name', help = 'This field cannot be blank', required = True)
parser.add_argument('category', help = 'This field cannot be blank', required = True)
parser.add_argument('quantity', help = 'This field cannot be blank', required = True)
parser.add_argument('reorder_level', help = 'This field cannot be blank', required = True)
parser.add_argument('price', help = 'This field cannot be blank', required = True)

product_fields = api.model('Product', {
    'product_name' : fields.String,
    'category': fields.String,
    'quantity': fields.Integer,
    'reorder_level': fields.Integer,
    'price': fields.Integer
})
@api.route('')
class ProductEndpoint(Resource):
    @api.expect(product_fields)
    @api.doc(security='apikey')
    @admin_required
    def post(self):
        """ Create a new product """
        args = parser.parse_args()
        product_name = args['product_name']
        category = args['category']
        quantity = args['quantity']
        reorder_level = args['reorder_level']
        price = args['price']

        new_product = Product(product_name, category, quantity, reorder_level, price)
        created_product = new_product.create_product()
        return make_response(jsonify({
            'status': 'ok',
            'message': 'product created successfully',
            'product': created_product
        }), 201)
       
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


    @api.expect(product_fields)
    @api.doc(security='apikey')
    @admin_required
    def put(self, product_id):
        """ Create a new product """
        args = parser.parse_args()
        product_name = args['product_name']
        category = args['category']
        quantity = args['quantity']
        reorder_level = args['reorder_level']
        price = args['price']

        u_product = Product(product_name, category, quantity, reorder_level, price)
        updated_product = u_product.update_product(product_id)
        return make_response(jsonify({
            'status': 'ok',
            'message': 'product edited successfully',
            'product': updated_product
        }), 201)  


    
    @api.doc(security='apikey')
    @admin_required
    def delete(self, product_id):
        product_to_delete = Product.get_single_product(product_id)
        if product_to_delete:
            Product.delete_product(self, product_id)
            return make_response(jsonify({
                'status': 'ok',
                'message': 'product deleted successfully'
            }))
        