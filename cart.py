import os
import requests
from flask import Flask, jsonify, request
from db import db, Product, Cart, carts  # Import the Product and Cart model,carts table, and db instance from db.py
from product import get_details, adj_product
from sqlalchemy import create_engine, MetaData, Table, select, update, insert, text

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'productcart.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Initialize the SQLAlchemy db with the Flask app
db.init_app(app)

# /cart/{user id} (GET): Retrieve the current contents of a user’s shopping cart, including product names, quantities, and total prices.
@app.route("/cart/<int:user_id>", methods=['GET'])
def get_cart(user_id):
    # Creating a Sqlite engine and metadata table, reflexting the table, then querying the data
    engine = create_engine('sqlite:///' + os.path.join(basedir, 'productcart.sqlite'))
    metadata = MetaData()
    carts_table = Table('carts', metadata, autoload=True, autoload_with=engine)
    connection = engine.connect()
    query = select([carts_table]).where(carts_table.c.cart_id == user_id)
    result = connection.execute(query)

    
    data = []
    for row in result:
        product_id = row["product_id"]
        product = requests.get(f'https://product-service-01oh.onrender.com/product/{product_id}')
        response = product.json()
        total = round(row["quantity"] * response["product"]["price"],2)
        data.append({'name':response["product"]["name"], 'quantity': row["quantity"], 'total': total})

    connection.close()
    return jsonify({"Cart Contents": data})
    

# /cart/{user id}/add/{product id} (POST): Add a specified quantity of a product to the user’s cart.
@app.route('/cart/<int:user_id>/add/<int:product_id>', methods=['POST'])
def add_product(user_id, product_id):
    data = request.json
    
    if "quantity" not in data:
        return jsonify({"error": "Quantity is required"}), 400

    engine = create_engine('sqlite:///' + os.path.join(basedir, 'productcart.sqlite'))
    metadata = MetaData()
    carts_table = Table('carts', metadata, autoload=True, autoload_with=engine)
    connection = engine.connect()
    query = text("SELECT * FROM carts WHERE cart_id = :user_id AND product_id = :product_id")
    result = connection.execute(query, user_id=user_id, product_id=product_id)
    existing_entry = result.scalar()
    
    if existing_entry:
        query = text("SELECT * FROM carts WHERE cart_id = :user_id AND product_id = :product_id")
        result = connection.execute(query, user_id=user_id, product_id=product_id)
        current_quantity = 0
        for row in result:
            current_quantity = row['quantity']
        stmt = update(carts_table).where(carts_table.c.cart_id == user_id).values(quantity=data["quantity"] + current_quantity)
        result = connection.execute(stmt)

        data = {"quantity": data["quantity"] * -1}
        response = requests.post(f'https://product-service-01oh.onrender.com/products/{product_id}', json=data)  
        connection.close()
        return jsonify({"message": "More Product Changed"})
    else:
        stmt = insert(carts_table).values(cart_id=user_id, product_id=product_id, quantity=data["quantity"])
        result = connection.execute(stmt)
        
        data = {"quantity": data["quantity"] * -1}
        response = requests.post(f'https://product-service-01oh.onrender.com/products/{product_id}', json=data)  
        connection.close()
        return jsonify({"message": "Product Changed"})

# /cart/{user id}/remove/{product id} (POST): Remove a specified quantity of a product from theuser’s cart.
@app.route('/cart/<int:user_id>/remove/<int:product_id>', methods=['POST'])
def remove_product(user_id, product_id):
    data = request.json
    
    if "quantity" not in data:
        return jsonify({"error": "Quantity is required"}), 400

    quantity_to_remove = {"quantity": data["quantity"] * -1}

    response = requests.post(f'http://127.0.0.1:5000/cart/{user_id}/add/{product_id}', json=quantity_to_remove)
    data = response.json()
    return data


@app.route('/cart', methods=['GET'])
def add_cart():
    new_cart = Cart()
    db.session.add(new_cart)
    db.session.commit()

    return jsonify({"message": "New cart created", "cart_id": new_cart.id}), 201

if __name__ == '__main__':
    app.run(debug=True)