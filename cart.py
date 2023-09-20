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
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True)
)
