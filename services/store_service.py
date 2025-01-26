from repositories.StoreRepository import StoreRepository
from domain.store import Store

class StoreService:
    def __init__(self):
        self.__store_repository = StoreRepository()

    def add_store(self, store_data):
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