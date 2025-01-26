from domain.store import Store
from DB.database import Database
from bson.objectid import ObjectId

class StoreRepository:
    def __init__(self):
        self.db = Database('mongodb://localhost:27017/', 'mydatabase')
        self.collection = self.db.get_collection('store')

    def add_store(self, store):
        self.collection.insert_one(store.__dict__)

    def get_store(self, store_id):
        store_data = self.collection.find_one({'_id': ObjectId(store_id)})
        if store_data:
            return Store(**store_data)

    def get_all_stores(self):
        stores = self.collection.find()
        return [Store(**store_data) for store_data in stores]

    def remove_store(self, store_id):
        result = self.collection.delete_one({'_id': ObjectId(store_id)})
        return result.deleted_count > 0