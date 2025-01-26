from flask import Flask, jsonify, request
from services.store_service import StoreService
from bson import ObjectId

app = Flask(__name__)
store_service = StoreService()

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
    store_service.add_store(store)
    return jsonify(store), 201

@app.route('/stores/<store_id>', methods=['DELETE'])
def remove_store(store_id):
    success = store_service.remove_store(store_id)
    if success:
        return jsonify({'message': 'Store removed'})
    else:
        return jsonify({'error': 'Store not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
