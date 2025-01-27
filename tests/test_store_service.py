import pytest
from io import BytesIO
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from services.store_service import StoreService
from services.menu_service import MenuService
from bson import ObjectId
from DB.database import Database

@pytest.fixture
def app():
    app = Flask(__name__)
    CORS(app)
    store_service = StoreService()
    menu_service = MenuService()

    @app.route('/')
    def index():
        return 'Index Page'

    @app.route('/stores', methods=['GET'])
    def get_all_stores():
        stores = store_service.get_all_stores()
        return jsonify(stores)

    @app.route('/stores/<store_id>', methods=['GET'])
    def get_store(store_id):
        store = store_service.get_store(store_id)
        if store:
            return jsonify(store)
        else:
            return jsonify({'error': 'Store not found'}), 404

    @app.route('/stores', methods=['POST'])
    def add_store():
        store = request.get_json()
        created_store = store_service.add_store(store)
        return jsonify(created_store), 201

    @app.route('/stores/<store_id>', methods=['DELETE'])
    def remove_store(store_id):
        success = store_service.remove_store(store_id)
        if success:
            return jsonify({'message': 'Store removed'})
        else:
            return jsonify({'error': 'Store not found'}), 404

    @app.route('/stores/<store_id>/menu', methods=['GET'])
    def get_menu(store_id):
        menu = menu_service.get_menu_by_store_id(store_id)
        if menu:
            return jsonify(menu.to_dict())
        else:
            return jsonify({'error': 'Menu not found'}), 404

    @app.route('/stores/<store_id>/menu', methods=['POST'])
    def add_menu(store_id):
        menu_data = request.get_json()
        menu_data['store_id'] = store_id
        menu_service.add_menu(menu_data)
        return jsonify(menu_data), 201

    @app.route('/stores/<store_id>/menu/<menu_id>', methods=['PUT'])
    def update_menu(store_id, menu_id):
        menu_data = request.get_json()
        success = menu_service.update_menu(store_id, menu_id, menu_data)
        if success:
            return jsonify(menu_data)
        else:
            return jsonify({'error': 'Menu not found'}), 404

    @app.route('/stores/<store_id>/menu/<menu_id>', methods=['DELETE'])
    def delete_menu(store_id, menu_id):
        success = menu_service.delete_menu(store_id, menu_id)
        if success:
            return jsonify({'message': 'Menu removed'})
        else:
            return jsonify({'error': 'Menu not found'}), 404

    @app.route('/stores/<store_id>/menu/image', methods=['POST'])
    def upload_menu_image(store_id):
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        image_file = request.files['image']
        image_url = store_service.upload_menu_image(store_id, image_file)
        if image_url:
            return jsonify({'image_url': image_url}), 201
        else:
            return jsonify({'error': 'Store not found'}), 404

    @app.route('/images/<image_id>', methods=['GET'])
    def get_image(image_id):
        image_data = store_service.db.get_collection('images').find_one({'_id': ObjectId(image_id)})
        if image_data:
            return send_file(BytesIO(image_data['image_data']), mimetype=image_data['content_type'], download_name=image_data['filename'])
        else:
            return jsonify({'error': 'Image not found'}), 404

    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture(autouse=True)
def run_around_tests():
    # Code to run before each test
    db = Database('mongodb://localhost:27017/', 'mydatabase')
    db.get_collection('store').delete_many({})
    db.get_collection('images').delete_many({})
    yield
    # Code to run after each test (if needed)

def test_upload_menu_image(client):
    # Create a store first
    store_data = {'name': 'Test Store', 'address': '123 Test St', 'menu_id': 'menu123'}
    response = client.post('/stores', json=store_data)
    assert response.status_code == 201
    store_id = response.json['_id']

    # Upload an image
    image_data = BytesIO(b'test image data')
    image_data.name = 'test_image.png'
    response = client.post(f'/stores/{store_id}/menu/image', content_type='multipart/form-data', data={'image': (image_data, 'test_image.png')})
    assert response.status_code == 201
    assert 'image_url' in response.json

    # Retrieve the image
    image_url = response.json['image_url']
    image_id = image_url.split('/')[-1]
    response = client.get(f'/images/{image_id}')
    assert response.status_code == 200
    assert response.data == b'test image data'