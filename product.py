# /products (GET): Retrieve a list of available grocery products, including their names, prices, and
# quantities in stock.
# /products/product id (GET): Get details about a specific product by its unique ID.
# /products (POST): Allow the addition of new grocery products to the inventory with information
# such as name, price, and quantity.

@app.route('/products', methods=['GET'])
def get_products():
    return 0
@app.route('/products/<int:product_id>', methods=['GET'])
def get_details(product_id):
    return 0
@app.route('/products', methods=['GET'])
def add_product(name, price, quantity):
    return 0