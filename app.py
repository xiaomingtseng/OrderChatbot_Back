#presentation layer
from flask import Flask, jsonify, request
from flask_cors import CORS
from service.StoreService import StoreService
from bson import ObjectId, errors
from infrastructure.database import Database
from infrastructure.menuRepo import MenuRepository
from infrastructure.cartRepo import CartReposiotry
from service.MenuService import MenuService
from domain.menu import Menu, MenuItem
from service.CartService import CartService
from domain.cart import Cart, CartItem

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

store_service = StoreService()

# Initialize database and repositories
db = Database()
menu_repo = MenuRepository(db)
menu_service = MenuService(menu_repo)
cart_repo = CartReposiotry(db)
cart_service = CartService(cart_repo)

@app.before_request
def handle_options():
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'OK'})
        origin = request.headers.get('Origin')
        if origin:
            response.headers['Access-Control-Allow-Origin'] = origin
        else:
            response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
        response.headers['Access-Control-Allow-Methods'] = 'GET,PUT,POST,DELETE,OPTIONS'
        return response

@app.after_request
def after_request(response):
    origin = request.headers.get('Origin')
    if origin:
        response.headers['Access-Control-Allow-Origin'] = origin
    else:
        response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET,PUT,POST,DELETE,OPTIONS'
    return response

@app.route('/')
def home():
    return "Hello, World!"

@app.route('/stores', methods=['GET', 'POST', 'OPTIONS'], strict_slashes=False)
def handle_stores():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'OK'}), 200
    if request.method == 'GET':
        stores = store_service.get_all_stores()
        return jsonify(stores)
    if request.method == 'POST':
        store_data = request.get_json()
        created_store = store_service.add_store(store_data)
        return jsonify(created_store), 201

@app.route('/stores/<store_id>', methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def handle_store(store_id):
    if request.method == 'GET':
        store = store_service.get_store_by_id(ObjectId(store_id))
        if store:
            return jsonify(store.to_dict()), 200
        else:
            return jsonify({'status': 'Store not found'}), 404
    if request.method == 'DELETE':
        success = store_service.delete_store(ObjectId(store_id))
        if success:
            return jsonify({'status': 'Store deleted'}), 200
        else:
            return jsonify({'status': 'Store not found'}), 404
    if request.method == 'PUT':
        update_data = request.get_json()
        success = store_service.update_store(ObjectId(store_id), update_data)
        if success:
            return jsonify({'status': 'Store updated'}), 200
        else:
            return jsonify({'status': 'Store not found'}), 404

@app.route('/menus', methods=['POST'])
def create_menu():
    data = request.json
    menu = Menu(image_id=data['image_id'], store_id=data['store_id'], menu_id=data['menu_item_ids'])
    result = menu_service.create_menu(menu)
    result['_id'] = str(result['_id'])
    return jsonify(result), 201

@app.route('/menus/<menu_id>', methods=['GET'])
def get_menu(menu_id):
    menu = menu_service.get_menu(menu_id)
    if menu:
        menu_dict = menu.__dict__
        return jsonify(menu_dict), 200
    return jsonify({'error': 'Menu not found'}), 404

@app.route('/menus/<menu_id>', methods=['PUT'])
def update_menu(menu_id):
    data = request.json
    result = menu_service.update_menu(menu_id, data)
    if result:
        return jsonify({'message': 'Menu updated successfully'}), 200
    return jsonify({'error': 'Menu not found'}), 404

@app.route('/menus/<menu_id>', methods=['DELETE'])
def delete_menu(menu_id):
    result = menu_service.delete_menu(menu_id)
    if result:
        return jsonify({'message': 'Menu deleted successfully'}), 200
    return jsonify({'error': 'Menu not found'}), 404

@app.route('/menu_items', methods=['POST'])
def create_menu_item():
    data = request.json
    menu_item = MenuItem(None, data['name'], data['price'], data['description'])
    result = menu_service.create_menu_item(menu_item)
    result['_id'] = str(result['_id'])
    return jsonify(result), 201

@app.route('/menu_items/<menu_item_id>', methods=['GET'])
def get_menu_item(menu_item_id):
    menu_item = menu_service.get_menu_item(menu_item_id)
    if menu_item:
        menu_item_dict = menu_item.__dict__
        return jsonify(menu_item_dict), 200
    return jsonify({'error': 'Menu item not found'}), 404

@app.route('/menu_items/<menu_item_id>', methods=['PUT'])
def update_menu_item(menu_item_id):
    data = request.json
    result = menu_service.update_menu_item(menu_item_id, data)
    if result:
        return jsonify({'message': 'Menu item updated successfully'}), 200
    return jsonify({'error': 'Menu item not found'}), 404

@app.route('/menu_items/<menu_item_id>', methods=['DELETE'])
def delete_menu_item(menu_item_id):
    result = menu_service.delete_menu_item(menu_item_id)
    if result:
        return jsonify({'message': 'Menu item deleted successfully'}), 200
    return jsonify({'error': 'Menu item not found'}), 404

@app.route('/cart', methods=['POST'])
def create_cart():
    cart = cart_service.create_cart()
    cart['_id'] = str(cart['_id'])
    return jsonify(cart), 201

@app.route('/cart/<cart_id>', methods=['GET'])
def get_cart(cart_id):
    try:
        cart = cart_service.get_cart_by_id(ObjectId(cart_id))
        if cart:
            return jsonify(cart.__dict__), 200
        return jsonify({'error': 'Cart not found'}), 404
    except errors.InvalidId:
        return jsonify({'error': 'Invalid cart ID'}), 400

@app.route('/cart/<cart_id>', methods=['PUT'])
def update_cart(cart_id):
    try:
        data = request.json
        cart = cart_service.update_cart(ObjectId(cart_id), data)
        if cart:
            return jsonify(cart.__dict__), 200
        return jsonify({'error': 'Cart not found'}), 404
    except errors.InvalidId:
        return jsonify({'error': 'Invalid cart ID'}), 400

@app.route('/cart/<cart_id>', methods=['DELETE'])
def delete_cart(cart_id):
    result = cart_service.delete_cart(cart_id)
    if result:
        return jsonify({'message': 'Cart deleted successfully'}), 200
    return jsonify({'error': 'Cart not found'}), 404

@app.route('/cart_item/<cart_item_id>', methods=['GET'])
def get_cart_item_details(cart_item_id):
    try:
        cart_item = cart_service.get_cart_item_details(cart_item_id)
        if cart_item:
            return jsonify(cart_item), 200
        return jsonify({'error': 'Cart item not found'}), 404
    except errors.InvalidId:
        return jsonify({'error': 'Invalid cart item ID'}), 400

@app.route('/cart/<cart_id>/items', methods=['POST'])
def add_cart_item(cart_id):
    data = request.json
    menu_item_id = data['menu_item_id']
    quantity = data['quantity']
    features = data.get('features', [])
    result = cart_service.add_cart_item(menu_item_id, quantity, features)
    if result:
        return jsonify({'message': 'Item added to cart successfully', 'cart_item': result}), 201
    return jsonify({'error': 'Failed to add item to cart'}), 400


if __name__ == '__main__':
    app.run(debug=True)
