from domain.cart import Cart
from domain.cart import CartItem
from domain.menu import MenuItem
from infrastructure.database import Database    
from bson import ObjectId
class CartReposiotry:
    def __init__(self, db: Database):
        self.cart_collection = db.get_collection('cart')   
        self.cart_item_collection = db.get_collection('cart_items')
        self.menu_item_collection = db.get_collection('menu_items')
    def create_cart(self):
        cart_data = {
            '_id': ObjectId(),
            'items': [],
            'total': 0
        }
        self.cart_collection.insert_one(cart_data)
        return cart_data
    def get_cart_by_id(self, cart_id: ObjectId):
        cart_data = self.cart_collection.find_one({'_id': cart_id})
        if cart_data:
            return Cart(str(cart_data['_id']), cart_data['items'], cart_data['total'])
        return None
    def update_cart(self, cart_id: ObjectId, update_data: dict):
        if '_id' in update_data:
            del update_data['_id']
        self.cart_collection.update_one({'_id': cart_id}, {'$set': update_data})
        updated_cart_data = self.cart_collection.find_one({'_id': cart_id})
        if updated_cart_data:
            return Cart(str(updated_cart_data['_id']), updated_cart_data['items'], updated_cart_data['total'])
        return None
    def delete_cart(self, cart_id: ObjectId):
        result = self.cart_collection.delete_one({'_id': ObjectId(cart_id)})
        return result.deleted_count > 0
    def get_menu_item_by_id(self, menu_item_id: ObjectId):
        menu_item_data = self.menu_item_collection.find_one({'_id': ObjectId(menu_item_id)})
        if menu_item_data:
            return MenuItem(
                str(menu_item_data['_id']),
                menu_item_data['name'],
                menu_item_data['price'],
                menu_item_data['category']
            )
        return None
    def add_cart_item(self, menu_item_id: ObjectId, quantity: int, features: list):
        cart_item_data = {
            '_id': ObjectId(),
            'menu_item_id': menu_item_id,
            'quantity': quantity,
            'features': features
        }
        self.cart_item_collection.insert_one(cart_item_data)
        return cart_item_data
    def remove_cart_item(self, cart_id: ObjectId, cart_item_id: ObjectId):
        self.delete_cart
    def get_cart_item_details(self, cart_item_id: ObjectId):
        cart_item_data = self.cart_item_collection.find_one({'_id': ObjectId(cart_item_id)})
        if cart_item_data:
            menu_item = self.get_menu_item_by_id(cart_item_data['menu_item_id'])
            menu_item_dict = menu_item.to_dict() if menu_item else None
            return {
                '_id': str(cart_item_data['_id']),
                'menu_item': menu_item_dict,
                'quantity': cart_item_data['quantity'],
                'features': cart_item_data['features']
            }
        return None