class Cart:
    def __init__(self, _id, items, total):
        self._id = _id
        self.items = items
        self.total = total

    
class CartItem:
    def __init__(self, cart_item_id, menu_item_id, quantity, features):
        self.cart_item_id = cart_item_id
        self.menu_item_id = menu_item_id
        self.quantity = quantity
        self.features = []