from domain.store import Store
from infrastructure.storeRepo import StoreRepository
from infrastructure.database import Database
from bson import ObjectId

class StoreService:
    def __init__(self):
        db = Database()  # Initialize the Database instance without parameters
        db.get_collection('stores').create_index('name', unique=True)  # Create unique index on 'name'
        self.__store_repo = StoreRepository(db)

    def add_store(self, store_data):
        if not store_data['name']:
            raise ValueError("Store name cannot be empty")
        
        store = Store(
            name=store_data['name'],
            description=store_data['description'],
            location=store_data['location'],
            menu_id=store_data['menu_id'] if 'menu_id' in store_data else ""
        )
        self.__store_repo.add_store(store)
        return store.__repr__()

    def get_all_stores(self):
        return self.__store_repo.get_all_stores()
    
    def get_store_by_id(self, store_id: ObjectId):
        return self.__store_repo.get_store_by_id(store_id)

    def delete_store(self, store_id: ObjectId):
        return self.__store_repo.delete_store(store_id)

    def update_store(self, store_id: ObjectId, update_data: dict):
        return self.__store_repo.update_store(store_id, update_data)
