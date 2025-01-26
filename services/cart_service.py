from pymongo import MongoClient
from bson.objectid import ObjectId
from domain.cart import Cart
from repositories.CartRepository import CartRepository

class CartService:
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['mydatabase']
        self.collection = self.db['cart']

    def add_to_cart(self, item):
        self.collection.insert_one(item)

    def remove_from_cart(self, item_id):
        self.collection.delete_one({'_id': ObjectId(item_id)})

    def get_cart_items(self):
        return list(self.collection.find())

    def clear_cart(self):
        self.collection.delete_many({})

    def get_total(self):
        return sum([item['price'] for item in self.collection.find()])

    def get_cart(self):
        cart = Cart()
        cart.items = self.get_cart_items()
        return cart