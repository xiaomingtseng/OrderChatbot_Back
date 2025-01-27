import uuid
from bson import ObjectId

class Store:
    def __init__(self, name, address, menu_id=None, _id=None):
        self._id = _id if _id else ObjectId()
        self.name = name
        self.address = address
        self.menu_id = menu_id
        self.menu_image_url = None

    def add_item(self, item):
        self.items.append(item)
    
    def get_store_info(self):
        return {
            '_id': str(self._id),
            'name': self.name,
            'address': self.address,
            'menu_id': self.menu_id,
            'menu_image_url': self.menu_image_url
        }

    @staticmethod
    def from_dict(data):
        return Store(
            name=data.get('name'),
            address=data.get('address'),
            menu_id=data.get('menu_id'),
            _id=ObjectId(data['_id']) if '_id' in data else None
        )