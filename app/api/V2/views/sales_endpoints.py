from flask import Flask, request, jsonify, Blueprint, json, make_response
from flask_restplus import Resource, reqparse, Api, Namespace, fields
from ..models.sales_model import Sales
from ..models.cart_model import Cart
from ..models.user_model import User
from app.api.V2.utils.auth import token_required, admin_required
from app.api.V2.utils.validator import Verify

api = Namespace('Sales_endpoints', description='A collection of endpoints for the sales model; includes get and post endpoints', 
path='api/v2/sales')
ns4 = Namespace('Seller sales endpoint', description='Get sales record by seller name')


parser = reqparse.RequestParser()
# parser.add_argument('product_name', help = 'This field cannot be blank', required = True)
# parser.add_argument('quantity', help = 'This field cannot be blank', required = True)
# parser.add_argument('total', help = 'This field cannot be blank', required = True)
# parser.add_argument('seller', help = 'This field cannot be blank', required = True)

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
        # args = parser.parse_args()
        # seller = args['seller']
        authentication_header = request.headers.get('Authorization')
        if authentication_header:    
            auth_token = authentication_header.split(" ")[1]
            identity = User.decode_auth_token(auth_token)
            seller = identity['sub']
        
            sales = Cart.get_all_cart_items(self, seller)
            if "message" in  sales:
                return {"message": "The cart is currently empty. Add items to cart to make a sale"}
            for item in range(len(sales)):
                product_name = sales[item]['product_name']
                quantity = sales[item]['quantity']
                total = sales[item]['total']
                seller = sales[item]['seller']
                new_sale = Sales(product_name, quantity, total, seller)
                created_sale = new_sale.create_sale()
                return make_response(jsonify({
                    'status': 'ok',
                    'message': 'Sale created successfully',
                    'sales': created_sale
                }), 201)
            return {'message': 'You are not authorized'}
            
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
