from domain.store import Store
from DB.database import Database
from bson.objectid import ObjectId
from pymongo.errors import DuplicateKeyError

class StoreRepository:
    def __init__(self):
        db = Database('mongodb://localhost:27017/', 'mydatabase')
        self.collection = db.get_collection('store')

    def add_store(self, store):
        self.collection.insert_one(store.__dict__)

    def get_store(self, store_id):
        store_data = self.collection.find_one({'_id': ObjectId(store_id)})
        if store_data:
            return Store.from_dict(store_data)
        return None

    def get_all_stores(self):
        stores = self.collection.find()
        return [Store.from_dict(store) for store in stores]

    def remove_store(self, store_id):
        result = self.collection.delete_one({'_id': ObjectId(store_id)})
        return result.deleted_count > 0

    def update_store(self, store):
        result = self.collection.update_one(
            {'_id': store._id},
            {'$set': store.__dict__}
        )
        return result.matched_count > 0