
from flask import Flask, request, jsonify, Blueprint, json, make_response
from flask_restplus import Resource, reqparse, Api, Namespace, fields
from ..models.sales_model import Sales
from ..models.user_model import User
from ..utils.auth import token_required, admin_required


api = Namespace('Sales_endpoints', description='A collection of endpoints for the sales model; includes get and post endpoints', 
path='api/v1/sales')


parser = reqparse.RequestParser()
parser.add_argument('product_name', help = 'This field cannot be blank', required = True)
parser.add_argument('quantity', help = 'This field cannot be blank', required = True)
parser.add_argument('total', help = 'This field cannot be blank', required = True)
parser.add_argument('seller', help = 'This field cannot be blank', required = True)

@api.route('')
class SalesEndpoint(Resource):
    sales_fields = api.model('Sale', {
    'product_name' : fields.String,
    'quantity': fields.Integer,
    'total': fields.Integer,
    'seller': fields.String
})
    @api.expect(sales_fields)
    @api.doc(security='apikey')
    @token_required
    def post(self):
        """ Create new sale """
        args = parser.parse_args()
        product_name = args['product_name']
        quantity = args['quantity']
        total = args['total']
        seller = args['seller']

<<<<<<< HEAD
        new_sale = Sales(product_name, quantity, total, seller)
        created_sale = new_sale.create_sale()
        return make_response(jsonify({
            'status': 'ok',
            'message': 'Sale created successfully',
            'sales': created_sale
        }), 201)
=======
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
                args = parser.parse_args()
                product_name = args['product_name']
                quantity = args['quantity']
                total = args['total']
                seller = args['seller']

                new_sale = Sales(product_name, quantity, total, seller)
                created_sale = new_sale.create_sale()
                return make_response(jsonify({
                    'status': 'ok',
                    'message': 'Sale created successfully',
                    'sales': created_sale
                }), 201)
>>>>>>> develop

    @api.doc(security='apikey')
    @admin_required
    def get(self):
        """Get all sales"""
<<<<<<< HEAD
        sales = Sales.get_all_sales(self)
        return make_response(jsonify({
            'message':  'success',
            'status': 'ok',
            'sales': sales
        }), 200)
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
                sales = Sales.get_all_sales(self)
                if len(sales) == 0:
                    return make_response(jsonify({
                        'message':  'No sales record. Make a sale orde',
                        'status': 'ok',
                        'sales': sales
                    }), 200)      
                sales = Sales.get_all_sales(self)
                return make_response(jsonify({
                    'message':  'success',
                    'status': 'ok',
                    'sales': sales
                }), 200)
>>>>>>> develop

@api.route('/<int:sales_id>')
class GetSingleSale(Resource):
    """Get single sale""" 
    @api.doc(security='apikey')
    @admin_required
    def get(self, sales_id):
        """Get a specific sale when provided with an id"""
<<<<<<< HEAD
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
=======
        """User authentication"""
        authentication_header = request.headers.get('Authorization')
        if authentication_header:
            try:
                auth_token = authentication_header.split(" ")[1]
                identity = User.decode_auth_token(auth_token)
                print(identity)
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
                if identity['role'] == 'attendant':
                    return make_response(jsonify({
                        'status': 'failed',
                        'message': 'You are not an admin'
                    }), 401)
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
>>>>>>> develop

