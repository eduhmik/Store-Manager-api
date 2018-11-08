from flask import Flask, request, jsonify, Blueprint, json, make_response
from flask_restplus import Resource, reqparse, Api, Namespace, fields
from ..models.cart_model import Cart
from ..models.product_model import Product
from ..models.user_model import User
from app.api.V2.utils.auth import token_required, admin_required
from app.api.V2.utils.validator import Verify

api = Namespace('Cart_endpoints', description='A collection of endpoints for the sales model; includes get and post endpoints', 
path='api/v2/sales')
ns4 = Namespace('Seller sales endpoint', description='Get sales record by seller name')


parser = reqparse.RequestParser()
parser.add_argument('product_name', help = 'This field cannot be blank', required = True)
parser.add_argument('quantity', help = 'This field cannot be blank', required = True)
parser.add_argument('total', help = 'This field cannot be blank', required = True)
# parser.add_argument('seller', help = 'This field cannot be blank', required = True)

cart_fields = api.model('Sale', {
    'product_name' : fields.String,
    'quantity': fields.Integer,
    'total': fields.Integer
    # 'seller': fields.String
})

@api.route('')
class CartEndpoint(Resource):
    @api.expect(cart_fields, validate=True)
    @api.doc(security='apikey')
    @token_required
    def post(self):
        """ Create new sale """
        args = parser.parse_args()
        product_name = args['product_name']
        quantity = args['quantity']
        total = args['total']
        # seller = args['seller']

        payload= [product_name, quantity, total]

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
       
        product = Product.get_product_by_name(product_name)
    
        if product:
            qty = product['quantity']
            rem_quantity = int(qty)
            price = product['price']
            new_price = int(quantity)*int(price)
            if rem_quantity == 0:
                return make_response(jsonify({'message': 'Product is not available'}), 404)
            if rem_quantity >= int(quantity): 
                rem_quantity = rem_quantity - int(quantity)
                authentication_header = request.headers.get('Authorization')
                if authentication_header:    
                    auth_token = authentication_header.split(" ")[1]
                    identity = User.decode_auth_token(auth_token)
                    seller = identity['sub']
                    new_sale = Cart(product_name, quantity, new_price, seller)
                    created_sale = new_sale.create_sale()
                    return make_response(jsonify({
                        'status': 'ok',
                        'message': 'Added to cart successfully',
                        'sales': created_sale
                    }), 201)
                return {'message': 'You are not authorized'}
            
            return make_response(jsonify({'message': 'The product you are trying to sell is higher than the stock level.\
    The remaining quantity is {}'.format(rem_quantity)}), 400)
        return {'message': 'Product you are trying to sell does not exist'}

@api.route('/<int:carts_id>')
class GetSingleCart(Resource):
    """Get single sale""" 
    @api.doc(security='apikey')
    @token_required
    def get(self, carts_id):
        """Get a specific sale when provided with an id"""
        cart_item = Cart.get_single_cart_item(self, carts_id) 
        if cart_item:
            return make_response(jsonify({
                'status': 'ok',
                'message': 'success',
                'cart': cart_item
            }), 200)
        return make_response(jsonify({
            'status': 'failed',
            'message': 'not found'
        }), 404)

    @api.expect(cart_fields)
    @api.doc(security='apikey')
    @token_required
    def put(self, carts_id):
        """ update a new product """
        args = parser.parse_args()
        product_name = args['product_name']
        quantity = args['quantity']

        find_product = Product.get_product_by_name(product_name)
        if find_product:
            authentication_header = request.headers.get('Authorization')
            if authentication_header:    
                auth_token = authentication_header.split(" ")[1]
                identity = User.decode_auth_token(auth_token)
                seller = identity['sub']
                cart_item = Cart.get_single_cart_item(self, carts_id)
                price = cart_item['price']
                total = int(price)*int(quantity)
                u_product = Cart(product_name, quantity, total, seller)
                updated_product = u_product.update_cart_item(carts_id)
                return make_response(jsonify({
                    'status': 'ok',
                    'message': 'Cart item edited successfully',
                    'product': updated_product
                }), 201)  

            return make_response(jsonify({
                'message': 'product does not exist.'
            }))
      
    @api.doc(security='apikey')
    @token_required
    def delete(self, carts_id):
        cart = Cart.get_single_cart_item(self, carts_id)
        if cart:
            Cart.delete_cart_item(self, carts_id)
            return make_response(jsonify({
                'status': 'ok',
                'message': 'Cart item deleted successfully'
            }))
        else:
            return {'message': 'Item does not exist'}

@api.route('/<seller>')
class GetCartItemsBySeller(Resource):
    """Get all cart items by seller""" 
    @api.doc(security='apikey')
    @token_required
    def get(self, seller):
        """Get a specific sale when provided with a seller name"""
        cart_items = Cart.get_all_cart_items(self, seller) 
        if cart_items:
            return make_response(jsonify({
                'status': 'ok',
                'message': 'success',
                'cart': cart_items
            }), 200)
        return make_response(jsonify({
            'status': 'failed',
            'message': 'not found'
        }), 404)

    @api.doc(security='apikey')
    @token_required
    def delete(self, seller):
        cart = Cart.get_all_cart_items(self, seller)
        if cart:
            Cart.delete_cart(self, seller)
            return make_response(jsonify({
                'status': 'ok',
                'message': 'Cart items deleted successfully'
            }))