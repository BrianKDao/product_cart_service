# /cart/{user id} (GET): Retrieve the current contents of a user’s shopping cart, including prod-
# uct names, quantities, and total prices.
# /cart/{user id}/add/{product id} (POST): Add a specified quantity of a product to the user’s cart.
# /cart/{user id}/remove/{product id} (POST): Remove a specified quantity of a product from the
# user’s cart.

import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from product import Product
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'tasks.sqlite')
db = SQLAlchemy(app)

# Cart Model
class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)

# Table to pair Carts to Products
carts = db.Table(
    'carts',
    db.Column('cart_id', db.Integer, db.ForeignKey('cart.id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True),
    db.Column('quantity', db.Integer, nullable=False)
)
# /cart/{user id} (GET): Retrieve the current contents of a user’s shopping cart, including product names, quantities, and total prices.
@app.route("/cart/<int:user_id>", methods=['GET'])
def get_cart(user_id):
    query = db.session.query(carts).filter(carts.cart_id==user_id)

    for row in query:
        # for every product in the cart, query through Products, get the products, return whatever its supposed to be
        filler = "delete this line later just using it as filler"
    
    return 0

# /cart/{user id}/add/{product id} (POST): Add a specified quantity of a product to the user’s cart.
@app.route('/cart/<int:user_id>/add/<int:product_id>', method=['POST'])
def add_product(user_id, product_id):
    data = request.json

    if "quantity" not in data:
        return jsonify({"error": "Quantity is required"}), 400

    product = Product.query.get(product_id)