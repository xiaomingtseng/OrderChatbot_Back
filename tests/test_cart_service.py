import pytest
from unittest.mock import patch, MagicMock
from services.cart_service import CartService
from bson import ObjectId

@pytest.fixture
@patch('services.cart_service.MongoClient')
def cart_service(MockMongoClient):
    mock_client = MockMongoClient.return_value
    mock_db = mock_client['mydatabase']
    mock_collection = mock_db['cart']
    service = CartService()
    return service, mock_collection

# def test_add_to_cart(cart_service):
#     service, mock_collection = cart_service
#     item = {'name': 'item1', 'price': 10}
#     service.add_to_cart(item)
#     mock_collection.insert_one.assert_called_with(item)

# def test_remove_from_cart(cart_service):
#     service, mock_collection = cart_service
#     item_id = str(ObjectId())
#     service.remove_from_cart(item_id)
#     mock_collection.delete_one.assert_called_with({'_id': ObjectId(item_id)})

# def test_get_cart_items(cart_service):
#     service, mock_collection = cart_service
#     mock_collection.find.return_value = [{'name': 'item1', 'price': 10, '_id': ObjectId()}]
#     items = service.get_cart_items()
#     assert items == [{'name': 'item1', 'price': 10, '_id': str(mock_collection.find.return_value[0]['_id'])}]

# def test_clear_cart(cart_service):
#     service, mock_collection = cart_service
#     service.clear_cart()
#     mock_collection.delete_many.assert_called_with({})

# def test_get_total(cart_service):
#     service, mock_collection = cart_service
#     mock_collection.find.return_value = [{'name': 'item1', 'price': 10}, {'name': 'item2', 'price': 20}]
#     total = service.get_total()
#     assert total == 30