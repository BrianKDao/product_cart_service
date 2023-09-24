import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from db import Product, Cart, carts

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'productcart.sqlite')
db = SQLAlchemy(app)

# /products (GET): Retrieve a list of available grocery products, including their names, prices, and quantities in stock.
@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    product_list = [{"name": product.name, "price": product.price, "quantity": product.quantity} for product in products]
    return jsonify({"products", product_list})

# /products/product id (GET): Get details about a specific product by its unique ID.
@app.route('/products/<int:product_id>', methods=['GET'])
def get_details(product_id):
    product = Product.query.get(product_id)
    if product:
        return jsonify({"product": {"id": product.name, "price": product.price, "quantity": product.quantity}})
    else:
        return jsonify({"error": "Product not found"}), 404

# /products (POST): Allow the addition of new grocery products to the inventory with information such as name, price, and quantity.
@app.route('/products', methods=['POST'])
def add_product(name, price, quantity):
    data = request.json
    if "name" not in data:
        return jsonify({"error": "Name is required"}), 400
    
    if "price" not in data:
        return jsonify({"error": "Price is required"}), 400
    
    if "quantity" not in data:
        return jsonify({"error": "Quantity is required"}), 400
    
    new_product = Product(name=data['name'], price=data['price'], quantity=data['quantity'])
    db.session.add(new_product)
    db.session.commit()

    return jsonify({"message": "Product Added", "product": {"name": new_product.name, "price": new_product.price, "quantity": new_product.quantity}})

# /products (POST): Allows the adjustment of product quantities 
@app.route('/products', methods=['POST'])
def adj_product(id, quantity):
    data = request.json
    if "id" not in data:
        return jsonify({"error": "Name is required"}), 400
    
    if "quantity" not in data:
        return jsonify({"error": "Quantity is required"}), 400
    
    

if __name__ == '__main__':
    app.run(debug=True)
