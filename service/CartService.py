from infrastructure.cartRepo import CartReposiotry
from bson import ObjectId

class CartService:
    def __init__(self, cart_repo: CartReposiotry):
        self.cart_repo = cart_repo

    def create_cart(self):
        return self.cart_repo.create_cart()

    def get_cart_by_id(self, cart_id: str):
        return self.cart_repo.get_cart_by_id(ObjectId(cart_id))

    def update_cart(self, cart_id: str, update_data: dict):
        return self.cart_repo.update_cart(ObjectId(cart_id), update_data)
    
    def add_item_to_cart(self, cart_id: str, cart_item_id: str):
        return self.cart_repo.add_item_to_cart(ObjectId(cart_id), ObjectId(cart_item_id))
    
    def delete_item_from_cart(self, cart_id: str, cart_item_id: str):
        return self.cart_repo.delete_item_from_cart(ObjectId(cart_id), ObjectId(cart_item_id))

    def delete_cart(self, cart_id: str):
        return self.cart_repo.delete_cart(ObjectId(cart_id))

    def get_cart_item_details(self, cart_item_id: str):
        return self.cart_repo.get_cart_item_details(ObjectId(cart_item_id))

    def add_cart_item(self, menu_item_id: str, quantity: int, features: list):
        cart_item_data = self.cart_repo.add_cart_item(ObjectId(menu_item_id), quantity, features)
        if cart_item_data:
            cart_item_data['_id'] = str(cart_item_data['_id'])
            cart_item_data['menu_item_id'] = str(cart_item_data['menu_item_id'])
        return cart_item_data

    def remove_cart_item(self, cart_id: str, cart_item_id: str):
        return self.cart_repo.remove_cart_item(ObjectId(cart_id), ObjectId(cart_item_id))