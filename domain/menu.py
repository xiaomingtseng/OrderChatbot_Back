# Menu實體
class Menu:
    def __init__(self, menu_id, image_id, store_id, menu_item_ids=None):
        self.menu_id = menu_id
        self.image_id = image_id
        self.store_id = store_id
        self.menu_item_ids = []

# MenuItem實體
class MenuItem:
    def __init__(self, _id, name, description, price):
        self._id = _id
        self.name = name
        self.description = description
        self.price = price

    def to_dict(self):
        return {
            '_id': str(self._id),
            'name': self.name,
            'description': self.description,
            'price': self.price
        }
