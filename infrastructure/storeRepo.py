from infrastructure.database import Database
from domain.store import Store
from pymongo.errors import DuplicateKeyError
from bson import ObjectId

class StoreRepository:
    def __init__(self, db: Database):
        self.store_collection = db.get_collection('stores')
        self.menu_collection = db.get_collection('menus')

    def add_store(self, store: Store):
        store_data = {
            '_id': store._id,
            'name': store.name,
            'description': store.description,
            'location': store.location,
            'menu_id': store.menu_id if store.menu_id else ""
        }
        try:
            self.store_collection.insert_one(store_data)
            return store_data
        except DuplicateKeyError:
            return None

    def get_store_by_id(self, store_id: ObjectId):
        store_data = self.store_collection.find_one({'_id': store_id})
        if store_data:
            return Store(store_data['name'], store_data['description'], store_data['location'], store_data['menu_id'], store_data['_id'])
        return None

    def get_all_stores(self):
        stores = self.store_collection.find()
        return [Store(store['name'], store['description'], store['location'], store['menu_id'], store['_id']).__repr__() for store in stores]

    def delete_store(self, store_id: ObjectId):
        result = self.store_collection.delete_one({'_id': store_id})
        return result.deleted_count > 0

    def update_store(self, store_id: ObjectId, update_data: dict):
        result = self.store_collection.update_one({'_id': store_id}, {'$set': update_data})
        return result.modified_count > 0
