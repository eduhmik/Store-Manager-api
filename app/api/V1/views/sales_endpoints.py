
from flask import Flask, request, jsonify, Blueprint, json, make_response
from flask_restplus import Resource, reqparse, Api, Namespace
from ..models.sales_model import Sales


api = Namespace('Sales_endpoints', description='A collection of endpoints for the sales model; includes get and post endpoints', 
path='api/v1/sales')

parser = reqparse.RequestParser()
parser.add_argument('sales_id')
parser.add_argument('product_id', help = 'This field cannot be blank', required = True)
parser.add_argument('product_name', help = 'This field cannot be blank', required = True)
parser.add_argument('quantity', help = 'This field cannot be blank', required = True)
parser.add_argument('total', help = 'This field cannot be blank', required = True)
parser.add_argument('seller', help = 'This field cannot be blank', required = True)

@api.route('')
class SalesEndpoint(Resource):

    def post(self):
        args = parser.parse_args()
        sales_id = args['sales_id']
        product_id = args['product_id']
        product_name = args['product_name']
        quantity = args['quantity']
        total = args['total']
        seller = args['seller']

        new_sale = Sales(sales_id, product_id, product_name, quantity, total, seller)
        created_sale = new_sale.create_sale()
        return make_response(jsonify({
            'status': 'ok',
            'message': 'Sale created successfully',
            'sales': created_sale
        }), 201)

    def get(self):
        """Get all sales"""
        sales = Sales.get_all_sales(self)
        return make_response(jsonify({
            'message':  'success',
            'status': 'ok',
            'sales': sales
        }), 200)

@api.route('/<sales_id>')
class GetSingleSale(Resource):
    """Get single sale"""
    
    def get(self, sales_id):
        """Get all sales and a specific sale when provided with an id"""
        single_sale = Sales.get_single_sale(self, sales_id) 
        if single_sale:
            return make_response(jsonify({
                'status': 'ok',
                'message': 'success',
                'sale': single_sale
            }), 200)
        return make_response(jsonify({
            'status': 'failed',
            'message': 'not found'
        }), 404)

