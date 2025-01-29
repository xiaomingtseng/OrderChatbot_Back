import os
from bson import ObjectId
from repositories.StoreRepository import StoreRepository
from domain.store import Store
from DB.database import Database

class StoreService:
    def __init__(self):
        self.__store_repository = StoreRepository()
        db = Database('mongodb://localhost:27017/', 'mydatabase')
        db.create_unique_index('store', 'name')
        self.db = db

    def add_store(self, store_data):
        if not store_data['name']:
            raise ValueError("Store name cannot be empty")
        
        store = Store(name=store_data['name'], address=store_data['address'], menu_id=store_data.get('menu_id'))
        self.__store_repository.add_store(store)
        return store.get_store_info()

    def get_store(self, store_id):
        store = self.__store_repository.get_store(store_id)
        if store:
            return store.get_store_info()
        return None

    def get_all_stores(self):
        stores = self.__store_repository.get_all_stores()
        return [store.get_store_info() for store in stores]

    def remove_store(self, store_id):
        return self.__store_repository.remove_store(store_id)

    def update_store(self, store_id, store_data):
        store = self.__store_repository.get_store(store_id)
        if store:
            store.name = store_data.get('name', store.name)
            store.address = store_data.get('address', store.address)
            store.menu_id = store_data.get('menu_id', store.menu_id)
            self.__store_repository.update_store(store)
            return True
        return False

    def upload_menu_image(self, store_id, image_file):
        # Read the image file as binary data
        image_data = image_file.read()
        
        # Store the image data in MongoDB
        image_id = self.db.get_collection('images').insert_one({
            'store_id': store_id,
            'image_data': image_data,
            'filename': image_file.filename,
            'content_type': image_file.content_type
        }).inserted_id
        
        # Generate the image URL (you can create an endpoint to serve this image)
        image_url = f'/images/{image_id}'
        
        # Update the store's menu with the image URL
        store = self.__store_repository.get_store(store_id)
        if store:
            store.menu_image_url = image_url
            self.__store_repository.update_store(store)
            return image_url
        return None