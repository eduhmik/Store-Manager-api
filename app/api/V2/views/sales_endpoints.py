from flask import Flask, request, jsonify, Blueprint, json, make_response
from flask_restplus import Resource, reqparse, Api, Namespace, fields
from ..models.sales_model import Sales
from ..models.user_model import User
from app.api.V2.utils.auth import token_required, admin_required
from app.api.V2.utils.validator import Verify

api = Namespace('Sales_endpoints', description='A collection of endpoints for the sales model; includes get and post endpoints', 
path='api/v2/sales')
ns4 = Namespace('Seller sales endpoint', description='Get sales record by seller name')


parser = reqparse.RequestParser()
parser.add_argument('product_name', help = 'This field cannot be blank', required = True)
parser.add_argument('quantity', help = 'This field cannot be blank', required = True)
parser.add_argument('total', help = 'This field cannot be blank', required = True)
parser.add_argument('seller', help = 'This field cannot be blank', required = True)

sales_fields = api.model('Sale', {
    'product_name' : fields.String,
    'quantity': fields.Integer,
    'total': fields.Integer,
    'seller': fields.String
})

@api.route('')
class SalesEndpoint(Resource):
    @api.expect(sales_fields, validate=True)
    @api.doc(security='apikey')
    @token_required
    def post(self):
        """ Create new sale """
        args = parser.parse_args()
        product_name = args['product_name']
        quantity = args['quantity']
        total = args['total']
        seller = args['seller']

        payload= [product_name, quantity, total, seller]

        if payload is False:
            return {'message':'Payload is invalid'},406
        elif Verify.is_empty(self, payload) is True:
            return {'message':'Required field is empty'},406
        elif Verify.is_whitespace(self, payload) is True:
            return {'message':'Required field contains only white spaces'},406
        elif int(quantity) < 1:
            return {'message':'Product quantity cannot be less than 1'},406
        elif int(total) < 1:
            return {'message':'Amount total cannot be less than 1'},406
       
        product = Sales.get_product_by_name(self, product_name)
    
        if product:
            qty = product['quantity']
            rem_quantity = int(qty)
            if rem_quantity == 0:
                return make_response(jsonify({'message': 'Product is not available'}), 404)
            if rem_quantity >= int(quantity): 
                rem_quantity = rem_quantity - int(quantity)
                new_sale = Sales(product_name, quantity, total, seller)
                created_sale = new_sale.create_sale()
                return make_response(jsonify({
                    'status': 'ok',
                    'message': 'Sale created successfully',
                    'sales': created_sale
                }), 201)
            
            return make_response(jsonify({'message': 'The product you are trying to sell is higher than the stock level.\
    The remaining quantity is {}'.format(rem_quantity)}), 400)
        return {'message': 'Product you are trying to sell does not exist'}

    @api.doc(security='apikey')
    @admin_required
    def get(self):
        """Get all sales"""
        sales = Sales.get_all_sales(self)
        return make_response(jsonify({
            'message':  'success',
            'status': 'ok',
            'sales': sales
        }), 200)

@api.route('/<int:sales_id>')
class GetSingleSale(Resource):
    """Get single sale""" 
    @api.doc(security='apikey')
    @admin_required
    def get(self, sales_id):
        """Get a specific sale when provided with an id"""
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

@api.route('/<seller>')
class GetSaleBySeller(Resource):
    """Get single sale by seller""" 
    @api.doc(security='apikey')
    @token_required
    def get(self, seller):
        """Get a specific sale when provided with a seller name"""
        sales_records = Sales.get_sales_by_seller(self, seller) 
        if sales_records:
            return make_response(jsonify({
                'status': 'ok',
                'message': 'success',
                'sale': sales_records
            }), 200)
        return make_response(jsonify({
            'status': 'failed',
            'message': 'not found'
        }), 404)
