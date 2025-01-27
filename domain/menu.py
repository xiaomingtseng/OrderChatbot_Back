from bson import ObjectId
from domain.menu_item import MenuItem

class Menu:
    def __init__(self, name, items, store_id=None, _id=None):
        self._id = _id if _id else ObjectId()
        self.name = name
        self.items = [MenuItem.from_dict(item) for item in items]  # items should be a list of MenuItem objects
        self.store_id = store_id

    def to_dict(self):
        return {
            '_id': str(self._id),
            'name': self.name,
            'items': [item.to_dict() for item in self.items],
            'store_id': self.store_id
        }

    @staticmethod
    def from_dict(data):
        return Menu(
            name=data.get('name'),
            items=[MenuItem.from_dict(item) for item in data.get('items', [])],
            store_id=data.get('store_id'),
            _id=ObjectId(data['_id']) if '_id' in data else None
        )