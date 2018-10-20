from flask import Flask, request, jsonify, Blueprint, json, make_response
from flask_restplus import Resource, reqparse, Api, Namespace
from ..models.product_model import Product

api = Namespace('Product_endpoints', description='A collection of endpoints for the product model; includes get and post endpoints', 
path='api/v1/products')

parser = reqparse.RequestParser()
parser.add_argument('product_id')
parser.add_argument('product_name', help = 'This field cannot be blank', required = True)
parser.add_argument('category', help = 'This field cannot be blank', required = True)
parser.add_argument('quantity', help = 'This field cannot be blank', required = True)
parser.add_argument('reorder_level', help = 'This field cannot be blank', required = True)
parser.add_argument('price', help = 'This field cannot be blank', required = True)

@api.route('')
class ProductEndpoint(Resource):
    
    def post(self):
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
    
    def get(self):
        """Get all products"""
        products = Product.get_all_products(self)
        return make_response(jsonify({
            'message':  'success',
            'status': 'ok',
            'product': products
        }), 200)



@api.route('/<product_id>')
class GetSingleProduct(Resource):
    """Get single product"""
    
    def get(self, product_id):
        """Get all products and a specific product when provided with an id"""
        single_product = Product.get_single_product(self, product_id) 
        if single_product:
            return make_response(jsonify({
                'status': 'ok',
                'message': 'success',
                'sale': single_product
            }), 200)
        return make_response(jsonify({
            'status': 'failed',
            'message': 'not found'
        }), 404)  
        