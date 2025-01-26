import uuid
from bson import ObjectId

class Store:
    def __init__(self, name='', address='', _id=None, items=None, menu_id=None):
        self._id = _id if _id else ObjectId()  # 使用 MongoDB 自動生成的 _id
        self.name = name
        self.address = address
        self.items = items if items is not None else []
        self.menu_id = menu_id  # 添加 menu_id 字段

    def add_item(self, item):
        self.items.append(item)
    
    def get_store_info(self):
        return {
            '_id': str(self._id),  # 將 _id 轉換為字符串
            'name': self.name,
            'address': self.address,
            'items': self.items,
            'menu_id': self.menu_id  # 返回 menu_id
        }