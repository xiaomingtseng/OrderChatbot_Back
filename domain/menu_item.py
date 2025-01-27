from bson import ObjectId

class MenuItem:
    def __init__(self, name, price, description=None, image_url=None, _id=None):
        self._id = _id if _id else ObjectId()
        self.name = name
        self.price = price
        self.description = description
        self.image_url = image_url

    def to_dict(self):
        return {
            '_id': str(self._id),
            'name': self.name,
            'price': self.price,
            'description': self.description,
            'image_url': self.image_url
        }

    @staticmethod
    def from_dict(data):
        return MenuItem(
            name=data.get('name'),
            price=data.get('price'),
            description=data.get('description'),
            image_url=data.get('image_url'),
            _id=ObjectId(data['_id']) if '_id' in data else None
        )