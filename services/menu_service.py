from DB.database import Database
from domain.menu import Menu
from bson import ObjectId

class MenuService:
    def __init__(self):
        db = Database('mongodb://localhost:27017/', 'mydatabase')
        self.collection = db.get_collection('menu')

    def get_menu_by_store_id(self, store_id):
        menu_data = self.collection.find_one({'store_id': store_id})
        return Menu.from_dict(menu_data) if menu_data else None

    def add_menu(self, menu_data):
        menu = Menu.from_dict(menu_data)
        self.collection.insert_one(menu.to_dict())

    def update_menu(self, store_id, menu_id, menu_data):
        menu = Menu.from_dict(menu_data)
        result = self.collection.update_one(
            {'store_id': store_id, '_id': ObjectId(menu_id)},
            {'$set': menu.to_dict()}
        )
        return result.matched_count > 0

    def delete_menu(self, store_id, menu_id):
        result = self.collection.delete_one({'store_id': store_id, '_id': ObjectId(menu_id)})
        return result.deleted_count > 0