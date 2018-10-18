from flask import Flask, request, jsonify, Blueprint, json, make_response
from flask_restful import Resource, reqparse 
from ..models import product_model

product = Blueprint('product', __name__, url_prefix='/api/v1')

prod = product_model.Product()


@product.route('/products', methods=['POST'])

def post_product(self):
    data = request.get_json()
    if not data:
        return jsonify({"message": "Please fill in the fields"})
    product_id = data.get("product_id")
    product_name = data.get("product_name")
    category = data.get("category")
    quantity = data.get("quantity")
    reorder_level = data.get("reoder_level")
    price = data.get("price")

    if product_name is None or not product_name:
        return jsonify({"message": "please enter product name"}), 206
    elif category is not category:
        return jsonify({"message": "please select the product's category"}), 206
    elif quantity is None or not quantity:
        return jsonify({"message": "please enter product quantity"}), 206
    elif reorder_level is None or not reorder_level:
        return jsonify({"message": "please enter product reorder level"}), 206
    elif price is None or not price:
        return jsonify({"message": "please enter product price"}), 206

    response =jsonify(prod.create_product(product_id, product_name, category, quantity, reorder_level, price))
    response.status_code = 201
    return response
    
    @product.route('/products', methods=['GET'])
    def get_all_products(self):
        response=jsonify(prod.get_all_products())
        response.status_code = 200
        return response

@product.route('/products/<product_id>', methods=['GET'])

def get_single_product(self, product_id):
        response = jsonify(prod.get_single_product(product_id))
        response.status_code = 200
        return response