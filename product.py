import os
from flask import Flask, jsonify, request
from db import db, Product  # Import the Product model and db instance from db.py

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'productcart.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the SQLAlchemy db with the Flask app
db.init_app(app)

# /products (GET): Retrieve a list of available grocery products, including their names, prices, and quantities in stock.
@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    product_list = [{'name': product.name, 'price': product.price, 'quantity': product.quantity} for product in products]
    return jsonify({"products": product_list})

# /products/product_id (GET): Get details about a specific product by its unique ID.
@app.route('/products/<int:product_id>', methods=['GET'])
def get_details(product_id):
    product = Product.query.get(product_id)
    if product:
        return jsonify({"product": {"id": product.id, "name": product.name, "price": product.price, "quantity": product.quantity}})
    else:
        return jsonify({"error": "Product not found"}), 404

# /products (POST): Allow the addition of new grocery products to the inventory with information such as name, price, and quantity.
@app.route('/products', methods=['POST'])
def add_product():
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

# /products/product_id (POST): Allows the adjustment of product quantities.
@app.route('/products/<int:product_id>', methods=['POST'])
def adj_product(product_id):
    data = request.json
    if "quantity" not in data:
        return jsonify({"error": "Quantity is required"}), 400
    
    product = Product.query.get(product_id)
    current_quantity = product.quantity
    new_quantity = current_quantity + data['quantity']
    product.quantity = new_quantity

    db.session.add(product)
    db.session.commit()

    return jsonify({"message": "Product quantity adjusted", "product": {"name": product.name, "price": product.price, "quantity": product.quantity}})

if __name__ == '__main__':
    app.run(debug=True)
