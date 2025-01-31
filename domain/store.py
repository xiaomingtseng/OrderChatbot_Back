from bson import ObjectId

class Store:
    def __init__(self, name, description, location, menu_id=None, _id=None):
        self._id = _id if _id else ObjectId()
        self.name = name
        self.description = description
        self.location = location
        self.menu_id = menu_id

    def to_dict(self):
        return {
            '_id': str(self._id),
            'name': self.name,
            'description': self.description,
            'location': self.location,
            'menu_id': self.menu_id
        }

    def __repr__(self):
        return f"<Store(id={self._id}, name={self.name}, location={self.location}, menu_id={self.menu_id})>"