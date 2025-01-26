import pytest
from services.store_service import StoreService
from DB.database import Database

@pytest.fixture
def store_service():
    # 清空集合
    db = Database('mongodb://localhost:27017/', 'mydatabase')
    collection = db.get_collection('store')
    collection.delete_many({})
    return StoreService()

def test_add_store(store_service):
    store_data = {'name': 'Store 1', 'address': '123 Main St', 'menu_id': 'menu123'}
    store_service.add_store(store_data)
    stores = store_service.get_all_stores()
    assert len(stores) == 1
    assert stores[0]['name'] == 'Store 1'
    assert stores[0]['address'] == '123 Main St'
    assert stores[0]['menu_id'] == 'menu123'

def test_get_store(store_service):
    store_data = {'name': 'Store 1', 'address': '123 Main St', 'menu_id': 'menu123'}
    store_service.add_store(store_data)
    stores = store_service.get_all_stores()
    store_id = stores[0]['_id']
    assert store_service.get_store(store_id) == stores[0]

def test_get_all_stores(store_service):
    store1 = {'name': 'Store 1', 'address': '123 Main St', 'menu_id': 'menu123'}
    store2 = {'name': 'Store 2', 'address': '456 Elm St', 'menu_id': 'menu456'}
    store_service.add_store(store1)
    store_service.add_store(store2)
    stores = store_service.get_all_stores()
    assert len(stores) == 2
    assert stores[0]['name'] == 'Store 1'
    assert stores[1]['name'] == 'Store 2'

def test_remove_store(store_service):
    store_data = {'name': 'Store 1', 'address': '123 Main St', 'menu_id': 'menu123'}
    store_service.add_store(store_data)
    stores = store_service.get_all_stores()
    store_id = stores[0]['_id']
    store_service.remove_store(store_id)
    assert store_service.get_store(store_id) is None