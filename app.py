from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from services.store_service import StoreService
from services.menu_service import MenuService
from bson import ObjectId, errors
from io import BytesIO

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)  # Enable CORS for all routes and origins
store_service = StoreService()
menu_service = MenuService()

@app.before_request
def handle_options():
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'OK'})
        response.headers.add('Access-Control-Allow-Origin', request.headers.get('Origin', '*'))
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    # print("Response Headers:", response.headers)
    return response

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>CORS Test</title>
    </head>
    <body>
        <h1>CORS Test</h1>
        <button id="testButton">Test CORS</button>
        <script>
            document.getElementById('testButton').addEventListener('click', function() {
                fetch('http://localhost:5000/', {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json'
                    }
                })
                .then(response => response.json())
                .then(data => console.log(data))
                .catch(error => console.error('Error:', error));
            });
        </script>
    </body>
    </html>
    '''

@app.route('/stores', methods=['GET', 'POST', 'OPTIONS'], strict_slashes=False)
def get_all_stores():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'OK'}), 200
    if request.method == 'GET':
        stores = store_service.get_all_stores()
        return jsonify(stores)
    if request.method == 'POST':
        store = request.get_json()
        created_store = store_service.add_store(store)
        return jsonify(created_store), 201

@app.route('/stores/<store_id>', methods=['GET', 'PUT', 'DELETE', 'OPTIONS'], strict_slashes=False)
def get_store(store_id):
    if request.method == 'OPTIONS':
        return jsonify({'status': 'OK'}), 200
    if request.method == 'GET':
        try:
            ObjectId(store_id)  # Validate store_id
        except errors.InvalidId:
            return jsonify({'error': 'Invalid store ID'}), 400

        store = store_service.get_store(store_id)
        if store:
            return jsonify(store)
        else:
            return jsonify({'error': 'Store not found'}), 404
    if request.method == 'PUT':
        store_data = request.get_json()
        success = store_service.update_store(store_id, store_data)
        if success:
            return jsonify(store_data)
        else:
            return jsonify({'error': 'Store not found'}), 404
    if request.method == 'DELETE':
        success = store_service.remove_store(store_id)
        if success:
            return jsonify({'message': 'Store removed'})
        else:
            return jsonify({'error': 'Store not found'}), 404

@app.route('/stores/<store_id>/menu', methods=['GET', 'POST', 'OPTIONS'], strict_slashes=False)
def get_menu(store_id):
    if request.method == 'OPTIONS':
        return jsonify({'status': 'OK'}), 200
    if request.method == 'GET':
        menu = menu_service.get_menu_by_store_id(store_id)
        if menu:
            return jsonify(menu.to_dict())
        else:
            return jsonify({'error': 'Menu not found'}), 404
    if request.method == 'POST':
        menu_data = request.get_json()
        menu_data['store_id'] = store_id
        menu_service.add_menu(menu_data)
        return jsonify(menu_data), 201

@app.route('/stores/<store_id>/menu/<menu_id>', methods=['PUT', 'DELETE', 'OPTIONS'], strict_slashes=False)
def update_menu(store_id, menu_id):
    if request.method == 'OPTIONS':
        return jsonify({'status': 'OK'}), 200
    if request.method == 'PUT':
        menu_data = request.get_json()
        success = menu_service.update_menu(store_id, menu_id, menu_data)
        if success:
            return jsonify(menu_data)
        else:
            return jsonify({'error': 'Menu not found'}), 404
    if request.method == 'DELETE':
        success = menu_service.delete_menu(store_id, menu_id)
        if success:
            return jsonify({'message': 'Menu removed'})
        else:
            return jsonify({'error': 'Menu not found'}), 404

@app.route('/stores/<store_id>/menu/image', methods=['POST', 'OPTIONS'], strict_slashes=False)
def upload_menu_image(store_id):
    if request.method == 'OPTIONS':
        return jsonify({'status': 'OK'}), 200
    if request.method == 'POST':
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        image_file = request.files['image']
        image_url = store_service.upload_menu_image(store_id, image_file)
        if image_url:
            return jsonify({'image_url': image_url}), 201
        else:
            return jsonify({'error': 'Store not found'}), 404

@app.route('/images/<image_id>', methods=['GET', 'OPTIONS'], strict_slashes=False)
def get_image(image_id):
    if request.method == 'OPTIONS':
        return jsonify({'status': 'OK'}), 200
    if request.method == 'GET':
        image_data = store_service.db.get_collection('images').find_one({'_id': ObjectId(image_id)})
        if image_data:
            return send_file(BytesIO(image_data['image_data']), mimetype=image_data['content_type'], download_name=image_data['filename'])
        else:
            return jsonify({'error': 'Image not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
